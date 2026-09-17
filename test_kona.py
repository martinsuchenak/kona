#!/usr/bin/env python3
import json
import unittest

from kona import (
    parse_kona, validate_lexicon,
    PipelineNode, StageNode, ActionNode,
)


class TestKonaParser(unittest.TestCase):
    def test_spoken_pipeline_parsing(self):
        code = 'dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)

        s1 = pipeline.stages[0]
        self.assertEqual(s1.body.action, "kwe")
        self.assertIn("deep/exhaustive", s1.body.modifiers)
        self.assertEqual(s1.body.targets[0]["type"], "poya")
        self.assertEqual(s1.body.targets[0]["args"], "security")

        s2 = pipeline.stages[1]
        self.assertEqual(s2.body.action, "tori")
        self.assertIn("dry_run/speculative", s2.body.modifiers)
        self.assertEqual(s2.body.targets[0]["type"], "kodo")
        self.assertEqual(s2.body.guards, ["migrations"])

        s3 = pipeline.stages[2]
        self.assertEqual(s3.body.action, "fasa")
        self.assertEqual(s3.body.formats[0], "table")

    def test_shorthand_pipeline_parsing(self):
        code = 'kwe.de @poya:"security" |> tori.ve @kodo !migrations |> fasa #table'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)
        self.assertEqual(pipeline.stages[0].body.action, "kwe")
        self.assertEqual(pipeline.stages[0].body.targets[0]["type"], "poya")

    def test_nested_pipeline_parsing(self):
        code = 'si teli bono te, (kwe.de @poya:"sec" |> fasa mesa) ali yuki baki'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 1)

        s1 = pipeline.stages[0]
        self.assertEqual(" ".join(s1.condition), "teli bono")
        self.assertIsInstance(s1.body, PipelineNode)
        self.assertEqual(len(s1.body.stages), 2)

        self.assertIsInstance(s1.else_branch, StageNode)
        self.assertEqual(s1.else_branch.body.action, "yuki")
        self.assertEqual(s1.else_branch.body.targets[0]["type"], "baki")

    def test_spoken_literals(self):
        code = 'kwe nomi backend API fino te, fasa mesa'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 2)
        self.assertEqual(pipeline.stages[0].body.targets[0]["args"], "backend API")

    def test_tool_call_compilation(self):
        code = 'kwe.de @poya:"backend" |> tori.ve @kodo !auth |> fasa #json'
        calls = parse_kona(code).to_tool_calls()
        self.assertEqual([c["tool"] for c in calls],
                         ["agent_search", "agent_transform", "agent_summarize"])
        self.assertIn("json", calls[2]["parameters"]["format_requested"])

    def test_grammatical_aspect(self):
        pipeline = parse_kona("yukiba te, makita te, fasasa")
        self.assertEqual([s.body.aspect for s in pipeline.stages],
                         ["progressive", "perfective", "habitual"])

    def test_nominalization(self):
        pipeline = parse_kona("tori kwena")
        body = pipeline.stages[0].body
        self.assertEqual(body.action, "tori")
        self.assertEqual(body.targets[0]["type"], "nominalization")
        self.assertEqual(body.targets[0]["args"], "kwe")

    def test_turing_expansions(self):
        # Numerals (120), boolean OR (lo), scoping (ina). 'wo' is digit 0.
        code = "kwe nipaduwo lo rogi ina seli te, kada te, fasa mesa"
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)

        t = pipeline.stages[0].body.targets
        self.assertEqual(t[0]["type"], "integer")
        self.assertEqual(t[0]["args"], 120)
        self.assertEqual(t[1]["type"], "operator")
        self.assertEqual(t[1]["value"], "OR")
        self.assertEqual(t[2]["type"], "rogi")
        self.assertEqual(t[3]["type"], "scope")
        self.assertEqual(t[3]["relation"], "ina")
        self.assertEqual(t[3]["args"], "seli")

        self.assertEqual(pipeline.stages[1].body.action, "kada")


