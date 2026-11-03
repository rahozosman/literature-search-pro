# 02. PubMed Deep Guide

PubMed (NLM/NCBI) indexes over 37 million citations, mostly biomedicine, from MEDLINE, PMC, and books. It is free, has a mature API, and is the starting point for any health or life-science search.

## Contents
1. What is inside PubMed
2. Search basics and automatic term mapping
3. Field tags
4. MeSH
5. Boolean, truncation, phrases, proximity
6. Filters and publication types
7. Dates
8. Advanced Search builder and History
9. Citation matching and known-item search
10. E-utilities API
11. Export formats
12. Pitfalls

## 1. What is inside PubMed

| Subset | Meaning | Tag |
|---|---|---|
| MEDLINE | Indexed with MeSH by NLM | `medline[sb]` |
| PubMed-not-MEDLINE | Publisher-supplied, in-process, or not indexed | `pubmednotmedline[sb]` |
| In-process / Publisher | Recent, not yet MeSH-indexed | `inprocess[sb]`, `publisher[sb]` |
| PMC | Full text in PubMed Central | `pubmed pmc[sb]` |

**Why it matters:** the newest papers lack MeSH terms. Always combine MeSH with `[tiab]` free-text synonyms or you will miss recent work.

## 2. Search basics and Automatic Term Mapping (ATM)

Typing `heart attack` into the basic box triggers ATM: PubMed maps it to MeSH, all fields, and may expand synonyms. This is convenient but opaque. For a reproducible search:

- Use **explicit field tags** (`[tiab]`, `[mh]`) so ATM does not interfere
- Check **Search Details** (below the results in the sidebar) to see what PubMed actually ran
- ATM is **switched off** for terms with a field tag, for truncated terms, and for phrases in quotes that are not in the phrase index

## 3. Field tags (most useful)

| Tag | Searches | Example |
|---|---|---|
| `[tiab]` | Title/Abstract (also keywords in recent records) | `statin*[tiab]` |
| `[ti]` | Title only | `"deep learning"[ti]` |
| `[tw]` | Text Words (title, abstract, MeSH, other terms, etc.) | `asthma[tw]` |
| `[mh]` | MeSH Terms (exploded) | `"Asthma"[mh]` |
| `[mh:noexp]` | MeSH, not exploded | `"Asthma"[mh:noexp]` |
| `[majr]` | MeSH Major Topic | `"Asthma"[majr]` |
| `[sh]` | MeSH Subheading | `"Diabetes Mellitus"[mh] AND therapy[sh]` |
| `[au]` | Author | `Smith J[au]` |
| `[1au]` / `[lastau]` | First / last author | `Doudna JA[1au]` |
| `[ad]` | Affiliation | `Harvard[ad]` |
| `[ta]` | Journal title abbreviation | `Lancet[ta]` |
| `[la]` | Language | `english[la]` |
| `[pt]` | Publication type | `"Randomized Controlled Trial"[pt]` |
| `[dp]` | Publication date | `2020:2024[dp]` |
| `[edat]` | Entrez date (when added) | `2024/01/01:3000[edat]` |
| `[sb]` | Subset | `systematic[sb]` |
| `[pmid]` | PMID | `12345678[pmid]` |
| `[doi]` | DOI | `10.1000/xyz[doi]` |
| `[gr]` | Grant number | `R01CA123456[gr]` |
| `[mhda]` | MeSH date | |
| `[all]` | All fields | |
| `[nm]` | Substance name (supplementary concept) | `"remdesivir"[nm]` |
| `[ot]` | Other term (author keywords) | |
| `[tt]` | Transliterated title | |

Both `[tiab]` and `[Title/Abstract]` work; tags are not case-sensitive.

## 4. MeSH (Medical Subject Headings)

NLM's controlled vocabulary: a tree hierarchy of about 30,000 descriptors. Benefits: handles synonyms, plural/spelling variants, and concept hierarchy automatically.

