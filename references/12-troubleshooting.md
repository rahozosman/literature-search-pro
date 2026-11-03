# 12. Troubleshooting

## Contents
1. Too many results
2. Too few or zero results
3. Irrelevant results
4. Known paper not appearing
5. Cannot access full text
6. Conflicting metadata
7. API and tool errors
8. Ambiguous or jargon-heavy topics
9. Updating and alerts
10. Diagnostic loop

## 1. Too many results (precision problem)

- Add a concept (AND) or narrow to `[ti]`/`[majr]`.
- Switch from all-fields to title/abstract.
- Add design filters (RCT, systematic review) or date limits (justified).
- Replace broad truncation (`child*`) with specific terms.
- Use `NOT` for clear noise only (e.g., `NOT animals[mh]` combined with humans).
- Sort by relevance and screen a defined top N; log it.

## 2. Too few or zero results (recall problem)

- Remove the least essential concept (often outcome or design).
- Add synonyms, spelling variants, acronyms; use truncation.
- Remove field tags to let ATM expand (PubMed) as a diagnostic.
- Check typos and unmatched parentheses or quotes.
- Remove the date or language filter.
- Try another database (Embase, Scopus, Europe PMC).
- Use `[tiab:~3]` proximity instead of exact phrases.
- Check that the concept is not too new for MeSH (use free text).

## 3. Irrelevant results

- Ambiguous abbreviations ("ALS", "MS", "CAT"): pair with full term or context words.
- Homonyms (cell, mouse, python): add context concept.
- Split concept blocks and view counts per line to see which one brings noise.
- Move from truncation to explicit forms.
- Use MeSH with subheadings or `[majr]`.

## 4. Known paper not appearing

1. Search its exact title in the target database. Found? Then your strategy missed it; study its title/abstract/indexing to see why (missing synonym, MeSH not yet assigned, concept not stated).
2. Not found? The database may not index that journal (check coverage) or the record is too new; try another.
3. Add the discovered terms to the strategy; re-run. Repeat for other seed papers ("test set" method).

## 5. Cannot access full text

Order: publisher OA link → PMC → Europe PMC → preprint server → **Unpaywall** → Google Scholar "All versions" → institutional proxy/library → author repository → email author → interlibrary loan. If only the abstract is accessible, say so and limit claims.

## 6. Conflicting metadata

Two sources disagree on year/volume/authors: prefer publisher/Crossref. Note that online-first vs issue year differ. Report the DOI; avoid mixing citations from two sources. Check for duplicates with different IDs (preprint and published).

## 7. API and tool errors

| Symptom | Likely cause | Fix |
|---|---|---|
| HTTP 429 | Rate limit | Wait; add API key; batch with `usehistory`; ≤3 req/s without key (NCBI) |
| HTTP 400 on esearch | Bad term syntax, unescaped characters | URL-encode, check quotes/brackets |
| Empty `idlist` | No matches or wrong field | Test in the web UI; inspect `translationset` and `querytranslation` in the esearch response |
| XML parse errors | Truncated response | Fetch in smaller batches; retry |
| Network unreachable | Sandbox without internet | Switch to Mode B/C; give queries to the user |
| Crossref 404 | DOI mistyped or not Crossref-registered (could be DataCite) | Try `doi.org` or DataCite API |
| Scholar CAPTCHA | Automated traffic | Stop; use manual or open APIs |

## 8. Ambiguous or jargon-heavy topics

- Ask one clarifying question if the answer changes the search (population, time, outcome).
- Provide two interpretations and search both if cheap.
- Check terminology differences between fields and countries (e.g., "paracetamol/acetaminophen", "frailty" in geriatrics vs materials).

## 9. Updating and alerts

- PubMed: save search → My NCBI → create alert; or rerun with `[edat]` from last run.
- Google Scholar: alerts for queries and for citations to key papers.
- Scopus/WoS/Embase: saved searches and alerts; cited-reference alerts.
- Europe PMC: saved searches with RSS or email.
- Record "last searched on" in the search log.

## 10. Diagnostic loop

1. Pick 3 to 5 seed papers you know are relevant.
2. Run strategy; are seeds present? If no, find terms missed.
3. Count per concept line; identify the bottleneck.
4. Adjust one thing at a time; log changes and counts.
5. Stop when new synonyms/databases add little new (saturation) and seeds are captured.
