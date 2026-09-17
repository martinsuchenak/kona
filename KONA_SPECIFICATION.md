# Kona (コナビ): Language Specification & Concept Document
**A Purely Functional, Acoustically Engineered Language for Human-AI Communication**

---

## 1. Executive Summary & Vision

**Kona** is a constructed spoken and written language (conlang) specifically engineered to optimize interaction between human operators and AI agents. It addresses two primary bottlenecks in modern human-AI interaction:

1. **The Acoustic Bottleneck (Speech / TTS / ASR)**: Natural languages suffer from phonemic overlap, homophones, indistinct consonant clusters, and ambiguous word boundaries that degrade automated speech recognition (ASR) and speech synthesis (TTS).
2. **The Semantic Bottleneck (Writing / Prompting)**: Natural-language prompts are structurally ambiguous around negative constraints, variable scoping and execution pipelines. Kona's contribution here is *unambiguous structure*, not token savings. Measured with `cl100k_base` across 10 agent tasks, Kona costs **+61.6% more tokens** than terse English of equivalent meaning, because its invented roots are out-of-vocabulary and fragment at 1.98 tokens per word (§5.1). Earlier claims of 50–70% savings compared against deliberately padded English using a fallback estimator that had no vocabulary and therefore scored every Kona word as a single token.

Kona models every interaction as a **purely functional computation**:
* **Intent as Pure Function Application**: Every utterance evaluates an explicit operation over typed inputs, subject to strict invariant guards.
* **Acoustically Separated Phonology**: Five cardinal vowels and a strict $(C)(G)V(n)$ cadence, with a machine-checked guarantee that no two free lexemes differ by a single confusable phoneme (§3.2). This bounds the error, it does not eliminate it: no phonology makes a recogniser infallible.
* **Dual-Modality Isomorphism**: A flowing spoken form and a dense written shorthand that compile to a byte-identical AST. This is enforced by `TestDualModalityIsomorphism` in the test suite, not merely asserted.

---

## 2. Theoretical Roots & Inspirations

Kona is an original language synthesis standing on the shoulders of several major traditions across linguistics, logic, and computer science:

| Tradition / Language | What Kona Adopts | What Kona Improves |
| :--- | :--- | :--- |
| **Montague Semantics & Lambda Calculus** | Treats all natural language phrases as formal functions ($e \to t$, $(e \to t) \to (e \to t)$). | Replaces academic mathematical notation with a natural, spoken syntax. |
| **Lojban / Loglan** | Syntactic unambiguity, predicate calculus foundation. | Replaces Lojban's harsh, difficult consonant clusters (`prami`, `klama`) with high-flow phonology. |
| **Toaq** | Particle-based quantifier scoping and formal functional semantics. | Tailors the lexicon directly to agentic execution and multi-agent coordination. |
| **Toki Pona & Polynesian Languages** | Minimalist, crystal-clear 5-vowel inventory, CV syllable structure, maximum acoustic contrast. | Expands expressive precision to handle complex engineering, data, and logic workflows. |
| **Functional Programming (Elixir / Haskell)** | Forward pipeline operator (`\|>`), referential transparency, immutable variable binding, guard constraints. | Brings algebraic composition directly into natural human speech. |

---

## 3. Phonology & Acoustic Engine

To guarantee that Speech-to-Text (ASR) models never mishear words and Text-to-Speech (TTS) models sound distinct and melodic:

### 3.1. Vowel Inventory (5 Cardinal Vowels)
Kona uses the five extreme points of the human vocal tract vowel space:
* `/a/` (*father*) — Open central
* `/e/` (*bed / café*) — Close-mid front
* `/i/` (*machine*) — Close front
* `/o/` (*more / tone*) — Close-mid back
* `/u/` (*flute*) — Close back

*Design rationale: There are no subtle diphthongs, reduced vowels (schwas), or near-collisions (such as English /ɪ/ vs /i:/ or /ʊ/ vs /u:/).*

### 3.2. Consonant Inventory (16 Consonants)

| Class | Consonants | IPA | Acoustic Characteristic |
| :--- | :--- | :--- | :--- |
| **Plosives** | `p`, `t`, `k`, `b`, `d`, `g` | /p t k b d g/ | Sharp onset, distinct burst transient |
| **Nasals** | `m`, `n` | /m n/ | Strong low-frequency resonance |
| **Fricatives** | `s`, `f`, `v` | /s f v/ | High-frequency spectral energy |
| **Affricate** | `j` | /dʒ/ | Distinct from every other onset |
| **Liquids & Glides** | `l`, `r`, `w`, `y` | /l r w j/ | Continuous, unmistakable formant glides |

