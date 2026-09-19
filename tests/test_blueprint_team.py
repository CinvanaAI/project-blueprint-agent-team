import json
from pathlib import Path

import pytest

from blueprint_team import BlueprintTeam, ROLES, parse_file_prompts, safe_output_path
from blueprint_team.demo import deterministic_runner


def test_role_order_and_fixed_artifacts() -> None:
    seen: list[str] = []

    def runner(role: str, instruction: str, context: dict[str, str]) -> str:
        seen.append(role)
        if role == "file_prompt_designer":
            return '{"files": []}'
        return f"output from {role}"

    result = BlueprintTeam(runner).run("Build a testable archive tool")
    assert seen == [role.name for role in ROLES]
    assert list(result.outputs) == [role.artifact_name for role in ROLES]


def test_blank_prompt_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        BlueprintTeam(deterministic_runner).run("  ")


@pytest.mark.parametrize("value", ["../secret.txt", "/absolute.txt", "C:/private.txt", "safe/../../escape"])
def test_unsafe_output_paths_are_rejected(tmp_path: Path, value: str) -> None:
    with pytest.raises(ValueError, match="Unsafe|escapes"):
        safe_output_path(tmp_path.resolve(), value)


def test_invalid_file_prompt_json_is_rejected() -> None:
    with pytest.raises(ValueError, match="strict JSON"):
        parse_file_prompts("not-json")
    with pytest.raises(ValueError, match="files array"):
        parse_file_prompts("{}")


def test_demo_writes_only_bounded_artifacts(tmp_path: Path) -> None:
    result = BlueprintTeam(deterministic_runner).run_and_write("Build a tiny local tool", tmp_path)
    assert len(result.outputs) == 6
    assert (tmp_path / "project_summary.md").is_file()
    assert (tmp_path / "project" / "app" / "core.py").read_text(encoding="utf-8").startswith("Implement")
    payload = json.loads((tmp_path / "file_prompts.json").read_text(encoding="utf-8"))
    assert len(payload["files"]) == 2
