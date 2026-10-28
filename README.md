# Formula 1 Race Intelligence

**Revised version prepared by Viraj Patidar.** Original project attribution to Ishita Singh is retained for transparency.

SkillWallet Tableau capstone, using the supplied educational dataset for 2010-2026.

## Current state

Prepared data, analysis, a nine-page report, source-quality audit, chart figures, demonstration notes and Flask embedding code are available. Three automated checks pass. Native Tableau authoring and publication require the user's Tableau Public sign-in. There is no completed `.twb`/`.twbx`, published demo, recorded video or GitHub repository yet. The SkillWallet completion indicators have not been changed.

## Reproduce

Python 3.12 or newer:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python prepare_data.py
.venv\Scripts\python build_report.py
.venv\Scripts\python -m unittest test_project.py
.venv\Scripts\python app.py
```

Open http://127.0.0.1:5050. The local `.packages` directory contains Flask and plotting dependencies for the current workspace; it is excluded from source control and the delivery ZIP.

Before starting Flask with the final published workbook, set `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL` to the real HTTPS Tableau Public `/views/Workbook/View` URLs. No invented or third-party output is preconfigured.

## Contents

- `data/F1 Racing Project Dataset.xlsx`: unchanged source.
- `data/prepared/`: five prepared source CSVs and reconciled analysis summaries.
- `data/audit.json`: counts, source URL and quality findings.
- `output/pdf/F1_Race_Intelligence_Report.pdf`: analysis and honest implementation status.
- `output/figures/`: six analytical figures, generated from source data using Python.
- `prepare_data.py`: reproducible validation and preparation.
- `app.py`, `templates/index.html`: Flask Tableau integration.
- `test_project.py`: metric reconciliation and web configuration checks.
- `TABLEAU_BUILD.md`: native workbook build specification.
- `DEMO_SCRIPT.md`: planned 5-7 minute screen-share narration.

## Definitions and limits

6,464 records are race entries, not 6,464 races. There are 334 distinct race IDs, 17 seasons, 10 teams, 19 driver names, 24 active circuits and 29 catalog circuits. There are 396 DNFs and 940 podium entries. Total race points are 31,906. Driver-season totals reconcile to the 311 annual standings rows.

The supplied data is not reliable historical F1 evidence: contemporary drivers appear in 2010, qualifying includes placeholders, and Carlos Sainz appears twice per race for different teams. We preserve rather than guess corrections. Host country is not driver nationality. Starting tyre compound is not full-race compound usage. The last race date supplied is 2026-08-02.

## Remaining acceptance checks

1. Sign in to Tableau Public and author native worksheets, dashboard and nine-scene story.
2. Validate all-data and filtered totals, Top N, device layouts and real Tableau rendering times.
3. Publish under the student's account and verify view access and embedding.
4. Record the 5-7 minute screen-share with the completed Tableau views.
5. Publish project files to the intended GitHub repository and add actual links to SkillWallet.
6. Update the report's implementation status with verified screenshots and measurements, then mark completed tasks in SkillWallet.

No report template was attached in the project documentation task when inspected; the report follows the listed step-by-step requirements.
