# XIFtyPython

Python binding for [XIFty](https://github.com/XIFtySense/XIFty).

`XIFtyPython` is a thin Python wrapper over the stable `xifty-ffi` C ABI. It is
ready for source-based use today and is intended to become the canonical Python
package for XIFty as distribution hardens.

## What You Get

- `version()` for the bound core version
- `probe(path)` for fast format detection and structural inspection
- `extract(path, view=...)` for JSON extraction across `full`, `raw`,
  `interpreted`, `normalized`, and `report` views
- a minimal Python surface with no hidden metadata logic layered on top of the
  core engine

## Quickstart

Clone the public core repo as a sibling checkout, then run the wrapper against
it:

```bash
git clone git@github.com:XIFtySense/XIFty.git ../XIFty
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 examples/basic_usage.py
```

If your core checkout lives elsewhere, set `XIFTY_CORE_DIR`:

```bash
XIFTY_CORE_DIR=/path/to/XIFty PYTHONPATH=src python3 examples/basic_usage.py
```

## Status

- source-first and usable today
- built on the stable `xifty-ffi` ABI
- CI validates the wrapper against the public XIFty core repo on every push
- packaging metadata is in place for future PyPI distribution

## License

MIT
