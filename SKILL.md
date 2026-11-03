---
name: literature-search-pro
description: Expert workflow for finding, defining, verifying, and documenting scientific articles across PubMed, Google Scholar, ScienceDirect, Scopus, Web of Science, Embase, Cochrane, Europe PMC, OpenAlex, Semantic Scholar, arXiv, IEEE, and other databases. Builds Boolean/MeSH search strategies, translates queries between databases, screens and appraises evidence, verifies citations (PMID/DOI) so nothing is fabricated, and saves every article as a structured Markdown record. Use this skill whenever the user mentions finding papers, literature search, literature review, systematic review, scoping review, PubMed, MeSH, Google Scholar, ScienceDirect, citations, references, "find studies on", "what does the research say", evidence synthesis, PICO, article lookup, DOI/PMID checks, or building a reading list, even if they never name a database.
---

# Literature Search Pro

A complete system for locating, defining, verifying, and documenting scientific articles. The goal is a search that is **comprehensive, reproducible, and honest**: every article reported must really exist, and every claim must trace back to a record.

## The three rules that matter most

1. **Never invent a citation.** Report only articles you actually retrieved or verified in this session (a PMID, DOI, or URL you saw). If you recall a paper from memory, label it `UNVERIFIED (from memory)` and verify it before the user relies on it. A fabricated reference is worse than no reference. Details: `references/08-verification-and-integrity.md`.
2. **Search the database's own language.** Each database has different field tags, thesauri, and wildcards. A query that works in PubMed fails silently in Scholar. Build the strategy once as concepts, then translate. See `references/06-syntax-translation.md`.
3. **Document the search.** Record the exact query, database, date, filters, and hit count so anyone can reproduce it. Use `templates/search-log.md`.

## Step 0: Detect your environment

Check which tools you have, then pick a mode:

| Mode | You have | What to do |
|---|---|---|
| **A. Live** | web search/fetch, or code with internet | Run searches, fetch records, verify DOIs/PMIDs, save MD records |
| **B. Code-only** | Code execution, no internet | Build queries and `scripts/`, give the user commands to run |
| **C. Chat-only** | Neither | Build expert query strings per database for the user to paste; explain how to export; never list "found" papers |

State the mode to the user in one line. In Mode C, any paper you name must be flagged unverified.

## Step 1: Clarify the question (2 minutes, not 20)

Identify the need, and ask at most one question if truly ambiguous:

- **Quick answer** ("what's known about X?") → Workflow 1
- **Targeted find** (specific paper, author, DOI, citation) → Workflow 2
- **Literature review / reading list** → Workflow 3
- **Systematic or scoping review** → Workflow 4 (`references/10-systematic-review-prisma.md`)
- **Verify or fix references** → Workflow 5 (`references/08-verification-and-integrity.md`)

Frame the question with the right model (PICO, PEO, SPIDER, PCC...). See `references/01-question-framing.md`.

## Step 2: Choose databases

| Field | Start here | Add for coverage |
|---|---|---|
| Biomedicine, clinical | PubMed/MEDLINE | Embase, Cochrane, Europe PMC, CINAHL, ClinicalTrials.gov |
| Life sciences, preprints | PubMed, Europe PMC | bioRxiv, medRxiv, Scopus |
| Psychology, behavior | PubMed, PsycINFO | Scopus, ERIC (education) |
| Engineering, CS | IEEE Xplore, ACM, arXiv | Scopus, Semantic Scholar, DBLP |
| Chemistry, materials, earth, general science | ScienceDirect, Scopus, Web of Science | Google Scholar |
| Social science, economics | Scopus, Web of Science, SSRN | EconLit, JSTOR |
| Anything, snowballing, gray lit | Google Scholar, OpenAlex | Semantic Scholar, CORE, Lens |

Full profiles of every database: `references/02` to `05`. A single database is never enough for a review; PubMed alone misses a large share of relevant studies.

