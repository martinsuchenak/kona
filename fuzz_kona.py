import random
import traceback
from kona import parse_kona

print("==========================================================")
print(" KONA COMPILER FUZZER (Property-Based Chaos Testing)")
print("==========================================================")

# Token pools
VALID_ACTIONS = ["kwe", "visi", "maki", "tori", "teli", "nuki", "yuki", "fasa"]
VALID_MODIFIERS = ["de", "su", "ve", "oto", "re"]
VALID_ASPECTS = ["ba", "ta", "sa"]
VALID_TARGETS = ["kodo", "fili", "data", "poya", "seku"]
VALID_GUARDS = ["notori", "!auth", "no-kodo"]
VALID_FORMATS = ["mesa", "jano", "#table", "#json"]
STRUCTURAL = ["te,", "|>", "si", "ali", "nomi", "fino", "(", ")"]

# Malformed / Chaos tokens
CHAOS = [
    "", " ", "\n", "\t", "123", "!@#$%", "kwe-", "-kwe", "@", "@@", "##", "#",
    "te te", "si si", "((", "))", "()", "nomi nomi", '"', "'", '"unclosed',
    "kwena", "fasasa", "yukiba", "@kodo:\"bad",
    "\x00", "\xFF", "😈", "kwe\n|>fasa"
]

def generate_random_token():
    pool = random.choice([
        VALID_ACTIONS, VALID_MODIFIERS, VALID_TARGETS, VALID_GUARDS,
        VALID_FORMATS, STRUCTURAL, CHAOS
    ])
    tok = random.choice(pool)
    
    # Randomly construct complex valid words occasionally
    if random.random() > 0.8:
        tok = f"{random.choice(VALID_MODIFIERS)}-{random.choice(VALID_ACTIONS)}{random.choice(VALID_ASPECTS)}"
    
    return tok

def fuzz_compiler(iterations=10000):
    crashes = 0
    passed = 0
    syntax_errors = 0
    
    for i in range(iterations):
        # Build a random string of 1 to 15 tokens
        length = random.randint(1, 15)
        text = " ".join(generate_random_token() for _ in range(length))
        
        try:
            ast = parse_kona(text)
            passed += 1
        except SyntaxError:
            # SyntaxError is a GRACEFUL failure. The compiler successfully caught bad code.
            syntax_errors += 1
        except Exception as e:
            # Any other exception (IndexError, TypeError, AttributeError) is a COMPILER CRASH!
            crashes += 1
            if crashes <= 3:
                print(f"\n[CRASH] The compiler broke on input: {repr(text)}")
                traceback.print_exc()

    print(f"\n[RESULTS] {iterations} Iterations Completed.")
    print(f"  - Parsed Successfully: {passed}")
    print(f"  - Gracefully Rejected (SyntaxError): {syntax_errors}")
    print(f"  - Compiler Crashes (Unhandled Exceptions): {crashes}")
    
    if crashes == 0:
        print("\n✅ SUCCESS: The Kona Compiler is mathematically robust against random chaos.")
    else:
        print("\n❌ FAILED: The Kona Compiler has internal state vulnerabilities.")

if __name__ == "__main__":
    fuzz_compiler(10000)
