"""Regenerate scalar records with the pinned OpenSysML code-generation checkout."""
import argparse
from pathlib import Path
from opensysml.generate import main as generate

ROOT=Path(__file__).resolve().parents[3]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    command=[str(ROOT/'models/libraries/marine/design.sysml'),
             '--format','dataclass','--definition','MarineDesign::Design',
             '--definition','MarineDesign::Parameters',
             '-o',str(ROOT/'tools/boat_analysis/model/design_types.py')]
    return generate(command + (['--check'] if args.check else []))

if __name__=='__main__':
    raise SystemExit(main())
