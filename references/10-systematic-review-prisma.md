# 10. Systematic and Scoping Reviews (PRISMA)

How to run a defensible review. Claude can do large parts (strategy, translation, screening support, extraction drafts), but certain steps require human oversight (dual screening, risk-of-bias judgment, protocol registration).

## Contents
1. Review types
2. Step-by-step workflow
3. Protocol and registration
4. Search methods (PRISMA-S)
5. Deduplication
6. Screening
7. Data extraction
8. Synthesis
9. PRISMA 2020 flow diagram
10. Updating a review
11. Rapid reviews and shortcuts

## 1. Review types

| Type | Purpose | Key guidance |
|---|---|---|
| Systematic review (SR) | Answer a focused question with explicit, reproducible methods | PRISMA 2020, Cochrane Handbook |
| Meta-analysis | Statistical pooling within an SR | PRISMA, RevMan/R metafor |
| Scoping review | Map evidence, concepts, gaps | PRISMA-ScR, JBI (PCC) |
| Rapid review | Time-limited SR with shortcuts | Cochrane Rapid Reviews guidance |
| Umbrella review | Review of systematic reviews | |
| Realist/critical interpretive | Explain how and why | RAMESES |
| Living review | Continually updated | |
| Narrative review | Expert overview, no formal methods | SANRA for quality |

## 2. Step-by-step workflow

1. Define question (PICO/PCC) → `01`
2. Write protocol; register (PROSPERO for health SRs; OSF for others)
3. Design search with an information specialist if possible
4. Search ≥3 databases + trial registries + citation chasing
5. Export, deduplicate
6. Screen (title/abstract → full text), dual if possible
7. Extract data (piloted form)
8. Appraise risk of bias → `07`
9. Synthesize (meta-analysis or narrative/SWiM)
10. Assess certainty (GRADE)
11. Report with PRISMA 2020 checklist and flow diagram

## 3. Protocol and registration

Protocol contents: rationale, objectives, eligibility (PICOS), information sources, search strategy (at least one fully drafted), study selection process, data items, risk-of-bias tool, synthesis plan, subgroup/sensitivity analyses, certainty assessment. Register before screening begins. Amendments are logged with reasons.

## 4. Search methods (PRISMA-S items)

Report for every source: platform/interface, date of search, **full strategy** (copy-paste ready), limits/filters with justification, hit counts, validation (known-item test), peer review of the search (PRESS checklist), and supplementary methods (citation chasing, contacting authors, handsearching, registries, gray literature).

Minimum database sets (health): MEDLINE (PubMed or Ovid), Embase, Cochrane CENTRAL, plus topic databases (CINAHL, PsycINFO), plus Scopus or WoS, plus Google Scholar (first 200 to 300). Registries: ClinicalTrials.gov, ICTRP.

**PRESS peer review of search strategies** checks: translation of the question, Boolean and proximity operators, subject headings, text-word searching, spelling/syntax/line numbers, limits and filters.

## 5. Deduplication

1. Export every database to RIS/CSV, keep raw files untouched.
2. Import into Zotero/EndNote/Rayyan/Covidence; run automated dedup.
3. Manual pass on near-matches: same DOI; same title + year + first author; same pages.
4. Keep the version with the most complete metadata; count and report duplicates removed.
5. Beware: conference abstract and full paper, preprint and publication, and multiple reports of one trial are **not** simple duplicates; link them to a single **study** (study vs report distinction).

## 6. Screening

- Pilot on ~50 records with all reviewers to calibrate criteria.
- Tools: Rayyan, Covidence, ASReview (active learning), EPPI-Reviewer, DistillerSR, Abstrackr.
- Track counts at each stage for PRISMA: records identified, duplicates removed, screened, excluded, full text sought, not retrieved, assessed, excluded with reasons, included.
- When Claude screens: provide a decision, a one-line reason, and a confidence; send all "maybe" and low-confidence items to a human.

## 7. Data extraction

Use a standardized form (spreadsheet or `templates/evidence-table.md`):
- Study ID, design, country, setting, funding
- Population (n, age, sex, condition severity)
- Intervention/exposure (dose, duration, delivery) and comparator
- Outcomes (definition, time points, measure)
- Results (means/SDs, events/totals, effect measure, 95% CI)
- Risk-of-bias judgments
- Notes (missing data, author contacts)
Double extraction for key outcomes; verify numbers against the source table. Never infer numbers that are not reported; contact authors or mark as missing.

## 8. Synthesis

- **Meta-analysis** when studies are sufficiently similar: random-effects model by default; report I² and prediction intervals; sensitivity analyses (leave-one-out, low-risk-of-bias only); publication bias (funnel plot, Egger's test if ≥10 studies).
- **Narrative synthesis / SWiM** (Synthesis Without Meta-analysis) when pooling is inappropriate: group by design, population, outcome; use vote-counting by direction of effect only with caution; present effect-direction plots.
- **Qualitative**: thematic synthesis, meta-ethnography, framework synthesis.
- Report heterogeneity sources and certainty (GRADE), not just p-values.

## 9. PRISMA 2020 flow diagram (text template)

```
IDENTIFICATION
  Records from databases (n = ..)  [PubMed n=, Embase n=, Scopus n=, ...]
  Records from registers (n = ..)
  Other methods: citation searching (n = ..)
  Duplicates removed (n = ..)
SCREENING
  Records screened (n = ..)  → excluded (n = ..)
  Reports sought for retrieval (n = ..) → not retrieved (n = ..)
  Reports assessed for eligibility (n = ..)
     → excluded with reasons (n = ..): wrong population (n), wrong design (n), ...
INCLUDED
  Studies included in review (n = ..)  (reports n = ..)
```
Use `templates/prisma-flow.md`. For a graphic, the PRISMA2020 Shiny app generates one.

## 10. Updating a review

Re-run saved strategies with a date filter (`[edat]` in PubMed) from the last search date; screen only new records; note the date and counts in the log. Living reviews set a schedule (monthly or quarterly).

## 11. Rapid reviews and shortcuts

If time is short, acceptable shortcuts must be stated as limitations: single screener with verification sample, one or two databases, recent date limits, English only, no gray literature. Never present a rapid process as a full systematic review.
