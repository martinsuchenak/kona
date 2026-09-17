#!/usr/bin/env python3
"""Kona token & compression benchmark.

Methodology notes, because the previous version overstated the result by a
wide margin:

1. TOKENIZER. Kona's words are invented strings. A real BPE vocabulary does not
   contain `kwe`, `dekwe`, `pakokaba` or `tokopasa`, so it splits them into 2-4
   pieces each. The old fallback estimator was purely length-based with no
   vocabulary, scoring every Kona word as exactly 1 token, which flattered Kona
   and penalised long English words. The estimator is still available so the
   script runs anywhere, but its numbers are labelled ESTIMATED and it refuses
   to print a headline figure. Install tiktoken for a real measurement.

2. BASELINE. Comparing telegraphic Kona against padded English ("Please perform
   an exhaustive search across the entire...") measures the padding, not the
   language. Each task now carries both a `english_natural` phrasing and an
   `english_terse` one -- what a competent operator would actually type. The
   terse baseline is the honest comparison and is the one reported first.

3. GUARDS. "Guard Invariant Verification: 100%" used to be a hardcoded literal
   in the task data. It is now measured: the utterance is compiled and the
   guards are read back off the AST.
"""

import re
import sys

from kona import parse_kona

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

try:
    import tiktoken
    ENC = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(ENC.encode(text))

    TOKENIZER_NAME = "tiktoken (cl100k_base)"
    TOKENIZER_IS_REAL = True
except ImportError:
    def count_tokens(text: str) -> int:
        """Length-based approximation. NOT a substitute for a real tokenizer.

        It has no vocabulary, so it cannot model the fragmentation that a real
        BPE applies to out-of-vocabulary Kona roots. It systematically
        UNDERCOUNTS Kona. Treat its output as an upper bound on Kona's
        advantage, never as a measurement.
        """
        words = re.findall(r"[A-Za-z]+|\d+|[^\w\s]", text)
        count = 0
        for w in words:
            if len(w) > 6 and w.isalpha():
                count += 1 + (len(w) - 6) // 4
            else:
                count += 1
        return count

    TOKENIZER_NAME = "length-based estimator (NOT a real tokenizer)"
    TOKENIZER_IS_REAL = False


