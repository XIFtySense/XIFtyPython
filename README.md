# XIFtyPython

Python package for XIFty.

This package currently builds against the XIFty core repository through the
stable `xifty-ffi` C ABI. Local development expects a sibling checkout of the
core repo at:

- `../XIFty`

You can override that location with `XIFTY_CORE_DIR`.

## Local Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 examples/basic_usage.py
```

## Packaging

This repo includes a `pyproject.toml` so it can evolve into a normal published
package. For now, the underlying core engine is still private, so local usage is
expected to link against a sibling XIFty checkout.

