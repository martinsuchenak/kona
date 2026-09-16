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

## Documentation

- [Language Specification](KONA_SPECIFICATION.md): Core theory, phonetics, formal grammar, and linguistic benchmarks.
- [Comprehensive Lexicon](LEXICON.md): 19-section reference dictionary covering numbers, actions, hardware, negotiation, conditionals, and real-world workflows.
- [Agent System Prompt](kona_system_prompt.md): Ready-to-use system prompt for zero-shot Kona execution in any foundation LLM.

---

## Quickstart

Run the compiler demo:
```bash
python3 kona.py --demo
```

Run the formal benchmark suite (3 linguistic benchmarks):
```bash
python3 kona.py --benchmarks
```

Launch the interactive REPL:
```bash
python3 kona.py --repl
```

Test conditional logic and pipelines directly from the CLI:
```bash
python3 kona.py 'si teli bono te, yuki tafu ali fasa baki'
```

---

## Proven Benchmarks

Kona has been verified against three formal linguistic stress-tests (`python3 kona.py --benchmarks`):
1. **Collaborative Problem-Solving & Debugging Dialogue**: Technical dispute, relative clauses (`ke`), durative aspect (`dura`), and contrastive preferences.
2. **Technical System Specification**: Authentication token expiry, caching constraints, and sequential procedure execution.
3. **The North Wind and the Sun (Universal Narrative Benchmark)**: Narrative storytelling, causative constructions (`maki`), and correlative comparatives (`masi A te, masi B`).

