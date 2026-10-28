"""Prepare, solve and replay the model through one repository command."""
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser('install')
    install_parser.add_argument('--source', help='Local OpenSysML Git checkout for an unpublished revision')
    for name in ("validate", "prepare", "recovery", "pitch", "audit", "evidence-check"):
        commands.add_parser(name)
    record = commands.add_parser("record", help="Execute cases into native AnalysisRecords evidence")
    record.add_argument("--case", action="append", required=True, dest="cases")
    record.add_argument("--output", required=True)
    study = commands.add_parser("study", help="Validate and execute a declarative native-analysis study")
    study.add_argument("config", nargs="?", help="YAML study configuration")
    study.add_argument("--schema", action="store_true", help="Print the versioned JSON Schema")
    study.add_argument("--output", help="Write the orchestration report or schema as JSON")
    solve = commands.add_parser("solve")
    solve.add_argument("--budget", type=int, default=40)
    solve.add_argument("--resume", action="store_true")
    solve.add_argument("--resolution", type=int, default=12)
    solve.add_argument("--route-profile", choices=["challenge", "all-season"], default="challenge")
    continuation = commands.add_parser("continue-sizing")
    continuation.add_argument("--target", type=float, default=1.2)
    continuation.add_argument("--step", type=float, default=.2)
    continuation.add_argument("--minimum-step", type=float, default=.025)
    continuation.add_argument("--budget", type=int, default=60)
    continuation.add_argument("--extensions", type=int, default=2)
    continuation.add_argument("--seed-run", default="2026-10-12-appendage-credibility")
    operating = commands.add_parser("operating")
    operating.add_argument("--budget", type=int, default=70)
    replay = commands.add_parser("replay")
    replay.add_argument("--budget", type=int, default=35)
    replay.add_argument("--workers", type=int, default=3)
    replay.add_argument("--scenarios", nargs="+", default=["nominal", "construction", "aerodynamic", "hydrodynamic", "energy", "combined"])
    args = parser.parse_args()
    if args.command == "install":
        from .model.install import main as install
        install(args.source)
    elif args.command == "validate":
        from .model.runtime import validate
        validate()
        print("Model validation passed; this is not physical verification.")
    elif args.command == "record":
        from .model.runtime import record_analyses
        print(record_analyses(args.cases, args.output))
    elif args.command == "study":
        import json
        from pathlib import Path
        from .studies.config import StudyConfig
        from .studies.runner import run_study, StudyExecutionError, StudyObjectivesError
        failed = None
        if args.schema:
            report = StudyConfig.model_json_schema()
        else:
            if args.config is None:
                parser.error("study requires a YAML configuration or --schema")
            try:
                report = run_study(args.config)
            except (StudyExecutionError, StudyObjectivesError) as error:
                report = error.report
                failed = str(error)
            except (ValueError, OSError) as error:
                parser.error(str(error))
        rendered = json.dumps(report, indent=2, allow_nan=False) + "\n"
        if args.output:
            output = Path(args.output).resolve()
            from .model.runtime import model_files
            protected = {path.resolve() for path in model_files()}
            if args.config:
                protected.add(Path(args.config).resolve())
            if output in protected:
                parser.error("Study output must not overwrite its configuration or an input model")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
            print(output)
        else:
            print(rendered, end="")
        if failed is not None:
            import sys
            print(failed, file=sys.stderr)
            raise SystemExit(1)
    elif args.command == "prepare":
        from .model.runtime import ROOT, validate
        (ROOT / ".tools").mkdir(exist_ok=True)
        validate()
        from sysml_python import Project
        from .model.install import binary_path
        Project(ROOT/'pyproject.toml', executable=binary_path()).prepare()
        from .model.preparation import prepare_mass, prepare_operating
        prepare_mass()
        print("Prepared mass reference evidence", flush=True)
        prepare_operating()
        print("Prepared operating reference evidence", flush=True)
        for name in ("hydrostatics", "resistance", "uncertainty"):
            importlib.import_module(f"tools.boat_analysis.model.{name}").prepare()
            print(f"Prepared {name}", flush=True)
    elif args.command == "solve":
        from .optimization.search import run
        run(args.budget, args.resume, args.resolution, args.route_profile)
    elif args.command == "continue-sizing":
        from .optimization.continuation import run
        run(args.target, args.step, args.minimum_step, args.budget, args.extensions, args.seed_run)
    elif args.command == "operating":
        from .optimization.operating import run
        run(args.budget)
    elif args.command == "replay":
        from .optimization.replay import run
        run(args.scenarios, args.budget, args.workers)
    elif args.command == "evidence-check":
        from .evidence.records import verify_run_sources
        from .model.runtime import ROOT
        import json
        # Aerodynamic evidence has its own schema and validator.
        manifests = [p for p in (ROOT/"evidence/runs").glob("*/manifest.json")
                     if {"files", "sourceRevision"} <= json.loads(p.read_text()).keys()]
        count = sum(verify_run_sources(p.parent) for p in manifests)
        print(f"Verified {count} archived source hashes.")
    else:
        module = {"recovery": "recovery", "pitch": "pitch", "audit": "resistance_audit"}[args.command]
        importlib.import_module(f"tools.boat_analysis.optimization.{module}").run()


if __name__ == "__main__":
    main()
