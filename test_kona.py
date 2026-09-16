#!/usr/bin/env python3
import unittest
import json
from kona import parse_kona, PipelineNode, StageNode, ActionNode

class TestKonaParser(unittest.TestCase):
    def test_spoken_pipeline_parsing(self):
        code = 'dekwe poya "security" te, vetori kodo notori "migrations" te, fasa mesa'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)

        s1 = pipeline.stages[0]
        self.assertEqual(s1.body.action, "kwe")
        self.assertIn("deep/exhaustive", s1.body.modifiers)
        self.assertEqual(s1.body.targets[0]["type"], "poya")
        self.assertEqual(s1.body.targets[1]["args"], "security")

        s2 = pipeline.stages[1]
        self.assertEqual(s2.body.action, "tori")
        self.assertIn("dry_run/speculative", s2.body.modifiers)
        self.assertEqual(s2.body.targets[0]["type"], "kodo")
        self.assertEqual(len(s2.body.guards), 1)
        self.assertEqual(s2.body.guards[0], "migrations")

        s3 = pipeline.stages[2]
        self.assertEqual(s3.body.action, "fasa")
        self.assertEqual(s3.body.formats[0], "table")

    def test_shorthand_pipeline_parsing(self):
        code = 'kwe.de @poya:"security" |> tori.ve @kodo !migrations |> fasa #table'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)

        s1 = pipeline.stages[0]
        self.assertEqual(s1.body.action, "kwe")
        self.assertEqual(s1.body.targets[0]["type"], "poya")

    def test_nested_pipeline_parsing(self):
        code = 'si teli bono te, (kwe.de @poya:"sec" |> fasa mesa) ali yuki baki'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 1)
        
        s1 = pipeline.stages[0]
        self.assertEqual(" ".join(s1.condition), "teli bono")
        self.assertTrue(isinstance(s1.body, PipelineNode))
        self.assertEqual(len(s1.body.stages), 2)
        
        self.assertTrue(isinstance(s1.else_branch, StageNode))
        self.assertEqual(s1.else_branch.body.action, "yuki")
        self.assertEqual(s1.else_branch.body.targets[0]["type"], "baki")
        
    def test_spoken_literals(self):
        code = 'kwe nomi backend API fino te, fasa mesa'
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 2)
        self.assertEqual(pipeline.stages[0].body.targets[0]["args"], "backend API")
        
    def test_tool_call_compilation(self):
        code = 'kwe.de @poya:"backend" |> tori.ve @kodo !auth |> fasa #json'
        pipeline = parse_kona(code)
        calls = pipeline.to_tool_calls()
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]["tool"], "agent_search")
        self.assertEqual(calls[1]["tool"], "agent_transform")
        self.assertEqual(calls[2]["tool"], "agent_summarize")
        self.assertIn("json", calls[2]["parameters"]["format_requested"])


    def test_grammatical_aspect(self):
        code = "yukiba te, makita te, fasasa"
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 3)
        self.assertEqual(pipeline.stages[0].body.aspect, "progressive")
        self.assertEqual(pipeline.stages[1].body.aspect, "perfective")
        self.assertEqual(pipeline.stages[2].body.aspect, "habitual")

    def test_nominalization(self):
        code = "tori kwena"
        pipeline = parse_kona(code)
        self.assertEqual(len(pipeline.stages), 1)
        self.assertEqual(pipeline.stages[0].body.action, "tori")
        self.assertEqual(pipeline.stages[0].body.targets[0]["type"], "nominalization")
        self.assertEqual(pipeline.stages[0].body.targets[0]["args"], "kwe")

if __name__ == "__main__":
    unittest.main()