class TestDualModalityIsomorphism(unittest.TestCase):
    """The README claims spoken and shorthand compile to an identical AST.
    Previously they did not: SHORTHAND_TARGET_MAP was dead code, so `@repo`
    produced target type 'repo' while `poya` produced 'poya'."""

    PAIRS = [
        ('dekwe poya "security" te, fasa mesa',
         'kwe.de @repo:"security" |> fasa #table'),
        ('kwe veba "AWS Azure Q3 revenue" te, fasa jano',
         'kwe @web:"AWS Azure Q3 revenue" |> fasa #json'),
        ('vetori kodo notori "migrations" te, fasa difa',
         'tori.ve @code !"migrations" |> fasa #diff'),
        ('oki pakokaba te, yuki tesi ina pakokaba te, fasa poti',
         'oki @sandbox |> yuki @test ina pakokaba |> fasa #list'),
    ]

    def test_modalities_produce_identical_ast(self):
        for spoken, written in self.PAIRS:
            with self.subTest(spoken=spoken):
                self.assertEqual(
                    json.dumps(parse_kona(spoken).to_tool_calls()),
                    json.dumps(parse_kona(written).to_tool_calls()),
                )


class TestStrictParsing(unittest.TestCase):
    """Regressions for inputs the old parser accepted silently."""

    def test_garbage_is_rejected(self):
        for bad in ["$$$ %%% ^^^", "zzz qqq xxx", "kwe \x00"]:
            with self.subTest(bad=bad):
                with self.assertRaises(SyntaxError):
                    parse_kona(bad)

    def test_unknown_word_is_rejected(self):
        with self.assertRaises(SyntaxError):
            parse_kona("kwe blorp")

    def test_unterminated_string_is_rejected(self):
        with self.assertRaises(SyntaxError):
            parse_kona('kwe poya "unterminated')

    def test_stray_paren_does_not_truncate_pipeline(self):
        # Used to compile to a single agent_search, silently dropping the
        # delete and the summary.
        with self.assertRaises(SyntaxError):
            parse_kona("kwe kodo ) |> nuki poya |> fasa mesa")

    def test_no_implicit_execute_fallback(self):
        # An utterance with no action is a declarative and must emit no calls.
        # It used to default to 'yuki' (execute).
        pipeline = parse_kona("kodo poya")
        self.assertTrue(pipeline.stages[0].body.is_declarative)
        self.assertEqual(pipeline.to_tool_calls(), [])

    def test_empty_input_emits_nothing(self):
        self.assertEqual(parse_kona("").to_tool_calls(), [])

    def test_else_without_if_is_rejected(self):
        # 'ali ve' raised TypeError deep in to_tool_calls (1656/20000 fuzz cases).
        with self.assertRaises(SyntaxError):
            parse_kona("ali ve")

    def test_unterminated_condition_is_rejected(self):
        with self.assertRaises(SyntaxError):
            parse_kona("si teli bono yuki tafu")

    def test_two_actions_in_one_stage_rejected(self):
        with self.assertRaises(SyntaxError):
            parse_kona("kwe fasa kodo")

    def test_clause_particle_licenses_second_predicate(self):
        body = parse_kona("visi tokopasa ke tu do").stages[0].body
        self.assertEqual(body.action, "visi")
        self.assertIn("do", body.subclauses)

    def test_modal_takes_complement(self):
        body = parse_kona("tu posi teli neto").stages[0].body
        self.assertEqual(body.action, "teli")
        self.assertEqual(body.modality, "possibility")

    def test_modifier_scopes_a_target(self):
        body = parse_kona("teli sunodata neto").stages[0].body
        self.assertIn("zero/without_delay", body.modifiers)
        self.assertEqual([t["type"] for t in body.targets], ["data", "neto"])

    def test_whole_word_beats_decomposition(self):
        # Roots that merely start with a modifier prefix must not be
        # mis-segmented: veba != ve+ba, rego != re+go, nolo != no+lo.
        for word in ["veba", "rego"]:
            with self.subTest(word=word):
                body = parse_kona(f"visi {word}").stages[0].body
                self.assertEqual(body.targets[0]["type"], word)
                self.assertEqual(body.modifiers, [])

        # debi ('must') is a modal action, not de+bi ([deep] + digit 8).
        body = parse_kona("debi teli kodo").stages[0].body
        self.assertEqual(body.action, "teli")
        self.assertEqual(body.modality, "obligation")
        self.assertEqual(body.modifiers, [])


