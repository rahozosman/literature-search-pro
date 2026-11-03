# 11. Output Templates

Pick the shape that matches the request. Keep chat replies short; place long deliverables in files.

## Contents
1. Quick answer
2. Search strategy only (Mode B/C)
3. Reading list
4. Literature review summary
5. Verification report
6. Known-item lookup
7. Style rules

## 1. Quick answer (Workflow 1)

```
**Bottom line:** one or two sentences, with certainty level.

**Evidence** (verified items only):
- Author Year, design, n, key result. [PMID/DOI]
- ...

**Gaps/caveats:** ...
**Searched:** PubMed, Europe PMC on 2026-11-03 | query in search-log.md
```

## 2. Search strategy only (Mode B/C)

```
Question and concepts (table)
Per database: ready-to-paste query in a code block + where to paste it + filters to tick + export instructions
Expected size and how to tune (too many → add concept; too few → remove/add synonyms)
Validation: 3 seed papers should appear
```
Never include a "results" table in this mode. State: "I couldn't run these searches here; results will come from your run."

## 3. Reading list

Group by purpose, not alphabetically:
1. **Start here** (best recent review/meta-analysis)
2. **Key primary studies** (landmark RCTs/cohorts)
3. **Methods papers**
4. **Contrasting/critical views**
5. **Newest preprints** (flagged)

Each item: citation (Vancouver), one-line why-read, design, access (OA link or "paywalled"), verification label.

## 4. Literature review summary

```
# Title
## Question and scope
## Methods (databases, dates, query pointers, criteria)
## Results
  - Search yield (n identified → n included)
  - Study characteristics (table)
  - Findings by theme/outcome
  - Quality of evidence
## Discussion (agreement, conflicts, gaps)
## Limitations of this search
## References (verified, numbered)
```
Length: 600 to 1500 words unless the user asks for more. Use tables for characteristics; keep prose for synthesis.

## 5. Verification report

```
| # | Reference as given | Status | Found record | Issue/correction |
```
Statuses from `08`. Summarize: `n verified, n partial, n not found, n retracted`. Provide corrected references separately.

## 6. Known-item lookup

```
Match: [full citation] (PMID, DOI, link)
Confidence: exact / probable / ambiguous
Differences from the query: ...
Access: OA link or routes
```

## 7. Style rules

- Citation style: ask or infer (Vancouver for medicine, APA for social sciences, IEEE for engineering). Default Vancouver.
- Always include a persistent identifier (DOI or PMID) when verified.
- Use `et al.` after 6 authors (Vancouver) or per style.
- Present effect sizes with CIs; do not round away uncertainty.
- Do not use hype words ("proves", "breakthrough"); calibrate.
- Separate **what the studies found** from **what you infer**.
- End with 1 to 3 concrete next steps (e.g., "run the Embase query", "I can draft the PRISMA flow").
