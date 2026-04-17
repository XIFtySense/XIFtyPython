# XIFty for Python

`xifty-python` is the official Python binding repo for XIFty.

It gives Python applications a thin, honest bridge into the XIFty metadata
engine so you can probe files, extract metadata views, and build ingestion
pipelines without shelling out to a CLI.

## What It Does

XIFty exposes four complementary metadata views:

- `raw`: direct extracted metadata values
- `interpreted`: decoded metadata with namespace meaning
- `normalized`: stable application-facing fields
- `report`: explicit issues and conflicts

This binding keeps that contract intact in Python.

## Quick Example

```python
from pathlib import Path
import xifty

result = xifty.extract(Path("photo.jpg"), view="normalized")
fields = {
    field["field"]: field["value"]["value"]
    for field in result["normalized"]["fields"]
}

print(result["input"]["detected_format"])
print(fields["device.make"])
print(fields["captured_at"])
```

## API

- `xifty.version()`
- `xifty.probe(path)`
- `xifty.extract(path, view="full")`

Supported `view` values:

- `"full"`
- `"raw"`
- `"interpreted"`
- `"normalized"`
- `"report"`

## Why Use It

Use this binding when you want:

- native Python access to XIFty
- normalized metadata fields for application logic
- raw and interpreted metadata for provenance-sensitive workflows
- explicit error and report surfaces instead of silent parsing shortcuts

Good fits include:

- upload-time metadata extraction
- photo library ingestion
- asset indexing pipelines
- back-office media processing

## Local Setup

This repo no longer assumes a sibling `../XIFty` checkout.

Prepare the canonical runtime artifact into a repo-local cache:

```bash
bash scripts/prepare-runtime.sh
```

Then run the binding:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 examples/basic_usage.py
PYTHONPATH=src python3 examples/gallery_ingest.py
```

Runtime resolution order is:

1. bundled runtime inside the built wheel, if present
2. `XIFTY_RUNTIME_DIR`, if explicitly set
3. repo-local runtime cache from `scripts/prepare-runtime.sh`
4. `XIFTY_CORE_DIR` as an explicit source-tree override for maintainers

This means normal consumers should not need a source checkout of `XIFty`, while
maintainers still retain an explicit source override path.

## Status

- release-ready wheel target on `macos-arm64` and `linux-x64`
- built wheels bundle the platform-native `xifty-ffi` runtime instead of
  requiring a source checkout
- built on the stable `xifty-ffi` ABI
- CI validates the wrapper against canonical runtime artifacts built from the
  public XIFty core repo
- not yet published to PyPI by default; publication should only happen once the
  wheel/install story is treated as fully ready

## License

MIT
