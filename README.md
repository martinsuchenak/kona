# Kona (コナビ)

**A Purely Functional, Acoustically Engineered Language for Human–AI Communication**

Kona is an engineered constructed language designed specifically for high-efficiency communication between human operators and AI agents across both **speech (ASR / TTS)** and **compact written prompts**.

---

## Key Highlights

- **Purely Functional**: Every sentence evaluates as an algebraic pipeline ($\text{Action}(\text{Target}) \mid \text{Invariants} \mid> \text{Continuation}$). The grammar is a strict recursive descent over a closed lexicon: an unknown word, an unbalanced paren or a stray `ali` is a syntax error, never a silently-accepted guess.
- **Acoustic Separation**: 5 cardinal vowels (`/a, e, i, o, u/`) and a strict $(C)(G)V(n)$ moraic cadence. Machine-checked invariant: zero homophones, zero true consonant clusters, and **no two free lexemes differ by a single confusable phoneme** (`python3 kona.py --validate`).
- **The 5 Universal Derivational Affixes**:
  1. `no-` (Polar Opposite): `bono` (good) $\to$ `nobono` (bad)
  2. `-koso` (Physical Hardware): `kisi` (hear) $\to$ `kisikoso` (microphone)
  3. `-peji` (Display / Surface): `visi` (see) $\to$ `visipeji` (screen / monitor)
  4. `-kaba` (Environment / Workspace): `kodo` (code) $\to$ `kodokaba` (IDE / workspace)
  5. `-yoti` (Specialist / Role): `kodo` (code) $\to$ `kodoyoti` (developer)
- **Keystroke Compression**: ~70% fewer characters than natural English.
- **Token cost — measured, not claimed**: Kona uses **+61.6% more tokens** than
  terse English of equivalent meaning (`cl100k_base`, 10 tasks). Its roots are
  invented strings absent from the BPE vocabulary and average **1.98 tokens per
  word**; the derivational compounds are worst (`kodoyoti` = 4 tokens vs
  `developer` = 1). The former "50–70% reduction" headline compared against
  deliberately padded English using a fallback estimator with no vocabulary.
  Kona's wins are unambiguous structure and keystrokes — not tokens.
  Reproduce: `./bench-env/bin/python benchmark_tokens.py`.
- **Dual-Modality Isomorphism** — both forms compile to a byte-identical AST (asserted by the test suite):
  - **Spoken Kona**: `dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa`
  - **Written Shorthand**: `kwe.de @repo:"security" |> tori.ve @code !"migrations" |> fasa #table`

---

## Documentation & Specification

- [Language Specification](KONA_SPECIFICATION.md): Core theory, phonetics, formal grammar, and linguistic benchmarks.
- [Comprehensive Lexicon](LEXICON.md): 19-section reference dictionary covering numbers, actions, hardware, negotiation, conditionals, and real-world workflows.
- [Formal EBNF Grammar](kona.ebnf): Standard ISO/IEC 14977 context-free grammar specification.
- [Agent System Prompt](kona_system_prompt.md): Ready-to-use system prompt for zero-shot Kona execution in any foundation LLM.

---

## Interactive Playground

Open [`playground.html`](playground.html) in any web browser to access the live dual-modality playground:
- Real-time compiler generating AST, emitted agent tool calls, and English translations as you type.
- Live keystroke compression meter against natural English.
- Native speech synthesis vocalizer using $(C)(G)V(n)$ moraic cadence.

The playground's lexicon is generated from `kona.py` by `generate_artifacts.py`,
so it cannot drift from the reference compiler. Note that the playground still
carries its own JavaScript *parser*; only the vocabulary is shared.

---

## Quickstart & CLI Tools

Run the compiler demo:
```bash
python3 kona.py --demo
```

Run the unit and regression test suite:
```bash
python3 test_kona.py
```

Check the lexicon against the phonology in the specification:
```bash
python3 kona.py --validate
```

Regenerate derived artifacts (EBNF terminals, playground lexicon) from `kona.py`:
```bash
python3 generate_artifacts.py          # rewrite
python3 generate_artifacts.py --check  # CI: fail if stale
```

Fuzz the whole compile path (parse + tool-call emission + translation):
```bash
python3 fuzz_kona.py
```

Run the token and compression benchmark. Install `tiktoken` first — without it
the script falls back to a vocabulary-free estimator that materially overstates
Kona's advantage, and it says so loudly:
```bash
python3 -m venv bench-env
./bench-env/bin/python -m pip install -r requirements-dev.txt
./bench-env/bin/python benchmark_tokens.py
```

Run the linguistic benchmark evaluation suite:
```bash
python3 kona.py --benchmarks
```

Launch the interactive REPL:
```bash
python3 kona.py --repl
```

Test pipelines directly from the CLI:
```bash
python3 kona.py 'si teli bono te, yuki tafu ali fasa baki'
```

---

## Editor Syntax Highlighting

Kona includes TextMate syntax highlighting for VS Code and compatible editors:
- Grammar: [`syntaxes/kona.tmLanguage.json`](syntaxes/kona.tmLanguage.json)
- Config: [`language-configuration.json`](language-configuration.json)
- Sample: [`example.kona`](example.kona)

### VS Code Extension

Build and package the extension (bundles the language client via esbuild):
```bash
npm install
npm run compile     # or: npm run package   -> kona-language-<version>.vsix
code --install-extension kona-language-0.3.0.vsix
```

The extension starts `kona_lsp.py`. It picks an interpreter in this order:
`kona.pythonPath` setting → the interpreter selected in the Python extension →
a workspace-local `lsp-env` (**trusted workspaces only**) → `python3` on PATH.

---

## Linguistic Benchmarks

Kona is exercised against three linguistic stress-tests (`python3 kona.py --benchmarks`):
1. **Collaborative Problem-Solving & Debugging Dialogue**: Technical dispute, relative clauses (`ke`), durative aspect (`dura`), and contrastive preferences.
2. **Technical System Specification**: Authentication token expiry, caching constraints, and sequential procedure execution.
3. **The North Wind and the Sun (Universal Narrative Benchmark)**: Narrative storytelling, causative constructions (`maki`), and correlative comparatives (`masi A te, masi B`).

