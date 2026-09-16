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
    "plani": {"name": "plan",      "desc": "Plan/Schedule/Sequence"},
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
    "doko":  {"name": "agree",     "desc": "Agree/Align/Consent"},
    "poki":  {"name": "propose",   "desc": "Propose/Suggest/Offer"},
    "keti":  {"name": "decide",    "desc": "Decide/Resolve/Determine"},
    "sapi":  {"name": "know",      "desc": "Know/Understand/Comprehend"},
    "veni":  {"name": "arrive",    "desc": "Arrive/Come/Approach"},
    "peli":  {"name": "delay",     "desc": "Delay/Postpone/Defer"},
    "tapi":  {"name": "type",      "desc": "Type/Keystroke/Input"},
    # Ext: Workflow & Git
    "yalo":  {"name": "approve",   "desc": "Approve/Accept/Merge"},
    "nolo":  {"name": "reject",    "desc": "Reject/Block/Revert"},
    "koma":  {"name": "compare",   "desc": "Compare/Diff"},
    "fiso":  {"name": "fix",       "desc": "Fix/Patch/Resolve"},
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
    "deli": "container_docker",
    "sisa": "system_os",
    "seli": "resource_lock",
    # Natural & Physical World
    "vento": "wind_air",
    "soli":  "sun_solar",
    "norte": "north_direction",
    "tela":  "fabric_cloak",
    "kalu":  "thermal_warmth",
    "luce":  "light_illumination",
    "powa":  "power_energy",
    "toko":  "time_interval",
    "sekunda": "second_unit",
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
    "delikaba": "sandbox_env",
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
    # Core Persons
    "mi":   "user_speaker",
    "tu":   "agent_listener",
    "ona":  "external_entity",
    "koli": "team_collective",
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

FORMATS = {
    "mesa": "table",
    "poti": "bullet_list",
    "jano": "json",
    "puro": "plain_text",
    "difa": "diff",
}

# Canonical mappings for shorthand
SHORTHAND_TARGET_MAP = {
    "@code":    "code",
    "@file":    "file",
    "@web":     "web",
    "@repo":    "repo",
    "@git":     "version_git",
    "@vcs":     "version_git",
    "@bug":     "bug_issue",
    "@issue":   "bug_issue",
    "@test":    "test_spec",
    "@docker":  "container_docker",
    "@sandbox": "container_docker",
    "@url":     "page_url",
    "@page":    "page_url",
    "@link":    "link",
    "@api":     "network_api",
    "@data":      "data_db",
    "@db":        "data_db",
    "@memo":      "memory_context",
    "@memory":    "memory_context",
    "@auth":      "security_secret",
    "@secret":    "security_secret",
    "@task":      "task",
    "@msg":       "message_email",
    "@mail":      "message_email",
    "@user":      "user_speaker",
    "@agent":     "agent_listener",
    "@team":      "team_collective",
    # Hardware & Physical compounds
    "@mic":       "microphone",
    "@cam":       "camera",
    "@screen":    "screen_display",
    "@display":   "screen_display",
    "@kb":        "keyboard",
    "@battery":   "battery_power",
    "@workspace": "workspace_ide",
    "@deadline":  "deadline",
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
            ("PIPE", r'\|>|te\s*,|te(?!\w)'),
            ("LPAREN", r'\('),
            ("RPAREN", r'\)'),
            ("STRING", r'"[^"]*"|\'[^\']*\''),
            ("NOMI", r'nomi\b'),
            ("FINO", r'fino\b'),
            ("SI", r'si\b'),
            ("ALI", r'(ali|:else:)\b'),
            ("GUARD", r'(![a-zA-Z_-]+|notori\b|no-[a-zA-Z_-]+)'),
            ("TARGET_AT", r'@[a-zA-Z_-]+(:("[^"]*"|\'[^\']*\'))?'),
            ("FORMAT_HASH", r'#(table|list|json|raw|diff)'),
            ("WORD", r'[a-zA-Z_-]+')
        ]
        
        scanner = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in rules))
        for match in scanner.finditer(self.text):
            type_ = match.lastgroup
            raw = match.group()
            if type_ == "WHITESPACE": continue
            
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
            for ec in else_calls:
                ec["parameters"]["condition"] = f"NOT ({' '.join(self.condition)})"
            calls.extend(else_calls)
        return calls

