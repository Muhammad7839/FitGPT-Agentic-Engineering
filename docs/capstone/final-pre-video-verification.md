# Final Pre-Video Verification

This is the final local verification barrier before Muhammad records. It records only safe, deterministic evidence.

## Passed local tests

- Core deterministic pytest suite: `82 passed`.
- Governed Docker policy/MCP/coursetools suite: `18 passed`.
- Pipeline integrity checker: `PASS`.
- Change Passport generation: passed.
- Demo helper: passed.
- JSON parse: `224` files valid.
- GitHub workflow YAML parse: `2` files valid.
- PPTX structure: `10` slides and `10` notes.
- PDF: `10` pages.
- Secret scan: `0` findings.
- Forbidden-file scan: `0` findings.
- `git diff --check`: passed.
- Holdout checksum: `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32`.

## Current pre-video score

`49 / 52`

This score is intentionally conservative. The unavailable points are documented in `docs/capstone/final-rubric-audit.md` and `docs/capstone/pre-video-rubric-gap-table.md`.

## Submission bundle

The repository does not commit a duplicate zip of the final submission files. A local ignored zip may be created at:

`.eval-artifacts/capstone/submission/AURA_Forge_Submission_Bundle.zip`

During this pass, a local ignored zip was created at that path. Size: about `1.48 MB`. Contents: final PPTX, PDF, speaker notes, teleprompter, final video script, recording cheat sheet, video evidence staging guide, submission links, final human checklist, submission README, and slide contact sheet.

Refresh it after any final video URL is known if LaunchCode requires one file upload.