#### Why the voicing pairs are retained

An earlier version of this specification declared a 10-consonant inventory that
excluded /b/, /d/, /g/ and /v/ on the grounds that voicing pairs are the classic
ASR confusion. That rule was never actually honoured — 38% of the lexicon used
the excluded consonants — and, more importantly, enforcing it would have made
transcription **worse**, not better.

The measurement (reproducible via `kona.validate_lexicon`):

| Lexicon | Minimal pairs | Voicing-confusable | Outright homophones |
| :--- | ---: | ---: | ---: |
| 16 consonants (current) | 77 | **0** | 0 |
| relexified to "pure" 10 | 114 | 2 | **3** |

Packing a fixed vocabulary into a smaller phonetic space *increases*
confusability. Collapsing the inventory merges the old `deli`/`teli`,
`doko`/`toko` and `du`/`tu` into true homophones — the exact failure the
restriction was meant to prevent.

**The guarantee Kona actually makes is at the level of words, not phonemes:**

> No two free lexemes differ by exactly one confusable phoneme,
> where the confusable pairs are /b p/, /d t/, /g k/, /v f/, /l r/, /m n/, /s f/.

This is machine-checked. `python3 kona.py --validate` fails the build if any
lexicon change violates it, and the same check runs as a unit test. Bound
morphemes are exempt by construction: the digit syllables occur only inside a
`ni`-prefixed numeral and the single-syllable modifiers occur only affixed to a
root, so no free word can appear in those slots to be confused with them.

Reaching zero required three changes: `deli` → `pako` (container), `doko` →
`wapo` (agree), and defining the conjunction as `mapo` (the previously-used
`to` was never in the lexicon at all, and collided with the action `do`).

### 3.3. Phonotactics & Syllables
* **Syllable Template**: `(C)(G)V`, with an optional nasal coda `n` permitted
  only word-finally. `G` is a glide /w j/.
* **Glide onsets are single articulations, not clusters.** `kwe` /kʷe/ and `dya`
  /dʲa/ are one labialised or palatalised onset. This is the standard
  Austronesian pattern and remains deterministically segmentable, because a
  glide is acoustically distinct from the vowel that follows it.
* **No true consonant clusters**: *str-*, *spl-*, *-kst*, and mid-word codas
  such as the *-nt-* in the old `vento` are forbidden. The four words that
  violated this — `vento`, `norte`, `sekunda`, `plani` — are now `venito`,
  `noreti`, `sekuni`, `pilani`. Two further words used consonants outside the
  inventory and were replaced: `luce` → `luke` and the digit `ze` (0) → `wo`.
* **Stress Rule**: Always on the penultimate syllable. This lets a recogniser
  segment words deterministically in continuous speech.
* **Whole-word-first resolution**: a word that is itself a lexeme is never
  decomposed into affixes. This is what keeps `veba` (web) from being read as
  `ve`+`ba`, `rego` (policy) as `re`+`go`, `nolo` (reject) as `no`+`lo`, or
  `debi` (must) as `de`+`bi`. Decomposition is attempted only when whole-word
  lookup fails.

---

## 4. The Pure Functional Grammar

### 4.1. The Type Hierarchy
In Kona, every concept has a formal semantic type:

1. **Entity ($\mathbf{e}$)**: Concrete or abstract data objects (files, repos, numbers, strings, tools, agents).
2. **Predicate / Action ($\mathbf{e \to t}$ or $\mathbf{e \to e}$)**: Functions that map entities to results or states.
3. **Higher-Order Modifier ($\mathbf{(e \to t) \to (e \to t)}$)**: Bound prefix functions that transform other actions (e.g. `dekwe`, `vetori`, `sufasa`).
4. **Guard / Invariant ($\mathbf{Constraint}$)**: Explicit bound prohibitions (e.g. `notori` = STRICTLY DO NOT modify).

### 4.2. Sentence Structure (The Evaluation Model)
Every command to an AI evaluates as an algebraic pipeline:

$$\mathbf{Function}(\mathbf{Target}) \;\vert\; \mathbf{Invariants} \;\vert> \mathbf{Continuation}$$

