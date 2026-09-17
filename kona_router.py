import json

from kona import parse_kona, PipelineNode, StageNode, ActionNode


class UnroutableError(Exception):
    """Raised when an utterance cannot be translated into a tool call that
    faithfully preserves its constraints.

    Refusing is the safe outcome. A guard that is silently dropped is worse
    than no guard at all, because the language teaches operators to rely on it.
    """


class ToolRouter:
    """Translates a Kona AST into concrete JSON tool calls.

    Every constraint the speaker expressed -- prohibitions (`notori`), dry-run
    (`ve`), conditions (`si`/`ali`) -- is carried into the emitted call or the
    utterance is refused. The router never emits a call that does less than it
    was asked, or more.
    """

    #: Actions that mutate state. These may only be emitted when every guard
    #: attached to them has been represented in the outgoing call.
    MUTATING = {"tori", "nuki", "maki", "yuki", "mova", "kiri", "fiso"}

    def __init__(self, allow_unmapped=False):
        self.allow_unmapped = allow_unmapped
        self.tool_mappings = {
            "kwe": self._route_search,
            "tori": self._route_edit,
            "visi": self._route_read,
            "yuki": self._route_execute,
            "maki": self._route_create,
        }

    # -- public API ---------------------------------------------------------

    def route_pipeline(self, node):
        """Route a parsed pipeline. Returns a list of tool calls.

        Raises UnroutableError rather than silently dropping any stage,
        constraint or nested pipeline.
        """
        calls = []
        for stage in self._iter_stages(node):
            calls.extend(self._route_stage(stage))
        return calls

    # -- internals ----------------------------------------------------------

    def _iter_stages(self, node):
        """Flatten nested pipelines. The previous version tested
        `isinstance(stage.body, ActionNode)` and silently skipped any
        parenthesised sub-pipeline."""
        if isinstance(node, PipelineNode):
            for stage in node.stages:
                yield from self._iter_stages(stage)
        elif isinstance(node, StageNode):
            yield node
        else:
            raise UnroutableError(f"unexpected AST node: {type(node).__name__}")

    def _route_stage(self, stage):
        calls = []

        if isinstance(stage.body, PipelineNode):
            inner = self.route_pipeline(stage.body)
        else:
            inner = self._route_action(stage.body)

        condition = " ".join(stage.condition) if stage.condition else None
        for call in inner:
            call["guards"]["condition"] = condition
        calls.extend(inner)

        if stage.else_branch:
            else_calls = self._route_stage(stage.else_branch)
            for call in else_calls:
                call["guards"]["condition"] = (
                    f"NOT ({condition})" if condition else "OTHERWISE"
                )
            calls.extend(else_calls)

        return calls

    def _route_action(self, node):
        if not isinstance(node, ActionNode):
            raise UnroutableError(f"unexpected body node: {type(node).__name__}")

        # Declaratives assert; they never execute.
        if node.is_declarative:
            return []

        handler = self.tool_mappings.get(node.action)
        if handler is None:
            if self.allow_unmapped:
                return []
            raise UnroutableError(
                f"action {node.action!r} has no tool mapping -- refusing to emit "
                f"a call rather than dropping the instruction silently"
            )

        call = handler(node)
        if call is None:
            raise UnroutableError(f"handler for {node.action!r} produced no call")

        # Attach every constraint the speaker expressed. This is the whole point
        # of the language: `notori "migrations"` must survive into the tool call.
        call["guards"] = {
            "prohibited": list(node.guards),
            "dry_run": "dry_run/speculative" in node.modifiers,
            "modifiers": list(node.modifiers),
            "aspect": node.aspect,
            "modality": node.modality,
            "condition": None,
        }

        self._assert_constraints_honoured(node, call)
        return [call]

    def _assert_constraints_honoured(self, node, call):
        """Fail loudly if a mutating action carries guards the tool cannot express."""
        if node.action in self.MUTATING and node.guards:
            if not call["guards"]["prohibited"]:
                raise UnroutableError(
                    f"{node.action!r} carries guards {node.guards} that the target "
                    f"tool cannot express -- refusing"
                )
        if "dry_run/speculative" in node.modifiers and not call["args"].get("DryRun"):
            raise UnroutableError(
                f"{node.action!r} was requested as a dry run but the target tool "
                f"has no dry-run mode -- refusing"
            )

    def _extract_args(self, node):
        args = []
        for t in node.targets:
            if t["type"] in ("literal", "string"):
                args.append(t["args"])
            elif t.get("args") is not None:
                args.append(t["args"])
            else:
                args.append(t["type"])
        return args

    # -- handlers -----------------------------------------------------------

    def _route_search(self, node):
        args = self._extract_args(node)
        return {
            "tool": "grep_search",
            "args": {"Query": args[0] if args else "", "SearchPath": "."},
            "description": f"Kona action: {node.action}",
        }

    def _route_edit(self, node):
        args = self._extract_args(node)
        return {
            "tool": "replace_file_content",
            "args": {
                "TargetFile": args[0] if args else None,
                "Instruction": "Follow Kona edit instructions",
                # Prohibitions travel with the call, not just in the AST.
                "ExcludePaths": list(node.guards),
                "DryRun": "dry_run/speculative" in node.modifiers,
            },
            "description": f"Kona action: {node.action}",
        }

    def _route_read(self, node):
        args = self._extract_args(node)
        return {
            "tool": "view_file",
            "args": {"AbsolutePath": args[0] if args else "."},
            "description": f"Kona action: {node.action}",
        }

    def _route_execute(self, node):
        args = self._extract_args(node)
        # Never build a shell string out of loose words. An execute stage must
        # name exactly one explicit, quoted command; anything else is refused.
        literals = [t["args"] for t in node.targets
                    if t["type"] == "literal" and isinstance(t["args"], str)]
        if len(literals) != 1:
            raise UnroutableError(
                "yuki (execute) requires exactly one quoted command literal, e.g. "
                'yuki "npm test" -- refusing to synthesise a command from '
                f"{args!r}"
            )
        return {
            "tool": "run_command",
            "args": {
                "CommandLine": literals[0],
                "DryRun": "dry_run/speculative" in node.modifiers,
            },
            "description": f"Kona action: {node.action}",
        }

    def _route_create(self, node):
        args = self._extract_args(node)
        return {
            "tool": "write_to_file",
            "args": {
                "TargetFile": args[0] if args else None,
                "CodeContent": None,
                "DryRun": "dry_run/speculative" in node.modifiers,
            },
            "description": f"Kona action: {node.action}",
        }


if __name__ == "__main__":
    router = ToolRouter()
    samples = [
        'kwe nomi auth config fino te, visi kodo',
        'vetori kodo notori "migrations"',
        'si teli bono te, visi kodo ali kwe baki',
        'nuki data sisa',
        'yuki kodo poya',
    ]
    for code in samples:
        print(f"\n--- {code}")
        try:
            print(json.dumps(router.route_pipeline(parse_kona(code)), indent=2))
        except (UnroutableError, SyntaxError) as e:
            print(f"  REFUSED: {e}")
