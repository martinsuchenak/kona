import random
import sys
import traceback

from kona import parse_kona

# Token pools
VALID_ACTIONS = ["kwe", "visi", "maki", "tori", "teli", "nuki", "yuki", "fasa"]
VALID_MODIFIERS = ["de", "su", "ve", "oto", "re"]
VALID_ASPECTS = ["ba", "ta", "sa"]
VALID_TARGETS = ["kodo", "fili", "data", "poya", "seku"]
VALID_GUARDS = ["notori", "!auth", "no-kodo"]
VALID_FORMATS = ["mesa", "jano", "#table", "#json"]
STRUCTURAL = ["te,", "|>", "si", "ali", "nomi", "fino", "(", ")", "ke", "pero"]

# Malformed / chaos tokens
CHAOS = [
    "", " ", "\n", "\t", "123", "!@#$%", "kwe-", "-kwe", "@", "@@", "##", "#",
    "te te", "si si", "((", "))", "()", "nomi nomi", '"', "'", '"unclosed',
    "kwena", "fasasa", "yukiba", "@kodo:\"bad",
    "\x00", "\xFF", "😈", "kwe\n|>fasa",
]


def generate_random_token():
    pool = random.choice([
        VALID_ACTIONS, VALID_MODIFIERS, VALID_TARGETS, VALID_GUARDS,
        VALID_FORMATS, STRUCTURAL, CHAOS,
    ])
    tok = random.choice(pool)

    # Occasionally build a complex well-formed word
    if random.random() > 0.8:
        tok = f"{random.choice(VALID_MODIFIERS)}-{random.choice(VALID_ACTIONS)}{random.choice(VALID_ASPECTS)}"

    return tok


def fuzz_compiler(iterations=10000, seed=None):
    """Fuzz the WHOLE compile path.

    The previous version stopped at parse_kona() and reported the compiler
    "mathematically robust". Every AST consumer -- to_tool_calls() and
    to_english() -- has to be exercised too: running the identical token pools
    through them surfaced 1656 TypeErrors in 20000 inputs, on inputs as short
    as 'ali ve'. A crash in the emitter is just as much a compiler bug as a
    crash in the parser.
    """
    if seed is not None:
        random.seed(seed)

    parsed = 0
    syntax_errors = 0
    crashes = 0
    seen = {}

    for _ in range(iterations):
        length = random.randint(1, 15)
        text = " ".join(generate_random_token() for _ in range(length))

        try:
            ast = parse_kona(text)
            # These are the stages the old fuzzer never reached.
            ast.to_tool_calls()
            ast.to_english()
            parsed += 1
        except SyntaxError:
            # A graceful, reported rejection. This is correct behaviour.
            syntax_errors += 1
        except Exception as e:
            crashes += 1
            key = type(e).__name__
            if key not in seen:
                seen[key] = text
                if crashes <= 3:
                    print(f"\n[CRASH] {key} on input: {text!r}")
                    traceback.print_exc()

    print(f"\n[RESULTS] {iterations} iterations (parse + to_tool_calls + to_english)")
    print(f"  - Compiled successfully .............. {parsed}")
    print(f"  - Gracefully rejected (SyntaxError) .. {syntax_errors}")
    print(f"  - Unhandled crashes .................. {crashes}")
    for kind, example in seen.items():
        print(f"      {kind}: e.g. {example!r}")

    if crashes == 0:
        print("\n✅ No unhandled exception reached any stage of the compiler.")
    else:
        print(f"\n❌ {crashes} inputs crashed the compiler.")
    return crashes


if __name__ == "__main__":
    print("=" * 62)
    print(" KONA COMPILER FUZZER (full compile path)")
    print("=" * 62)
    sys.exit(1 if fuzz_compiler(10000, seed=None) else 0)
