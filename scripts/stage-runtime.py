#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_RUNTIME_DIR = ROOT / "src" / "xifty" / "_runtime"


def bundled_runtime_dir() -> Path:
    override = os.environ.get("XIFTY_RUNTIME_DIR")
    if override:
        return Path(override).resolve()

    cache_root = Path(os.environ.get("XIFTY_RUNTIME_CACHE_DIR", ROOT / ".xifty-runtime"))
    runtime_version = os.environ.get(
        "XIFTY_RUNTIME_VERSION",
        (ROOT / "runtime-version.txt").read_text().strip(),
    )

    if sys.platform == "darwin" and os.uname().machine in {"arm64", "aarch64"}:
        target = "macos-arm64"
    elif sys.platform.startswith("linux") and os.uname().machine in {"x86_64", "amd64"}:
        target = "linux-x64"
    else:
        raise SystemExit(f"unsupported host for staging runtime: {sys.platform} / {os.uname().machine}")

    return (cache_root / f"xifty-runtime-{target}-v{runtime_version}").resolve()


def main():
    runtime_dir = bundled_runtime_dir()
    manifest = runtime_dir / "manifest.json"
    if not manifest.exists():
        raise SystemExit(
            f"missing runtime manifest at {manifest}; run scripts/prepare-runtime.sh "
            "or set XIFTY_RUNTIME_DIR"
        )

    shutil.rmtree(PACKAGE_RUNTIME_DIR, ignore_errors=True)
    PACKAGE_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(manifest, PACKAGE_RUNTIME_DIR / "manifest.json")
    shutil.copytree(runtime_dir / "include", PACKAGE_RUNTIME_DIR / "include")
    shutil.copytree(runtime_dir / "lib", PACKAGE_RUNTIME_DIR / "lib")

    parsed = json.loads(manifest.read_text())
    print(
        f"Staged XIFty runtime {parsed['core_version']} "
        f"for {parsed['target']} into {PACKAGE_RUNTIME_DIR}"
    )


if __name__ == "__main__":
    main()
