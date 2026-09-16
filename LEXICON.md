# Kona (コナビ) Lexicon & Dictionary
**Comprehensive Vocabulary for Universal Human Speech & AI Agent Workflows**

---

## 1. Grammatical Architecture

Kona is purely functional. Every root word belongs to one of five semantic categories:

| Category | Type Notation | Semantic Role | Example |
| :--- | :--- | :--- | :--- |
| **Prp (Pronoun / Person)** | $\mathbf{e}$ | Core entities, participants | `mi` (I), `tu` (agent) |
| **Act (Action / Verb)** | $\mathbf{e \to t}$ or $\mathbf{e \to e}$ | Functions that operate on entities | `kwe` (search), `tori` (edit) |
| **Tar (Target / Object)** | $\mathbf{e}$ | Scopes, files, data, system entities | `kodo` (code), `veba` (web) |
| **Mod (Modifier / Adverb)** | $\mathbf{(e \to t) \to (e \to t)}$ | Bound prefixes transforming actions | `de-` (deep), `ve-` (dry-run) |
| **Fmt (Format / Mode)** | $\mathbf{Type}$ | Output representations | `mesa` (table), `jano` (json) |
| **Rel (Relational / Logical)**| $\mathbf{Bool / Logic}$ | Operators, relations, guards | `sama` (equal), `no-` (guard) |

---

## 2. Word Formation Engine (The 5 Universal Derivational Affixes)

Kona achieves maximum vocabulary efficiency by using **5 systematic derivational affixes**. You learn a small set of primitive base words, and these 5 affixes automatically generate thousands of precise concepts with zero guesswork.

```
┌─────────────────────────────────────────────────────────────┐
│                 The 5 Universal Affixes                     │
├───────────┬───────────────────┬─────────────────────────────┤
│ 1. no-    │ Polar Opposite    │ bono (good)  → nobono (bad) │
│ 2. -koso  │ Hardware / Device │ kisi (hear)  → kisikoso(mic)│
│ 3. -peji  │ Screen / Surface  │ visi (see)   → visipeji(mon)│
│ 4. -kaba  │ Space / Enclosure │ kodo (code)  → kodokaba(IDE)│
│ 5. -yoti  │ Actor / Specialist│ kodo (code)  → kodoyoti(dev)│
└───────────┴───────────────────┴─────────────────────────────┘
```

### 2.1. Affix 1: `no-` (Polar Opposites / Antonyms)
Instead of memorizing arbitrary opposite words (like *good* vs *bad*, *easy* vs *hard*), attach `no-` directly to the base root. This cuts vocabulary memorization in half:

| Base Concept | Opposite (`no-`) | English Meaning |
| :--- | :--- | :--- |
| `bono` (good) | **`nobono`** | Bad, poor, flawed |
| `fasi` (easy / simple) | **`nofasi`** | Hard, difficult, complex |
| `pura` (safe / secure) | **`nopura`** | Risky, dangerous, vulnerable |
| `kore` (correct / right) | **`nokore`** | Wrong, incorrect, error |
| `doko` (agree / align) | **`nodoko`** | Disagree, dispute, object |
| `sapi` (understand) | **`nosapi`** | Misunderstand, confuse |
| `fide` (trust / confident)| **`nofide`** | Distrust, doubt, skeptical |
| `gala` (satisfied / happy)| **`nogala`** | Frustrated, dissatisfied, unhappy |
| `tranki` (calm / steady) | **`notranki`** | Urgent, stressed, chaotic |
| `puro` (clean / pure) | **`nopuro`** | Impure, noisy, corrupted |

### 2.2. Affix 2: `-koso` (Physical Hardware / Devices / Tools)
$$\mathbf{Sense / Action} + \mathbf{koso} \ (\text{tool}) \implies \mathbf{Physical Hardware Device}$$

* `kisi` (hear) + `koso` = **`kisikoso`** $\to$ Microphone / Audio input
* `sono` (sound) + `koso` = **`sonokoso`** $\to$ Speaker / Audio output
* `visi` (see) + `koso` = **`visikoso`** $\to$ Camera / Webcam / Optical sensor
* `tapi` (type/keystroke) + `koso` = **`tapikoso`** $\to$ Keyboard / Keypad
* `powa` (power/energy) + `koso` = **`powakoso`** $\to$ Battery / Power supply
* `toko` (time) + `koso` = **`tokokoso`** $\to$ Clock / Timer / Chronometer
* `para` (stop/halt) + `koso` = **`parakoso`** $\to$ Brake / Interrupt trigger

