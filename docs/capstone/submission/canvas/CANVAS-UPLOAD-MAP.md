# Canvas Upload Map

Use this directory for the final LaunchCode Canvas upload package.

## Required Links

GitHub repository link:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering`

Current access status: `PUBLIC`. On September 1, 2026, the anonymous branch page and raw grader quickstart both returned HTTP `200`.

Verified implementation commit: `a7813c453b369dcaf0dd2fe27196d730c1889c67`

Verified governance CI: https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/33517133584

Walkthrough video:

`https://youtu.be/srFGYvnEd7c`

Current compliance status: Canvas reports approximately 13 minutes against a 10-minute cap. Keep this as the historical recording reference until Muhammad and Codex complete the video step together.

## Required PDF Uploads

Architecture write-up:

`01_AURA_Forge_Architecture_Writeup.pdf`

Impact report:

`02_AURA_Forge_Impact_and_Tool_Evolution.pdf`

Stakeholder one-pager:

`03_AURA_Forge_Stakeholder_One_Pager.pdf`

Ops-ready runbook:

`04_AURA_Forge_Ops_Runbook.pdf`

ADR package:

`05_AURA_Forge_ADR_Package.pdf`

Rubric self-check:

`06_AURA_Forge_Rubric_Self_Check.pdf`

Sanitization note:

`07_AURA_Forge_Sanitization_Note.pdf`

Final presentation:

`00_AURA_Forge_Final_Presentation.pdf`

## Upload Order

1. Paste the verified public GitHub repository link requested by Learn at LaunchCode.
2. If Canvas requires the walkthrough now, use the current historical link but disclose that the video-length correction remains pending; do not call it compliant.
3. Upload `01_AURA_Forge_Architecture_Writeup.pdf`.
4. Upload `02_AURA_Forge_Impact_and_Tool_Evolution.pdf`.
5. Upload `03_AURA_Forge_Stakeholder_One_Pager.pdf`.
6. Upload `04_AURA_Forge_Ops_Runbook.pdf`.
7. Upload `05_AURA_Forge_ADR_Package.pdf`.
8. Upload `06_AURA_Forge_Rubric_Self_Check.pdf`.
9. Upload `07_AURA_Forge_Sanitization_Note.pdf`.
10. Upload or attach `00_AURA_Forge_Final_Presentation.pdf` where Canvas asks for the completed slide deck.

## Rebuild Sources

- PDF build dependency: `requirements.txt` in this directory.
- PDFs `01` through `05`: `scripts/build-canvas-submission-pdfs.py`.
- PDF `06`: `scripts/build-canvas-rubric-self-check.py` and `06_AURA_Forge_Rubric_Self_Check.md`.
- The video and presentation PDF were not rebuilt during the non-video revision.
