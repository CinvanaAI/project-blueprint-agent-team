# Project Blueprint Agent Team

A six-stage recipe for turning a project request into an inspectable design brief. Each named role receives the original request and earlier outputs; the final stage writes per-file implementation prompts.

## Try it

Python 3.11 or newer.

```sh
python -m pip install -e .
python -m blueprint_team "Build a greeting tool" --output ./demo-output
```

The offline demonstration writes six role artifacts and prompts for `app/core.py` and `tests/test_core.py`. Those `.py` files contain English implementation instructions. They are inputs to a future coding step, not executable generated software. The command reports six review artifacts.

## How it works

Separate role outputs make a proposed design traceable before code creation begins. Read the [mechanism and implementation notes](docs/MECHANISM.md) for the specific boundaries and source links.

## Scope

No experiment here establishes that six roles improve model quality. JSON/path failures may leave earlier artifacts, so use a fresh output directory. The injected runner is the extension point; a live model provider is not included.

## Verify

`python -m pytest` runs the behavior tests (install `pytest` first). The runnable example above provides a separate first-use check.

MIT licensed; see [LICENSE.md](LICENSE.md). Origin and release boundaries are documented in [ORIGIN.md](ORIGIN.md) and [SECURITY.md](SECURITY.md).
## Inspect the example result

Open the [saved synthetic result](examples/captured-result.json) alongside its [input and demonstration](blueprint_team/demo.py). The result is from the bundled synthetic example; local machine paths and temporary run identifiers are excluded from public projections.