### 2.3. Affix 3: `-peji` (Screens / Canvases / Sheets)
$$\mathbf{Domain / Mode} + \mathbf{peji} \ (\text{surface}) \implies \mathbf{Visual Interface Display}$$

* `visi` (see) + `peji` = **`visipeji`** $\to$ Screen / Monitor / Display
* `kiri` (write/script) + `peji` = **`kiripeji`** $\to$ Document editor / Notepad canvas
* `mesa` (table) + `peji` = **`mesapeji`** $\to$ Spreadsheet / Table view
* `peji` standalone = Webpage / Page

### 2.4. Affix 4: `-kaba` (Scopes / Environments / Workspaces)
$$\mathbf{Object / Entity} + \mathbf{kaba} \ (\text{room/space}) \implies \mathbf{Execution Environment}$$

* `kodo` (code) + `kaba` = **`kodokaba`** $\to$ IDE / Workspace directory
* `deli` (container) + `kaba` = **`delikaba`** $\to$ Sandbox / Containerized runtime
* `data` (database) + `kaba` = **`datakaba`** $\to$ Database warehouse / Cluster
* `kaba` standalone = Physical room / Office

### 2.5. Affix 5: `-yoti` (Roles / Actors / Specialists)
$$\mathbf{Domain / Skill} + \mathbf{yoti} \ (\text{person}) \implies \mathbf{Role / Specialist}$$

* `kodo` (code) + `yoti` = **`kodoyoti`** $\to$ Programmer / Software Engineer
* `maki` (create) + `yoti` = **`makiyoti`** $\to$ Designer / Author / Creator
* `teli` (test) + `yoti` = **`teliyoti`** $\to$ QA Tester / Verifier
* `yoti` standalone = User / Human operator / Account


---

## 3. Agreement, Disagreement & Negotiation

Essential for discussing plans, trade-offs, and alignment with humans and AI agents.

| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`doko`** | /'do.ko/ | Agree, consensus, align, consent | Agree, align |
| **`nodoko`** | /'no.do.ko/ | Disagree, objection, dispute | Disagree, differ |
| **`poki`** | /'po.ki/ | Propose, suggest, offer | Suggest, offer |
| **`keti`** | /'ke.ti/ | Decide, resolve, determine, settle | Decide, settle |
| **`kambi`** | /'kam.bi/ | Compromise, trade-off, exchange | Compromise, trade |
| **`akwe`** | /'a.kwe/ | Accept, approve, confirm | Accept, approve |
| **`noakwe`** | /'no.a.kwe/ | Reject, decline, veto | Reject, decline |
| **`si`** | /si/ | If, on condition that, provided | If, condition |
| **`nosi`** | /'no.si/ | Unless, except if | Unless, except |

## 4. Thought, Cognition & Perception

### 4.1. Mind & Belief
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`pensa`** | /'pen.sa/ | Think, believe, consider | Think, reckon |
| **`sapi`** | /'sa.pi/ | Know, understand, make sense | Understand, know |
| **`luma`** | /'lu.ma/ | Idea, concept, thought, view | Idea, concept |
| **`nido`** | /'ni.do/ | Need, require, lack | Need, want |
| **`suki`** | /'su.ki/ | Like, enjoy, appreciate | Like, love |
| **`peli`** | /'pe.li/ | Prefer, choose, favor | Prefer, rather |
| **`senso`** | /'sen.so/ | Feel, sense, impression, vibe | Feeling, impression |

### 4.2. Sensory Perception & Speech
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`sono`** | /'so.no/ | Sound, audio, voice, tone | Sound, noise, voice |
| **`wada`** | /'wa.da/ | Word, term, vocabulary | Word, name |
| **`linga`** | /'lin.ga/ | Language, speech system | Language, tongue |
| **`kisi`** | /'ki.si/ | Hear, listen, perceive audio | Hear, listen |
| **`visi`** | /'vi.si/ | See, look, watch, inspect | See, look, read |
| **`kalo`** | /'ka.lo/ | Speak, talk, pronounce, vocalize | Speak, talk |

## 5. Physical World & Devices (AI-Human Interaction)

