# 05. Other Databases and Open APIs

Catalog of everything else worth searching, with syntax and API notes. Verify endpoints and limits against current documentation before relying on them; services change.

## Contents
1. Free open-access indexes with APIs (Europe PMC, OpenAlex, Semantic Scholar, Crossref, CORE, DOAJ, Unpaywall)
2. Preprint servers (arXiv, bioRxiv/medRxiv, SSRN, OSF Preprints)
3. Clinical and evidence sources (Cochrane, ClinicalTrials.gov, WHO ICTRP, guidelines)
4. Discipline databases (PsycINFO, CINAHL, ERIC, EconLit, IEEE, ACM, DBLP, MathSciNet, AGRICOLA, GeoRef, Chemical Abstracts)
5. Theses, gray literature, patents, datasets
6. Non-English and regional databases
7. Quick API recipes

## 1. Free open indexes with APIs

### Europe PMC
Biomedical literature: MEDLINE, PMC, preprints (bioRxiv, medRxiv, Research Square, others), patents, Agricola, NHS guidelines. Full-text search for open-access content and text-mined annotations.
- Web: europepmc.org. Syntax: `TITLE:"deep learning" AND ABSTRACT:cancer`, `AUTH:"Smith J"`, `PUB_YEAR:[2020 TO 2025]`, `OPEN_ACCESS:y`, `SRC:MED` (MEDLINE), `SRC:PPR` (preprints), `HAS_FT:y`, `DOI:`, `PMID:`, `CITES:PMID_SRC` (papers citing).
- REST: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<q>&format=json&pageSize=100&resultType=core`; cursor paging with `cursorMark`.
- Strengths: free, full text, preprints, grant (Europe PMC funders) links.

### OpenAlex
Open catalog of about 250+ million works, authors, institutions, venues, concepts/topics, funders; successor to Microsoft Academic Graph. Good for bibliometrics, snowballing, and bulk.
- Endpoint: `https://api.openalex.org/works?search=<text>&filter=publication_year:2020-2025,type:article&per-page=50&cursor=*`.
- Useful filters: `title_and_abstract.search:`, `abstract.search:`, `cites:W123`, `cited_by:W123`, `doi:`, `is_oa:true`, `from_publication_date:`, `primary_location.source.id:`, `authorships.author.id:`.
- Add `mailto=you@example.com` for the polite pool; check current docs for API-key and rate-limit rules.
- Metadata can be incomplete or mis-assigned; verify key papers elsewhere.

### Semantic Scholar (Allen Institute)
AI-assisted index of over 200 million papers, strong in CS, biomed. Provides TLDR summaries, influential-citation counts, recommendations.
- Graph API: `https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&fields=title,year,authors,externalIds,abstract,citationCount&limit=100`; `/paper/DOI:<doi>`, `/paper/<id>/citations`, `/paper/<id>/references`.
- Free tier is rate limited; an API key raises limits.

### Crossref
Registration agency for DOIs; best for **metadata verification** and reference lists.
- `https://api.crossref.org/works/<DOI>`; search `?query.bibliographic=<citation string>&rows=5`; filters `from-pub-date:`, `type:journal-article`, `has-abstract:true`.
- Add `mailto=` for the polite pool. Retraction/correction notices appear in `relation` and `update-to` fields; Crossref also hosts the Retraction Watch database.
- Abstracts are often missing.

### CORE
Aggregator of open-access full texts and repositories (hundreds of millions of records). `core.ac.uk`, API requires a free key. Good for finding legal PDFs.

### DOAJ (Directory of Open Access Journals)
Curated list of vetted open-access journals; use to check journal legitimacy and find OA articles (`doaj.org/api`).

### Unpaywall
`https://api.unpaywall.org/v2/<DOI>?email=you@example.com` returns the best open-access location (`best_oa_location.url_for_pdf`, `oa_status`).

### Lens.org / Dimensions
Scholarly + patents linkage (Lens is free for basic use; Dimensions has a free tier with limits). Useful for patent citations of scholarly works.

## 2. Preprint servers

| Server | Scope | Search tips |
|---|---|---|
| **arXiv** | Physics, math, CS, stats, q-bio, econ | API `http://export.arxiv.org/api/query?search_query=ti:"graph neural" AND abs:molecule&max_results=50`; prefixes `ti:`, `abs:`, `au:`, `cat:`, `all:`; `submittedDate:[202401010000 TO 202412312359]` |
| **bioRxiv / medRxiv** | Biology / health sciences | Website advanced search; API `https://api.biorxiv.org/details/<server>/<from>/<to>`; also searchable in Europe PMC |
| **SSRN** | Social sciences, law, economics | Site search; mostly working papers |
| **OSF Preprints / PsyArXiv / SocArXiv / EarthArXiv** | Discipline preprints | OSF API |
| **Research Square** | Multidisciplinary (some under journal review) | Europe PMC indexes them |
| **ChemRxiv** | Chemistry | Site search |

**Rule**: preprints are **not peer reviewed**. Flag `status: preprint` in every record, check whether a published version exists (look for the DOI "published in" link), and never present preprint findings as established.

## 3. Clinical and evidence sources

