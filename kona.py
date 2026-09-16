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

class KonaPipeline:
    def __init__(self, raw: str):
        self.raw = raw
        self.steps: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_raw": self.raw,
            "pipeline_length": len(self.steps),
            "execution_steps": self.steps
        }

    def to_english(self) -> List[str]:
        """Translates the parsed Kona pipeline into clear English steps."""
        lines = []
        for s in self.steps:
            prefix = ""
            if s.get("condition"):
                prefix = f"IF ({s['condition']}) THEN: "
            action = s["action"].capitalize()
            mods = f" [{', '.join(s['modifiers'])}]" if s["modifiers"] else ""
            targets = []
            for t in s["targets"]:
                t_str = f"@{t['type']}" + (f"('{t['value']}')" if t["value"] else "")
                targets.append(t_str)
            target_str = f" on {', '.join(targets)}" if targets else ""
            args_str = f" with args {s['arguments']}" if s["arguments"] else ""
            
            guards = ""
            if s["guards_prohibited"]:
                guards = " (STRICT GUARD: DO NOT " + ", ".join(
                    f"{g['action']} {g['target']}" for g in s["guards_prohibited"]
                ) + ")"
            
            fmt = f" -> Format output as {s['output_format']}" if s["output_format"] else ""
            else_branch = f" [ELSE: {s['alternative']}]" if s.get("alternative") else ""
            lines.append(f"Step {s['step_index']}: {prefix}{action}{mods}{target_str}{args_str}{guards}{fmt}{else_branch}")
        return lines

    def to_tool_calls(self) -> List[Dict[str, Any]]:
        """Compiles Kona pipeline into executable agent tool calls."""
        calls = []
        for s in self.steps:
            tool_name = f"agent_{s['action']}"
            params = {
                "condition": s.get("condition"),
                "modifiers": s["modifiers"],
                "targets": s["targets"],
                "arguments": s["arguments"],
                "prohibited_invariants": s["guards_prohibited"],
                "format": s["output_format"],
                "else_branch": s.get("alternative")
            }
            calls.append({"tool": tool_name, "parameters": params})
        return calls

def parse_kona(text: str) -> KonaPipeline:
    """
    Parses both Spoken Kona and Written Shorthand into a normalized pipeline AST.
    Pipeline delimiters:
      - Written shorthand: '|>'
      - Spoken Kona: 'te,' or 'te ' (consecutive action connector)
    """
    text = text.strip()
    pipeline = KonaPipeline(text)

    # Detect pipe splitters: '|>' or spoken particle 'te' (with optional comma)
    if "|>" in text:
        raw_stages = [s.strip() for s in text.split("|>")]
    else:
        # Split on 'te' preceded and followed by word boundaries/punctuation
        raw_stages = [s.strip() for s in re.split(r'[\s,]+te[\s,]+|\bte\b', text)]

    i = 0
    while i < len(raw_stages):
        stage = raw_stages[i]
        if not stage:
            i += 1
            continue

        # Check if stage is a conditional prefix: 'si [cond]'
        if stage.startswith("si ") or stage.startswith("si:"):
            cond_text = stage[3:].strip()
            i += 1
            if i < len(raw_stages):
                next_stage = raw_stages[i]
                alt = None
                if " ali " in next_stage:
                    main_act, alt = next_stage.split(" ali ", 1)
                elif " :else: " in next_stage:
                    main_act, alt = next_stage.split(" :else: ", 1)
                else:
                    main_act = next_stage
                step = parse_stage(main_act, len(pipeline.steps))
                step["condition"] = cond_text
                step["alternative"] = alt.strip() if alt else None
                pipeline.steps.append(step)
                i += 1
                continue
        
        step = parse_stage(stage, len(pipeline.steps))
        pipeline.steps.append(step)
        i += 1

    return pipeline