Hardware, sensors, compute environments, and physical surroundings commonly discussed when working with agents.

### 5.1. Hardware & Sensors
| Kona Root | IPA | Functional Origin | Physical Device Meaning |
| :--- | :--- | :--- | :--- |
| **`kisikoso`** | /'ki.si.ko.so/ | `kisi` (hear) + `koso` (tool) | Microphone, audio input |
| **`sonokoso`** | /'so.no.ko.so/ | `sono` (sound) + `koso` (tool) | Speaker, audio output |
| **`visikoso`** | /'vi.si.ko.so/ | `visi` (see) + `koso` (tool) | Camera, webcam, optical sensor |
| **`visipeji`** | /'vi.si.pe.ji/ | `visi` (see) + `peji` (page/surface) | Screen, monitor, display |
| **`tapikoso`** | /'ta.pi.ko.so/ | `tapi` (type) + `koso` (tool) | Keyboard, keypad |
| **`powakoso`** | /'po.wa.ko.so/ | `powa` (power) + `koso` (tool) | Battery, power supply |
| **`kompu`** | /'kom.pu/ | International base | Computer, PC, laptop, host |
| **`fono`** | /'fo.no/ | International base | Phone, mobile device |

### 5.2. Physical Environment & Spaces
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`kaba`** | /'ka.ba/ | Room, chamber, enclosure, office | Room, office |
| **`mesa`** | /'me.sa/ | Desk, table, flat work surface | Desk, table |
| **`luce`** | /'lu.ce/ | Light, lamp, illumination | Light, lamp |
| **`deli`** | /'de.li/ | Box, container, enclosure | Box, container |

## 6. Spatial Navigation & Movement Compounding

Useful for interface navigation, scrolling, data movement, and spatial commands:

### 6.1. Spatial Primitives
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`supra`** | /'su.pra/ | Up, above, top, high | Up, top |
| **`suba`** | /'su.ba/ | Down, below, bottom, low | Down, bottom |
| **`ante`** | /'an.te/ | Front, forward, ahead | Forward, front |
| **`posa`** | /'po.sa/ | Back, backward, behind | Back, rear |
| **`dira`** | /'di.ra/ | Right (direction) | Right |
| **`leva`** | /'le.va/ | Left (direction) | Left |
| **`medo`** | /'me.do/ | Middle, center, halfway | Middle, center |

### 6.2. Movement Actions & Directional Compounds
* `mova` (move/shift) $\to$ **`movasupra`** (scroll up / upload), **`movasuba`** (scroll down / download)
* `ira` (go/navigate) $\to$ **`iraina`** (log in / enter), **`irauta`** (log out / exit)
* `porta` (carry/transfer) $\to$ **`portakoso`** (USB / drive / data carrier)
* `para` (stop/halt/pause) $\to$ **`parakoso`** (brake / pause button / interrupt)

---

## 7. Time, Scheduling & Deadlines

Compounding with **`toko`** (time/duration):

| Kona Word | Components | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`tokofini`** | `toko` + `fini` (end) | Deadline, timeout, expiration | Deadline, timeout |
| **`tokooki`** | `toko` + `oki` (start) | Scheduled start time, launch | Start time |
| **`tokopasa`** | `toko` + `pasa` (past) | Audit log, history, past records | History, log |
| **`tokofutu`** | `toko` + `futu` (future) | Roadmap, forecast, queue | Roadmap, future |
| **`dya`** | International base | Day (24 hours) | Day |
| **`wiki`** | International base | Week (7 days) | Week |
| **`musa`** | International base | Month | Month |
| **`yara`** | International base | Year | Year |

---

## 8. Sensory Levels (Audio & Brightness Compounding)

Using **`sono`** (sound/volume) and **`luce`** (light):

* `nosono` (`no-` + `sono`) $\to$ Mute / Silent / No audio
* `subasono` (`suba` + `sono`) $\to$ Quiet / Low volume
* `suprasono` (`supra` + `sono`) $\to$ Loud / High volume
* `subaluce` (`suba` + `luce`) $\to$ Dim light / Dark mode
* `supraluce` (`supra` + `luce`) $\to$ Bright light / High contrast

---

