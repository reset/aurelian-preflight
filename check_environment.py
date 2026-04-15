#!/usr/bin/env python3

from __future__ import annotations

import platform
from pathlib import Path
import shutil
import subprocess
import sys


PYTHON_CANDIDATES = [
    sys.executable,
    "python3.13",
    "python3.12",
    "python3.11",
    "python3.10",
    "python3",
    "python",
]


def parse_semver(raw_version: str) -> tuple[int, int, int]:
    version = raw_version.strip().lstrip("v").split()[0]
    pieces = version.split(".")
    major = int(pieces[0]) if len(pieces) > 0 else 0
    minor = int(pieces[1]) if len(pieces) > 1 else 0
    patch = int(pieces[2]) if len(pieces) > 2 else 0
    return major, minor, patch


def is_wsl() -> bool:
    if platform.system() != "Linux":
        return False

    release = platform.release().lower()
    if "microsoft" in release or "wsl" in release:
        return True

    proc_version = Path("/proc/version")
    if not proc_version.exists():
        return False

    return "microsoft" in proc_version.read_text(encoding="utf-8").lower()


def running_from_windows_mount(path: Path) -> bool:
    return path.resolve().as_posix().startswith("/mnt/")


def find_supported_python() -> tuple[str, str] | None:
    seen: set[str] = set()

    for candidate in PYTHON_CANDIDATES:
        resolved = candidate
        if not resolved:
            continue
        if not resolved.startswith("/"):
            resolved = shutil.which(resolved) or ""
        if not resolved or resolved in seen:
            continue
        seen.add(resolved)

        completed = subprocess.run(
            [
                resolved,
                "-c",
                (
                    "import sys; "
                    "print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
                ),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            continue

        version = (completed.stdout or completed.stderr).strip()
        if parse_semver(version) >= (3, 10, 0):
            return resolved, version

    return None


def main() -> int:
    print("Aurelian live interview environment check")
    print("-----------------------------------------")
    print(f"Platform: {platform.system()} {platform.release()}")
    if is_wsl() and running_from_windows_mount(Path.cwd()):
        print("[WARN] WSL repo is running from /mnt/... which is often slower")
        print("       than the Linux filesystem. If possible, use a path under ~/ instead.")
    print()

    missing = []

    if shutil.which("git") is None:
        print("[FAIL] git: not found")
        missing.append("git")
    else:
        completed = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        output = (completed.stdout or completed.stderr).strip()
        if completed.returncode == 0:
            print(f"[ OK ] git: {output}")
        else:
            print(f"[FAIL] git: command exited with {completed.returncode}")
            missing.append("git")

    python_info = find_supported_python()
    if python_info is None:
        print("[FAIL] python: no Python 3.10+ interpreter found")
        missing.append("python>=3.10")
    else:
        python_path, version = python_info
        print(f"[ OK ] python: {version} ({python_path})")

    print()
    if missing:
        print("Environment check failed.")
        print("Missing or broken tools:", ", ".join(missing))
        print("Please let the recruiting team know before the interview.")
        return 1

    print("Environment check passed.")
    print("No repo review or coding prep is expected before the interview.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