BENCHMARK_TASKS = [
    {
        "name": "1. Deep Security Audit",
        "english_natural": "Please perform an exhaustive search across the entire security repository, analyze the vulnerabilities, and present the final findings formatted as a markdown table.",
        "english_terse": "exhaustively search security repo, report findings as a table",
        "kona_spoken": 'dekwe poya "security" te, fasa mesa',
        "kona_written": 'kwe.de @repo:"security" |> fasa #table',
    },
    {
        "name": "2. Safe Dry-Run Refactoring",
        "english_natural": "Propose a refactoring for the main codebase, but under no circumstances should you modify any files in the migrations directory. Show a dry-run preview.",
        "english_terse": "dry-run refactor code, never touch migrations, show diff",
        "kona_spoken": 'vetori kodo notori "migrations" te, fasa difa',
        "kona_written": 'tori.ve @code !"migrations" |> fasa #diff',
        "expect_guards": ["migrations"],
    },
    {
        "name": "3. Web Data Extraction",
        "english_natural": "Query the web for the latest AWS and Azure Q3 cloud revenue figures, extract the core metrics, and output the result strictly in valid JSON format.",
        "english_terse": "search web for AWS Azure Q3 revenue, output JSON",
        "kona_spoken": 'kwe veba "AWS Azure Q3 revenue" te, fasa jano',
        "kona_written": 'kwe @web:"AWS Azure Q3 revenue" |> fasa #json',
    },
    {
        "name": "4. Conditional Deploy / Rollback",
        "english_natural": "Run the automated test suite, and if the tests pass successfully, deploy the task to production. Otherwise, report a bug issue.",
        "english_terse": "run tests; if pass, deploy task; else report bug",
        "kona_spoken": 'si teli bono te, yuki tafu ali fasa baki',
        "kona_written": 'si teli bono |> yuki @task :else: fasa @bug',
    },
    {
        "name": "5. Token Expiry & Cache Flush",
        "english_natural": "When the user requests secret credentials, check the secret in cache memory. If expired, immediately fetch a new token from the network API, update the secret, and save to cache for two time intervals.",
        "english_terse": "on secret request check cache; if expired fetch new token from API, update secret, cache for 2 intervals",
        "kona_spoken": 'ti yoti kwe seku te, teli seku ina memo te, leke suno futu uta neto seku te, tori seku te, do memo pasa duo toko',
        "kona_written": 'kwe @seku |> teli @memo |> leke.suno @api |> tori @seku |> do @memo',
    },
    {
        "name": "6. Sandbox Test Execution",
        "english_natural": "Initialize a clean isolated Docker container environment, execute all regression test specifications inside the sandbox, and summarize the results as a bulleted list.",
        "english_terse": "start clean sandbox, run regression tests inside, summarize as list",
        "kona_spoken": 'oki pakokaba te, yuki tesi ina pakokaba te, fasa poti',
        "kona_written": 'oki @sandbox |> yuki @test ina pakokaba |> fasa #list',
    },
    {
        "name": "7. Fast Git Pull & Build",
        "english_natural": "Fetch the latest git commits from the remote repository immediately, and run the automated build and verification checks on the code.",
        "english_terse": "pull latest git, run build and checks",
        "kona_spoken": 'leke vasi te, teli kodo',
        "kona_written": 'leke @git |> teli @code',
    },
    {
        "name": "8. Resource Lock Release",
        "english_natural": "Check whether the resource mutex lock is currently active. If locked, release the lock immediately and restart the query loop.",
        "english_terse": "if lock held, release it and restart query loop",
        "kona_spoken": 'si seli dura te, nuki seli te, reteli toko',
        "kona_written": 'si seli dura |> nuki @lock |> teli.re @toko',
    },
    {
        "name": "9. User Screen Camera Check",
        "english_natural": "Inspect the user camera hardware and the primary display monitor, verify both devices are functional, and send a notification message.",
        "english_terse": "check camera and display work, then notify",
        "kona_spoken": 'visi visikoso mapo visipeji te, teli te, do meso',
        "kona_written": 'visi @cam @display |> teli |> do @msg',
    },
    {
        "name": "10. Brief Status Triage",
        "english_natural": "Give me a very brief, high-level summary explaining the current error log history without diving into deep file implementation details.",
        "english_terse": "brief summary of error log history",
        "kona_spoken": 'sufasa tokopasa baki',
        "kona_written": 'fasa.su @log',
    },
]


def _measure_guards(task):
    """Measure, rather than assert, that declared guards survive compilation."""
    expected = task.get("expect_guards")
    if not expected:
        return None
    per_form = []
    for form in ("kona_spoken", "kona_written"):
        found = []
        for stage in parse_kona(task[form]).stages:
            found.extend(getattr(stage.body, "guards", []))
        per_form.append(sorted(found))
    # The guard must survive in BOTH modalities, identically.
    return all(g == sorted(expected) for g in per_form)


def report_fragmentation():
    """Show how the tokenizer splits the lexicon.

    This is the mechanism behind the token result. Kona roots are invented
    strings absent from any BPE vocabulary, so they fragment; the derivational
    compounds (`-koso`, `-kaba`, `-yoti`) fragment worst, which is unfortunate
    because they are the language's headline feature.
    """
    if not TOKENIZER_IS_REAL:
        print("  (needs a real tokenizer: pip install tiktoken)")
        return

    import collections
    from kona import (ACTIONS, TARGETS, MODIFIERS, PARTICLES, QUALITIES, FORMATS)

    words = sorted(set(ACTIONS) | set(TARGETS) | set(MODIFIERS)
                   | set(PARTICLES) | set(QUALITIES) | set(FORMATS))
    counts = {w: count_tokens(w) for w in words}
    total = sum(counts.values())

    print("\nLEXICON FRAGMENTATION")
    print(f"  {len(words)} lexemes -> {total} tokens "
          f"({total / len(words):.2f} tokens per word)")
    hist = collections.Counter(counts.values())
    for n in sorted(hist):
        print(f"    {n} token(s): {hist[n]:3} words")

    print("\n  Worst (all are derivational compounds):")
    for w in sorted(words, key=lambda w: -counts[w])[:6]:
        pieces = [ENC.decode([t]) for t in ENC.encode(w)]
        print(f"    {w:10} {counts[w]} tokens  {pieces}")

    print("\n  The same concepts in English:")
    for kona_word, english in [("kodoyoti", "developer"), ("kodokaba", "workspace"),
                               ("kisikoso", "microphone"), ("tokofini", "deadline")]:
        print(f"    {kona_word:10} {counts.get(kona_word, count_tokens(kona_word))} vs "
              f"{english:10} {count_tokens(english)}")