class TestCompilePathRobustness(unittest.TestCase):
    """The old fuzzer only called parse_kona(). These exercise the full path."""

    def test_every_benchmark_compiles_end_to_end(self):
        import re
        src = open(__file__.replace("test_kona.py", "kona.py")).read()
        body = src[src.index("def run_benchmarks"):]
        utterances = re.findall(r'\("(?:User|Agent|Spec|Story)",\s*\'([^\']+)\'\)', body)
        self.assertGreater(len(utterances), 0)
        for u in utterances:
            with self.subTest(utterance=u):
                ast = parse_kona(u)
                ast.to_tool_calls()
                ast.to_english()

    def test_fuzz_full_compile_path(self):
        import random
        import fuzz_kona
        random.seed(1234)
        crashes = []
        for _ in range(4000):
            n = random.randint(1, 15)
            text = " ".join(fuzz_kona.generate_random_token() for _ in range(n))
            try:
                ast = parse_kona(text)
                ast.to_tool_calls()
                ast.to_english()
            except SyntaxError:
                pass
            except Exception as e:
                crashes.append((text, type(e).__name__, str(e)))
        self.assertEqual(crashes[:3], [], f"{len(crashes)} non-SyntaxError crashes")


class TestLexicon(unittest.TestCase):
    def test_lexicon_matches_specification(self):
        problems = validate_lexicon()
        self.assertEqual(problems, [], "\n".join(problems))

    def test_documented_words_exist_in_the_compiler(self):
        """LEXICON.md must not document words the compiler cannot parse.

        It used to document ~90 such words, including `bono`, which only
        appeared to work because `si` conditions skipped lexical validation.
        """
        import re
        from pathlib import Path
        from kona import (ACTIONS, TARGETS, MODIFIERS, FORMATS, PARTICLES,
                          DIGITS, QUALITIES)

        lexicon = Path(__file__).with_name("LEXICON.md")
        if not lexicon.exists():
            self.skipTest("LEXICON.md not present")

        known = (set(ACTIONS) | set(TARGETS) | set(MODIFIERS) | set(FORMATS)
                 | set(PARTICLES) | set(DIGITS) | set(QUALITIES))
        shape = re.compile(r'^(?:[ptkbdgmnsfvlrwyj]?[wy]?[aeiou])+n?$')

        suffixes = ("na", "ba", "ta", "sa", "koso", "peji", "kaba", "yoti")

        def numeral(w):
            return (w.startswith("ni") and len(w) >= 4 and len(w) % 2 == 0
                    and all(w[i:i + 2] in DIGITS for i in range(2, len(w), 2)))

        def derivable(w):
            return (any(w.startswith(m) and w[len(m):] in known for m in MODIFIERS)
                    or any(w.endswith(s) and w[:-len(s)] in known for s in suffixes)
                    or numeral(w)
                    or (w.startswith("ro") and (w[2:] in known or numeral(w[2:])))
                    or w in suffixes)

        text = lexicon.read_text()

        # Appendix A explicitly records vocabulary that is documented but not
        # yet implemented. Those are exempt; anything else is drift.
        proposed = set()
        m = re.search(r"<!-- PROPOSED-BEGIN -->(.*?)<!-- PROPOSED-END -->",
                      text, re.S)
        if m:
            proposed = set(re.findall(r"`([a-z]+)`", m.group(1)))
            text = text[:m.start()] + text[m.end():]

        cited = {w for w in re.findall(r"`([a-z]{2,10})`", text)
                 if shape.match(w) and w not in proposed}
        # Compounds of two known roots are legal derivations too.
        def compound(w):
            return any(w[:i] in known and w[i:] in known for i in range(2, len(w) - 1))

        orphans = sorted(w for w in cited
                         if w not in known and not derivable(w) and not compound(w))
        self.assertEqual(
            orphans, [],
            f"{len(orphans)} words documented in LEXICON.md are unknown to the "
            f"compiler: {orphans}")


class TestArtifactsInSync(unittest.TestCase):
    def test_generated_artifacts_are_current(self):
        """kona.ebnf and playground.html are generated from kona.py."""
        import generate_artifacts
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = generate_artifacts.main(check=True)
        self.assertEqual(rc, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