## 9. Texture, Manner & Speed
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`kura`** | /'ku.ra/ | Crisp, sharp, clear, distinct | Crisp, clear |
| **`rima`** | /'ri.ma/ | Rhythm, tempo, beat, cadence | Rhythm, beat |
| **`poko`** | /'po.ko/ | A bit, a little, slightly | A little, slightly |
| **`muto`** | /'mu.to/ | Much, very, many, a lot | Very, much, many |
| **`masi`** | /'ma.si/ | More (comparative) | More |
| **`puro`** | /'pu.ro/ | Pure, clean, authentic | Pure, natural |
| **`meka`** | /'me.ka/ | Mechanical, robotic, artificial | Robotic, machine |

---

## 10. Questions & Connectors
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`ke`** | /ke/ | What? Which? | What? |
| **`kwa`** | /kwa/ | Why? For what reason? | Why? |
| **`ko`** | /ko/ | How? In what manner? | How? |
| **`kwi`** | /kwi/ | Who? Whom? | Who? |
| **`ti`** | /ti/ | When? At what time? | When? |
| **`pero`** | /'pe.ro/ | But, however, yet | But, however |
| **`kasi`** | /'ka.si/ | Because, since, as | Because, since |
| **`to`** | /to/ | And, with, together with | And, with |
| **`o`** | /o/ | Or, either | Or |
| **`sama`** | /'sa.ma/ | Like, similar to, as, equal | Like, same as |
| **`ali`** | /'a.li/ | Other, different, else | Other, else |
| **`kono`** | /'ko.no/ | Therefore, so, consequently | So, therefore |

---

## 11. Quantifiers & Data Pointers

High-stakes commands (like deletions or refactors) require exact blast-radius constraints.

| Kona Root | IPA | Meaning | Written Shorthand |
| :--- | :--- | :--- | :--- |
| **`oli`** | /'o.li/ | All, every, universal | `@all` |
| **`uni`** | /'u.ni/ | Some, one, a specific instance | `@some` |
| **`pato`** | /'pa.to/ | The previous output / piped data | `@prev` |
| **`kito`** | /'ki.to/ | This, the current context | `@this` |

---

## 12. Spoken Literals (Code-Switching)

When speaking Kona, you often need to pass arbitrary English strings, git hashes, or passwords that do not follow Kona phonotactics. Use these boundary particles to tell the ASR and parser to treat the enclosed audio as a raw string literal.

| Kona Root | IPA | Meaning | Written Equivalent |
| :--- | :--- | :--- | :--- |
| **`nomi`** | /'no.mi/ | Start of raw literal / Name | `"` (Opening quote) |
| **`fino`** | /'fi.no/ | End of raw literal | `"` (Closing quote) |

*Example:* `kwe poya nomi backend API fino te, fasa mesa` (Search repo "backend API", format as table).

---

## 13. General Action Primitives (Verbs & Modals)

| Kona Root | IPA | Meaning | Written Shorthand |
| :--- | :--- | :--- | :--- |
| **`kwe`** | /kwe/ | Search, find, query, grep | `kwe` / `find` |
| **`maki`** | /'ma.ki/ | Make, create, scaffold, write | `maki` / `new` |
| **`tori`** | /'to.ri/ | Transform, edit, refactor, modify | `tori` / `edit` |
| **`teli`** | /'te.li/ | Test, verify, benchmark, check | `teli` / `test` |
| **`nuki`** | /'nu.ki/ | Delete, remove, purge, prune | `nuki` / `rm` |
| **`fasa`** | /'fa.sa/ | Summarize, explain, speak, render | `fasa` / `sum` |
| **`yuki`** | /'ju.ki/ | Execute, run, trigger, deploy | `yuki` / `run` |
| **`plani`** | /'pla.ni/ | Plan, schedule, organize | `plani` / `plan` |
| **`visi`** | /'vi.si/ | View, read, inspect, display | `visi` / `cat` |
| **`leke`** | /'le.ke/ | Fetch, pull, download, receive | `leke` / `get` |
| **`do`** | /do/ | Give, send, emit, push, notify | `do` / `send` |
| **`posi`** | /'po.si/ | Can, could, able, capacity | `can` |
| **`debi`** | /'de.bi/ | Should, must, ought, obligation | `must` |

---

## 12. Agent Domain Targets & Entities

