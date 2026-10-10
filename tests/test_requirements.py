"""Integration checks for the native publishing outputs, not a second SysML parser."""
import re
import unittest
from scripts.render_requirements import native, native_graph, native_register, MODELS


class PublishingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dot = native_graph()
        cls.markdown = native_register()
        cls.nodes = dict(re.findall(r'"(n[0-9]+)" \[.*?<b>([A-Za-z0-9_:]+) :', cls.dot))
        cls.nodes = {key: name.rsplit("::", 1)[-1] for key, name in cls.nodes.items()}
        links = re.findall(r'"(n[0-9]+)" -> "(n[0-9]+)" \[label="derive"', cls.dot)
        cls.edges = [(cls.nodes[b], cls.nodes[a]) for a, b in links]

    def test_native_validation(self):
        native("-validate")

    def test_challenge_is_standalone(self):
        native("-validate", models=MODELS[:1])

    def test_diagram_preserves_expected_derivations(self):
        expected = {
            *(("transGorgeChallenge", target) for target in ["courseCompletion", "repeatedOperation", "unassistedAttempt", "sailingPropulsion", "liveObservation", "emergencyIntervention"]),
            *(("hawaiiVoyage", target) for target in ["multiDayEndurance", "navigationAndControl", "communications", "resetRecovery", "missionEvidence"]),
            ("courseCompletion", "roundTrip"), ("repeatedOperation", "multiDayEndurance"),
            ("unassistedAttempt", "navigationAndControl"), ("sailingPropulsion", "roundTrip"),
            ("liveObservation", "communications"), ("emergencyIntervention", "communications"),
            ("roundTrip", "navigationAndControl"), ("roundTrip", "resetRecovery"),
            ("roundTrip", "communications"), ("roundTrip", "ingressResponse"),
            ("roundTrip", "missionEvidence"), ("multiDayEndurance", "energyAwareness"),
            ("multiDayEndurance", "lowEnergyRecovery"), ("energyAwareness", "lowEnergyRecovery"),
        }
        self.assertEqual(set(self.edges), expected)
        self.assertEqual(len(self.edges), len(expected))
        self.assertEqual(len(self.nodes), 17)

    def test_exactly_two_top_level_drivers(self):
        roots = set(self.nodes.values()) - {target for _, target in self.edges}
        self.assertEqual(roots, {"transGorgeChallenge", "hawaiiVoyage"})

    def test_register_preserves_ids_status_and_relationships(self):
        ids = re.findall(r"^\| ([CHEM]-[0-9]+) \|", self.markdown, re.MULTILINE)
        expected = {"H-001", "M-001", "M-002",
                    *(f"C-00{i}" for i in range(7)), *(f"E-00{i}" for i in range(1, 8))}
        self.assertEqual(set(ids), expected)
        self.assertEqual(len(ids), len(expected))
        for source, target in self.edges:
            self.assertIn(f"| {source} | {target} | open |", self.markdown)
        rows = [line for line in self.markdown.splitlines() if line.startswith('| ')]
        self.assertEqual(len(rows), 17 + 25 + 4)
        data = [line for line in rows if line not in (
            '| ID | Requirement | Status | Statement |',
            '| Original | Derived | Status | Rationale |', '| --- | --- | --- | --- |')]
        self.assertTrue(all(' | open | ' in line for line in data))


if __name__ == '__main__':
    unittest.main()
