import json
from kona import parse_kona, PipelineNode, ActionNode

class ToolRouter:
    """
    Translates a Kona Abstract Syntax Tree (AST) into specific JSON Tool Calls.
    """
    def __init__(self):
        self.tool_mappings = {
            "kwe": self._route_search,
            "tori": self._route_edit,
            "visi": self._route_read,
            "yuki": self._route_execute,
            "maki": self._route_create,
        }

    def route_pipeline(self, pipeline: PipelineNode):
        tool_calls = []
        for stage in pipeline.stages:
            if isinstance(stage.body, ActionNode):
                action = stage.body.action
                if action in self.tool_mappings:
                    tool_call = self.tool_mappings[action](stage.body)
                    if tool_call:
                        tool_calls.append(tool_call)
        return tool_calls

    def _extract_args(self, action_node):
        args = []
        for t in action_node.targets:
            if t["type"] == "literal":
                args.append(t["args"])
            elif t["type"] == "string":
                args.append(t["args"])
            else:
                args.append(t["type"])
        return args

    def _route_search(self, node):
        args = self._extract_args(node)
        query = args[0] if args else ""
        return {
            "tool": "grep_search",
            "args": {
                "Query": query,
                "SearchPath": "."
            },
            "description": f"Kona action: {node.action}"
        }

    def _route_edit(self, node):
        return {
            "tool": "replace_file_content",
            "args": {
                "TargetFile": "<path>",
                "Instruction": "Follow Kona edit instructions"
            },
            "description": f"Kona action: {node.action}"
        }

    def _route_read(self, node):
        args = self._extract_args(node)
        target = args[0] if args else "."
        return {
            "tool": "view_file",
            "args": {
                "AbsolutePath": target
            }
        }

    def _route_execute(self, node):
        args = self._extract_args(node)
        cmd = " ".join(str(a) for a in args)
        return {
            "tool": "run_command",
            "args": {
                "CommandLine": cmd
            }
        }

    def _route_create(self, node):
        return {
            "tool": "write_to_file",
            "args": {
                "TargetFile": "<path>",
                "CodeContent": "<content>"
            }
        }

if __name__ == "__main__":
    router = ToolRouter()
    code = "kwe nomi \"auth config\" fino |> tori"
    print(f"Routing Pipeline: {code}")
    ast = parse_kona(code)
    tools = router.route_pipeline(ast)
    print(json.dumps(tools, indent=2))
