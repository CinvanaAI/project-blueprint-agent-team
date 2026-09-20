# Project Blueprint Agent Team

An experiment in handing one request through six fixed roles, from clarification to a per-file implementation brief. Each role sees the original request and every earlier role's text. The output is a **plan for implementation**, not working software.

The earlier experiment used AutoGen and particular model configurations. This public continuation keeps its role sequence behind one injectable Python callable; the included runner is deterministic and offline. [Origin](ORIGIN.md)

## Follow the handoffs

Python 3.11 or later, from this checkout:

```sh
python -m pip install -e .
python -m examples.walkthrough
python -m blueprint_team "Build a greeting tool" --output ./demo-output
python -m pip install pytest
python -m pytest -q
```

[The captured run](examples/captured-result.json) includes each call's instruction and context keys, all six returned artifacts, and both implementation prompts. The CLI saves those artifacts.

| Role | Adds to the next role's context |
| --- | --- |
| Prompt interpreter | `project_summary.md` |
| System architect | `folder_map.md` |
| Dependency mapper | `dependency_map.md` |
| File prompt designer | `file_prompts.json` |
| Validator | `validation_report.md` |
| Spec writer | `final_summary.md` |

The final role sees the request plus five prior artifacts. The file prompt designer supplies the paths/prompts; the spec writer adds a summary. Files are written only after all six calls return.

**Files under `demo-output/project/`, including `app/core.py`, contain English implementation prompts. Do not run them as Python.** The paths describe intended future files.

## Reuse the coordinator

```python
from blueprint_team import BlueprintTeam
from blueprint_team.demo import deterministic_runner

calls = []
def runner(role, instruction, context):
    calls.append((role, tuple(context)))
    return deterministic_runner(role, instruction, context)

result = BlueprintTeam(runner).run("Describe a local greeting tool")
assert len(calls) == 6
assert "file_prompts.json" in result.outputs
```

Replace `runner(role, instruction, context) -> str` with a trusted implementation. It must return nonempty text. The file-prompt role must return strict JSON shaped like `{"files": [{"path": "app/core.py", "prompt": "Implement ..."}]}`. [The demo runner](blueprint_team/demo.py) shows all response contracts.

[core.py](blueprint_team/core.py) owns role order, context accumulation and output paths. “Validator” means another text-producing role, not independent software verification. Only the file-prompt envelope and destination paths receive structural checks.

## Scope and next experiment

There is no measured evidence here that six roles beat one good planning prompt. No code is generated or tested and no provider is bundled. A role exception stops `run_and_write` before output writing. Later parsing/writing failures can leave partial artifacts; use a new output directory to avoid overwriting earlier results.

A useful next comparison would hold the request and evaluation criteria fixed, then compare a single-stage planner with this sequence.

[Mechanism](docs/MECHANISM.md) · [Tests](tests/test_blueprint_team.py) · [Security](SECURITY.md) · [License](LICENSE.md)