* **Spoken Kona**: Uses bound prefixes and the percussive connector **`te`** (inspired by Japanese action chaining):
  $$\text{[Action + Target]} + [\mathbf{notori} + \text{Invariants}] + [\mathbf{te,} + \text{Next Action}]$$
* **Written Shorthand**:
  $$\text{fn}(\text{args}) \ ![\text{guards}] \ \vert> \ \text{fn}_2$$
* **Relative Clauses**: Attached via linker **`ke`**:
  $$\mathbf{[Noun]} + \mathbf{ke} + \mathbf{[Clause]} \implies \text{tokopasa ke tu do (logs that you sent)}$$
* **Ternary Conditionals**: Formatted algebraically:
  $$\mathbf{si} \ \text{[Condition]} \ \mathbf{te,} \ \text{[Action]} \ \mathbf{ali} \ \text{[Alternative]}$$

### 4.3. The 5 Universal Derivational Affixes
1. **`no-` (Polar Opposite)**: `bono` (good) $\to$ `nobono` (bad), `fasi` (easy) $\to$ `nofasi` (hard), `pura` (safe) $\to$ `nopura` (risky).
2. **`-koso` (Physical Device)**: `kisi` (hear) $\to$ `kisikoso` (mic), `sono` (sound) $\to$ `sonokoso` (speaker), `tapi` (type) $\to$ `tapikoso` (keyboard).
3. **`-peji` (Display / Surface)**: `visi` (see) $\to$ `visipeji` (screen/monitor), `kiri` (write) $\to$ `kiripeji` (editor canvas).
4. **`-kaba` (Environment / Space)**: `kodo` (code) $\to$ `kodokaba` (IDE workspace), `pako` (container) $\to$ `pakokaba` (sandbox).
5. **`-yoti` (Specialist / Role)**: `kodo` (code) $\to$ `kodoyoti` (developer), `maki` (create) $\to$ `makiyoti` (designer).

---

## 5. Language Benchmarks

Three linguistic stress-tests. Every utterance below is verbatim from
`kona.py --benchmarks` and is asserted to compile end-to-end by
`TestCompilePathRobustness`; the specification can no longer quote Kona that
the compiler would reject.

### Benchmark 1: Collaborative Problem-Solving & Debugging Dialogue
```
User:  mi visi tokopasa ke tu do, pero baki nosapi kasi data yuki dura
User:  tu posi teli neto ke nuki pasa te, reoki
User:  si ye te, koli debi peli masi tokofini te, para kwena
Agent: mi teli sunodata neto te, neto no nuki pero data yuki masi deko sekuni kasi seli
Agent: mi poki ke koli nuki seli pasa te, reteli toko kwena
```

### Benchmark 2: Technical System Specification
```
Spec: ti yoti kwe seku te, teli seku ina memo
Spec: si seku fini te, leke suno futu uta neto seku
Spec: tori seku te, do memo pasa duo toko
```

### Benchmark 3: Universal Narrative Benchmark (The North Wind and the Sun)
```
Story: venito noreti mapo soli nowapo dura ke masi powa, ti irayoti veni ina tela kalu
Story: ona wapo ke yoti maki irayoti te, nuki tela te, debi sapi masi powa supera
Story: futu venito noreti do powa sama muto te, pero masi venito yuki te, masi irayoti koli tela
Story: futu soli do luke mapo kalu te ina suno toko irayoti nuki tela
Story: kono venito noreti debi fasa ye ke soli masi powa supera duo
```

---

### 5.1. Token Cost (measured)

Measured with `tiktoken` / `cl100k_base` over the 10 agent tasks in
`benchmark_tokens.py`:

| Baseline | Tokens | Kona spoken | Delta |
| :--- | ---: | ---: | ---: |
| English, natural phrasing | 272 | 181 | −33.5% |
| English, terse phrasing | 112 | 181 | **+61.6%** |

**Kona costs more tokens than terse English.** The mechanism is
out-of-vocabulary fragmentation: no BPE vocabulary contains Kona's invented
roots, so they split into pieces. Across the 165-lexeme vocabulary the mean is
**1.98 tokens per word**, and only 30 lexemes encode as a single token.

The derivational compounds — `-koso`, `-kaba`, `-yoti`, the feature the language
leads with — are the worst affected:

