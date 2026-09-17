#!/usr/bin/env python3
"""
Kona (コナビ) Language Engine
Purely Functional, Acoustically Engineered Language for AI Agent Communication.
"""

import re
import json
import sys
import subprocess
from typing import Dict, Any, List, Optional

# ============================================================================
# 1. THE KONA LEXICON (Agentic Operations, Targets, & Modifiers)
# ============================================================================

ACTIONS = {
    # Existing core
    "kwe":   {"name": "search",    "desc": "Query/Search/Grep"},
    "maki":  {"name": "create",    "desc": "Create/Generate/Scaffold"},
    "tori":  {"name": "transform", "desc": "Edit/Refactor/Modify"},
    "teli":  {"name": "verify",    "desc": "Test/Benchmark/Verify"},
    "nuki":  {"name": "delete",    "desc": "Delete/Prune/Purge"},
    "fasa":  {"name": "summarize", "desc": "Summarize/Explain/Report"},
    "yuki":  {"name": "execute",   "desc": "Run/Execute/Deploy"},
    "pilani": {"name": "plan",      "desc": "Plan/Schedule/Sequence"},
    # Expanded universal & workflow actions
    "visi":  {"name": "view",      "desc": "Read/View/Inspect/Cat"},
    "leke":  {"name": "fetch",     "desc": "Pull/Fetch/Download/Receive"},
    "do":    {"name": "emit",      "desc": "Send/Emit/Notify/Push"},
    "oki":   {"name": "start",     "desc": "Open/Start/Initialize"},
    "fini":  {"name": "finish",    "desc": "End/Complete/Terminate"},
    "mova":  {"name": "move",      "desc": "Move/Shift/Transfer"},
    "ira":   {"name": "navigate",  "desc": "Go/Navigate/Visit"},
    "para":  {"name": "pause",     "desc": "Stop/Halt/Pause"},
    "posi":  {"name": "can",       "desc": "Can/Could/Able"},
    "debi":  {"name": "must",      "desc": "Must/Should/Ought"},
    # Social, alignment & negotiation
    "wapo":  {"name": "agree",     "desc": "Agree/Align/Consent"},
    "poki":  {"name": "propose",   "desc": "Propose/Suggest/Offer"},
    "keti":  {"name": "decide",    "desc": "Decide/Resolve/Determine"},
    "sapi":  {"name": "know",      "desc": "Know/Understand/Comprehend"},
    "veni":  {"name": "arrive",    "desc": "Arrive/Come/Approach"},
    "peli":  {"name": "delay",     "desc": "Delay/Postpone/Defer"},
    "tapi":  {"name": "type",      "desc": "Type/Keystroke/Input"},
    "kisi":  {"name": "listen",    "desc": "Hear/Listen/Receive audio"},
    # Ext: Workflow & Git
    "yalo":  {"name": "approve",   "desc": "Approve/Accept/Merge"},
    "nolo":  {"name": "reject",    "desc": "Reject/Block/Revert"},
    "koma":  {"name": "compare",   "desc": "Compare/Diff"},
    "fiso":  {"name": "fix",       "desc": "Fix/Patch/Resolve"},
    "kada":  {"name": "iterate",   "desc": "Map/For-Each"},
    "kiri":  {"name": "write",     "desc": "Write/Author/Draft"},
}

TARGETS = {
    # System & Code
    "kodo": "code",
    "fili": "file",
    "poya": "repo",
    "vasi": "version_git",
    "baki": "bug_issue",
    "tesi": "test_spec",
    "pako": "container_docker",
    "sisa": "system_os",
    "seli": "resource_lock",
    # Natural & Physical World
    "venito": "wind_air",
    "soli":  "sun_solar",
    "noreti": "north_direction",
    "tela":  "fabric_cloak",
    "kalu":  "thermal_warmth",
    "luke":  "light_illumination",
    "powa":  "power_energy",
    "toko":  "time_interval",
    "sekuni": "second_unit",
    "minuta":  "minute_unit",
    "kora":    "hour_unit",
    "dya":     "day_unit",
    "wiki":    "week_unit",
    "irayoti": "traveler",
    # Hardware & Physical Devices (-koso compounding)
    "kisikoso": "microphone",
    "sonokoso": "speaker",
    "visikoso": "camera",
    "visipeji": "screen_display",
    "tapikoso": "keyboard",
    "powakoso": "battery_power",
    "tokokoso": "timer_clock",
    "parakoso": "brake_interrupt",
    # Workspaces & Environments (-kaba compounding)
    "kodokaba": "workspace_ide",
    "pakokaba": "sandbox_env",
    "datakaba": "data_warehouse",
    # Specialized Roles (-yoti compounding)
    "kodoyoti": "developer",
    "makiyoti": "designer_creator",
    "teliyoti": "qa_tester",
    # Time Compounding
    "tokofini": "deadline",
    "tokooki":  "start_schedule",
    "tokopasa": "history_log",
    "tokofutu": "forecast_roadmap",
    # Web & Network
    "veba": "web",
    "peji": "page_url",
    # Ext: Cloud & DevOps
    "kusa": "cluster_node",
    "fuka": "container_pod",
    "rogi": "log_trace",
    "pota": "port_endpoint",
    "toka": "token_key",
    
    # Ext: Code Types
    "fumo": "function_method",
    "vari": "variable_state",
    "kila": "class_module",
    "raya": "array_list",
    "sito": "string_text",
    
    # Ext: UI & Web
    "buta": "button_element",
    "foma": "input_form",
    "pika": "image_media",
    "wina": "window_modal",
    
    # Ext: Debugging & Config
    "fogo": "error_crash",
    "mori": "root_cause",
    "simo": "symptom_metric",
    "tuma": "memory_dump",
    "figa": "configuration",
    "rego": "rule_policy",
    "vito": "state_mode",
    
    # Ext: Real World / Physical
    "moni": "money_cost",
    "teka": "building_office",
    "karo": "vehicle_transport",
    "nami": "food_sustenance",
    "misu": "water_liquid",
    "liba": "document_book",
    "wela": "location_coordinates",
    "liki": "link",
    "neto": "network_api",
    # Data & Knowledge
    "data": "data_db",
    "memo": "memory_context",
    "seku": "security_secret",
    # Communication & Workflow
    "tafu": "task",
    "meso": "message_email",
    "yoti": "user",
    "sono": "sound_audio",
    "wada": "word_token",
    "koso": "tool_instrument",
    # Core Persons
    "mi":   "user_speaker",
    "tu":   "agent_listener",
    "ona":  "external_entity",
    "koli": "team_collective",
}

