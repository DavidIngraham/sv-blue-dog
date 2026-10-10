"""Install the pinned native renderer locally; never use a moving nightly tag."""
import hashlib
import io
import platform
import tarfile
import urllib.request
import zipfile
from pathlib import Path

RELEASE = "nightly-20261009-28106371e"
ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "windows-amd64": "0e1562e74e2ede1de12937196772b811466f9dccfc566133531e869364a9bb9c",
    "linux-amd64": "72426e639a52351e5be8b577a58cba043027e0acb4c5de0670638a4e622b1184",
    "linux-arm64": "16b196a542b6217e790fb0c417509d79810e805b845e1619f7141c539dd1cd11",
    "darwin-amd64": "b45f6577712bf842d2b6d8aafd082603aceabad2c353ed075406cd88a9ab27d7",
    "darwin-arm64": "6dade50d74914f9842688f08b2d4e45efa2d72699b83c7989fdad2c50adf1beb",
}

def binary_path():
    return ROOT / ".tools" / RELEASE / ("sysml.exe" if platform.system() == "Windows" else "sysml")

def main():
    arch = {"x86_64": "amd64", "amd64": "amd64", "aarch64": "arm64", "arm64": "arm64"}[platform.machine().lower()]
    target = f"{platform.system().lower()}-{arch}"
    digest = HASHES[target]
    suffix = ".zip" if target.startswith("windows") else ".tar.gz"
    name = f"sysml-{target}{suffix}"
    url = f"https://github.com/Open-MBEE/OpenSysML/releases/download/{RELEASE}/{name}"
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != digest:
        raise SystemExit("OpenSysML archive checksum mismatch")
    # Extract only the executable bytes; never extract arbitrary archive paths.
    if suffix == ".zip":
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            candidates = [n for n in archive.namelist() if Path(n).name in {"sysml.exe", f"sysml-{target}.exe"}]
            if len(candidates) != 1:
                raise SystemExit("Expected exactly one sysml executable")
            executable = archive.read(candidates[0])
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            candidates = [m for m in archive.getmembers() if m.isfile() and Path(m.name).name in {"sysml", f"sysml-{target}"}]
            if len(candidates) != 1:
                raise SystemExit("Expected exactly one sysml executable")
            executable = archive.extractfile(candidates[0]).read()
    path = binary_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(executable)
    path.chmod(0o755)
    print(f"Installed {RELEASE}: {path}")

if __name__ == "__main__":
    main()
