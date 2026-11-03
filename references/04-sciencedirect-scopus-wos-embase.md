# 04. ScienceDirect, Scopus, Web of Science, Embase (and other subscription platforms)

These platforms require institutional access (ScienceDirect and Scopus have partial free tiers). Without live access, build the query and give the user instructions; never claim results.

## Contents
1. ScienceDirect
2. Scopus
3. Web of Science
4. Embase
5. Ovid MEDLINE and PsycINFO
6. EBSCOhost (CINAHL, Academic Search)
7. Choosing between them
8. Export workflows

> Platform interfaces and limits change. When live browsing is available, confirm syntax in the platform's help page before relying on details below.

---

## 1. ScienceDirect (Elsevier)

Full-text platform for Elsevier journals and books (plus some content from other publishers, including Cell Press and The Lancet), about 18 million items. Strength: full-text search in physical sciences, engineering, life sciences, health, social sciences. Not a multidisciplinary index of other publishers.

**Search fields (Advanced Search)**: Search terms (full text and metadata), Title/abstract/author-specified keywords, Author(s), Journal or book title, Year(s), Volume/Issue/Pages, Affiliation, References, ISSN/ISBN, Title.

**Syntax**
- Boolean `AND`, `OR`, `NOT` in uppercase. Parentheses supported (nest as needed). 
- **Limit of about 8 Boolean operators per field**; split long strategies over multiple fields or runs (`Title, abstract, keywords` and `Search terms`).
- Phrases: `"machine learning"`. Exact match with special characters: curly braces `{c-reactive protein}`.
- Wildcards: `*` for zero or more characters (`neuro*`), `?` for a single character (`wom?n`). Truncation works but may not be accepted at the start of a word.
- Proximity is not supported in the basic interface; use phrase and AND.
- Automatic stemming and plural handling in many cases; use quotes to prevent.
- Searching "Title, abstract or author-specified keywords" is the closest analog to `[tiab]`.

**Filters** (left rail): Years, Article type (Review articles, Research articles, Encyclopedia, Book chapters, Case reports, Conference abstracts, Data articles, Editorials, Short communications...), Publication title, Subject areas, Access type (Open access/open archive).

**Practical tips**
- Search `Title, abstract or author-specified keywords` first; full text creates very noisy results.
- Use **Article type = Review articles** to find reviews quickly, and "Research articles" for primary studies.
- Each record shows highlights, graphical abstracts, and **Recommended articles**; reference lists link out.
- Export: select records → **Export** → RIS/BibTeX/text; there are per-export limits (check the interface). Save the search and enable an **alert**.
- Free vs paywalled: open access items carry an icon; otherwise institutional login.
- For reproducibility record: field used, exact string, filters, date, count.

**Query example (ScienceDirect)**
```
Title, abstract, keywords: ("deep learning" OR "convolutional neural network*") AND (defect* OR fault*) AND ("solar cell*" OR photovoltaic*)
Years: 2019-2025   Article type: Research articles
```

---

## 2. Scopus (Elsevier)

Largest curated abstract and citation database across disciplines (journals, conference proceedings, books). Excellent for citation analysis, author profiles (Author ID), affiliations (Affiliation ID), and subject filters.

**Field codes**: `TITLE()`, `ABS()`, `KEY()` (author + index keywords), `TITLE-ABS-KEY()`, `AUTH()`, `AUTHLASTNAME()`, `AFFIL()`, `SRCTITLE()`, `ISSN()`, `DOI()`, `PMID()`, `REF()`, `DOCTYPE()`, `LANGUAGE()`, `PUBYEAR`, `SUBJAREA()`, `FUND-SPONSOR()`, `OPENACCESS(1)`, `ALL()`.

**Operators**: `AND`, `OR`, `AND NOT`; proximity `W/n` (within n, any order), `PRE/n` (in order); wildcards `*` (any number of characters) and `?` (one character). Phrases: `"..."` (loose, ignores punctuation) or `{...}` (exact).

**Example**
```
TITLE-ABS-KEY(("type 2 diabet*" OR T2DM) AND (exercis* OR "physical activity") AND (HbA1c OR "glycated h*moglobin"))
AND PUBYEAR > 2014 AND PUBYEAR < 2026 AND DOCTYPE(ar) AND LANGUAGE(english)
```
**DOCTYPE codes**: `ar` article, `re` review, `cp` conference paper, `ch` book chapter, `bk` book, `ed` editorial, `le` letter, `no` note, `sh` short survey, `er` erratum.

**Features**: Analyze results, Cited by, Documents by author, Author search (h-index), Citation overview, Compare sources (CiteScore), Alerts, Export up to the platform limit (CSV/RIS/BibTeX), "Secondary documents", Scopus AI (if licensed).

---

## 3. Web of Science Core Collection (Clarivate)

Selective, curated; SCIE, SSCI, AHCI, ESCI, plus CPCI, BKCI. Strong for citation searching with "Cited references" and cited reference search (finds papers citing a work even if it is not indexed).

**Field tags**: `TS=` (Topic: title, abstract, author keywords, Keywords Plus), `TI=`, `AB=`, `AK=`, `AU=`, `AI=` (author identifier), `SO=` (source), `PY=`, `DO=`, `PMID=`, `AD=`, `OG=`, `FO=` (funding), `WC=` (WoS category), `DT=` (document type), `LA=`, `CF=`, `ALL=`.