DIGITS = {
    "wo": "0", "pa": "1", "du": "2", "ti": "3", "fo": "4",
    "mu": "5", "sa": "6", "ke": "7", "bi": "8", "go": "9"
}
MODIFIERS = {
    "su":   "fast/brief",
    "de":   "deep/exhaustive",
    "ve":   "dry_run/speculative",
    "no":   "prohibit/guard_not",
    "oto":  "autonomous/auto",
    "re":   "repeat/retry/loop",
    "suno": "zero/without_delay",
    "dura": "continuous/in_progress",
    "pasa": "past/completed",
    "futu": "future/scheduled",
}

# Qualities / stative predicates. These are the words that appear in `si`
# conditions ("si teli bono te," = if the test is good). They were documented in
# LEXICON.md but absent from the compiler, which only went unnoticed because
# condition contents used to bypass lexical validation entirely.
QUALITIES = {
    "bono": "good",
    "simi": "easy_simple",
    "fide": "trusted_confident",
    "gala": "satisfied_happy",
    "kore": "correct_right",
    "pura": "safe_secure",
}

FORMATS = {
    "mesa": "table",
    "poti": "bullet_list",
    "jano": "json",
    "puro": "plain_text",
    "difa": "diff",
}

# Closed class of structural particles. These are the only free-standing words
# that are neither an action, target, modifier nor format. Declaring them
# explicitly is what lets the parser reject everything else (see Parser.STRICT).
PARTICLES = {
    "si":     "if",
    "te":     "pipe_then",
    "ali":    "else",
    "nomi":   "literal_open",
    "fino":   "literal_close",
    "ke":     "relative_linker",
    "ina":    "scope_inside",
    "uta":    "scope_outside",
    "lo":     "logical_or",
    "mapo":   "logical_and",
    "pero":   "contrast_but",
    "masi":   "comparative_more",
    "supera":  "superlative_above",
    "sama":   "equative_same",
    "kasi":   "causal_because",
    "kono":   "conclusive_therefore",
    "ye":     "affirmative_yes",
    "ti":     "topic_marker",
    "duo":    "quantifier_two",
    "deko":   "quantifier_ten",
    "muto":   "quantifier_many",
    "notori": "guard_prohibit",
    # Quantifiers & deixis. kona_asr.py already listed these as structural words
    # in its Whisper prompt while the compiler did not know them.
    "oli":    "quantifier_all",
    "uni":    "quantifier_some",
    "pato":   "deixis_previous_output",
    "kito":   "deixis_this_current",
}

# Ordinal prefix: ro- + numeral ("rosuno" = 1st, "roduo" = 2nd).
ORDINAL_PREFIX = "ro"

# Bound morphemes: these never stand alone as words. Keeping them bound is what
# removes the /d/~/t/ confusion between the modifier `de` and the pipe particle
# `te` -- `de` only ever occurs affixed (dekwe, kwe.de), never as its own word.
BOUND_PREFIXES = set(MODIFIERS)
ASPECT_SUFFIXES = {"ba": "progressive", "ta": "perfective", "sa": "habitual"}
NOMINALIZER = "na"

# Particles that open a subordinate clause. A clause may carry its own predicate,
# so a second action after one of these is grammatical rather than an error.
CLAUSE_PARTICLES = {"ke", "pero", "kasi", "kono", "mapo", "lo", "si"}

# Modal verbs take a complement predicate ('posi teli' = can verify). The modal
# becomes a modality marker on the stage; the complement is the real action.
MODALS = {"posi": "possibility", "debi": "obligation"}
DERIVATIONAL_SUFFIXES = {
    "koso": "physical_device",
    "peji": "display_surface",
    "kaba": "environment_space",
    "yoti": "specialist_role",
}