### 12.1. Coding & Version Control (DevOps)
| Kona Root | IPA | Domain Meaning | Shorthand |
| :--- | :--- | :--- | :--- |
| **`kodo`** | /'ko.do/ | Code, implementation, script | `@code` |
| **`fili`** | /'fi.li/ | File, document, asset | `@file` |
| **`poya`** | /'po.ja/ | Project, repository, directory | `@repo` |
| **`vasi`** | /'va.si/ | Version, Git commit, branch, diff | `@git` / `@vcs` |
| **`baki`** | /'ba.ki/ | Bug, defect, issue, error | `@bug` / `@issue` |
| **`tesi`** | /'te.si/ | Test suite, unit test, spec | `@test` |
| **`deli`** | /'de.li/ | Container, Docker, sandbox | `@docker` / `@sandbox` |
| **`seli`** | /'se.li/ | Mutex, resource lock, latch | `@lock` |

### 12.2. Natural Elements & Physical World
| Kona Root | IPA | Meaning | English Analog |
| :--- | :--- | :--- | :--- |
| **`vento`** | /'ven.to/ | Wind, airflow, breeze | Wind |
| **`soli`** | /'so.li/ | Sun, sunlight, solar | Sun |
| **`norte`** | /'nor.te/ | North (cardinal direction) | North |
| **`tela`** | /'te.la/ | Fabric, cloth, garment, cloak | Cloth, cloak |
| **`kalu`** | /'ka.lu/ | Heat, thermal warmth (`nokalu` = cold) | Warmth, cold |
| **`irayoti`** | /'i.ra.jo.ti/ | Traveler, passerby (`ira` + `yoti`) | Traveler |


### 12.3. Web & Browsing
| Kona Root | IPA | Domain Meaning | Shorthand |
| :--- | :--- | :--- | :--- |
| **`veba`** | /'ve.ba/ | Web, internet search, Google | `@web` |
| **`peji`** | /'pe.ji/ | Web page, URL, document view | `@url` / `@page` |
| **`liki`** | /'li.ki/ | Link, hyperlink, navigation click | `@link` |
| **`neto`** | /'ne.to/ | Network, HTTP API, endpoint | `@api` |

### 12.4. Data & Storage
| Kona Root | IPA | Domain Meaning | Shorthand |
| :--- | :--- | :--- | :--- |
| **`data`** | /'da.ta/ | Dataset, database, records | `@data` / `@db` |
| **`memo`** | /'me.mo/ | Memory, context window, state | `@memory` |
| **`seku`** | /'se.ku/ | Security, secret, token, auth | `@auth` / `@secret` |

### 12.5. Communication & Tasks
| Kona Root | IPA | Domain Meaning | Shorthand |
| :--- | :--- | :--- | :--- |
| **`tafu`** | /'ta.fu/ | Task, job, workflow, pipeline | `@task` |
| **`meso`** | /'me.so/ | Message, email, notification | `@msg` / `@mail` |
| **`yoti`** | /'jo.ti/ | User, client, account | `@user` |

---

## 13. Higher-Order Modifiers (Bound Prefixes)

Modifiers bind directly to actions to create compound functions:

| Prefix | IPA | Semantic Effect | Example | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **`de-`** | /de/ | Deep, recursive, exhaustive | `dekwe` | Deep search |
| **`su-`** | /su/ | Fast, brief, concise, shallow | `sufasa` | Summarize briefly |
| **`ve-`** | /ve/ | Speculative, dry-run, simulation | `vetori` | Propose diff without saving |
| **`no-`** | /no/ | Strict prohibition, invariant guard | `notori` | DO NOT modify |
| **`oto-`** | /'o.to/ | Automatic, autonomous, loop | `otoyuki`| Run autonomously |
| **`re-`** | /re/ | Repeat, retry, loop, update | `reteli` | Re-test / retry test |

---

## 14. Output Formats

| Kona Root | IPA | Format Meaning | Shorthand |
| :--- | :--- | :--- | :--- |
| **`mesa`** | /'me.sa/ | Table, matrix, grid | `#table` |
| **`jano`** | /'ja.no/ | JSON, structured key-value | `#json` |
| **`poti`** | /'po.ti/ | Bullet list, numbered list | `#list` |
| **`puro`** | /'pu.ro/ | Raw text, unformatted code | `#raw` |
| **`difa`** | /'di.fa/ | Unified diff, patch, git diff | `#diff` |

---

## 15. Numbers, Quantities & Mathematics

