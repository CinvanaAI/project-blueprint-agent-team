# Project Blueprint Agent Team: mechanism

[BlueprintTeam](../blueprint_team/core.py) orders prompt interpretation, architecture, dependency mapping, per-file prompt design, validation and specification. A runner callable receives each role, its instruction, the request and previous output context. [deterministic_runner](../blueprint_team/demo.py) supplies a fixed synthetic example. The writer checks relative paths to prevent accidental escape from the output directory.

## Limits that matter

No experiment here establishes that six roles improve model quality. JSON/path failures may leave earlier artifacts, so use a fresh output directory. The injected runner is the extension point; a live model provider is not included.

## Demonstration contract

Input: A project request passed through six named roles.

Expected observation: Six design artifacts and per-file implementation prompts.

The bundled example uses synthetic material. Its observed output establishes that bounded path, not every possible integration.
