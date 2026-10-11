"""Prepare, solve and replay the model through one repository command."""
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "validate", "prepare", "recovery", "pitch", "audit", "evidence-check"):
        commands.add_parser(name)
    solve = commands.add_parser("solve")
    solve.add_argument("--budget", type=int, default=40)
    solve.add_argument("--resume", action="store_true")
    solve.add_argument("--resolution", type=int, default=12)
    solve.add_argument("--route-profile", choices=["challenge", "all-season"], default="challenge")
    operating = commands.add_parser("operating")
    operating.add_argument("--budget", type=int, default=70)
    replay = commands.add_parser("replay")
    replay.add_argument("--budget", type=int, default=35)
    replay.add_argument("--workers", type=int, default=3)
    replay.add_argument("--scenarios", nargs="+", default=["nominal", "construction", "aerodynamic", "hydrodynamic", "energy", "combined"])
    args = parser.parse_args()
    if args.command == "install":
        from .model.install import main as install
        install()
    elif args.command == "validate":
        from .model.runtime import validate
        validate()
        print("Model validation passed; this is not physical verification.")
    elif args.command == "prepare":
        from .model.runtime import ROOT, validate
        (ROOT / ".tools").mkdir(exist_ok=True)
        validate()
        for name in ("mass", "operating", "hydrostatics", "resistance", "uncertainty"):
            importlib.import_module(f"tools.boat_analysis.model.{name}").prepare()
            print(f"Prepared {name}", flush=True)
    elif args.command == "solve":
        from .optimization.search import run
        run(args.budget, args.resume, args.resolution, args.route_profile)
    elif args.command == "operating":
        from .optimization.operating import run
        run(args.budget)
    elif args.command == "replay":
        from .optimization.replay import run
        run(args.scenarios, args.budget, args.workers)
    elif args.command == "evidence-check":
        from .evidence.records import CURRENT, verify_baseline_sources, verify_run_sources
        print(f"Verified {verify_baseline_sources() + verify_run_sources(CURRENT)} archived source hashes.")
    else:
        module = {"recovery": "recovery", "pitch": "pitch", "audit": "resistance_audit"}[args.command]
        importlib.import_module(f"tools.boat_analysis.optimization.{module}").run()


if __name__ == "__main__":
    main()
