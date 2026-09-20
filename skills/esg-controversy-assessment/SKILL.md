---
name: esg-controversy-assessment
description: Use this skill whenever you're given a company name plus a news article, report excerpt, or other text and asked to assess it for an ESG (Environmental, Social, Governance) controversy — e.g. "does this describe an ESG controversy for {company}?", "classify this incident", "score this ESG issue". Produces a structured assessment (category, pillar/sub-pillar, nature of harm, scale of impact, company role, case status, severity, and a 0-9 score with a flag color).
allowed-tools: Read, Grep, Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/score.py *), Bash(python ${CLAUDE_SKILL_DIR}/scripts/score.py *)
---

# ESG Controversy Assessment

Assess whether a piece of text describes an ESG controversy for a given company, classify it, and score its severity. Follow these steps in order; do not skip steps even if the answer seems obvious.

## Step 1 — Detect controversy

Given `(company, text)`, decide: does the text describe an ESG controversy involving `company`? See the definition in [references/taxonomy.md](references/taxonomy.md#1-controversy-detection).

Answer **Positive** or **Negative**. If Negative, stop here and report: "No ESG controversy detected for {company} in this text."

## Step 2 — Classify primary category

If Positive, classify the primary category as **Environmental**, **Social**, or **Governance** — see [references/taxonomy.md](references/taxonomy.md#2-primary-esg-category).

## Step 3 — Classify subcategory / pillar

Based on the Step 2 category, pick the matching subcategory list in [references/taxonomy.md](references/taxonomy.md):

- **Environmental** → one Environmental subcategory (§3).
- **Governance** → one Governance subcategory (§4).
- **Social** → a `Pillar : Sub-Pillar` pair (§5).

## Step 4 — Nature of Harm and Scale of Impact

Using the pillar-specific criteria in [references/harm-impact-role-status.md](references/harm-impact-role-status.md):

1. Assess **Nature of Harm**: Very Serious / Serious / Medium / Minimal.
2. Assess **Scale of Impact**: Extremely Widespread / Extensive / Limited / Low.

Both rubrics differ by pillar (Environmental / Governance / Social) — use the section matching the Step 2 category.

## Step 5 — Company Role and Case Status

Using [references/harm-impact-role-status.md](references/harm-impact-role-status.md):

1. Assess **Company Role**: Direct or Indirect.
2. Assess **Case Status**: Active (Ongoing / Partially Concluded / Concluded) or Inactive (Archived / Historical Concern).

## Step 6 — Compute severity and score

This step is a fixed lookup-table calculation — do not compute it by reasoning, run the bundled script so the result is exact:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py "<Nature of Harm>" "<Scale of Impact>" "<Company Role>" "<Case Status Sub-Category>"
```

If `python3` isn't a recognized command on this system (e.g. some Windows setups), use `python` instead of `python3`.

Notes:
- `<Case Status Sub-Category>` must be one of `Ongoing`, `Partially Concluded`, `Concluded` — the scoring matrix only covers Active cases. If the case is Inactive (Archived / Historical Concern), skip this step and note that no numeric score applies.
- The script prints `Severity`, `Score` (0-9, lower = more severe), and `Flag` (Red / Orange / Yellow / Green).

## Step 7 — Report the assessment

Return a structured result, e.g.:

```json
{
  "Category": "Environmental",
  "Pillar": "Toxic Emissions & Waste",
  "Nature of harm": {"Nature of harm": "Minimal", "Details": "..."},
  "Scale of impact": {"Scale of impact": "Low", "Details": "..."},
  "Role of the company": {"Company role": "Direct", "Details": "..."},
  "status": {"Status A": "Active", "Status B": "Ongoing", "Details": "..."},
  "Severity": "Minor",
  "Score": 6,
  "Flag": "Green Flag"
}
```

For Social controversies, include both `"Pillar"` and `"Sub-Pillar"` keys.

See [examples/coca-cola-leak.md](../../examples/coca-cola-leak.md) for a fully worked example.
