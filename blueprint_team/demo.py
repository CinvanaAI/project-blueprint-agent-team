from __future__ import annotations

import json
from typing import Mapping


def deterministic_runner(role: str, instruction: str, context: Mapping[str, str]) -> str:
    project = context["original_prompt"]
    if role == "prompt_interpreter":
        return f"# Clarified project\n\nBuild: {project}\n\nConstraint: keep the example offline and testable."
    if role == "system_architect":
        return "# Folder map\n\n- `app/core.py`: domain behavior\n- `tests/test_core.py`: offline verification"
    if role == "dependency_mapper":
        return "# Dependencies\n\n`tests/test_core.py` imports `app/core.py`; the domain has no external service dependency."
    if role == "file_prompt_designer":
        return json.dumps(
            {
                "files": [
                    {"path": "app/core.py", "prompt": "Implement the clarified domain behavior."},
                    {"path": "tests/test_core.py", "prompt": "Test the public domain behavior offline."},
                ]
            },
            indent=2,
        )
    if role == "validator":
        return "# Validation\n\nThe two files agree on names, dependency direction, and offline scope."
    if role == "spec_writer":
        return "# Handoff\n\nThe project blueprint is internally consistent and ready for implementation review."
    raise ValueError(f"Unknown demo role: {role}")
