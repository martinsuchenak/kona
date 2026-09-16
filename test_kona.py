#!/usr/bin/env python3
"""
Unit and Regression Test Suite for the Kona Language Engine.
Tests AST parsing, dual-modality isomorphism, guard constraints, conditionals,
and tool call compilation.
"""

import unittest
from kona import parse_kona, KonaPipeline


class TestKonaParser(unittest.TestCase):

    def test_spoken_pipeline_parsing(self):
        code = 'dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.steps), 3)

        s1 = pipeline.steps[0]
        self.assertEqual(s1["action"], "search")
        self.assertIn("deep/exhaustive", s1["modifiers"])
        self.assertEqual(s1["targets"][0]["type"], "repo")
        self.assertEqual(s1["targets"][0]["value"], "security")

        s2 = pipeline.steps[1]
        self.assertEqual(s2["action"], "transform")
        self.assertIn("dry_run/speculative", s2["modifiers"])
        self.assertEqual(s2["targets"][0]["type"], "code")
        self.assertEqual(len(s2["guards_prohibited"]), 1)
        self.assertEqual(s2["guards_prohibited"][0]["action"], "tori")
        self.assertEqual(s2["guards_prohibited"][0]["target"], "migrations")

        s3 = pipeline.steps[2]
        self.assertEqual(s3["action"], "summarize")
        self.assertEqual(s3["output_format"], "table")

    def test_shorthand_pipeline_parsing(self):
        code = 'kwe.de @repo:"security" |> tori.ve @code !tori @"migrations" |> fasa #table'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.steps), 3)

        s1 = pipeline.steps[0]
        self.assertEqual(s1["action"], "search")
        self.assertIn("deep/exhaustive", s1["modifiers"])
        self.assertEqual(s1["targets"][0]["type"], "repo")
        self.assertEqual(s1["targets"][0]["value"], "security")

        s2 = pipeline.steps[1]
        self.assertEqual(s2["action"], "transform")
        self.assertIn("dry_run/speculative", s2["modifiers"])
        self.assertEqual(s2["targets"][0]["type"], "code")
        self.assertEqual(len(s2["guards_prohibited"]), 1)
        self.assertEqual(s2["guards_prohibited"][0]["action"], "tori")
        self.assertEqual(s2["guards_prohibited"][0]["target"], "migrations")

        s3 = pipeline.steps[2]
        self.assertEqual(s3["action"], "summarize")
        self.assertEqual(s3["output_format"], "table")

    def test_dual_modality_isomorphism(self):
        spoken = 'dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa'
        shorthand = 'kwe.de @repo:"security" |> tori.ve @code !tori @"migrations" |> fasa #table'

        p_spoken = parse_kona(spoken)
        p_short = parse_kona(shorthand)

        self.assertEqual(len(p_spoken.steps), len(p_short.steps))
        for i in range(len(p_spoken.steps)):
            s_sp = p_spoken.steps[i]
            s_sh = p_short.steps[i]
            self.assertEqual(s_sp["action"], s_sh["action"], f"Action mismatch at step {i+1}")
            self.assertEqual(s_sp["modifiers"], s_sh["modifiers"], f"Modifier mismatch at step {i+1}")
            self.assertEqual(s_sp["output_format"], s_sh["output_format"], f"Format mismatch at step {i+1}")
            self.assertEqual(
                len(s_sp["guards_prohibited"]),
                len(s_sh["guards_prohibited"]),
                f"Guards mismatch at step {i+1}"
            )

    def test_negative_guards(self):
        cases = [
            ('tori kodo !tori @"auth"', "tori", "auth"),
            ('tori kodo notori "auth"', "tori", "auth"),
            ('tori kodo no-tori "auth"', "tori", "auth"),
        ]
        for expr, expected_act, expected_target in cases:
            p = parse_kona(expr)
            self.assertEqual(len(p.steps), 1)
            guards = p.steps[0]["guards_prohibited"]
            self.assertEqual(len(guards), 1, f"Failed on expression: {expr}")
            self.assertEqual(guards[0]["action"], expected_act)
            self.assertEqual(guards[0]["target"], expected_target)

    def test_conditional_branching(self):
        expr = 'si teli bono te, yuki tafu ali fasa baki'
        p = parse_kona(expr)
        self.assertEqual(len(p.steps), 1)
        step = p.steps[0]
        self.assertEqual(step["condition"], "teli bono")
        self.assertEqual(step["action"], "execute")
        self.assertEqual(step["targets"][0]["type"], "task")
        self.assertEqual(step["alternative"], "fasa baki")

    def test_bound_modifier_ordering(self):
        # 'suno' must not be prematurely matched as 'su'
        expr_su = 'sufasa kodo'
        p_su = parse_kona(expr_su)
        self.assertEqual(p_su.steps[0]["action"], "summarize")
        self.assertIn("fast/brief", p_su.steps[0]["modifiers"])

        expr_de = 'dekwe poya'
        p_de = parse_kona(expr_de)
        self.assertEqual(p_de.steps[0]["action"], "search")
        self.assertIn("deep/exhaustive", p_de.steps[0]["modifiers"])

    def test_output_formats(self):
        formats = [
            ('#table', 'table'),
            ('mesa', 'table'),
            ('#json', 'json'),
            ('jano', 'json'),
            ('#list', 'bullet_list'),
            ('poti', 'bullet_list'),
            ('#diff', 'diff'),
            ('difa', 'diff'),
            ('#raw', 'plain_text'),
            ('puro', 'plain_text'),
        ]
        for tok, expected_fmt in formats:
            expr = f'fasa {tok}'
            p = parse_kona(expr)
            self.assertEqual(p.steps[0]["output_format"], expected_fmt, f"Failed for token {tok}")

    def test_tool_call_compilation(self):
        expr = 'kwe.de @repo:"backend" |> tori.ve @code !tori @"auth" |> fasa #json'
        p = parse_kona(expr)
        calls = p.to_tool_calls()
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]["tool"], "agent_search")
        self.assertEqual(calls[1]["tool"], "agent_transform")
        self.assertEqual(calls[2]["tool"], "agent_summarize")
        self.assertEqual(calls[2]["parameters"]["format"], "json")

    def test_english_translation(self):
        expr = 'kwe.de @repo:"backend" |> fasa #table'
        p = parse_kona(expr)
        lines = p.to_english()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("Step 1: Search [deep/exhaustive]"))
        self.assertTrue(lines[1].endswith("Format output as table"))

    def test_benchmark_utterances(self):
        utterances = [
            'mi visi tokopasa ke tu do, pero baki nosapi kasi data yuki dura',
            'tu posi teli si neto nuki pasa reoki',
            'si ye, koli debi peli masi tokofini, no retori kwe',
            'ti yoti kwe seku te, teli seku ina memo',
            'si seku fini te, leke suno futu uta neto seku',
            'tori seku te, do memo pasa duo toko',
            'vento norte to soli nodoko dura ke masi powa, ti irayoti veni ina tela kalu',
        ]
        for u in utterances:
            p = parse_kona(u)
            self.assertGreater(len(p.steps), 0, f"Pipeline was empty for benchmark utterance: {u}")


if __name__ == "__main__":
    unittest.main()
