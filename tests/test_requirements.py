import unittest
import re

from scripts.render_requirements import extract, MODEL, CHALLENGE, native_graph, project_sources, load_model, native_register


BASE = """package Requirements {
    private import RequirementDerivation::*;
    requirement def <'M-1'> Mission { doc /* Complete the mission. */ }
    requirement def <'E-1'> Function { doc /* Perform a function. */ }
    requirement mission : Mission;
    requirement function : Function;
    #derivation connection rationale {
        doc /* A reason for this derivation. */
        end #original source ::> mission;
        end #derive target ::> function;
    }
} """


class DerivationTests(unittest.TestCase):
    def test_native_diagram_preserves_all_derivations(self):
        requirements, edges = extract(project_sources())
        dot = native_graph()
        nodes = dict(re.findall(r'"(n[0-9]+)" \[.*?<b>([A-Za-z0-9_:]+) :', dot))
        nodes = {key: name.rsplit("::", 1)[-1] for key, name in nodes.items()}
        self.assertEqual(set(nodes.values()), set(requirements))
        links = re.findall(r'"(n[0-9]+)" -> "(n[0-9]+)" \[label="derive"', dot)
        # Native notation points from derived to original.
        self.assertEqual({(nodes[b], nodes[a]) for a, b in links},
                         {(e["source"], e["target"]) for e in edges})
        self.assertEqual(len(links), len(edges))

    def test_project_model_preserves_complete_graph(self):
        requirements, edges = extract(project_sources())
        self.assertEqual({r["id"] for r in requirements.values()},
                         {"C-000", "H-001", "M-001", "M-002", *(f"E-00{i}" for i in range(1, 8)), *(f"C-00{i}" for i in range(1, 7))})
        self.assertEqual({(e["source"], e["target"]) for e in edges}, {
            *(("transGorgeChallenge", target) for target in ["courseCompletion", "repeatedOperation", "unassistedAttempt", "sailingPropulsion", "liveObservation", "emergencyIntervention"]),
            *(("hawaiiVoyage", target) for target in ["multiDayEndurance", "navigationAndControl", "communications", "resetRecovery", "missionEvidence"]),
            ("courseCompletion", "roundTrip"), ("repeatedOperation", "multiDayEndurance"),
            ("unassistedAttempt", "navigationAndControl"), ("sailingPropulsion", "roundTrip"),
            ("liveObservation", "communications"), ("emergencyIntervention", "communications"),
            ("roundTrip", "navigationAndControl"), ("roundTrip", "resetRecovery"),
            ("roundTrip", "communications"), ("roundTrip", "ingressResponse"),
            ("roundTrip", "missionEvidence"), ("multiDayEndurance", "energyAwareness"),
            ("multiDayEndurance", "lowEnergyRecovery"), ("energyAwareness", "lowEnergyRecovery"),
        })

    def test_exactly_two_top_level_drivers(self):
        requirements, edges = extract(project_sources())
        roots = set(requirements) - {edge["target"] for edge in edges}
        self.assertEqual(roots, {"transGorgeChallenge", "hawaiiVoyage"})

    def test_challenge_is_independent_of_vehicle(self):
        source = CHALLENGE.read_text(encoding="utf-8-sig")
        self.assertTrue(load_model(source).ok)
        self.assertNotIn("BlueDog", source)

    def test_vehicle_import_needs_challenge(self):
        with self.assertRaises(ValueError):
            load_model(MODEL.read_text(encoding="utf-8-sig"))

    def test_duplicate_requirement_id_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            extract(BASE.replace("<'E-1'>", "<'M-1'>"))

    def test_role_metadata_defines_direction_not_end_name(self):
        source = BASE.replace('source ::>', 'arbitraryOne ::>').replace('target ::>', 'arbitraryTwo ::>')
        requirements, edges = extract(source)
        self.assertEqual(len(requirements), 2)
        self.assertEqual([(e['source'], e['target']) for e in edges], [('mission', 'function')])

    def test_missing_endpoint_is_not_silently_dropped(self):
        with self.assertRaisesRegex(ValueError, '(?i)unresolved'):
            extract(BASE.replace('::> function', '::> missing'))

    def test_missing_role_fails(self):
        with self.assertRaises(ValueError):
            extract(BASE.replace('#derive', '#original'))

    def test_cycle_fails(self):
        reverse = '''#derivation connection reverse {
            doc /* Circular reasoning. */
            end #original a ::> function;
            end #derive b ::> mission;
        }'''
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            extract(BASE[:BASE.rfind('}')] + reverse + '}')

    def test_status_comes_from_typed_metadata(self):
        source = BASE.replace(
            'doc /* Complete the mission.',
            '@ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::tbc; } doc /* Complete the mission.')
        requirements, edges = extract(source)
        self.assertEqual(requirements['mission']['status'], 'tbc')
        self.assertEqual(requirements['function']['status'], 'unspecified')
        self.assertEqual(edges[0]['status'], 'unspecified')

    def test_native_register_preserves_requirements_and_derivations(self):
        requirements, edges = extract(project_sources())
        markdown = native_register()
        for req in requirements.values():
            self.assertIn(f"| {req['id']} | {req['name']} | {req['status']} |", markdown)
        for edge in edges:
            self.assertIn(f"| {edge['source']} | {edge['target']} | {edge['status']} |", markdown)
        self.assertEqual(len([line for line in markdown.splitlines() if line.startswith('| ')]),
                         len(requirements) + len(edges) + 4)

    def test_project_status_annotations(self):
        requirements, edges = extract(project_sources())
        self.assertEqual({r['status'] for r in requirements.values()}, {'open'})
        self.assertEqual({e['status'] for e in edges}, {'open'})

    def test_invalid_sysml_is_rejected(self):
        with self.assertRaises(Exception):
            extract(BASE.replace('requirement mission : Mission;', 'requirement mission : ;'))


if __name__ == '__main__':
    unittest.main()
