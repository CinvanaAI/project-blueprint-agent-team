from __future__ import annotations

import argparse
from pathlib import Path

from .core import BlueprintTeam
from .demo import deterministic_runner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the offline project-blueprint agent-team demo.")
    parser.add_argument("prompt", help="Project request to turn into a reviewed blueprint")
    parser.add_argument("--output", type=Path, default=Path("blueprint-output"))
    args = parser.parse_args()

    result = BlueprintTeam(deterministic_runner).run_and_write(args.prompt, args.output)
    print(f"Wrote {len(result.outputs)} review artifacts plus safe project prompt files to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