# Canonical mappings for shorthand.
#
# These resolve an English shorthand alias to the *Kona root*, not to the
# English gloss. That is what makes the two modalities isomorphic: `@repo` and
# `poya` both produce a target of type "poya", so the spoken and written forms
# of the same utterance compile to a byte-identical AST. (Aliases that are
# already Kona roots -- `@poya`, `@kodo` -- pass through unchanged.)
SHORTHAND_TARGET_MAP = {
    "code":    "kodo",
    "file":    "fili",
    "web":     "veba",
    "repo":    "poya",
    "git":     "vasi",
    "vcs":     "vasi",
    "bug":     "baki",
    "issue":   "baki",
    "test":    "tesi",
    "docker":  "pako",
    "sandbox": "pakokaba",
    "url":     "peji",
    "page":    "peji",
    "link":    "liki",
    "api":     "neto",
    "lock":      "seli",
    "log":       "rogi",
    "logs":      "rogi",
    "container": "pako",
    "pod":       "fuka",
    "data":      "data",
    "db":        "data",
    "memo":      "memo",
    "memory":    "memo",
    "auth":      "seku",
    "secret":    "seku",
    "task":      "tafu",
    "msg":       "meso",
    "mail":      "meso",
    "user":      "mi",
    "agent":     "tu",
    "team":      "koli",
    # Hardware & Physical compounds
    "mic":       "kisikoso",
    "cam":       "visikoso",
    "screen":    "visipeji",
    "display":   "visipeji",
    "kb":        "tapikoso",
    "battery":   "powakoso",
    "workspace": "kodokaba",
    "deadline":  "tokofini",
}

SHORTHAND_FORMAT_MAP = {
    "#table": "table",
    "#list":  "bullet_list",
    "#json":  "json",
    "#raw":   "plain_text",
    "#diff":  "diff",
}


# ============================================================================
# 2. PARSER & AST BUILDER
# ============================================================================


class Token:
    def __init__(self, type_: str, value: str, raw: str):
        self.type = type_
        self.value = value
        self.raw = raw
    def __repr__(self):
        return f"Token({self.type}, {self.raw})"

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.tokens = []
        self.tokenize()
        self.pos = 0

    def tokenize(self):
        rules = [
            ("WHITESPACE", r'\s+'),
            # Comments, matching language-configuration.json so the editor and
            # the compiler agree on what is commented out.
            ("COMMENT", r'//[^\n]*|/\*.*?\*/'),
            # A bare comma is a prosodic clause pause with no semantic content.
            # 'te,' is matched by PIPE below before this rule can see the comma.
            ("COMMA", r','),
            # ';' is an utterance separator, equivalent to a spoken 'te,'.
            ("PIPE", r'\|>|te\s*,|te(?!\w)|;'),
            ("LPAREN", r'\('),
            ("RPAREN", r'\)'),
            ("STRING", r'"[^"]*"|\'[^\']*\''),
            ("NOMI", r'nomi\b'),
            ("FINO", r'fino\b'),
            ("SI", r'si\b'),
            # ':else:' must not be followed by \b -- a colon is not a word char,
            # so '(ali|:else:)\b' could never match the shorthand form at all.
            ("ALI", r'ali\b|:else:'),
            # '!"literal"' is the shorthand counterpart of spoken 'notori "literal"'.
            ("GUARD", r'!"[^"]*"|!\'[^\']*\'|![a-zA-Z_-]+|notori\b|no-[a-zA-Z_-]+'),
            ("TARGET_AT", r'@[a-zA-Z_-]+(?::("[^"]*"|\'[^\']*\'|[a-zA-Z_][a-zA-Z0-9_]*))?'),
            ("FORMAT_HASH", r'#(?:table|list|json|raw|diff)'),
            # Dotted/hyphenated affixation (kwe.de, su-kwe) is a single word.
            ("WORD", r'[a-zA-Z_][a-zA-Z0-9_]*(?:[.-][a-zA-Z0-9_]+)*')
        ]
        
        scanner = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in rules), re.S)

        # Scan strictly: every character must be consumed by some rule. re.finditer
        # would silently skip anything unmatched, which is how '$$$ %%%' used to
        # compile cleanly into an execute call.
        pos = 0
        while pos < len(self.text):
            match = scanner.match(self.text, pos)
            if not match:
                raise SyntaxError(
                    f"SyntaxError: unexpected character {self.text[pos]!r} "
                    f"at position {pos}"
                )
            pos = match.end()
            type_ = match.lastgroup
            raw = match.group()
            if type_ in ("WHITESPACE", "COMMA", "COMMENT"): continue

            value = raw
            if type_ == "STRING":
                value = raw[1:-1]
            self.tokens.append(Token(type_, value, raw))

    def peek(self):
        if self.pos < len(self.tokens): return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None):
        tok = self.peek()
        if expected_type and (not tok or tok.type != expected_type):
            raise SyntaxError(f"SyntaxError: Expected {expected_type}, got {tok.type if tok else 'EOF'} at '{tok.raw if tok else ''}'")
        if tok: self.pos += 1
        return tok

class ASTNode:
    def to_english(self) -> List[str]: raise NotImplementedError()
    def to_tool_calls(self) -> List[Dict]: raise NotImplementedError()

class PipelineNode(ASTNode):
    def __init__(self, stages):
        self.stages = stages
    def to_english(self):
        out = []
        for i, s in enumerate(self.stages):
            eng = s.to_english()
            if i > 0:
                out.append("THEN: " + eng[0])
                out.extend(eng[1:])
            else:
                out.extend(eng)
        return out
    def to_tool_calls(self):
        out = []
        for s in self.stages:
            out.extend(s.to_tool_calls())
        return out

