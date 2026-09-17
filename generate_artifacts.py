#!/usr/bin/env python3
"""Generate derived artifacts from the single source of truth in kona.py.

Both kona.ebnf and playground.html used to carry hand-maintained copies of the
lexicon, and both had drifted: the playground was down to 20 of 31 actions and
22 of 83 targets, so the "live compiler" on the demo page was running a
different language from the compiler.

Run this after any lexicon change:

    python3 generate_artifacts.py          # rewrite the artifacts
    python3 generate_artifacts.py --check  # fail if they are out of date (CI)
"""

import json
import re
import sys
from pathlib import Path

from kona import (
    ACTIONS, TARGETS, MODIFIERS, FORMATS, PARTICLES, DIGITS,
    ASPECT_SUFFIXES, DERIVATIONAL_SUFFIXES, SHORTHAND_TARGET_MAP,
    SHORTHAND_FORMAT_MAP, CONSONANTS, VOWELS,
)

ROOT = Path(__file__).parent
BEGIN = "(* BEGIN GENERATED -- edit kona.py, then run generate_artifacts.py *)"
END = "(* END GENERATED *)"
JS_BEGIN = "// BEGIN GENERATED -- edit kona.py, then run generate_artifacts.py"
JS_END = "// END GENERATED"


def _alternation(name, items, comment_of=None, indent=4):
    """Render an EBNF alternation, one lexeme per line with its gloss."""
    pad = " " * indent
    lines = [f"{name}"]
    for i, item in enumerate(sorted(items)):
        lead = "=" if i == 0 else "|"
        gloss = comment_of(item) if comment_of else None
        text = f'{pad}{lead} "{item}"'
        if gloss:
            text = f"{text:<24}(* {gloss} *)"
        lines.append(text)
    lines.append(f"{pad};")
    return "\n".join(lines)


def build_ebnf_section() -> str:
    parts = [
        BEGIN,
        "",
        "(* Terminal vocabularies below are generated from kona.py. Do not edit",
        "   them here: edit the lexicon and regenerate. *)",
        "",
        _alternation("BaseAction", ACTIONS, lambda w: ACTIONS[w]["name"]),
        "",
        _alternation("BaseTarget", TARGETS, lambda w: TARGETS[w]),
        "",
        _alternation("Modifier", MODIFIERS, lambda w: MODIFIERS[w]),
        "",
        _alternation("FormatSpecifier", FORMATS, lambda w: FORMATS[w]),
        "",
        _alternation("Particle", PARTICLES, lambda w: PARTICLES[w]),
        "",
        _alternation("Digit", DIGITS, lambda w: DIGITS[w]),
        "",
        _alternation("AspectSuffix", ASPECT_SUFFIXES, lambda w: ASPECT_SUFFIXES[w]),
        "",
        _alternation("DerivationalSuffix", DERIVATIONAL_SUFFIXES,
                     lambda w: DERIVATIONAL_SUFFIXES[w]),
        "",
        _alternation("ShorthandTargetAlias", SHORTHAND_TARGET_MAP,
                     lambda w: f"= {SHORTHAND_TARGET_MAP[w]}"),
        "",
        "(* Phonology, enforced by kona.validate_lexicon() *)",
        f"Consonant = {' | '.join(chr(34)+c+chr(34) for c in sorted(CONSONANTS))} ;",
        f"Vowel     = {' | '.join(chr(34)+v+chr(34) for v in sorted(VOWELS))} ;",
        'Glide     = "w" | "y" ;',
        "Syllable  = [ Consonant ] , [ Glide ] , Vowel ;",
        'Word      = Syllable , { Syllable } , [ "n" ] ;',
        "",
        END,
    ]
    return "\n".join(parts)


def build_playground_section() -> str:
    def js(name, obj):
        return f"    const {name} = {json.dumps(obj, indent=6, sort_keys=True)};"

    actions = {k: v["name"] for k, v in ACTIONS.items()}
    # The marker lines carry no leading indent here: splice() replaces the
    # markers themselves, so adding indent would compound on every run.
    return "\n".join([
        JS_BEGIN,
        js("ACTIONS", actions),
        js("ACTION_DESC", {k: v["desc"] for k, v in ACTIONS.items()}),
        js("TARGETS", dict(TARGETS)),
        js("MODIFIERS", dict(MODIFIERS)),
        js("FORMATS", dict(FORMATS)),
        js("PARTICLES", dict(PARTICLES)),
        js("DIGITS", dict(DIGITS)),
        js("ASPECTS", dict(ASPECT_SUFFIXES)),
        js("SHORTHAND_TARGETS", dict(SHORTHAND_TARGET_MAP)),
        js("SHORTHAND_FORMATS", dict(SHORTHAND_FORMAT_MAP)),
        JS_END,
    ])


def splice(path: Path, begin: str, end: str, payload: str) -> str:
    text = path.read_text()
    pattern = re.compile(
        re.escape(begin) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: payload, text)
    raise SystemExit(
        f"{path.name}: could not find the generated block markers.\n"
        f"  Expected a region delimited by:\n    {begin}\n    {end}")


def main(check=False):
    targets = [
        (ROOT / "kona.ebnf", BEGIN, END, build_ebnf_section()),
        (ROOT / "playground.html", JS_BEGIN, JS_END, build_playground_section()),
    ]
    stale = []
    for path, begin, end, payload in targets:
        if not path.exists():
            print(f"  skip {path.name} (not found)")
            continue
        new = splice(path, begin, end, payload)
        if new != path.read_text():
            stale.append(path.name)
            if not check:
                path.write_text(new)
                print(f"  updated {path.name}")
        else:
            print(f"  up to date: {path.name}")

    if check and stale:
        print(f"\n✗ out of date: {', '.join(stale)}")
        print("  run: python3 generate_artifacts.py")
        return 1
    if not check:
        print("\n✓ artifacts regenerated from kona.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
