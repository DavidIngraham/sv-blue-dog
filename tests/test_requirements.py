import unittest

from scripts.render_requirements import extract, MODEL


BASE = """package Requirements {
    private import RequirementDerivation::*;
    requirement def <'M-1'> Mission { doc /* CONFIRMED INTENT: Complete the mission. */ }
    requirement def <'E-1'> Function { doc /* PROPOSED: Perform a function. */ }
    requirement mission : Mission;
    requirement function : Function;
    #derivation connection rationale {
        doc /* PROPOSED: A reason for this derivation. */
        end #original source ::> mission;
        end #derive target ::> function;
    }
} """


class DerivationTests(unittest.TestCase):
    def test_project_model_preserves_complete_graph(self):
        requirements, edges = extract(MODEL.read_text(encoding="utf-8-sig"))
        self.assertEqual({r["id"] for r in requirements.values()},
                         {"M-001", "M-002", *(f"E-00{i}" for i in range(1, 8))})
        self.assertEqual({(e["source"], e["target"]) for e in edges}, {
            ("roundTrip", "navigationAndControl"), ("roundTrip", "resetRecovery"),
            ("roundTrip", "communications"), ("roundTrip", "ingressResponse"),
            ("roundTrip", "missionEvidence"), ("multiDayEndurance", "energyAwareness"),
            ("multiDayEndurance", "lowEnergyRecovery"), ("energyAwareness", "lowEnergyRecovery"),
        })

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
            doc /* PROPOSED: Circular reasoning. */
            end #original a ::> function;
            end #derive b ::> mission;
        }'''
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            extract(BASE[:BASE.rfind('}')] + reverse + '}')

    def test_invalid_sysml_is_rejected(self):
        with self.assertRaises(Exception):
            extract(BASE.replace('requirement mission : Mission;', 'requirement mission : ;'))


if __name__ == '__main__':
    unittest.main()