- **Cochrane Library**: CDSR (systematic reviews), CENTRAL (controlled trials register; core for RCT searching). Syntax: `[mh "Diabetes Mellitus, Type 2"]`, `"type 2 diabet*":ti,ab,kw`, `NEAR/5`, `NEXT`. MeSH explosion with `[mh ^term]` to exclude explosion.
- **ClinicalTrials.gov**: registry; API v2 `https://clinicaltrials.gov/api/v2/studies?query.cond=diabetes&query.intr=exercise&pageSize=50`. Search for unpublished or ongoing trials (publication bias).
- **WHO ICTRP** (trial registry portal) and national registries (ISRCTN, EU CTR/CTIS, ANZCTR, ChiCTR, CTRI).
- **Guidelines**: NICE, SIGN, USPSTF, WHO, GIN (Guidelines International Network), ECRI.
- **Evidence summaries**: UpToDate and DynaMed are clinical decision tools (not primary sources; cite the underlying studies).
- **PROSPERO**: registry of systematic review protocols (check for existing reviews, register your own).
- **Epistemonikos**: database of systematic reviews with "evidence matrix".
- **TRIP Database**, **PEDro** (physiotherapy), **OTseeker** (occupational therapy), **ClinicalKey**, **Health Evidence**.
- **FDA / EMA** documents (drug approval packages, assessment reports) for unpublished trial data.
- **Retraction Watch Database** and **PubPeer** for integrity.

## 4. Discipline databases

| Discipline | Database | Notes |
|---|---|---|
| Psychology | **PsycINFO** (APA) | Thesaurus, methodology filters; through Ovid/EBSCO |
| Nursing | **CINAHL** | Strong on nursing and allied health |
| Education | **ERIC** (free) | `eric.ed.gov`, API available |
| Economics | **EconLit**, RePEc, SSRN | |
| Engineering/CS | **IEEE Xplore**, **ACM Digital Library**, **DBLP**, Inspec, **Compendex** | IEEE: `"Document Title":"x"`, `"Abstract":x`, `NEAR/n`, `ONEAR/n` |
| Math | MathSciNet, zbMATH | |
| Agriculture | AGRICOLA, CAB Abstracts, AGRIS | |
| Geoscience | GeoRef, Earth-prints | |
| Chemistry | SciFinder (CAS), Reaxys, ChemRxiv | Structure/reaction search |
| Physics | arXiv, INSPIRE-HEP (high-energy), NASA ADS (astro) | |
| Law | Westlaw, LexisNexis, HeinOnline, SSRN | |
| Sports/rehab | SPORTDiscus, PEDro | |
| Humanities | JSTOR, Project MUSE, MLA International Bibliography | |
| Public health | Global Health, WHO IRIS, PAHO | |
| Pharma/toxicology | TOXLINE (via PubMed), Embase, DailyMed | |
| Food | FSTA | |

## 5. Theses, gray literature, patents, datasets

- **Theses**: ProQuest Dissertations & Theses, EThOS (UK, via British Library), OATD, NDLTD, DART-Europe.
- **Gray literature**: OpenGrey (archived), GreyNet, Google Scholar `site:` searches, WHO IRIS, OECD, World Bank, government sites.
- **Conference abstracts**: Embase, Scopus, WoS CPCI, society websites.
- **Patents**: Google Patents, Espacenet, WIPO PATENTSCOPE, Lens.
- **Datasets**: Google Dataset Search, Zenodo, Dryad, Figshare, GEO, ICPSR, Harvard Dataverse.

## 6. Non-English and regional databases

- **China**: CNKI, Wanfang, VIP/CQVIP, SinoMed
- **Latin America**: LILACS, SciELO, Redalyc
- **Japan**: J-STAGE, CiNii, Ichushi-Web
- **Korea**: KoreaMed, KCI
- **India**: IndMED
- **Middle East**: IMEMR (WHO EMRO), Iraqi Academic Scientific Journals
- **Africa**: African Index Medicus, AJOL
- **Russia**: eLIBRARY.RU
- **Europe**: HAL, Persée (France), Dialnet (Spanish)

Include these when excluding non-English work could bias results (global health, traditional medicine, regional epidemiology). Use machine translation for screening, and flag it.

## 7. Quick API recipes

```
# Europe PMC: open-access RCTs on exercise and T2DM, 2020 onward
curl "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(TITLE_ABS:%22type%202%20diabetes%22%20AND%20TITLE_ABS:exercise)%20AND%20PUB_YEAR:%5B2020%20TO%202025%5D&format=json&pageSize=25"

# OpenAlex: works citing a given paper
curl "https://api.openalex.org/works?filter=cites:W2741809807&per-page=25&mailto=you@example.com"

# Crossref: verify a DOI and get metadata
curl "https://api.crossref.org/works/10.1038/nature12373?mailto=you@example.com"

# Semantic Scholar: search
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=graph+neural+networks&fields=title,year,externalIds&limit=10"

# Unpaywall: legal PDF link
curl "https://api.unpaywall.org/v2/10.1038/nature12373?email=you@example.com"

# ClinicalTrials.gov v2
curl "https://clinicaltrials.gov/api/v2/studies?query.cond=type+2+diabetes&query.intr=exercise&pageSize=10"

# arXiv
curl "http://export.arxiv.org/api/query?search_query=all:transformer+AND+cat:cs.CL&max_results=10"
```
(The example OpenAlex ID and DOI are illustrative; look up real IDs before use.)