def parse_stage(stage: str, index: int) -> Dict[str, Any]:
    condition = None
    alternative = None

    # Check for conditional: si [condition] ... ali [alternative]
    if stage.startswith("si ") or stage.startswith("si:"):
        # Check for alternative branch
        if " ali " in stage:
            parts = stage.split(" ali ", 1)
            stage_main = parts[0]
            alternative = parts[1].strip()
        elif " :else: " in stage:
            parts = stage.split(" :else: ", 1)
            stage_main = parts[0]
            alternative = parts[1].strip()
        else:
            stage_main = stage
        
        # Extract condition: first 2-3 words after 'si'
        cond_tokens = split_tokens(stage_main)
        if len(cond_tokens) > 2:
            condition = f"{cond_tokens[1]} {cond_tokens[2]}"
            # The remaining tokens represent the action
            stage = " ".join(cond_tokens[3:]) if len(cond_tokens) > 3 else cond_tokens[1]
        else:
            condition = cond_tokens[1] if len(cond_tokens) > 1 else "true"
            stage = " ".join(cond_tokens[2:])

    tokens = split_tokens(stage)
    
    action_info = {"verb": None, "modifiers": []}
    targets = []
    literals = []
    guards_prohibited = []
    out_format = None

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        # 1. Check for negative guards: e.g. !tori @"auth", no-tori "auth", or bound notori "auth"
        if tok.startswith("!") or tok.startswith("no-") or (tok.startswith("no") and tok[2:] in ACTIONS):
            if tok.startswith("!"):
                guard_verb = tok.lstrip("!")
            elif tok.startswith("no-"):
                guard_verb = tok.replace("no-", "")
            else:
                guard_verb = tok[2:]
            i += 1
            guard_target = tokens[i] if i < len(tokens) else None
            guards_prohibited.append({
                "action": guard_verb,
                "target": clean_literal(guard_target) if guard_target else None
            })
            i += 1
            continue

        # 2. Check for format markers: #table, #json or mesa, jano
        if tok in SHORTHAND_FORMAT_MAP:
            out_format = SHORTHAND_FORMAT_MAP[tok]
            i += 1
            continue
        if tok in FORMATS:
            out_format = FORMATS[tok]
            i += 1
            continue

        # 3. Check for shorthand targets: @repo, @code, @file("...")
        if any(tok.startswith(prefix) for prefix in SHORTHAND_TARGET_MAP):
            for prefix, mapped in SHORTHAND_TARGET_MAP.items():
                if tok.startswith(prefix):
                    val = tok[len(prefix):].lstrip(":").strip("()\"'")
                    if not val and i + 1 < len(tokens) and (tokens[i+1].startswith('"') or tokens[i+1].startswith("'")):
                        i += 1
                        val = clean_literal(tokens[i])
                    targets.append({"type": mapped, "value": val if val else None})
                    break
            i += 1
            continue

        # 4. Check for actions with modifiers:
        # e.g., 'de-kwe', 'kwe.de', 've-tori', 'tori.ve', 'kwe'
        base_verb, mods = extract_verb_and_modifiers(tok)
        if base_verb in ACTIONS:
            action_info["verb"] = ACTIONS[base_verb]["name"]
            action_info["modifiers"].extend(mods)
            i += 1
            continue

        # 5. Check for plain targets (spoken): kodo, fili, veba
        if tok in TARGETS:
            target_type = TARGETS[tok]
            # Check if next token is a string literal argument
            if i + 1 < len(tokens) and (tokens[i+1].startswith('"') or tokens[i+1].startswith("'")):
                i += 1
                targets.append({"type": target_type, "value": clean_literal(tokens[i])})
            else:
                targets.append({"type": target_type, "value": None})
            i += 1
            continue

        # 6. Fallback string literals
        if tok.startswith('"') or tok.startswith("'"):
            literals.append(clean_literal(tok))
            i += 1
            continue

        # General literal / identifier
        literals.append(tok)
        i += 1

    return {
        "step_index": index + 1,
        "action": action_info["verb"] or "process",
        "modifiers": action_info["modifiers"],
        "targets": targets,
        "arguments": literals,
        "guards_prohibited": guards_prohibited,
        "output_format": out_format
    }

def split_tokens(s: str) -> List[str]:
    pattern = r'[!#@]?[\w\.\-]+|\"[^\"]*\"|\'[^\']*\''
    return re.findall(pattern, s)

def clean_literal(s: str) -> str:
    return s.strip("\"'")

def extract_verb_and_modifiers(tok: str):
    mods = []
    # 1. Check dot shorthand: kwe.de, tori.ve
    if "." in tok:
        parts = tok.split(".")
        verb = parts[0]
        for m in parts[1:]:
            if m in MODIFIERS:
                mods.append(MODIFIERS[m])
        return verb, mods
    
    # 2. Check hyphenated notation: de-kwe, su-fasa
    if "-" in tok:
        parts = tok.split("-")
        verb = parts[-1]
        for p in parts[:-1]:
            if p in MODIFIERS:
                mods.append(MODIFIERS[p])
        return verb, mods

    # 3. Check bound morpheme prefix: dekwe, vetori, sufasa, sunodata
    for m in sorted(MODIFIERS.keys(), key=len, reverse=True):
        if tok.startswith(m) and tok[len(m):] in ACTIONS:
            return tok[len(m):], [MODIFIERS[m]]

    return tok, []

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
