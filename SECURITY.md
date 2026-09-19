# Security posture

Model output is untrusted input. The file-prompt stage must return strict JSON, and every path is normalized, checked for absolute/drive/parent traversal, resolved, and required to remain beneath the chosen root.

This protects the artifact writer from direct path escape. It does not make generated implementation prompts or any later generated code trustworthy. Review generated artifacts before another system executes or installs them.

The bundled demo is offline and deterministic. The repository contains no credentials or model-provider configuration.