def run_benchmark():
    width = 104
    print("=" * width)
    print("KONA TOKEN & COMPRESSION BENCHMARK")
    print(f"Tokenizer: {TOKENIZER_NAME}")
    if not TOKENIZER_IS_REAL:
        print()
        print("  ! No real tokenizer available. The estimator has no vocabulary, so it")
        print("    scores every invented Kona root as a single token while a real BPE")
        print("    splits them into 2-4. Numbers below OVERSTATE Kona's advantage.")
        print("    Install tiktoken for a real measurement:  pip install tiktoken")
    print("=" * width)

    hdr = (f"{'Task':<32} | {'EN nat':>6} | {'EN terse':>8} | {'Kona spk':>8} | "
           f"{'vs natural':>10} | {'vs terse':>9}")
    print(hdr)
    print("-" * width)

    tot_nat = tot_terse = tot_spk = tot_wrt = 0
    parsed_ok = 0
    guard_results = []

    for task in BENCHMARK_TASKS:
        nat = count_tokens(task["english_natural"])
        terse = count_tokens(task["english_terse"])
        spk = count_tokens(task["kona_spoken"])
        wrt = count_tokens(task["kona_written"])

        tot_nat += nat
        tot_terse += terse
        tot_spk += spk
        tot_wrt += wrt

        try:
            parse_kona(task["kona_spoken"])
            parse_kona(task["kona_written"])
            parsed_ok += 1
        except SyntaxError as e:
            print(f"  ! {task['name']}: does not compile -- {e}")

        g = _measure_guards(task)
        if g is not None:
            guard_results.append(g)

        print(f"{task['name']:<32} | {nat:>6} | {terse:>8} | {spk:>8} | "
              f"{100*(spk-nat)/nat:>9.1f}% | {100*(spk-terse)/terse:>8.1f}%")

    print("=" * width)
    print(f"\nTOTALS over {len(BENCHMARK_TASKS)} tasks")
    print(f"  English (natural phrasing) ....... {tot_nat} tokens")
    print(f"  English (terse phrasing) ......... {tot_terse} tokens")
    print(f"  Kona spoken ...................... {tot_spk} tokens")
    print(f"  Kona written ..................... {tot_wrt} tokens")
    print()
    print(f"  Kona spoken vs natural English ... {100*(tot_spk-tot_nat)/tot_nat:+.1f}%"
          "   <- flattering comparison: measures English padding")
    print(f"  Kona spoken vs terse English ..... {100*(tot_spk-tot_terse)/tot_terse:+.1f}%"
          "   <- the honest like-for-like figure")
    if not TOKENIZER_IS_REAL:
        print("       (both figures are an UPPER BOUND on Kona's advantage -- see the")
        print("        tokenizer warning above)")
    else:
        print()
        print("  Kona costs MORE tokens than terse English. Its roots are invented")
        print("  strings absent from the BPE vocabulary, so they fragment; see the")
        print("  fragmentation table below. Kona's wins are unambiguous structure")
        print("  and keystrokes, not tokens.")

    print()
    print(f"  Compiles (spoken + written) ...... {parsed_ok}/{len(BENCHMARK_TASKS)}")
    if guard_results:
        ok = sum(1 for g in guard_results if g)
        print(f"  Guards survive compilation ....... {ok}/{len(guard_results)} "
              f"(measured from the AST, not asserted)")
    else:
        print("  Guards ........................... no guarded tasks in this set")
    report_fragmentation()
    print("=" * width)

    return 0 if parsed_ok == len(BENCHMARK_TASKS) else 1


if __name__ == "__main__":
    sys.exit(run_benchmark())