class StageNode(ASTNode):
    def __init__(self, body, condition=None, else_branch=None):
        self.body = body
        self.condition = condition
        self.else_branch = else_branch

    def to_english(self):
        out = []
        cond_str = ""
        if self.condition:
            cond_str = f"IF ({' '.join(self.condition)}) -> "
        
        body_eng = self.body.to_english()
        
        if cond_str:
            out.append(f"{cond_str}{body_eng[0]}")
            out.extend([f"  {line}" for line in body_eng[1:]])
        else:
            out.extend(body_eng)
            
        if self.else_branch:
            else_eng = self.else_branch.to_english()
            out.append(f"ELSE: {else_eng[0]}")
            out.extend([f"  {line}" for line in else_eng[1:]])
        return out

    def to_tool_calls(self):
        calls = self.body.to_tool_calls()
        if self.condition:
            for c in calls:
                c["parameters"]["condition"] = " ".join(self.condition)
        if self.else_branch:
            else_calls = self.else_branch.to_tool_calls()
            # An 'ali' branch is only meaningful under a condition. Guard against
            # self.condition being None, which raised TypeError on inputs as
            # short as 'ali ve'.
            negated = (f"NOT ({' '.join(self.condition)})"
                       if self.condition else "OTHERWISE")
            for ec in else_calls:
                ec["parameters"]["condition"] = negated
            calls.extend(else_calls)
        return calls

