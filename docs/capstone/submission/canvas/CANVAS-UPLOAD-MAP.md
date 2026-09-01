# Canvas Upload Map

Use this directory for the final LaunchCode Canvas upload package.

## Required Links

GitHub repository link:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering`

Current access status: `PRIVATE`. Do not resubmit this link until a logged-out grader can open the exact `capstone/aura-forge` branch.

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

1. Confirm the current revision is committed, pushed, and green in fresh GitHub CI.
2. Confirm the repository and exact branch open in a logged-out browser.
3. Complete and verify a walkthrough at or below 10 minutes.
4. Paste the verified GitHub repository link.
5. Paste the compliant walkthrough video link.
6. Upload `01_AURA_Forge_Architecture_Writeup.pdf`.
7. Upload `02_AURA_Forge_Impact_and_Tool_Evolution.pdf`.
8. Upload `03_AURA_Forge_Stakeholder_One_Pager.pdf`.
9. Upload `04_AURA_Forge_Ops_Runbook.pdf`.
10. Upload `05_AURA_Forge_ADR_Package.pdf`.
11. Upload `06_AURA_Forge_Rubric_Self_Check.pdf`.
12. Upload `07_AURA_Forge_Sanitization_Note.pdf`.
13. Upload or attach `00_AURA_Forge_Final_Presentation.pdf` where Canvas asks for the completed slide deck.

## Rebuild Sources

- PDF build dependency: `requirements.txt` in this directory.
- PDFs `01` through `05`: `scripts/build-canvas-submission-pdfs.py`.
- PDF `06`: `scripts/build-canvas-rubric-self-check.py` and `06_AURA_Forge_Rubric_Self_Check.md`.
- The video and presentation PDF were not rebuilt during the non-video revision.
