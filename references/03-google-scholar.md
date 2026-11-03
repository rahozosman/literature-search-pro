# 03. Google Scholar Deep Guide

Google Scholar (GS) indexes scholarly articles, theses, books, preprints, court opinions, and patents across publishers and repositories. It is broad, fast, and free, but opaque: coverage, ranking, and update rules are not published.

## Contents
1. Strengths and limits
2. Operators that work
3. Ranking behavior
4. Filters and settings
5. Snowballing with "Cited by", "Related articles", "All versions"
6. Finding full text legally
7. Gray literature and theses
8. Alerts and Library
9. Exporting and tools
10. Rules for using GS in a systematic review
11. Pitfalls

## 1. Strengths and limits

**Strengths**: full-text indexing (matches words inside papers, not only abstracts), gray literature, books, theses, preprints, non-English work, citation counts, cross-publisher coverage, "Cited by" for forward snowballing.

**Limits**
- **No API and no sanctioned bulk export.** Automated scraping violates Google's terms and triggers CAPTCHAs/blocks. Do not scrape; search manually, or use sanctioned sources (OpenAlex, Semantic Scholar, Crossref) for programmatic work.
- **Only the first 1,000 results** per query are viewable (about 100 pages of 10).
- **No Boolean parentheses** and weak Boolean support, no truncation, no controlled vocabulary.
- **Ranking is not reproducible**; results shift over time, location, and personalization.
- **Citation counts** are inflated by duplicates, preprints, and self-citation; treat as rough.
- Inconsistent metadata; quality control is low (predatory journals can appear).

Because of these, GS is a **supplement** to PubMed/Scopus/Embase, never the sole source for a review.

## 2. Operators that work

| Goal | Syntax | Notes |
|---|---|---|
| Exact phrase | `"gut microbiome"` | Quotes bind words in order |
| OR | `cancer OR carcinoma` | `OR` must be uppercase; `\|` also works |
| AND | implicit (space) | |
| Exclude | `-review` | Minus directly before the word |
| Title only | `intitle:diabetes` | `allintitle: diabetes exercise` requires all words in title |
| Author | `author:"Jennifer Doudna"` or `author:doudna` | Use quotes for full names |
| Journal/source | `source:"Nature"` | |
| Wildcard in phrase | `"effect of * on mortality"` | `*` stands for one or more words, not a truncation |
| File type | `filetype:pdf` | Limits to PDF; works only sometimes |
| Site | `site:who.int` | Restricts to a domain; excellent for gray literature |
| Related | `related:URL` | Legacy; use the "Related articles" link instead |

Things that do **not** work: nested parentheses, `AND` as an explicit operator (ignored), `*` as suffix truncation (`diabet*`), proximity operators, field tags like `[tiab]`.

**Workarounds for long Boolean queries**: Run several short searches and combine results manually, or collapse synonyms with `OR` in 2 to 3 term groups; GS also limits query length (around 256 characters).

## 3. Ranking behavior

Ranking weighs full text, author, publication source, and **citation counts** heavily. Consequences:
- Highly cited older papers outrank new ones. Use the **Since YYYY** filter or **Sort by date** to find recent work.
- A precise phrase with a distinctive term surfaces the target paper quickly (use for known-item search: paste the exact title in quotes).
- Check only top 200 to 300 for a review (rather than all 1,000) and document it.

## 4. Filters and settings

Left sidebar: **Any time / Since year / Custom range**, **Sort by relevance / date**, **Any type / Review articles**, **include/exclude patents**, **include/exclude citations**, **Create alert**.

Advanced search (menu → Advanced search): all words, exact phrase, at least one, none of the words, where words occur (anywhere or title), author, publication, date range.

Settings → **Library links** (set your university to see "Find it @ Institution" links), **Bibliography manager** (show "Import into BibTeX/RefMan/EndNote" links), **Languages**, **Results per page** (up to 20).

## 5. Snowballing

Three engines in every result:

1. **Cited by N**: forward snowballing (who cited this?). Within results, tick "Search within citing articles" and add keywords to narrow.
2. **Related articles**: papers similar in content; good for discovery but not systematic.
3. **All N versions**: finds free PDFs (preprints, repository copies), other databases' records, and duplicates.

**Backward snowballing**: read the paper's reference list (publisher page or PDF) and search titles in GS.

Citation chasing is the fastest way to expand from 3 to 5 seed papers into a full set. Document each seed and what it led to (see `templates/search-log.md`).

## 6. Finding full text legally

Order of attempts:
1. Click the **[PDF]/[HTML]** link on the right of the result (usually an open-access copy).
2. **All versions** → repository copies, preprints, PMC.
3. Library link (your institution).
4. **Unpaywall**/**OpenAlex**/**CORE** lookup by DOI (`scripts/verify_citation.py --oa` queries Unpaywall).
5. Author's institutional repository or ResearchGate/Academia (check publisher policy).
6. Email the corresponding author; request via interlibrary loan.

Do **not** recommend pirate sites. Explain legal options instead.

## 7. Gray literature and theses

- `site:` operator: `"malaria vaccine" site:who.int`, `site:nice.org.uk`, `site:gov`, `site:edu filetype:pdf`
- Theses: search `"thesis" OR "dissertation"` plus topic; also use ProQuest Dissertations, EThOS, OATD.
- Conference papers: add `conference OR proceedings`; use arXiv, IEEE, ACM.
- Regulatory docs, clinical practice guidelines, white papers, NGO reports: use `filetype:pdf` plus the organization domain.
- Always record the URL and access date; web content changes.

## 8. Alerts and Library

- **Alerts**: from a search, **Create alert** emails new matches. Also create alerts for an author's profile and for citations to key papers.
- **My Library**: save results, apply labels; export saved items to BibTeX/CSV/RefMan/EndNote.
- **Author profiles** (when public): list of publications, h-index, i10-index; verify manually as profiles can merge distinct authors.

## 9. Exporting and tools

- Per result: the **quote mark** ("Cite") shows MLA, APA, Chicago, Harvard, Vancouver and BibTeX/EndNote/RefMan/RefWorks links.
- **Publish or Perish** (desktop software) queries GS and other APIs for analysis; it operates under rate limits and users must follow Google's terms. Mention the risk of blocks.
- Better programmatic routes: **OpenAlex**, **Semantic Scholar**, **Crossref**, **Europe PMC** (all open).

## 10. Rules for using GS in a systematic review

(Reflects common methodological guidance, e.g., Gusenbauer & Haddaway, 2020, "Which academic search systems are suitable for systematic reviews?")
- GS lacks reproducibility features required by PRISMA-S; use it only as a **supplementary** source.
- Screen the first **100 to 300** results sorted by relevance and report that cutoff.
- Log the exact query, date, number screened, and any filters.
- Use for snowballing and gray literature, not as a principal database.

## 11. Pitfalls

- Searching for `AND`: it is ignored; only `OR` and `-` matter.
- Over-trusting citation counts and "top results" as quality.
- Assuming a paper is peer-reviewed because GS lists it.
- Forgetting the 1,000-result ceiling (split queries by year with the custom range).
- Not setting library links, then thinking papers are paywalled.
- Scraping: leads to temporary IP blocks and breaches terms.