Kona uses a strict decimal $(C)V$ base-10 counting system engineered for rapid pronunciation and unambiguous speech recognition.

### 15.1. Digits (0–9) and Powers of Ten
| Digit | Kona Word | IPA | Etymological Origin |
| :--- | :--- | :--- | :--- |
| **0** | **`nono`** | /'no.no/ | `no` (none/null) |
| **1** | **`suno`** | /'su.no/ | Single / unique / one |
| **2** | **`duo`** | /'du.o/ | Universal dual |
| **3** | **`trio`** | /'tri.o/ | Universal tri |
| **4** | **`kato`** | /'ka.to/ | Greek *tetra* / Latin *quattuor* |
| **5** | **`pento`** | /'pen.to/ | Greek *penta* |
| **6** | **`sekso`** | /'sek.so/ | Latin *sex* |
| **7** | **`seto`** | /'se.to/ | Italian *sette* |
| **8** | **`okto`** | /'ok.to/ | Greek *okto* |
| **9** | **`novo`** | /'no.vo/ | Latin *novem* |
| **10** | **`deko`** | /'de.ko/ | Greek *deka* |
| **100** | **`sento`** | /'sen.to/ | Latin *centum* |
| **1,000** | **`kilo`** | /'ki.lo/ | Metric *kilo* |
| **1,000,000** | **`mega`** | /'me.ga/ | Metric *mega* |

### 15.2. Compounding Numbers
Numbers compound naturally in standard place value:
* **12** = `deko duo` *(ten two)*
* **35** = `trio deko pento` *(three tens five)*
* **250** = `duo sento pento deko` *(two hundreds five tens)*
* **Ordinals (1st, 2nd, 3rd)**: Add `ro-` $\to$ `rosuno` (1st), `roduo` (2nd), `rotrio` (3rd).
* **Percentage**: `sentopa` $\to$ `deko sentopa` = 10%.

### 15.3. Mathematical Operations
| Operation | Kona Operator | Spoken | Shorthand | Example |
| :--- | :--- | :--- | :--- | :--- |
| **Add (+)** | `masi` | *masi* | `+` | `duo masi trio sama pento` (2 + 3 = 5) |
| **Subtract (-)** | `meni` | *meni* | `-` | `pento meni duo sama trio` (5 - 2 = 3) |
| **Multiply (×)** | `muto` | *muto* | `*` | `trio muto kato sama deko duo` (3 × 4 = 12) |
| **Divide (÷)** | `parti` | *parti* | `/` | `deko parti duo sama pento` (10 ÷ 2 = 5) |
| **Equal (=)** | `sama` | *sama* | `==` | |

---

## 16. Functional Flow Control (Conditionals & Pattern Matching)

In Kona, all flow control is modeled as **pure algebraic expressions**:

### 16.1. Ternary Conditional (`si ... te, ... ali ...`)
$$\mathbf{si} \ \text{[Predicate]} \ \mathbf{te,} \ \text{[True-branch]} \ \mathbf{ali} \ \text{[False-branch]}$$

* **Kona Spoken**:
  > `si teli bono te, yuki tafu ali fasa baki.`
* **Kona Shorthand**:
  > `si teli.bono |> yuki @task :else: fasa @bug`
* **English**: *"If the test passes, execute the task; otherwise, report the bug."*

### 16.2. Pattern Matching (`sama ... te`)
$$\mathbf{sama} \ \text{[Pattern]} \ \mathbf{te,} \ \text{[Action]}$$

* `sama nono te, fasa "empty"` *(When 0, return "empty")*
* `sama suno te, fasa "single"` *(When 1, return "single")*
* `sama muto te, fasa "many"` *(When many, return "many")*

---

## 17. Data Types & Functional Operations (Map, Filter, Reduce)

### 17.1. Data Primitives
| Data Type | Kona Name | Components | Meaning |
| :--- | :--- | :--- | :--- |
| **Integer / Float** | `sunodata` | `suno` (number) + `data` | Numeric scalar |
| **String / Text** | `wadadata` | `wada` (word) + `data` | Text / String |
| **Boolean** | `binadata` | `bina` (binary) + `data` | True / False |
| **List / Array** | `potidata` | `poti` (list) + `data` | Ordered sequence |
| **Map / Dict** | `janodata` | `jano` (json) + `data` | Key-value store |