class ActionNode(ASTNode):
    def __init__(self, action, modifiers, targets, guards, formats, aspect=None,
                 particles=None, subclauses=None, modality=None):
        self.action = action
        self.modifiers = modifiers
        self.targets = targets
        self.guards = guards
        self.formats = formats
        self.aspect = aspect
        self.particles = particles or []
        self.subclauses = subclauses or []
        self.modality = modality

    @property
    def is_declarative(self) -> bool:
        """True when the utterance carries no action word: an assertion, not a
        command. Declaratives emit no tool calls."""
        return self.action is None

    def to_english(self):
        if self.is_declarative:
            t_desc = [
                f"'{t['args']}'" if t["type"] == "literal"
                else TARGETS.get(t["type"], t["type"])
                for t in self.targets
            ]
            line = f"ASSERT (no action): {', '.join(t_desc) if t_desc else 'empty utterance'}"
            return [line] if not self.particles else [line, f"Particles: {', '.join(self.particles)}"]

        act_desc = ACTIONS.get(self.action, {"name": self.action})["name"].upper()


        if self.aspect == "progressive":
            act_desc = "CURRENTLY " + act_desc + "-ING"
        elif self.aspect == "perfective":
            act_desc = "FINISHED " + act_desc
        elif self.aspect == "habitual":
            act_desc = "HABITUALLY " + act_desc

        if self.modifiers:
            mod_desc = " ".join([m for m in self.modifiers])
            act_desc = f"[{mod_desc}] {act_desc}"
            
        t_desc = []
        for t in self.targets:
            if t["type"] == "literal":
                t_desc.append(f"'{t['args']}'")
            else:
                base = t["type"]
                desc = TARGETS.get(base, base)
                if t["args"]:
                    desc += f" (args: {t['args']})"
                t_desc.append(desc)
                
        line = f"Execute {act_desc} on targets: {', '.join(t_desc) if t_desc else 'implicit'}"
        out = [line]
        if self.guards:
            out.append(f"Constraints: prohibited invariants -> {', '.join(self.guards)}")
        if self.formats:
            out.append(f"Output Format: {', '.join(self.formats)}")
        return out

    def to_tool_calls(self):
        # A declarative asserts something; it never executes.
        if self.is_declarative:
            return []
        # Nested same-type quotes inside an f-string are Python 3.12+ only
        # (PEP 701); bind the name first so this stays importable on 3.9-3.11.
        name = ACTIONS.get(self.action, {"name": self.action})["name"].lower()
        return [{
            "tool": f"agent_{name}",
            "parameters": {
                "aspect": self.aspect,
                "modifiers": self.modifiers,
                "targets": self.targets,
                "prohibited_invariants": self.guards,
                "format_requested": self.formats,
                "particles": self.particles,
                "subclause_predicates": self.subclauses,
                "modality": self.modality,
                "condition": None
            }
        }]

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse(self):
        node = self.parse_pipeline()
        # Every token must be consumed. Without this, a stray ')' silently
        # truncated the rest of the pipeline instead of being reported.
        leftover = self.lexer.peek()
        if leftover is not None:
            raise SyntaxError(
                f"SyntaxError: unexpected {leftover.type} {leftover.raw!r} "
                f"after end of pipeline"
            )
        return node

    def _assert_known_word(self, word: str):
        """Reject a word that is neither a lexeme nor derivable from one."""
        if (word in ACTIONS or word in TARGETS or word in MODIFIERS
                or word in FORMATS or word in PARTICLES or word in QUALITIES):
            return
        # Derived forms: nominalization, aspect, modifier prefix, numerals.
        if word.endswith(NOMINALIZER) and word[:-len(NOMINALIZER)] in ACTIONS:
            return
        for sfx in ASPECT_SUFFIXES:
            if word.endswith(sfx) and word[:-len(sfx)] in ACTIONS:
                return
        for m in MODIFIERS:
            if word.startswith(m):
                rest = word[len(m):]
                if rest in ACTIONS or rest in TARGETS or rest in QUALITIES:
                    return
                if any(rest.endswith(s) and rest[:-len(s)] in ACTIONS
                       for s in ASPECT_SUFFIXES):
                    return
        if word.startswith("ni") and len(word) >= 4 and len(word) % 2 == 0:
            if all(word[i:i + 2] in DIGITS for i in range(2, len(word), 2)):
                return
        raise SyntaxError(
            f"SyntaxError: unknown word {word!r} is not in the Kona lexicon "
            f"(quote it, or wrap it in 'nomi ... fino', to use it as a literal)"
        )

    def parse_pipeline(self):
        stages = []
        stages.append(self.parse_stage())
        while self.lexer.peek() and self.lexer.peek().type == "PIPE":
            self.lexer.consume("PIPE")
            stages.append(self.parse_stage())
        return PipelineNode(stages)

    def parse_stage(self):
        condition = None
        else_branch = None
        
        if self.lexer.peek() and self.lexer.peek().type == "SI":
            self.lexer.consume("SI")
            condition = []
            while self.lexer.peek() and self.lexer.peek().type not in ("PIPE", "ALI", "RPAREN"):
                tok = self.lexer.consume()
                # Conditions are held as raw tokens, but they are still Kona and
                # must be lexically valid. Skipping this check is what allowed
                # 'bono' -- documented in LEXICON.md but absent from the
                # compiler -- to go unnoticed inside every `si` clause.
                if tok.type == "WORD":
                    self._assert_known_word(tok.raw)
                condition.append(tok.raw)
            if not condition:
                raise SyntaxError("SyntaxError: 'si' (if) has an empty condition")
            # The condition must be closed by 'te,' / '|>' before the consequent.
            if not (self.lexer.peek() and self.lexer.peek().type == "PIPE"):
                raise SyntaxError(
                    "SyntaxError: condition after 'si' is not terminated -- "
                    "close it with 'te,' (spoken) or '|>' (shorthand)"
                )
            self.lexer.consume("PIPE")
                
        if self.lexer.peek() and self.lexer.peek().type == "LPAREN":
            self.lexer.consume("LPAREN")
            body = self.parse_pipeline()
            self.lexer.consume("RPAREN")
        else:
            body = self.parse_action_expr()
            
        if self.lexer.peek() and self.lexer.peek().type == "ALI":
            if condition is None:
                raise SyntaxError(
                    "SyntaxError: 'ali' (else) has no matching 'si' (if)"
                )
            self.lexer.consume("ALI")
            else_branch = self.parse_stage()

        return StageNode(body, condition, else_branch)

    def parse_action_expr(self):
        action = None
        aspect = None
        modifiers = []
        targets = []
        guards = []
        formats = []
        particles = []
        subclauses = []
        clause_open = False
        modality = None
        
        # LPAREN terminates an action expression: it opens a nested pipeline and
        # is handled by parse_stage. Previously it fell through every branch and
        # was silently discarded.
        while self.lexer.peek() and self.lexer.peek().type not in ("PIPE", "ALI", "RPAREN", "LPAREN"):
            tok = self.lexer.consume()
            
            if tok.type == "WORD":
                val = tok.raw
                if val in FORMATS:
                    formats.append(FORMATS[val])
                    continue
                if val in MODIFIERS:
                    modifiers.append(MODIFIERS[val])
                    continue
                if val in TARGETS:
                    targets.append({"type": val, "args": None})
                    continue
                    
                # Check nominalization
                if val.endswith("na") and val[:-2] in ACTIONS:
                    targets.append({"type": "nominalization", "args": val[:-2]})
                    continue

                if "." in val:
                    parts = val.split(".")
                    val = parts[0]
                    for p in parts[1:]:
                        if p in MODIFIERS: modifiers.append(MODIFIERS[p])
                elif "-" in val:
                    parts = val.split("-")
                    val = parts[-1]
                    for p in parts[:-1]:
                        if p in MODIFIERS: modifiers.append(MODIFIERS[p])
                else:
                    # Whole-word lookup always wins over decomposition (checked
                    # above), so roots that merely start with a modifier -- norte,
                    # veba, rego, debi -- are never mis-segmented. Only if the word
                    # is NOT itself a lexeme do we try to split it.
                    for m in sorted(MODIFIERS.keys(), key=len, reverse=True):
                        if val.startswith(m):
                            rest = val[len(m):]
                            is_action = (rest in ACTIONS or
                                         any(rest.endswith(sfx) and rest[:-2] in ACTIONS
                                             for sfx in ASPECT_SUFFIXES))
                            # A modifier may also scope a TARGET (sunodata =
                            # [without-delay] data). The LSP offers these
                            # completions, so the parser must accept them.
                            is_target = rest in TARGETS
                            if is_action or is_target:
                                modifiers.append(MODIFIERS[m])
                                val = rest
                                break
                                
                # Check aspect
                for asp_suf, asp_name in [("ba", "progressive"), ("ta", "perfective"), ("sa", "habitual")]:
                    if val.endswith(asp_suf) and val[:-2] in ACTIONS:
                        aspect = asp_name
                        val = val[:-2]
                        break
                            
                if val == "lo":
                    targets.append({"type": "operator", "value": "OR"})
                    continue
                
                if val in ("ina", "uta"):
                    nxt = self.lexer.peek()
                    if nxt and nxt.type in ("WORD", "STRING"):
                        scope_target = self.lexer.consume().value
                        # Resolve base target if it is a shorthand target
                        if scope_target.startswith("@"):
                            scope_target = scope_target[1:]
                            if ":" in scope_target:
                                scope_target = scope_target.split(":")[0]
                        targets.append({"type": "scope", "relation": val, "args": scope_target})
                    continue

                if val.startswith("ni") and len(val) >= 4 and len(val) % 2 == 0:
                    num_str = ""
                    valid_num = True
                    syls = [val[i:i+2] for i in range(2, len(val), 2)]
                    for s in syls:
                        if s in DIGITS:
                            num_str += DIGITS[s]
                        else:
                            valid_num = False
                    if valid_num:
                        targets.append({"type": "integer", "args": int(num_str)})
                        continue

                if val in TARGETS:
                    # Re-checked after affix decomposition (sunodata -> data).
                    targets.append({"type": val, "args": None})
                elif val in QUALITIES:
                    targets.append({"type": "quality", "args": val,
                                    "gloss": QUALITIES[val]})
                elif val in ACTIONS:
                    if action is None:
                        action = val
                    elif action in MODALS and modality is None:
                        modality = MODALS[action]
                        action = val
                    elif clause_open:
                        # A subordinate clause (opened by ke/pero/kasi/...) has
                        # its own predicate: 'visi tokopasa ke tu do'.
                        subclauses.append(val)
                        clause_open = False
                    else:
                        raise SyntaxError(
                            f"SyntaxError: stage already has action {action!r}; "
                            f"{val!r} is a second action -- separate them with 'te,' or '|>', "
                            f"or link them with a clause particle (ke, pero, kasi)"
                        )
                elif val in PARTICLES:
                    particles.append(PARTICLES[val])
                    if val in CLAUSE_PARTICLES:
                        clause_open = True
                elif val in DERIVATIONAL_SUFFIXES or val in ASPECT_SUFFIXES:
                    raise SyntaxError(
                        f"SyntaxError: {val!r} is a bound suffix and cannot stand alone"
                    )
                else:
                    # Strict: an unrecognised word is an error, not a literal.
                    # Free text must be quoted, or delimited by nomi ... fino.
                    raise SyntaxError(
                        f"SyntaxError: unknown word {val!r} is not in the Kona lexicon "
                        f"(quote it, or wrap it in 'nomi ... fino', to use it as a literal)"
                    )


            elif tok.type == "TARGET_AT":
                t = tok.raw[1:]
                arg = None
                if ":" in t:
                    parts = t.split(":", 1)
                    t = parts[0]
                    arg = parts[1].strip("\"'")
                # Resolve the English alias to its Kona root so that `@repo` and
                # `poya` produce the same target type -- this is what makes the
                # spoken and shorthand modalities compile to one identical AST.
                root = SHORTHAND_TARGET_MAP.get(t, t)
                if root not in TARGETS:
                    raise SyntaxError(
                        f"SyntaxError: unknown shorthand target '@{t}'"
                    )
                targets.append({"type": root, "args": arg})
            elif tok.type == "FORMAT_HASH":
                formats.append(SHORTHAND_FORMAT_MAP[tok.raw])
            elif tok.type == "GUARD":
                if tok.raw.startswith("!"):
                    guards.append(tok.raw[1:].strip("\"'"))
                elif tok.raw.startswith("notori"):
                    nxt = self.lexer.peek()
                    if nxt and nxt.type in ("WORD", "STRING"):
                        guards.append(self.lexer.consume().value)
                    else:
                        guards.append("general")
                elif tok.raw.startswith("no-"): guards.append(tok.raw[3:])
                else: guards.append(tok.raw)
            elif tok.type == "NOMI":
                literal_parts = []
                while self.lexer.peek() and self.lexer.peek().type != "FINO":
                    literal_parts.append(self.lexer.consume().raw)
                if self.lexer.peek() and self.lexer.peek().type == "FINO":
                    self.lexer.consume("FINO")
                targets.append({"type": "literal", "args": " ".join(literal_parts)})
            elif tok.type == "SI":
                # An embedded conditional opens a subordinate clause with its
                # own predicate: 'posi teli si neto nuki'.
                particles.append(PARTICLES["si"])
                clause_open = True
            elif tok.type == "STRING":
                # A string immediately after an un-argued target binds to it, so
                # spoken `poya "security"` and shorthand `@repo:"security"` yield
                # the same single target. Otherwise it stands as its own literal.
                if targets and targets[-1].get("args") is None \
                        and targets[-1]["type"] in TARGETS:
                    targets[-1]["args"] = tok.value
                else:
                    targets.append({"type": "literal", "args": tok.value})
            else:
                # Strict: no token may be silently discarded.
                raise SyntaxError(
                    f"SyntaxError: unexpected {tok.type} {tok.raw!r} in action expression"
                )
                
        # No implicit action. An utterance with no action word is a DECLARATIVE
        # (an assertion, as in the narrative benchmarks), not a command -- it
        # compiles to zero tool calls. Defaulting to 'yuki' (execute) meant any
        # unparsed noise became an execute call.
        return ActionNode(action, modifiers, targets, guards, formats, aspect,
                          particles, subclauses, modality)

