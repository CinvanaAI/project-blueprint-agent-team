from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Mapping


AgentRunner = Callable[[str, str, Mapping[str, str]], str]


@dataclass(frozen=True)
class RoleSpec:
    name: str
    instruction: str
    artifact_name: str


@dataclass(frozen=True)
class BlueprintResult:
    prompt: str
    outputs: dict[str, str]


ROLES = (
    RoleSpec(
        "prompt_interpreter",
        "Clarify scope, features, constraints, and assumptions. Return a structured project summary.",
        "project_summary.md",
    ),
    RoleSpec(
        "system_architect",
        "Design a complete folder and file blueprint from the clarified summary.",
        "folder_map.md",
    ),
    RoleSpec(
        "dependency_mapper",
        "Explain dependencies and interactions among the proposed modules.",
        "dependency_map.md",
    ),
    RoleSpec(
        "file_prompt_designer",
        "Return strict JSON with a files array. Each item needs a relative path and implementation prompt.",
        "file_prompts.json",
    ),
    RoleSpec(
        "validator",
        "Check names, references, dependencies, completeness, and alignment with the original request.",
        "validation_report.md",
    ),
    RoleSpec(
        "spec_writer",
        "Compile the validated result into a concise downstream handoff without claiming code was built.",
        "final_summary.md",
    ),
)


class BlueprintTeam:
    def __init__(self, runner: AgentRunner):
        self._runner = runner

    def run(self, prompt: str) -> BlueprintResult:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("A non-empty project prompt is required.")

        outputs: dict[str, str] = {}
        for role in ROLES:
            context = {"original_prompt": prompt, **outputs}
            response = self._runner(role.name, role.instruction, context)
            if not isinstance(response, str) or not response.strip():
                raise ValueError(f"Agent stage {role.name} returned no usable text.")
            outputs[role.artifact_name] = response.strip()
        return BlueprintResult(prompt=prompt, outputs=outputs)

    def run_and_write(self, prompt: str, output_root: Path) -> BlueprintResult:
        result = self.run(prompt)
        write_result(result, output_root)
        return result


def write_result(result: BlueprintResult, output_root: Path) -> list[Path]:
    root = output_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for artifact_name, content in result.outputs.items():
        target = safe_output_path(root, artifact_name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content + "\n", encoding="utf-8")
        written.append(target)

    prompts = parse_file_prompts(result.outputs["file_prompts.json"])
    project_root = safe_output_path(root, "project")
    project_root.mkdir(parents=True, exist_ok=True)
    for relative_path, file_prompt in prompts:
        target = safe_output_path(project_root, relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file_prompt + "\n", encoding="utf-8")
        written.append(target)

    return written


def parse_file_prompts(raw: str) -> list[tuple[str, str]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("File-prompt stage must return strict JSON.") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), list):
        raise ValueError("File-prompt JSON must contain a files array.")

    parsed: list[tuple[str, str]] = []
    for index, item in enumerate(payload["files"]):
        if not isinstance(item, dict):
            raise ValueError(f"File-prompt item {index} must be an object.")
        relative_path = item.get("path")
        prompt = item.get("prompt")
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise ValueError(f"File-prompt item {index} has no path.")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"File-prompt item {index} has no prompt.")
        parsed.append((relative_path.strip(), prompt.strip()))
    return parsed


def safe_output_path(root: Path, relative_path: str) -> Path:
    normalized = relative_path.replace("\\", "/").strip()
    pure = PurePosixPath(normalized)
    if not normalized or pure.is_absolute() or ".." in pure.parts or ":" in normalized or "\x00" in normalized:
        raise ValueError(f"Unsafe output path: {relative_path!r}")
    candidate = root.joinpath(*pure.parts).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Output path escapes the selected root: {relative_path!r}")
    return candidate
