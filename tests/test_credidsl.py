import io
import unittest
from decimal import Decimal

from app import app
from credidsl import DEFAULT_POLICY, DEMO_VARIANT, analyze, decide, validate_application
from simulation import read_cases, simulate, synthetic_cases, validation_study

MINIMAL = """REGLA perfil_elegible PRIORIDAD 10
SI puntaje >= 650 ENTONCES APROBAR
POR_DEFECTO REVISION_MANUAL"""
SAMPLE = {"puntaje": "650", "ingreso_mensual": "2200", "ratio_deuda": "0.35"}


class LanguageTests(unittest.TestCase):
    def test_documented_example_tokens_and_tree(self):
        result = analyze(MINIMAL)
        self.assertTrue(result.accepted)
        self.assertEqual(
            [token.kind for token in result.tokens],
            "REGLA ID PRIORIDAD ENTERO SI ID GE ENTERO ENTONCES APROBAR POR_DEFECTO REVISION_MANUAL".split(),
        )
        self.assertEqual((result.tokens[6].text, result.tokens[6].line, result.tokens[6].column), (">=", 2, 12))
        self.assertTrue(result.tree.startswith("(pol (reg REGLA perfil_elegible"))
        self.assertIsNotNone(result.policy)

    def test_stage_specific_errors_never_return_executable_policy(self):
        examples = [
            (MINIMAL.replace(">=", "@"), "léxico", 2, 12),
            (MINIMAL.replace("ENTONCES ", ""), "sintáctico", 2, 19),
            (MINIMAL.replace("puntaje", "puntajee"), "semántico", 2, 4),
            (MINIMAL.replace("650", "650.5"), "semántico", 2, 15),
            (MINIMAL.replace("puntaje >= 650", "ratio_deuda <= 1.20"), "semántico", 2, 19),
            (MINIMAL.replace("PRIORIDAD 10", "PRIORIDAD 0"), "semántico", 1, 33),
        ]
        for policy, stage, line, column in examples:
            with self.subTest(policy=policy):
                analysis = analyze(policy)
                self.assertIsNone(analysis.policy)
                self.assertEqual((analysis.diagnostics[0].stage, analysis.diagnostics[0].line, analysis.diagnostics[0].column),
                                 (stage, line, column))
        self.assertIsNone(analyze(MINIMAL.rsplit("\n", 1)[0]).policy)
        self.assertIsNone(analyze(MINIMAL + "\nAPROBAR").policy)
        self.assertIsNone(analyze(MINIMAL, check_semantics=False).policy)

    def test_grouping_changes_decision_and_keywords_do_not_split_identifiers(self):
        expression = "puntaje >= 650 O ingreso_mensual >= 2000 Y ratio_deuda <= 0.35"
        grouped = "(puntaje >= 650 O ingreso_mensual >= 2000) Y ratio_deuda <= 0.35"
        a = analyze(MINIMAL.replace("puntaje >= 650", expression).replace("perfil_elegible", "REGLA_A"))
        b = analyze(MINIMAL.replace("puntaje >= 650", grouped))
        application = validate_application({**SAMPLE, "ratio_deuda": "0.70"})
        self.assertEqual(decide(a.policy, application).action, "APROBAR")
        self.assertEqual(decide(b.policy, application).action, "REVISION_MANUAL")

    def test_priority_ties_and_fallback(self):
        before, fallback = MINIMAL.rsplit("\n", 1)
        rule = "REGLA otra PRIORIDAD {} SI puntaje >= 650 ENTONCES {}"
        application = validate_application(SAMPLE)
        for priority, action, expected, names in [
            (10, "RECHAZAR", "REVISION_MANUAL", ("perfil_elegible", "otra")),
            (10, "APROBAR", "APROBAR", ("perfil_elegible", "otra")),
            (20, "RECHAZAR", "RECHAZAR", ("otra",)),
            (1, "RECHAZAR", "APROBAR", ("perfil_elegible",)),
        ]:
            policy = analyze("\n".join((before, rule.format(priority, action), fallback))).policy
            result = decide(policy, application)
            self.assertEqual((result.action, result.rules), (expected, names))
        policy = analyze(MINIMAL.replace("POR_DEFECTO REVISION_MANUAL", "POR_DEFECTO RECHAZAR")).policy
        result = decide(policy, validate_application({**SAMPLE, "puntaje": "649"}))
        self.assertEqual((result.action, result.rules), ("RECHAZAR", ()))

    def test_decisions_match_reference_for_100_cases(self):
        cases = synthetic_cases()
        result = simulate(analyze(DEFAULT_POLICY).policy, cases, analyze(DEMO_VARIANT).policy)

        def reference(case, threshold):
            if case["ratio_deuda"] > Decimal("0.50"):
                return "RECHAZAR"
            if case["puntaje"] >= threshold and case["ingreso_mensual"] >= 1800:
                if case["ratio_deuda"] <= Decimal("0.35"):
                    return "APROBAR"
            return "REVISION_MANUAL"

        expected = [(reference(case, 650), reference(case, 700)) for _, case in cases]
        self.assertEqual(len(expected), 100)
        self.assertEqual([(row["a"].action, row["b"].action) for row in result["rows"]], expected)
        self.assertEqual(result["changed"], 3)

    def test_validation_study(self):
        result = validation_study()
        self.assertEqual(result["base"], {"detected": 3, "missed": 5, "false_rejections": 0})
        self.assertEqual(result["full"], {"detected": 8, "missed": 0, "false_rejections": 0})
        self.assertTrue(all(row["full"] == row["expected"] for row in result["rows"]))


class WebTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_render_and_policy_comparison(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        response = self.client.post("/evaluate", data={"action": "compare"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Decisiones distintas", response.get_data(as_text=True))
        result = self.client.get("/api/demo").get_json()
        self.assertEqual((result["cases"], result["changed"]), (100, 3))
        self.assertEqual(len(read_cases(self.client.get("/demo.csv").data)), 100)

    def test_csv_compare_and_data_errors(self):
        header = b"id,puntaje,ingreso_mensual,ratio_deuda\n"
        for score, expected in [(b"650", 200), (b"650.5", 400), (b"1001", 400)]:
            with self.subTest(score=score):
                response = self.client.post("/evaluate", data={
                    "action": "compare", "cases": (io.BytesIO(header + b"F1," + score + b",2200,0.35\n"), "casos.csv"),
                })
                self.assertEqual(response.status_code, expected)
                if expected == 200:
                    self.assertIn("F1", response.get_data(as_text=True))
                    self.assertIn("Cambió", response.get_data(as_text=True))
        response = self.client.post("/evaluate", data={"action": "case", "ratio_deuda": "NaN"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_policy_preserves_input_and_prevents_execution(self):
        invalid = MINIMAL.replace("puntaje", "puntajee")
        response = self.client.post("/evaluate", data={
            "action": "compare", "policy_a": MINIMAL, "policy_b": invalid,
        })
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("puntajee", page)
        self.assertIn("Semántico", page)
        self.assertIn("Línea 2, columna 4", page)
        self.assertNotIn("Decisiones distintas", page)


if __name__ == "__main__":
    unittest.main()