def parse_kona(text: str) -> ASTNode:
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.parse()


# ============================================================================
# 2b. LEXICON VALIDATOR (phonotactics + acoustic distance)
# ============================================================================

# The consonant inventory the lexicon actually uses. See KONA_SPECIFICATION §3.2.
# 16 consonants. The voiced/voiceless pairs (/b p/, /d t/, /g k/, /v f/) are
# retained deliberately: the acoustic guarantee is enforced at the level of
# whole words by validate_lexicon(), not by banning phonemes. No two free
# lexemes differ by a single confusable phoneme, which is the property that
# actually protects transcription -- see the CONFUSABLE_PAIRS check below.
CONSONANTS = set("ptkbdgmnsfvlrwyj")
VOWELS = set("aeiou")

# Pairs a speech recogniser genuinely confuses under noise. Kona's acoustic
# guarantee is that no two FREE lexemes differ by exactly one of these.
CONFUSABLE_PAIRS = {
    frozenset(p) for p in
    [("b", "p"), ("d", "t"), ("g", "k"), ("v", "f"),
     ("l", "r"), ("m", "n"), ("s", "f")]
}


def _free_lexemes() -> set:
    """Words that can stand alone. Bound morphemes (digits, aspect suffixes,
    single-syllable modifiers) are excluded: they only ever occur affixed or
    inside a 'ni' numeral, where no free word can appear, so context alone
    disambiguates them."""
    return (set(ACTIONS) | set(TARGETS) | set(FORMATS) | set(PARTICLES)
            | set(QUALITIES))


