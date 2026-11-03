# 08. Verification and Research Integrity

AI systems can produce plausible but fake references (wrong authors, invented DOIs, real titles attached to wrong journals). This file is the antidote. Follow it every time a reference reaches the user.

## Contents
1. Verification status labels
2. The 5-point citation check
3. Verifying with tools (Mode A/B)
4. Verifying without tools (Mode C)
5. Fixing a broken or suspicious reference
6. Retractions and corrections
7. Predatory and low-quality journals
8. Preprints and versions
9. Copyright and full-text rules
10. Honest reporting language

## 1. Verification status labels (use on every item)

| Label | Meaning |
|---|---|
| `VERIFIED-DB` | Retrieved from a database record in this session (PMID/DOI/URL seen) |
| `VERIFIED-DOI` | DOI resolves; Crossref/PubMed metadata matches title, authors, year |
| `PARTIAL` | Some fields confirmed (e.g., title found, volume/pages unconfirmed) |
| `UNVERIFIED` | From memory or user-supplied; not checked |
| `NOT-FOUND` | Searched and could not locate: may not exist; say so |
| `RETRACTED` | Retraction notice found; never recommend without warning |

If the status is not `VERIFIED-*`, tell the user plainly.

## 2. The 5-point citation check

1. **Existence**: record found in PubMed, Crossref, Scopus, or the publisher site.
2. **Identity**: title matches (allowing small differences), first author surname, year, journal.
3. **Locators**: volume, issue, pages/article number, DOI (or PMID) match one another.
4. **Content**: the abstract actually supports how the paper is being cited (do not cite a paper for a claim it does not make).
5. **Status**: not retracted, no expression of concern, no major correction affecting the claim.

## 3. Verifying with tools

**DOI** → `https://doi.org/<DOI>` should redirect to the publisher; or `https://api.crossref.org/works/<DOI>`.
**PMID** → `https://pubmed.ncbi.nlm.nih.gov/<PMID>/`.
**Title only** → PubMed: `"full title words"[ti]`; Crossref: `query.bibliographic`.
**Retraction** → PubMed `[pt]`: the record shows "Retraction in"/"Retracted publication"; Crossref `update-to`; Retraction Watch database; publisher page banner.
**Script**: `python scripts/verify_citation.py --doi 10.xxxx/yyyy` or `--title "..." --author Smith --year 2020`.

Verification precedence if sources disagree: publisher/Crossref DOI record > PubMed > Scopus/WoS > Google Scholar > memory.

## 4. Verifying without tools (Mode C)

- Do **not** claim a paper exists. Say: "I recall a paper that may be relevant (unverified): [description]. Please check by searching `...` in PubMed."
- Provide the exact search string that would locate it.
- Prefer describing a **research direction** or search strategy over listing specific citations.
- Never fabricate DOIs, PMIDs, page numbers, or quotes. If asked for a DOI from memory, decline to guess and give the lookup route instead.

## 5. Fixing a suspicious reference

Typical errors: swapped authors, wrong year (online vs print), conflated papers with similar titles, real journal with fake article, merged titles, wrong volume.
1. Search by distinctive title words and first author.
2. If one close match exists, show the **corrected** reference and list what changed.
3. If several candidates, list them and ask which the user meant.
4. If none, mark `NOT-FOUND` and suggest the user check their source. Do not "repair" it into a plausible fabrication.

## 6. Retractions and corrections

- Check every key paper before it anchors a claim.
- PubMed marks retractions with publication type `Retracted Publication` and links `Retraction in`; corrections appear as `Erratum in` or `Published Erratum`.
- Expressions of concern: publisher notice; PubMed `Expression of Concern` publication type may be present.
- Citing a retracted paper is only acceptable when discussing the retraction; label it **RETRACTED**.
- Papers citing retracted work may need re-evaluation (reference lists of included studies).
- Retraction Watch database (hosted by Crossref) is the broadest source.

## 7. Predatory and low-quality journals

Check:
- Indexed in **MEDLINE/PMC**, Scopus, WoS, or **DOAJ** (not a guarantee, but a good filter)
- Publisher is a member of COPE, OASPA, or similar
- Transparent peer review process, editorial board verifiable, ISSN legitimate
- No spam solicitation; realistic turnaround; APCs disclosed
- Retraction history; Think. Check. Submit. checklist
- Cabells Predatory Reports (subscription) and community lists are imperfect; judge by evidence

Predatory journals can still appear in PubMed Central (some in PMC but not MEDLINE) and Google Scholar. State journal concerns neutrally and let the user decide.

## 8. Preprints and versions

- Preprint: label `status: preprint`; look for the published version via DOI relation, Europe PMC, or Crossref.
- Multiple versions (v1, v2): cite the version used.
- Conference abstract vs full paper: do not treat abstract results as final.
- Registered Report: protocol accepted before data; high credibility for design.

## 9. Copyright and full-text rules

- Summarize in your own words; short quotations (a sentence or less) with attribution only when wording matters.
- Do not reproduce full abstracts of paywalled papers at length; do not paste full text.
- Recommend legal access (PMC, OA, Unpaywall, library, author request). Never recommend Sci-Hub or pirate sources.
- Do not present text from a paper you have not read; if only the abstract was seen, say "based on the abstract".

## 10. Honest reporting language

Use calibrated phrases:
- "The abstract reports..." (not "the study proves...")
- "Evidence is limited to two small RCTs (n=60 and n=84)..."
- "I could not access the full text, so risk of bias is provisional."
- "I found no studies matching X in PubMed; this may reflect search limits, not absence of evidence."
- Report absence carefully: absence of results in one database is not evidence of absence.

Always end deliverables with a **Limitations** line covering databases searched, date, language limits, and verification status.
