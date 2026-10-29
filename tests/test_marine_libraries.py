import json
from tools.boat_analysis.model.runtime import ROOT, native, validate


def test_libraries_validate_without_blue_dog():
    files = tuple((ROOT / "models/libraries").rglob("*.sysml"))
    assert validate(files)["status"] == "holds"
    for file in files:
        assert "BlueDog" not in file.read_text(encoding="utf-8")


def test_another_boat_can_use_actuation_without_vehicle_requirements(tmp_path):
    case = tmp_path / "other-boat.sysml"
    case.write_text('''package OtherBoat {
        private import ScalarValues::*;
        analysis example {
            out attribute power : Real [3] ordered nonunique =
                Analysis::Energy::Actuation::DrivePower(1,0.2,0.8,0.4,1,0.1,0,0.02,0.98);
        }
    }''', encoding="utf-8")
    files = (*tuple((ROOT / "models/libraries").rglob("*.sysml")), case)
    report = json.loads(native("-analysis", "OtherBoat::example", "-json", models=files))
    assert report["status"] == "holds"