def _confusable(a: str, b: str):
    """Return the confusable phoneme pair if a and b differ by exactly one."""
    if len(a) != len(b):
        return None
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    if len(diff) != 1:
        return None
    return diff[0] if frozenset(diff[0]) in CONFUSABLE_PAIRS else None


def validate_lexicon() -> List[str]:
    """Check the lexicon against the phonology in KONA_SPECIFICATION §3.

    Returns a list of violations; empty means the lexicon honours the spec.
    Run via `python3 kona.py --validate` and in the test suite, so the lexicon
    and the specification cannot drift apart again.
    """
    import itertools
    problems = []
    every = (set(ACTIONS) | set(TARGETS) | set(MODIFIERS)
             | set(FORMATS) | set(PARTICLES) | set(DIGITS) | set(QUALITIES))

    # 1. Phonotactics: every word is a run of (C)(G)V syllables, optional final
    #    'n'. G is a glide /w j/ -- a labialised or palatalised onset such as
    #    `kwe` or `dya` is a single articulation, not a cluster, and stays
    #    deterministically segmentable. See KONA_SPECIFICATION §3.3.
    cons = ''.join(sorted(CONSONANTS))
    vows = ''.join(sorted(VOWELS))
    syllable = re.compile(rf'^(?:[{cons}]?[wy]?[{vows}])+n?$')
    for w in sorted(every):
        if not syllable.match(w):
            bad = sorted({c for c in w if c not in CONSONANTS and c not in VOWELS})
            problems.append(
                f"phonotactics: {w!r} is not (C)V(n)"
                + (f" -- uses {bad} outside the inventory" if bad else " -- consonant cluster")
            )

    # 2. Acoustic distance: no two free lexemes may be a confusable minimal pair.
    free = sorted(_free_lexemes())
    for a, b in itertools.combinations(free, 2):
        pair = _confusable(a, b)
        if pair:
            problems.append(
                f"acoustic: {a!r} ~ {b!r} differ only by /{pair[0]}/ vs /{pair[1]}/"
            )

    # 3. No free lexeme may be a homophone of another.
    for a, b in itertools.combinations(free, 2):
        if a == b:
            problems.append(f"homophone: {a!r}")

    # 4. Digits must be mutually non-confusable inside a numeral.
    for a, b in itertools.combinations(sorted(DIGITS), 2):
        pair = _confusable(a, b)
        if pair:
            problems.append(
                f"numeral: digit {a!r}({DIGITS[a]}) ~ {b!r}({DIGITS[b]}) "
                f"differ only by /{pair[0]}/ vs /{pair[1]}/"
            )

    return problems

# ============================================================================
# 3. ACOUSTIC ENGINE (Speech Synthesis via macOS)
# ============================================================================

def speak_kona(kona_text: str, voice: Optional[str] = "Damayanti"):
    """
    Speaks Kona aloud using native macOS speech synthesis.
    Defaults to the Austronesian 'Damayanti' engine with moraic 'te' phrasing.
    """
    spoken = kona_text
    spoken = spoken.replace("|>", " te, ")
    spoken = spoken.replace(".", "")
    spoken = re.sub(r'@repo:?\"?([^\"]*)\"?', r'poya "\1"', spoken)
    spoken = re.sub(r'@code', 'kodo', spoken)
    spoken = re.sub(r'@file:?\"?([^\"]*)\"?', r'fili "\1"', spoken)
    spoken = re.sub(r'@web:?\"?([^\"]*)\"?', r'veba "\1"', spoken)
    spoken = re.sub(r'#table', 'mesa', spoken)
    spoken = re.sub(r'#json', 'jano', spoken)
    spoken = re.sub(r'!(\w+)', r'notori \1', spoken)

    print(f"🎙️ [Audio Engine Vocalizing with {voice}]: \"{spoken}\"")
    
    cmd = ["say"]
    if voice:
        cmd.extend(["-v", voice])
    cmd.extend(["-r", "170", spoken])
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Audio playback error: {e}", file=sys.stderr)

# ============================================================================
# 4. CLI DEMO
# ============================================================================

def demo():
    print("=" * 70)
    print("Kona Language Prototype: Spoken & Written Functional Agent Interface")
    print("=" * 70)

    samples = [
        (
            "Spoken: Deep Search -> Propose Refactor -> Table Summary",
            'dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa'
        ),
        (
            "Written Shorthand (Identical AST)",
            'kwe.de @repo:"security" |> tori.ve @code !"migrations" |> fasa #table'
        ),
        (
            "Conditional Logic: If Test Good -> Execute Task ELSE: Report Bug",
            'si teli bono te, yuki tafu ali fasa baki'
        ),
        (
            "Web Query -> JSON Data Extraction",
            'kwe veba "AWS Azure Q3 revenue" te, fasa jano'
        ),
    ]

    for label, code in samples:
        print(f"\n--- {label} ---")
        print(f"Kona Input:  {code}")
        ast = parse_kona(code)
        print("English Translation:")
        for line in ast.to_english():
            print(f"  • {line}")
        print("Compiled Agent Tool Calls:")
        print(json.dumps(ast.to_tool_calls(), indent=2))

