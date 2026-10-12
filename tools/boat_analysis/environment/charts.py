"""Extract auditable course-planning features from downloaded NOAA S-57 cells.

Run in a uv environment containing pyogrio and geopandas. Source exchange sets
must retain their update files beside the base cell. GDAL applies those updates.
This extracts evidence, not a navigable route or a clearance certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


LAYERS = (
    "BCNLAT", "BOYLAT", "LIGHTS", "RESARE", "FAIRWY", "RECTRC",
    "NAVLNE", "BRIDGE", "DAMCON", "DEPARE", "LNDARE", "OBSTRN",
    "MORFAC", "LOKBSN", "UNSARE",
)


def extract(source: Path, destination: Path) -> None:
    import pyogrio

    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    features = []
    for cell in sorted(source.rglob("*.000")):
        available = dict(pyogrio.list_layers(cell))
        dsid = pyogrio.read_dataframe(cell, layer="DSID")
        files = sorted(cell.parent.glob(cell.stem + ".*"))
        manifest.append({
            "cell": cell.stem,
            "dataset_identification": json.loads(dsid.to_json(orient="records")),
            "source_files": [
                {"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in files if p.is_file()
            ],
        })
        for layer in LAYERS:
            if layer not in available:
                continue
            frame = pyogrio.read_dataframe(cell, layer=layer)
            # Preserve all S-57 attributes, including feature identifiers and
            # restrictions. No interpretation of a missing field as clearance.
            collection = json.loads(frame.to_json(default=lambda value: value.tolist()))
            for feature in collection["features"]:
                feature["properties"].update(source_cell=cell.stem, object_class=layer)
            features.extend(collection["features"])
    if not manifest:
        raise ValueError(f"No S-57 base cells found under {source}")
    (destination / "chart-features.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (destination / "chart-extraction.json").write_text(
        json.dumps({"gdal_version": pyogrio.__gdal_version_string__,
                    "updates": "GDAL S-57 default APPLY; exchange-set files retained beside base",
                    "layers": LAYERS, "cells": manifest}, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    extract(args.source, args.destination)