### 17.2. Higher-Order Collection Operations
* **Map (Transform Each)**: `torimuto` (transform-all)
  - `potidata te, torimuto fasa` $\to$ Map each element to its string summary.
* **Filter (Keep Matching)**: `kwemuto` (search-all / filter)
  - `potidata te, kwemuto kore` $\to$ Filter list to keep only correct elements.
* **Reduce / Fold (Accumulate All)**: `kolido` (all-into-one)
  - `potidata te, kolido masi` $\to$ Fold with addition (sum the entire list).
* **Length / Count**: `numa` $\to$ `numa potidata` (count items in list).

---

## 18. Social Discourse & Conversational Polite Markers

Natural interaction between human operators and agents:

| Kona Phrase | Meaning | Tone / Usage |
| :--- | :--- | :--- |
| **`salu`** | Hello / Hi / Greetings | General friendly opening |
| **`danki`** | Thank you / Thanks | Gratitude |
| **`plasi`** | Please (if you will) | Courteous request |
| **`vale`** | Goodbye / Farewell | Session closing |
| **`ye kore`** | Exactly / That's right | Strong agreement |
| **`nokore`** | Incorrect / That's a mistake | Clear error correction |
| **`refasa plasi`** | Please say that again / Repeat | Request clarification |
| **`kwa luma?`** | What do you mean? | Asking for intent/concept |
| **`tranki`** | No rush / Take your time | Relieving urgency |

---

## 19. Real Workflow Demonstrations


### Workflow 1: Git Feature Branch & Pull Request
* **English**: *"Create a new branch 'feature-auth', refactor the code without modifying test files, run tests, and propose a commit message."*
* **Kona Spoken**:
  > `maki vasi "feature-auth" te, vetori kodo notori tesi te, teli poya te, fasa meso.`
* **Kona Shorthand**:
  > `maki @git:"feature-auth" |> tori.ve @code !tori @test |> teli @repo |> fasa @msg`

### Workflow 2: Web Scraping & Database Ingestion
* **English**: *"Fetch the web page, extract the pricing table into JSON, and insert it into the database."*
* **Kona Spoken**:
  > `leke peji "https://example.com" te, fasa jano mesa te, do data.`
* **Kona Shorthand**:
  > `leke @page:"https://example.com" |> fasa #json #table |> do @data`

### Workflow 3: Bug Hunt & Root Cause Analysis
* **English**: *"Deeply inspect the repo for memory leaks, display the diff, and explain the cause concisely."*
* **Kona Spoken**:
  > `dekwe poya "leak" te, visi difa te, sufasa.`
* **Kona Shorthand**:
  > `kwe.de @repo:"leak" |> visi #diff |> fasa.su`

### Workflow 4: Autonomous Task Execution
* **English**: *"Start the task in Docker, test it until complete, and notify me with an email message."*
* **Kona Spoken**:
  > `oki tafu ina deli te, ototeli poya te, do meso mi.`
* **Kona Shorthand**:
  > `oki @task @docker |> teli.oto @repo |> do @msg @user`

---

### Benchmark 1: Collaborative Problem-Solving & Debugging Dialogue
```
User:  mi visi tokopasa ke tu do, pero baki nosapi kasi data yuki dura.
User:  tu posi teli si neto nuki pasa reoki?
User:  si ye, koli debi peli masi tokofini, no retori kwe.

Agent: mi teli sunodata neto. neto no nuki, pero data yuki masi deko sekunda kasi seli.
Agent: mi poki ke koli nuki seli pasa te, reteli toko kwe.
```

---

### Benchmark 2: Technical System Specification
```
ti yoti kwe seku te, teli seku ina memo.
si seku fini te, leke suno futu uta neto seku.
tori seku te, do memo pasa duo toko.
```

---

### Benchmark 3: Universal Narrative Benchmark (The North Wind and the Sun)
```
vento norte to soli nodoko dura ke masi powa, ti irayoti veni ina tela kalu.
ona doko ke: yoti ke pasa maki irayoti nuki tela, debi sapi masi powa supra ali.
futu vento norte do powa sama muto posi, pero masi vento yuki te, masi irayoti koli tela; fini te, vento norte para tafu.
futu soli do luce to kalu, te ina suno toko irayoti nuki tela.
kono vento norte debi fasa ye ke soli masi powa supra duo.
```

