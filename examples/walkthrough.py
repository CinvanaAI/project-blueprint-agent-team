"""Capture six role contexts and outputs using only the deterministic runner."""
import json
import tempfile
from pathlib import Path
from blueprint_team import BlueprintTeam
from blueprint_team.demo import deterministic_runner

calls = []
def observe(role, instruction, context):
    calls.append({"role": role, "instruction": instruction, "context_keys": list(context)})
    return deterministic_runner(role, instruction, context)

with tempfile.TemporaryDirectory(prefix="blueprint-team-") as temporary:
    root = Path(temporary)
    result = BlueprintTeam(observe).run_and_write("Build a greeting tool", root)
    files = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
             for p in sorted((root / "project").rglob("*")) if p.is_file()}
    assert len(result.outputs) == 6 and len(files) == 2
    assert len(calls[-1]["context_keys"]) == 6
    print(json.dumps({"request": result.prompt, "calls": calls, "role_artifacts": result.outputs,
                      "implementation_prompts": files, "software_implemented": False}, indent=2))
