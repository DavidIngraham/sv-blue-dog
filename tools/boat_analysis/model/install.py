"""Build the upstream CLI, Python service and MCP from one verified revision."""
import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REVISION = "23ca2e2f0f1fae4da6bc3e1488951cb017ed43e2"
RELEASE = "develop-" + REVISION[:9]
SOURCE_SHA256 = "9a3bcf85cf42597063682edc497daa43e2b674577981e0c62216bc1a06e08e62"
ROOT = Path(__file__).resolve().parents[3]
COMMANDS = ("sysml", "sysml-grpc", "sysml-mcp")


def binary_path(command="sysml"):
    if command not in COMMANDS:
        raise ValueError(f"Unknown OpenSysML command: {command}")
    return ROOT / ".tools" / RELEASE / (command + (".exe" if platform.system() == "Windows" else ""))


def main(source_checkout=None):
    go = shutil.which("go")
    if not go:
        raise SystemExit("Install Go 1.25 or later to build the pinned OpenSysML development revision.")
    destination = binary_path().parent
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination / "source.zip"
    if source_checkout is not None:
        subprocess.run(["git", "-C", str(Path(source_checkout).resolve()), "archive",
                        "--format=zip", f"--prefix=OpenSysML-{REVISION}/",
                        "--output", str(archive_path), REVISION], check=True)
    if not archive_path.exists():
        with urllib.request.urlopen(f"https://codeload.github.com/DavidIngraham/OpenSysML/zip/{REVISION}", timeout=120) as response:
            archive_path.write_bytes(response.read())
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("OpenSysML source archive checksum mismatch")
    with tempfile.TemporaryDirectory(prefix='bluedog-opensysml-') as directory:
        source = Path(directory)
        build(go, archive_path, source)
        shutil.copytree(source / 'client' / 'python', destination / 'source' / 'client' / 'python',
                        dirs_exist_ok=True)


def build(go, archive_path, source):
    prefix = f"OpenSysML-{REVISION}/"
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            if not member.filename.startswith(prefix):
                raise ValueError("Unexpected upstream archive root")
            relative = Path(member.filename[len(prefix):])
            target = (source / relative).resolve()
            if not target.is_relative_to(source.resolve()):
                raise ValueError("Unsafe upstream archive path")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    env = dict(os.environ, CGO_ENABLED="0")
    for command in COMMANDS:
        print(f"Building upstream {command} at {REVISION}", flush=True)
        subprocess.run([go, "build", "-trimpath", "-ldflags",
                        f"-s -w -X main.Version={RELEASE} -X main.Commit={REVISION}",
                        "-o", str(binary_path(command)), f"./cmd/{command}"],
                       cwd=source, env=env, check=True)
        print(f"Installed {command} at {REVISION}: {binary_path(command)}", flush=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', help='Local Git checkout containing the pinned revision')
    main(parser.parse_args().source)
