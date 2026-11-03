# 09. Markdown Article Records ("define the article in MD files")

Every article the user keeps becomes one Markdown file with YAML front matter and fixed sections. This turns a messy pile of PDFs and links into a structured, searchable, version-controllable knowledge base that works in Obsidian, VS Code, Zotero notes, Notion import, GitHub, or as context for any LLM.

## Contents
1. Folder layout
2. File naming
3. Front matter schema
4. Body sections
5. Filling rules
6. Index and evidence table
7. Linking and tags
8. Batch generation
9. Example record

## 1. Folder layout

```
literature/
├── INDEX.md                  # table of all records (auto or manual)
├── search-log.md             # every search run (see templates/search-log.md)
├── evidence-table.md         # comparative table across studies
├── records/
│   ├── Smith2021_PMID12345678.md
│   ├── Lee2019_doi-10.1016-j.cell.2019.01.001.md
│   └── ...
├── excluded/                 # optional: excluded records with reasons
└── exports/                  # raw database exports (.nbib, .ris, .csv) untouched
```

## 2. File naming

`FirstAuthorSurname + Year + _ + identifier`
- Prefer `PMID<number>`; else `doi-<sanitized-doi>` (replace `/` with `-`, drop unsafe characters); else a short title slug.
- ASCII only; no spaces; keep under 100 characters.
- Same author and year, different paper: identifier makes it unique.

## 3. Front matter schema

```yaml
---
type: article
title: "Full title exactly as published"
authors: ["Smith J", "Lee K", "Garcia M"]
year: 2021
journal: "Diabetes Care"
volume: "44"
issue: "5"
pages: "1123-1131"
doi: "10.2337/dc20-1234"
pmid: "12345678"
pmcid: "PMC1234567"
url: "https://doi.org/10.2337/dc20-1234"
study_design: "RCT"            # RCT | cohort | case-control | cross-sectional | SR | MA | scoping | qualitative | case-report | preclinical | narrative-review | other
status: published              # published | preprint | conference-abstract | retracted
open_access: true
sample_size: 120
population: "Adults with T2DM, mean age 58"
intervention: "Supervised aerobic exercise, 12 weeks"
comparator: "Usual care"
primary_outcome: "HbA1c change"
risk_of_bias: "some concerns"  # low | some concerns | high | not-assessed
verification: VERIFIED-DB      # see 08
retraction_checked: true
relevance: high                # high | medium | low
decision: include              # include | exclude | maybe
exclusion_reason: ""
source_database: ["PubMed"]
date_retrieved: "2026-11-03"
search_ref: "S1"
tags: [t2dm, exercise, hba1c]
---
```
Leave unknown values as empty strings or `null`; do not guess.

## 4. Body sections (use these exact headings)

```markdown
# Title (short citation: Smith 2021)

## Citation
Vancouver or APA reference string.

## Summary (2 to 4 sentences, own words)
What was done, in whom, and what was found.

## Key findings
- Primary outcome: effect size (95% CI), p, direction
- Secondary outcomes
- Harms/adverse events

## Methods snapshot
Design, setting, sampling, duration, measures, analysis.

## Strengths
## Limitations
(authors' stated and your own)

## Risk of bias notes
Domain-level notes (tool used).

## Relevance to the question
How it answers or fails to answer the user's question.

## Quotes (optional, short, with page)
> "..." (p. X)

## Notes and follow-ups
Related papers to chase (cited/citing), open questions.
```

## 5. Filling rules

- **Source fidelity**: every number must be traceable to the abstract or full text you actually saw. If only the abstract was available, set `evidence_level: abstract-only` and say so in Summary.
- **Own words**: summaries paraphrase; quote sparingly.
- **No guesses**: unknown sample size is `null`, not an estimate.
- **Dates**: `date_retrieved` is the day the record was verified.
- **Consistent controlled lists** for `study_design`, `status`, `risk_of_bias`, `decision` so files can be filtered (Obsidian Dataview, grep, pandas).
- **One paper per file**; do not merge a paper and its erratum (link them in Notes).

## 6. Index and evidence table

`INDEX.md` columns: `File | Authors Year | Design | n | Key result | Decision | Verification`.
`evidence-table.md`: one row per included study (see `templates/evidence-table.md`).

Generate both from front matter with `scripts/pubmed_search.py` (which writes `INDEX.md`) or a short script over `records/*.md`.

## 7. Linking and tags

- Link related records with wiki links: `[[Lee2019_PMID23456789]]`.
- Add `cites:` / `cited_by:` arrays in front matter for networks if wanted.
- Tags: topic, population, method; keep a small controlled vocabulary.

## 8. Batch generation

`python scripts/pubmed_search.py --query '...' --max 50 --out literature/` fetches PubMed XML and writes one record per article with metadata filled (title, authors, journal, year, volume, pages, DOI, PMID, PMCID, abstract, publication types, MeSH terms). **The script cannot judge design, risk of bias, or relevance**; fields such as `risk_of_bias`, `relevance`, and `decision` are left for the reviewer (Claude or human) after reading.

## 9. Example record

```markdown
---
type: article
title: "Effects of aerobic training on glycemic control in type 2 diabetes: a randomized trial"
authors: ["Smith J", "Lee K"]
year: 2021
journal: "Example Journal of Diabetes"
volume: "44"
issue: "5"
pages: "1123-1131"
doi: "10.0000/example.2021.0001"
pmid: "00000000"
study_design: RCT
status: published
sample_size: 120
risk_of_bias: some concerns
verification: EXAMPLE-ONLY-NOT-A-REAL-PAPER
decision: include
tags: [t2dm, exercise]
---
# Smith 2021

## Summary
(Illustrative placeholder. Real records contain only information from a retrieved paper.)
```
(The example above is a deliberately fake placeholder to show structure; never publish such an entry as a real reference.)