**How to use**
1. Open **MeSH Database** (pubmed.ncbi.nlm.nih.gov, "Advanced" → "MeSH Database", or the NCBI MeSH page).
2. Search your concept, read the Scope Note and Entry Terms.
3. Add to the search builder; choose subheadings if needed; note whether to **explode** (default) to include narrower terms.
4. Use `[mh]` for explosion, `[mh:noexp]` for exact heading, `[majr]` if the topic must be central.

**Subheadings** (qualifiers) narrow a heading: `"Hypertension/drug therapy"[mh]` or `"Hypertension"[mh] AND "drug therapy"[sh]`. Use subheadings only when precision matters; they reduce recall.

**Caveats**
- Indexing lags weeks to months for new records. Always add `[tiab]` terms.
- Index terms are assigned by humans/automation and can be wrong. Do not rely on MeSH alone.
- Headings change; older records are updated, so a search done in 2015 may behave differently today.
- Check the heading's **year introduced**: before that, records used older terms.

## 5. Boolean, truncation, phrases, proximity

- **Boolean operators must be uppercase**: `AND`, `OR`, `NOT`. Processing is left to right; use **parentheses** to control logic.
- **Truncation**: `diabet*` (min. 4 characters before the asterisk). PubMed uses the first 600 variations; when exceeded it warns you. Truncation disables ATM for that term.
- **Truncation inside quoted phrases** (e.g., `"type 2 diabet*"[tiab]`) is accepted only with a field tag in current PubMed; confirm in Search Details that it was not split, and if in doubt list explicit variants (`"type 2 diabetes" OR "type 2 diabetic"`).
- **Phrases**: `"quality of life"[tiab]` with quotes and a tag. Without a tag, the phrase must be in PubMed's phrase index, otherwise it is split.
- **Proximity** (Title/Abstract, Title, Affiliation only): `"hip fracture"[tiab:~3]` finds the words within 3 words of each other in any order. Use `"term1 term2"[tiab:~N]`. Handy when phrase search is too strict. Not available for MeSH or [tw].
- **Wildcards** inside words (`?`) are not supported in PubMed; use truncation or explicit OR variants.
- **Hyphens**: `type-2` and `type 2` index differently; include both or use quotes.
- **Stop words**: PubMed ignores very common words only in unquoted searches.

## 6. Filters and publication types

Sidebar filters add tags behind the scenes (e.g., `Free full text`, `Humans`, age groups). For reproducibility, write them out:

| Need | Query fragment |
|---|---|
| Randomized trials | `randomized controlled trial[pt]` |
| Meta-analysis | `meta-analysis[pt]` |
| Systematic reviews | `systematic[sb]` |
| Reviews | `review[pt]` |
| Clinical trial (all types) | `clinical trial[pt]` |
| Case reports | `case reports[pt]` |
| Humans only | `humans[mh]` |
| Animals only | `animals[mh] NOT humans[mh]` |
| Age: adult | `adult[mh]` |
| Has abstract | `hasabstract` |
| Free full text | `free full text[sb]` |
| English | `english[la]` |
| Exclude preprints | `NOT preprint[pt]` |
| Retracted | `retracted publication[pt]` |
| Exclude retracted | `NOT retracted publication[pt]` |

Be careful: **publication-type filters rely on indexing**. Recent RCTs may not carry the tag yet. For a sensitive trial search, combine: `(randomized controlled trial[pt] OR randomized[tiab] OR randomised[tiab] OR placebo[tiab] OR "clinical trial"[tiab])`. The Cochrane Highly Sensitive Search Strategy is the gold standard; search for "Cochrane Handbook Chapter 4 technical supplement".

PubMed also provides **Clinical Queries** (therapy, diagnosis, etiology, prognosis, clinical prediction guides; systematic review filter) validated by Haynes et al. Use for quick clinical answers.

## 7. Dates