class ActionNode(ASTNode):
    def __init__(self, action, modifiers, targets, guards, formats, aspect=None):
        self.action = action
        self.modifiers = modifiers
        self.targets = targets
        self.guards = guards
        self.formats = formats
        self.aspect = aspect
        
    def to_english(self):
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
        return [{
            "tool": f"agent_{ACTIONS.get(self.action, {"name": self.action})["name"].lower()}",
                        "parameters": {
                "aspect": self.aspect,
                "modifiers": self.modifiers,
                "targets": self.targets,
                "prohibited_invariants": self.guards,
                "format_requested": self.formats,
                "condition": None
            }
        }]

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse(self):
        return self.parse_pipeline()

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
            while self.lexer.peek() and self.lexer.peek().type not in ("PIPE",):
                tok = self.lexer.consume()
                if tok.raw == ":": break
                condition.append(tok.raw)
            if self.lexer.peek() and self.lexer.peek().type == "PIPE":
                self.lexer.consume("PIPE")
                
        if self.lexer.peek() and self.lexer.peek().type == "LPAREN":
            self.lexer.consume("LPAREN")
            body = self.parse_pipeline()
            self.lexer.consume("RPAREN")
        else:
            body = self.parse_action_expr()
            
        if self.lexer.peek() and self.lexer.peek().type == "ALI":
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
        
        while self.lexer.peek() and self.lexer.peek().type not in ("PIPE", "ALI", "RPAREN"):
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
                    for m in sorted(MODIFIERS.keys(), key=len, reverse=True):
                        # Avoid prematurely matching modifier if it is nominalization (handled above) or aspect
                        if val.startswith(m):
                            rest = val[len(m):]
                            if rest in ACTIONS or (rest.endswith("ba") and rest[:-2] in ACTIONS) or (rest.endswith("ta") and rest[:-2] in ACTIONS) or (rest.endswith("sa") and rest[:-2] in ACTIONS):
                                modifiers.append(MODIFIERS[m])
                                val = rest
                                break
                                
                # Check aspect
                for asp_suf, asp_name in [("ba", "progressive"), ("ta", "perfective"), ("sa", "habitual")]:
                    if val.endswith(asp_suf) and val[:-2] in ACTIONS:
                        aspect = asp_name
                        val = val[:-2]
                        break
                            
                if val in ACTIONS:
                    action = val
                else:
                    targets.append({"type": "literal", "args": val})
                    
            elif tok.type == "TARGET_AT":
                t = tok.raw[1:]
                arg = None
                if ":" in t:
                    parts = t.split(":", 1)
                    t = parts[0]
                    arg = parts[1].strip("\"'")
                targets.append({"type": t, "args": arg})
            elif tok.type == "FORMAT_HASH":
                formats.append(SHORTHAND_FORMAT_MAP[tok.raw])
            elif tok.type == "GUARD":
                if tok.raw.startswith("!"): guards.append(tok.raw[1:])
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
            elif tok.type == "STRING":
                targets.append({"type": "literal", "args": tok.value})
                
        if not action:
            action = "yuki" # fallback implicit action
            
        return ActionNode(action, modifiers, targets, guards, formats, aspect)

def parse_kona(text: str) -> ASTNode:
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.parse()

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
            'kwe.de @repo:"security" |> tori.ve @code !tori @"migrations" |> fasa #table'
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
                ("User", 'tu posi teli si neto nuki pasa reoki'),
                ("User", 'si ye, koli debi peli masi tokofini, no retori kwe'),
                ("Agent", 'mi teli sunodata neto te, neto no nuki pero data yuki masi deko sekunda kasi seli'),
                ("Agent", 'mi poki ke koli nuki seli pasa te, reteli toko kwe')
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
                ("Story", 'vento norte to soli nodoko dura ke masi powa, ti irayoti veni ina tela kalu'),
                ("Story", 'ona doko ke yoti ke pasa maki irayoti nuki tela debi sapi masi powa supra ali'),
                ("Story", 'futu vento norte do powa sama muto posi, pero masi vento yuki te masi irayoti koli tela'),
                ("Story", 'futu soli do luce to kalu te ina suno toko irayoti nuki tela'),
                ("Story", 'kono vento norte debi fasa ye ke soli masi powa supra duo')
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = " ".join(sys.argv[1:])
        if arg == "--demo":
            demo()
        elif arg == "--benchmarks":
            run_benchmarks()
        elif arg == "--repl":
            repl()
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
