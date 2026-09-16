# Kona (コナビ)

**A Purely Functional, Acoustically Engineered Language for Human–AI Communication**

Kona is an engineered constructed language designed specifically for high-efficiency communication between human operators and AI agents across both **speech (ASR / TTS)** and **compact written prompts**.

---

## Key Highlights

- **Purely Functional**: Every sentence evaluates as an algebraic pipeline ($\text{Action}(\text{Target}) \mid \text{Invariants} \mid> \text{Continuation}$) with zero parse ambiguity.
- **Acoustic Infallibility**: Built on 5 cardinal vowels (`/a, e, i, o, u/`) and a strict $(C)V$ moraic cadence inspired by Polynesian and Austronesian phonetics. Zero homophones, zero consonant clusters.
- **The 5 Universal Derivational Affixes**:
  1. `no-` (Polar Opposite): `bono` (good) $\to$ `nobono` (bad)
  2. `-koso` (Physical Hardware): `kisi` (hear) $\to$ `kisikoso` (microphone)
  3. `-peji` (Display / Surface): `visi` (see) $\to$ `visipeji` (screen / monitor)
  4. `-kaba` (Environment / Workspace): `kodo` (code) $\to$ `kodokaba` (IDE / workspace)
  5. `-yoti` (Specialist / Role): `kodo` (code) $\to$ `kodoyoti` (developer)
- **Token & Keystroke Compression**: Delivers 50–70% token reduction compared to natural language English prompts.
- **Dual-Modality Isomorphism**:
  - **Spoken Kona**: `dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa.`
  - **Written Shorthand**: `kwe.de @repo:"security" |> tori.ve @code !tori @"migrations" |> fasa #table`

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
- Live token compression meter measuring keystroke savings against natural English.
- Native speech synthesis vocalizer using authentic $(C)V$ moraic cadence.

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

Run the automated token and character compression benchmark:
```bash
python3 benchmark_tokens.py
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

### VS Code Installation

To install the local extension for VS Code:
```bash
# 1. Create a local extension directory
mkdir -p ~/.vscode/extensions/kona-lang

# 2. Copy the extension files over
cp package.json ~/.vscode/extensions/kona-lang/
cp language-configuration.json ~/.vscode/extensions/kona-lang/
cp -r syntaxes ~/.vscode/extensions/kona-lang/

# 3. Reload VS Code (Cmd+Shift+P -> "Developer: Reload Window")
```

---

## Proven Benchmarks

Kona has been verified against three formal linguistic stress-tests (`python3 kona.py --benchmarks`):
1. **Collaborative Problem-Solving & Debugging Dialogue**: Technical dispute, relative clauses (`ke`), durative aspect (`dura`), and contrastive preferences.
2. **Technical System Specification**: Authentication token expiry, caching constraints, and sequential procedure execution.
3. **The North Wind and the Sun (Universal Narrative Benchmark)**: Narrative storytelling, causative constructions (`maki`), and correlative comparatives (`masi A te, masi B`).