- Publication date: `2018:2024[dp]` or `2018/03/01:2024/12/31[dp]`
- Open-ended: `2020:3000[dp]`
- Date added: `[edat]`; use for **updating** a search: `("2024/06/01"[edat] : "3000"[edat])`
- `[dp]` includes both electronic and print dates; a paper published online December 2023 in a 2024 issue appears under both.

## 8. Advanced Search builder and History

- **Advanced** page lets you build queries line by line, each in the **History** table (#1, #2...) and combine with `#1 AND #2`. Shows counts for each line: excellent for diagnosing which concept is too restrictive.
- Download the history/search details to document the strategy.
- Create **My NCBI** alerts to get new matching papers by email (search saved, "Create alert").

## 9. Known-item and citation matching

- Single Citation Matcher (PubMed "Advanced" → "Single Citation Matcher"): journal, year, volume, page, author.
- Searching by title: `"exact title words"[ti]` or paste the full title.
- By DOI: `10.xxxx/yyyy[doi]`.
- Batch Citation Matcher for lists.
- Always confirm the match by checking authors, journal, year, and volume against the user's reference.

## 10. E-utilities API

Base: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

| Utility | Purpose | Key parameters |
|---|---|---|
| `esearch.fcgi` | Query → PMID list | `db=pubmed`, `term`, `retmax`, `retstart`, `usehistory=y`, `sort`, `datetype`, `mindate`, `maxdate`, `retmode=json` |
| `efetch.fcgi` | PMIDs → full records | `db=pubmed`, `id`, `rettype=abstract|medline|xml`, `retmode=text|xml` |
| `esummary.fcgi` | PMIDs → brief summaries | `version=2.0`, `retmode=json` |
| `elink.fcgi` | Related/cited links | `dbfrom=pubmed`, `cmd=neighbor|citedin|refs` |
| `einfo.fcgi` | Database field list | |
| `ecitmatch.cgi` | Citation string → PMID | `bdata` |

**Rules of the road**
- Rate limit: **3 requests/second** without an API key, **10/second** with one (free from an NCBI account). Be polite.
- Include `tool=` and `email=` so NCBI can contact you if there is a problem.
- `usehistory=y` returns `WebEnv` and `query_key`; reuse them in `efetch` to page through big result sets without resending PMIDs.
- `esearch` returns up to **10,000** IDs per query window; for larger sets, split by date range.
- Fetch in batches (200 to 500 records); use POST for long ID lists.
- Sort options: `relevance` (Best Match), `pub_date`, `Author`, `JournalName`.
- Retrieval of full text: not through PubMed; follow DOI, PMC (`pmc` db, `elink` with `cmd=prlinks`), or Unpaywall.

**Example esearch (curl)**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22type+2+diabetes%22%5Btiab%5D+AND+exercise%5Btiab%5D&retmax=100&retmode=json&usehistory=y&tool=litsearch&email=you@example.com
```

`scripts/pubmed_search.py` wraps all of this and writes MD records automatically.

## 11. Export formats

From the results page: **Save** (summary/PMID list/abstract text/CSV), **Send to → Citation manager** (`.nbib`, importable into Zotero, EndNote, Mendeley), **Clipboard**, **Collections**. For reproducibility, export PMIDs and the query. `.nbib` is MEDLINE tagged format; RIS conversion tools exist.

## 12. Pitfalls checklist

- [ ] Relying on MeSH alone (misses new papers)
- [ ] Using lowercase `and`/`or` (treated as search words)
- [ ] Truncating below 4 characters (not allowed)
- [ ] Forgetting that truncation disables ATM and MeSH mapping for that word
- [ ] Not checking Search Details after a plain-text search
- [ ] Trusting publication-type filters for recent papers
- [ ] Stopping at 10,000 results in the API without date-splitting
- [ ] Not saving the search date (PubMed changes daily)
- [ ] Equating PubMed with all of biomedical literature (add Embase, Scopus, Cochrane)
