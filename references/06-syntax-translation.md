# 06. Syntax Translation Cheat Sheet

Build the strategy once as concept blocks, then translate. `scripts/build_query.py` automates the table below.

## Contents
1. Master comparison table
2. Translation recipe
3. Worked translation (one strategy, nine platforms)
4. Common translation errors

## 1. Master comparison table

| Feature | PubMed | Scopus | Web of Science | Embase (embase.com) | Ovid MEDLINE | Cochrane | EBSCO (CINAHL) | ScienceDirect | Google Scholar |
|---|---|---|---|---|---|---|---|---|---|
| Title/abstract | `term[tiab]` | `TITLE-ABS-KEY(term)` | `TS=(term)` | `term:ti,ab,kw` | `term.ti,ab.` | `term:ti,ab,kw` | `TI term OR AB term` | "Title, abstract, keywords" field | `term` (all text) |
| Controlled vocab | `term[mh]` | n/a (index keywords via `KEY`) | n/a (Keywords Plus in TS) | `'term'/exp` | `exp term/` | `[mh term]` | `MH "term+"` | n/a | n/a |
| Phrase | `"a b"[tiab]` | `"a b"` or `{a b}` | `"a b"` | `'a b'` | `"a b".ti,ab.` | `"a b"` | `"a b"` | `"a b"` | `"a b"` |
| Truncation | `abc*` (≥4 chars) | `abc*` | `abc*` | `abc*` | `abc*` or `abc$` | `abc*` | `abc*` | `abc*` | not supported |
| Single-char wildcard | not supported | `?` | `?` and `$` | `?` | `?` / `#` | `?` | `?` / `#` | `?` | not supported |
| Proximity | `"a b"[tiab:~N]` | `a W/N b`, `a PRE/N b` | `a NEAR/N b` | `a NEAR/N b`, `NEXT/N` | `a adjN b` | `a NEAR/N b` | `a N5 b`, `a W5 b` | not supported | not supported |
| Boolean | `AND OR NOT` | `AND OR AND NOT` | `AND OR NOT` | `AND OR NOT` | `and or not` | `AND OR NOT` | `AND OR NOT` | `AND OR NOT` | space, `OR`, `-` |
| Year | `2020:2024[dp]` | `PUBYEAR > 2019 AND PUBYEAR < 2025` | `PY=(2020-2024)` | `[2020-2024]/py` | `limit to yr="2020-2024"` | date filter | date limiter | Years filter | custom range |
| Doc type | `review[pt]` | `DOCTYPE(re)` | `DT=(Review)` | `[review]/it` | `limit to review` | filter | PT filter | Article type filter | "Review articles" |
| Language | `english[la]` | `LANGUAGE(english)` | `LA=English` | `[english]/lim` | `limit to english` | | LA | | |

## 2. Translation recipe

1. **Write concept blocks** (plain list):
   - Block A: `{type 2 diabetes, T2DM, NIDDM, adult-onset diabetes}`
   - Block B: `{exercise, physical activity, training}`
   - Block C: `{HbA1c, glycated hemoglobin}`
2. Map each block's **controlled terms** per database (MeSH in PubMed/Ovid/Cochrane, Emtree in Embase, CINAHL Headings in EBSCO). Controlled vocab names differ: "Diabetes Mellitus, Type 2" (MeSH) vs "non insulin dependent diabetes mellitus" (Emtree).
3. Convert **free-text** terms into the field syntax of each platform.
4. Apply **limits** (dates, language, design) with each platform's syntax.
5. **Run each translation and compare**: counts should be in a plausible ratio (Embase generally returns more than PubMed; Scopus more than WoS). Test with known papers.
6. Log each final string.

## 3. Worked translation

Concepts: (A) type 2 diabetes, (B) exercise, (C) HbA1c. Years 2015-2025, English.

