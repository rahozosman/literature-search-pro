# Worked Example: "Does exercise lower HbA1c in type 2 diabetes?"

(Illustrates the process. No real paper is cited; run the searches to get real results.)

## 1. Mode and framing
Mode: live (web + code). PICO: P adults with T2DM; I structured exercise; C usual care; O HbA1c. Design: RCTs and their systematic reviews.

## 2. Concept blocks
| Block | MeSH | Free text |
|---|---|---|
| Diabetes | Diabetes Mellitus, Type 2 | type 2 diabet*, T2DM, NIDDM |
| Exercise | Exercise | exercis*, physical activity, training |
| Outcome | Glycated Hemoglobin | HbA1c, glycated hemoglobin |

## 3. Generate queries
```
python scripts/build_query.py \
  --block "dx=type 2 diabet*;T2DM;NIDDM" --block "tx=exercis*;physical activity;training" \
  --block "out=HbA1c;glycated hemoglobin" \
  --mesh "dx=Diabetes Mellitus, Type 2" --mesh "tx=Exercise" --mesh "out=Glycated Hemoglobin" \
  --emtree "dx=non insulin dependent diabetes mellitus" --years 2015-2025 --lang english --design rct
```
Paste the PubMed version into PubMed; check "Search Details".

## 4. Run and save
```
python scripts/pubmed_search.py --query '<paste PubMed query>' --max 100 --out literature --email you@example.com
```
Creates `literature/records/*.md`, `INDEX.md`, `results.csv`, `search-log.md`.

## 5. Validate
Do 3 known trials appear? If one is missing, read its title/abstract, find the unmatched term, add it, rerun, log the change (see `references/12`).

## 6. Screen and appraise
For each record: confirm RCT in Methods; extract n, intervention, duration, HbA1c change with CI; judge RoB 2; set `decision` and `relevance` in the front matter.

## 7. Verify before reporting
```
python scripts/verify_citation.py --pmid <PMID> --oa
```
Check for retraction flags. Mark verification status.

## 8. Deliver
Short answer with certainty (e.g., "moderate certainty; heterogeneity high"), a results table, the final queries per database (Embase, Scopus, Cochrane versions from `build_query.py`), limitations, next steps (run Embase/Cochrane; PRISMA flow).