**Operators**: `AND`, `OR`, `NOT`, `NEAR/n` (within n words, any order), `SAME` (same address field/sentence in some fields), wildcards `*`, `?`, `$` (zero or one character, e.g., `colo$r`).

**Example**
```
TS=(("type 2 diabet*" OR T2DM) AND (exercis* OR "physical activity") AND (HbA1c OR "glycated hemoglobin"))
AND PY=(2015-2025) AND DT=(Article OR Review) AND LA=English
```
**Notes**: Keywords Plus broadens `TS=`; use `TI=` plus `AB=` to be stricter. Citation reports, "Create alert", "Cited reference search". Search history lets you combine sets (`#1 AND #2`).

---

## 4. Embase (Elsevier; also via Ovid)

Biomedical and pharmacological database (about 40 million records), strongest for drugs, devices, pharmacovigilance, European coverage, conference abstracts. Uses **Emtree** thesaurus (larger than MeSH). Includes all MEDLINE records indexed plus unique journals.

**embase.com syntax**
- Emtree terms: `'type 2 diabetes mellitus'/exp` (explode), `/de` (as-is, no explosion), `/mj` (major focus).
- Free text in fields: `'type 2 diabet*':ti,ab,kw` (title, abstract, author keywords).
- Proximity: `NEAR/n` (any order), `NEXT/n` (in order).
- Drug subheadings (`:lnk`), publication types `[randomized controlled trial]/lim`, `[embase]/lim` to restrict to records not in MEDLINE, `[medline]/lim`.
- Years: `[2015-2025]/py`.
- Quotes for phrases: `'heart attack'` uses single quotes.

**Example**
```
('type 2 diabetes mellitus'/exp OR 'type 2 diab*':ti,ab,kw OR t2dm:ti,ab,kw)
AND ('exercise'/exp OR exercis*:ti,ab,kw OR 'physical activity':ti,ab,kw)
AND ('glycosylated hemoglobin'/exp OR hba1c:ti,ab,kw)
AND ([randomized controlled trial]/lim OR random*:ti,ab,kw)
AND [2015-2025]/py
```
**Tip**: search Embase for the **Embase-only** subset (`[embase]/lim NOT [medline]/lim`) after PubMed to measure additional yield.

---

## 5. Ovid MEDLINE and PsycINFO (Ovid syntax)

Ovid is a common interface for MEDLINE, Embase, PsycINFO, Global Health, CAB Abstracts.

- Line-by-line searching; combine with `1 AND 2` or `or/1-3`.
- Subject headings: `exp Diabetes Mellitus, Type 2/` (explode), `Diabetes Mellitus, Type 2/` (no explode with `*` for major: `*Diabetes.../`).
- Free text: `(type 2 diabet* or T2DM).ti,ab,kf.` (title, abstract, keyword heading words)
- Truncation `*` or `$` (unlimited), `?` (zero or one character), `#` (single character, e.g., `wom#n`).
- Proximity: `adjN` (within N words, any order): `(hip adj3 fracture).ti,ab.`; `adj` alone = adjacent in order.
- Limits: `limit 3 to (english language and yr="2015-Current")`, `limit to randomized controlled trial`.
- PsycINFO: headings use `exp Anxiety/`; fields `.ti,ab,id.`; methodology limit `exp Clinical Trials/`.

---

## 6. EBSCOhost (CINAHL, Academic Search, SPORTDiscus, ERIC)

- Fields: `TI`, `AB`, `TX` (all text), `AU`, `SU` (subject), `MH` (CINAHL Headings exact), `MM` (major), `AB`, `SO`.
- Proximity: `N5` (within 5, any order), `W5` (within 5, in order).
- Truncation `*`, wildcard `?` (one char), `#` (zero or one).
- Explode: `MH "Diabetes Mellitus, Type 2+"` (plus sign explodes).
- Boolean in uppercase. Limiters: published date, peer reviewed, research article.

---

## 7. Choosing between them

| Need | Best choice | Why |
|---|---|---|
| Full-text search of Elsevier journals | ScienceDirect | Only platform with full-text for them |
| Cross-discipline coverage + analytics | Scopus | Large, curated, citation tools |
| Citation chasing, high-impact filter | Web of Science | Cited-reference search, curation |
| Drug/device/pharmacology | Embase | Emtree depth, conference abstracts |
| Nursing/allied health | CINAHL | Specialized indexing |
| Psychology | PsycINFO | Thesaurus + method tags |
| Free and open | PubMed, Europe PMC, OpenAlex | No subscription needed |

Overlap is large but not total: Scopus and WoS share a core of journals; each has unique titles. For systematic reviews, minimal recommended sets (Bramer et al., 2017, "Optimal database combinations for literature searches in systematic reviews") include Embase, MEDLINE, Web of Science Core Collection, and Google Scholar (top 200 to 300) for high recall.

## 8. Export workflows

| Platform | Export |
|---|---|
| ScienceDirect | Select → Export → RIS / BibTeX / text |
| Scopus | Export → RIS, BibTeX, CSV, Mendeley, SciVal; choose fields (include abstract, references) |
| WoS | Export → Plain text, RIS, BibTeX, Excel; record content "Full record + cited references" |
| Embase | Export → RIS / CSV / Excel; select fields |
| Ovid | Export → RIS/EndNote; choose "Complete reference" |
| EBSCO | Add to folder → Export → RIS |

After export: import to a reference manager (Zotero, EndNote, Mendeley), **deduplicate** (use the Bramer method or the reference manager's tool; see `10`), and keep an untouched raw export per database for the audit trail.