**PubMed**
```
("Diabetes Mellitus, Type 2"[mh] OR "type 2 diabet*"[tiab] OR T2DM[tiab] OR NIDDM[tiab])
AND ("Exercise"[mh] OR exercis*[tiab] OR "physical activity"[tiab])
AND ("Glycated Hemoglobin"[mh] OR HbA1c[tiab] OR "glycated hemoglobin"[tiab])
AND 2015:2025[dp] AND english[la]
```
**Scopus**
```
TITLE-ABS-KEY(("type 2 diabet*" OR T2DM OR NIDDM) AND (exercis* OR "physical activity") AND (HbA1c OR "glycated hemoglobin"))
AND PUBYEAR > 2014 AND PUBYEAR < 2026 AND LANGUAGE(english)
```
**Web of Science**
```
TS=(("type 2 diabet*" OR T2DM OR NIDDM) AND (exercis* OR "physical activity") AND (HbA1c OR "glycated hemoglobin"))
AND PY=(2015-2025) AND LA=English
```
**Embase**
```
('non insulin dependent diabetes mellitus'/exp OR 'type 2 diabet*':ti,ab,kw OR t2dm:ti,ab,kw OR niddm:ti,ab,kw)
AND ('exercise'/exp OR exercis*:ti,ab,kw OR 'physical activity':ti,ab,kw)
AND ('glycosylated hemoglobin'/exp OR hba1c:ti,ab,kw OR 'glycated hemoglobin':ti,ab,kw)
AND [2015-2025]/py AND [english]/lim
```
**Ovid MEDLINE** (line by line)
```
1. exp Diabetes Mellitus, Type 2/
2. (type 2 diabet* or T2DM or NIDDM).ti,ab,kf.
3. 1 or 2
4. exp Exercise/
5. (exercis* or physical activity).ti,ab,kf.
6. 4 or 5
7. exp Glycated Hemoglobin/
8. (HbA1c or glycated hemoglobin).ti,ab,kf.
9. 7 or 8
10. 3 and 6 and 9
11. limit 10 to (english language and yr="2015-Current")
```
**Cochrane Library**
```
#1 [mh "Diabetes Mellitus, Type 2"] OR "type 2 diabet*":ti,ab,kw OR T2DM:ti,ab,kw
#2 [mh Exercise] OR exercis*:ti,ab,kw OR "physical activity":ti,ab,kw
#3 [mh "Glycated Hemoglobin"] OR HbA1c:ti,ab,kw
#4 #1 AND #2 AND #3 with Publication Year from 2015 to 2025
```
**EBSCO CINAHL**
```
(MH "Diabetes Mellitus, Type 2+" OR TI("type 2 diabet*" OR T2DM) OR AB("type 2 diabet*" OR T2DM))
AND (MH "Exercise+" OR TI(exercis* OR "physical activity") OR AB(exercis* OR "physical activity"))
AND (MH "Glycosylated Hemoglobin" OR TI(HbA1c) OR AB(HbA1c))
```
**ScienceDirect** (field "Title, abstract or author-specified keywords")
```
("type 2 diabet*" OR T2DM) AND (exercis* OR "physical activity") AND (HbA1c OR "glycated hemoglobin")
Years 2015-2025; Article type: Research articles, Review articles
```
**Google Scholar** (simplified; no truncation, no nesting)
```
"type 2 diabetes" exercise HbA1c
"type 2 diabetes" "physical activity" "glycated hemoglobin"
```
Run several variants, set date range 2015 to 2025.

## 4. Common translation errors

- **MeSH to Emtree mismatch**: do not paste MeSH into Embase; look up Emtree terms.
- **Proximity vs phrase**: `"physical activity"` as phrase misses "activity, physical"; use proximity where supported.
- **Truncation limits**: PubMed requires 4 characters; Ovid truncation inside quotes behaves differently.
- **Case and quotes**: Ovid is case-insensitive; Embase single quotes denote phrases; Scopus braces mean exact.
- **Limit syntax drift**: WoS `PY=(2015-2025)` inclusive; Scopus `PUBYEAR > 2014` exclusive.
- **Scopus `AND NOT`**, not `NOT` alone.
- **Date filters on PubMed** are `[dp]` (publication), not `[edat]`.
- **Nested parentheses** not supported in Google Scholar.
- **Keywords Plus** (WoS) adds terms absent from titles/abstracts, so `TS=` has higher recall but lower precision than `TI=`/`AB=`.