| Kona | Tokens | BPE pieces | English | Tokens |
| :--- | ---: | :--- | :--- | ---: |
| `kodoyoti` | 4 | `k` `od` `oy` `oti` | developer | 1 |
| `kodokaba` | 4 | `k` `od` `ok` `aba` | workspace | 1 |
| `kisikoso` | 4 | `k` `is` `ik` `oso` | microphone | 2 |
| `tokofini` | 3 | `tok` `of` `ini` | deadline | 1 |

This does not invalidate the design; it relocates its value. Kona's advantages
are **unambiguous structure** (guards, scoping and pipelines that cannot be
misread) and **keystrokes/speech**, where a short (C)(G)V word is fast to say and
easy to recognise. Token efficiency is not among them, and the specification no
longer claims it.

Two levers exist if token cost matters for a given deployment:

1. **Prefer the written shorthand.** It uses English aliases (`@repo`, `@code`)
   that are in-vocabulary: 151 tokens versus 181 for the spoken form.
2. **Choose single-token spellings.** Lexeme spelling is a free parameter. A
   relexification that selects roots which encode as one BPE token would close
   most of the gap — at the cost of breaking every existing corpus, and it would
   tie the language to one tokenizer's vocabulary.

---

## 6. Real-World Demonstrations

Both modalities below compile to a byte-identical AST.

### Example 1: Code Review & Dry-Run Fix
* **Kona Spoken**:
  > `dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa`
* **Kona Shorthand**:
  > `kwe.de @repo:"security" |> tori.ve @code !"migrations" |> fasa #table`

Note the guard form: `!"migrations"` is the shorthand counterpart of spoken
`notori "migrations"`. The earlier `!tori @"migrations"` was malformed — it
guarded the *action* `tori` and left `migrations` dangling as a separate target,
so the two modalities did not in fact agree.

### Example 2: Rapid Data Extraction & Analysis
* **Kona Spoken**:
  > `kwe veba "AWS Azure Q3 revenue" te, fasa jano`
* **Kona Shorthand**:
  > `kwe @web:"AWS Azure Q3 revenue" |> fasa #json`

The argument form is `@target:"value"`. Parentheses are reserved for nested
pipelines: `@veba("...")` opened a sub-pipeline and silently discarded the
`fasa #json` stage.


---

## 7. Implementation Status & Roadmap

| Milestone | Status | Details |
| :--- | :--- | :--- |
| **1. Phonetic Synthesis & Verification** | **Completed** | Native macOS speech engine (`Damayanti`, Austronesian Latin phonotactics), 5 cardinal vowels, moraic `te` pacing. |
| **2. Python Compiler & Transpiler** | **Completed** | `kona.py`: strict recursive-descent parser over a closed lexicon, dual-modality (spoken `te,` and written `\|>`), AST, guards, English translation, tool-call emission. Unknown words, unbalanced parens and stray `ali` are syntax errors. |
| **3. Lexicon Validator** | **Completed** | `kona.py --validate` enforces §3 phonotactics and the acoustic-distance invariant. Runs as a unit test, so the lexicon cannot drift from this document. |
| **4. Dual-Modality Isomorphism** | **Completed** | Spoken and shorthand forms compile to a byte-identical AST, asserted by `TestDualModalityIsomorphism`. |
| **5. Constraint-Preserving Tool Router** | **Completed** | `kona_router.py` carries guards, dry-run and conditions into the emitted call, and raises `UnroutableError` rather than emitting a call that silently does more than it was asked. |
| **6. Multi-Benchmark Evaluation Suite** | **Completed** | 3 benchmarks, every utterance asserted to compile end-to-end. |
| **7. Portable LLM Agent System Prompt** | 🟡 **Active** | `kona_system_prompt.md` for zero-shot Kona in any foundation model. |
| **8. Formal Grammars** | 🟡 **Active** | `kona.ebnf` and `Kona.g4` describe the surface syntax; terminal vocabularies are generated from `kona.py`. Neither claims to prove semantic unambiguity — that rests on lexical closure and whole-word-first resolution, which are enforced in the parser. |
| **9. Real-Tokenizer Compression Study** | **Completed** | Measured with `tiktoken`/`cl100k_base`: **+61.6% vs terse English**, 1.98 tokens per lexeme. Result is negative for Kona and is reported as such. See §5.1. |
| **10. ASR Word-Error-Rate Validation** | ⚪ **Planned** | The acoustic invariant is proved combinatorially over the lexicon, not yet measured end-to-end against a recogniser on the `audio/` corpus. |
