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

Prepare the core dependency into a repo-local cache:

```bash
bash scripts/prepare-core.sh
```

Then run the binding:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 examples/basic_usage.py
PYTHONPATH=src python3 examples/gallery_ingest.py
```

You can still override the core location explicitly with `XIFTY_CORE_DIR`.

## Status

- source-first and usable today
- built on the stable `xifty-ffi` ABI
- CI validates the wrapper against the public XIFty core repo
- packaging metadata is in place for future PyPI distribution

## License

MIT