## Step 3: Build the strategy

1. List 2 to 4 **concepts** (e.g., population, intervention, outcome).
2. For each concept, list **synonyms, spelling variants, acronyms, and controlled vocabulary** (MeSH, Emtree).
3. Join synonyms with `OR` inside a concept; join concepts with `AND`; exclude with `NOT` sparingly (it can remove relevant papers).
4. Test: does a handful of known relevant papers appear? If not, the strategy is too narrow.
5. Translate to each database (`scripts/build_query.py` automates this).

Worked example, PubMed:
```
("Diabetes Mellitus, Type 2"[Mesh] OR "type 2 diabet*"[tiab] OR T2DM[tiab])
AND ("Exercise"[Mesh] OR exercis*[tiab] OR "physical activity"[tiab])
AND ("Glycated Hemoglobin"[Mesh] OR HbA1c[tiab] OR "glycated hemoglobin"[tiab])
AND (randomized controlled trial[pt] OR randomized[tiab] OR randomised[tiab])
```

## Step 4: Execute

- **PubMed:** run in the web UI, or via E-utilities (`scripts/pubmed_search.py`). 
- **Google Scholar:** manual only; it has no API and prohibits scraping. Use it for snowballing and gray literature (`references/03-google-scholar.md`).
- **ScienceDirect, Scopus, WoS, Embase:** subscription platforms; give the user the translated query and export instructions. Open APIs (Europe PMC, OpenAlex, Crossref, Semantic Scholar) work in Mode A/B.
- Scan results by title, then abstract. Snowball: check references of key papers (backward) and "cited by" (forward).

## Step 5: Screen and appraise

Apply inclusion/exclusion criteria written **before** looking at results. Classify design using the evidence hierarchy and flag risk of bias. See `references/07-screening-and-appraisal.md`.

## Step 6: Define each article as a Markdown record

For every article kept, write one `.md` file using `templates/article-record.md` (YAML front matter + structured sections). Name files `FirstAuthorYear_PMID-or-DOI-slug.md`. This makes the corpus searchable, diffable, and portable to Obsidian, Zotero notes, Notion, or any LLM context. Full spec: `references/09-markdown-article-records.md`.

## Step 7: Deliver

Use the templates in `references/11-output-templates.md`. Always include:

- The final query for each database, date run, and hit counts
- A results table (author, year, design, key finding, PMID/DOI, verification status)
- Limitations of the search (databases not covered, language, paywalls)
- A clear line separating **verified** from **unverified** items

Keep chat replies short; put the bulk in files (the evidence table, MD records, search log).

## Reference map: load only what you need

| File | Read when |
|---|---|
| `references/01-question-framing.md` | Turning a vague topic into a searchable question |
| `references/02-pubmed.md` | Anything involving PubMed, MeSH, or E-utilities |
| `references/03-google-scholar.md` | Scholar searching, snowballing, gray literature |
| `references/04-sciencedirect-scopus-wos-embase.md` | Elsevier and other subscription platforms |
| `references/05-other-databases.md` | Cochrane, Europe PMC, OpenAlex, arXiv, IEEE, PsycINFO, etc. |
| `references/06-syntax-translation.md` | Converting a query between databases |
| `references/07-screening-and-appraisal.md` | Inclusion criteria, study design, risk of bias |
| `references/08-verification-and-integrity.md` | Checking citations, retractions, predatory journals |
| `references/09-markdown-article-records.md` | Saving articles as MD files |
| `references/10-systematic-review-prisma.md` | Systematic/scoping reviews, PRISMA flow |
| `references/11-output-templates.md` | Formatting the final deliverable |
| `references/12-troubleshooting.md` | Too many/few results, access problems |

Scripts (Python 3.8+, standard library only): `scripts/pubmed_search.py`, `scripts/build_query.py`, `scripts/verify_citation.py`. Run with `--help`.