def run_benchmarks():
    print("=" * 75)
    print("Kona Linguistic & Agentic Benchmarks Suite")
    print("=" * 75)

    benchmarks = [
        {
            "id": "Benchmark 1",
            "title": "Collaborative Debugging & Problem-Solving Dialogue",
            "lines": [
                ("User", 'mi visi tokopasa ke tu do, pero baki nosapi kasi data yuki dura'),
                ("User", 'tu posi teli neto ke nuki pasa te, reoki'),
                ("User", 'si ye te, koli debi peli masi tokofini te, para kwena'),
                ("Agent", 'mi teli sunodata neto te, neto no nuki pero data yuki masi deko sekuni kasi seli'),
                ("Agent", 'mi poki ke koli nuki seli pasa te, reteli toko kwena')
            ]
        },
        {
            "id": "Benchmark 2",
            "title": "Technical System Procedure: Token Expiry & Cache Invalidation",
            "lines": [
                ("Spec", 'ti yoti kwe seku te, teli seku ina memo'),
                ("Spec", 'si seku fini te, leke suno futu uta neto seku'),
                ("Spec", 'tori seku te, do memo pasa duo toko')
            ]
        },
        {
            "id": "Benchmark 3",
            "title": "Universal Narrative Benchmark: The North Wind and the Sun",
            "lines": [
                ("Story", 'venito noreti mapo soli nowapo dura ke masi powa, ti irayoti veni ina tela kalu'),
                ("Story", 'ona wapo ke yoti maki irayoti te, nuki tela te, debi sapi masi powa supera'),
                ("Story", 'futu venito noreti do powa sama muto te, pero masi venito yuki te, masi irayoti koli tela'),
                ("Story", 'futu soli do luke mapo kalu te ina suno toko irayoti nuki tela'),
                ("Story", 'kono venito noreti debi fasa ye ke soli masi powa supera duo')
            ]
        }
    ]

    for bm in benchmarks:
        print(f"\n{'#' * 75}")
        print(f"[{bm['id']}] {bm['title']}")
        print(f"{'#' * 75}")
        for speaker, utterance in bm["lines"]:
            print(f"\n[{speaker}] {utterance}")
            ast = parse_kona(utterance)
            print("  Parsed Pipeline AST:")
            for line in ast.to_english():
                print(f"    • {line}")
            tool_calls = ast.to_tool_calls()
            if tool_calls:
                print(f"  Emitted Agent Tool Operations ({len(tool_calls)}):")
                for tc in tool_calls:
                    params_summary = []
                    if tc["parameters"]["modifiers"]:
                        params_summary.append(f"mods={tc['parameters']['modifiers']}")
                    if tc["parameters"]["targets"]:
                        params_summary.append(f"targets={[t['type'] for t in tc['parameters']['targets']]}")
                    if tc["parameters"]["prohibited_invariants"]:
                        params_summary.append(f"guards={tc['parameters']['prohibited_invariants']}")
                    if tc["parameters"]["condition"]:
                        params_summary.append(f"if={tc['parameters']['condition']}")
                    summary_str = f" ({', '.join(params_summary)})" if params_summary else ""
                    print(f"    -> {tc['tool']}{summary_str}")

def repl():
    print("=" * 60)
    print("Kona Interactive REPL (type 'exit' to quit, 'say <cmd>' to vocalize)")
    print("=" * 60)
    while True:
        try:
            cmd = input("\nkona> ").strip()
            if not cmd:
                continue
            if cmd in ("exit", "quit"):
                break
            if cmd.startswith("say "):
                speak_kona(cmd[4:])
                continue
            ast = parse_kona(cmd)
            print("\nEnglish Intent:")
            for line in ast.to_english():
                print(f"  • {line}")
            print("\nAgent Tool Calls:")
            print(json.dumps(ast.to_tool_calls(), indent=2))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Kona REPL.")
            break
        except SyntaxError as e:
            # A parse error must not end the session.
            print(f"  ✗ {e}")
        except Exception as e:
            print(f"  ✗ internal error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = " ".join(sys.argv[1:])
        if arg == "--demo":
            demo()
        elif arg == "--benchmarks":
            run_benchmarks()
        elif arg == "--repl":
            repl()
        elif arg == "--validate":
            problems = validate_lexicon()
            if problems:
                print(f"✗ Lexicon violates KONA_SPECIFICATION §3 ({len(problems)} issues):")
                for p in problems:
                    print(f"  - {p}")
                sys.exit(1)
            print("✓ Lexicon honours KONA_SPECIFICATION §3 "
                  "(phonotactics, acoustic distance, numeral distinctness).")
        elif arg.startswith("--say "):
            text = arg[6:]
            speak_kona(text)
        else:
            ast = parse_kona(arg)
            print("English Translation:")
            for line in ast.to_english():
                print(f"  • {line}")
            print("\nAgent Tool Calls:")
            print(json.dumps(ast.to_tool_calls(), indent=2))
    else:
        demo()
