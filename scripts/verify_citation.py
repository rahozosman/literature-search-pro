#!/usr/bin/env python3
"""
verify_citation.py - Check that a reference really exists and matches what was
claimed. Uses Crossref (DOIs), PubMed E-utilities (PMIDs) and optionally
Unpaywall (legal open-access link).  Standard library only.

Examples
  python verify_citation.py --doi 10.1038/nature12373 --email you@example.com
  python verify_citation.py --pmid 23995678
  python verify_citation.py --title "Exact title words" --author Smith --year 2020
  python verify_citation.py --doi 10.1038/nature12373 --claimed-title "Nanometre-scale thermometry in a living cell" --oa
  python verify_citation.py --file refs.txt        # one DOI or PMID per line (prefix "pmid:" for PMIDs)

Output states: FOUND, FOUND-MISMATCH (record exists but differs from the claim),
NOT-FOUND, plus retraction/correction flags where the source exposes them.
A missing record in one source is NOT proof a paper is fake; try another source.
Requires internet.
"""
import argparse
import difflib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "literature-search-pro/1.0 (mailto:{email})"


def http_json(url, email):
    req = urllib.request.Request(url, headers={"User-Agent": UA.format(email=email or "unknown@example.com")})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def crossref_by_doi(doi, email):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    if email:
        url += "?mailto=" + urllib.parse.quote(email)
    try:
        return http_json(url, email)["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def summarize_crossref(m):
    title = (m.get("title") or [""])[0]
    year = ""
    for k in ("published-print", "published-online", "issued", "created"):
        dp = m.get(k, {}).get("date-parts", [[None]])[0]
        if dp and dp[0]:
            year = str(dp[0])
            break
    authors = [f"{a.get('family','')} {''.join(w[0] for w in a.get('given','').split())}".strip()
               for a in m.get("author", [])]
    flags = []
    for u in m.get("update-to", []) or []:
        flags.append(f"update-to: {u.get('type')} ({u.get('DOI')})")
    rel = m.get("relation", {}) or {}
    for k in rel:
        if "retract" in k.lower() or "correct" in k.lower() or "concern" in k.lower():
            flags.append(f"relation: {k}")
    for u in (m.get("update-policy"), ):
        pass
    if re.search(r"retract", title, re.I):
        flags.append("title mentions retraction")
    return {
        "source": "Crossref", "doi": m.get("DOI"), "title": title, "authors": authors,
        "journal": (m.get("container-title") or [""])[0], "year": year,
        "volume": m.get("volume", ""), "issue": m.get("issue", ""), "pages": m.get("page", ""),
        "type": m.get("type", ""), "flags": flags,
    }


def pubmed_by_pmid(pmid, email):
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id="
           + urllib.parse.quote(pmid) + "&tool=literature-search-pro" + ("&email=" + urllib.parse.quote(email) if email else ""))
    data = http_json(url, email)
    rec = data.get("result", {}).get(pmid)
    if not rec or "error" in rec:
        return None
    doi = next((i["value"] for i in rec.get("articleids", []) if i.get("idtype") == "doi"), "")
    ptypes = rec.get("pubtype", [])
    flags = []
    if "Retracted Publication" in ptypes:
        flags.append("PubMed publication type: Retracted Publication")
    for c in rec.get("references", []) if False else []:
        pass
    return {
        "source": "PubMed", "pmid": pmid, "doi": doi, "title": rec.get("title", ""),
        "authors": [a.get("name", "") for a in rec.get("authors", [])],
        "journal": rec.get("fulljournalname", ""), "year": (rec.get("pubdate", "")[:4]),
        "volume": rec.get("volume", ""), "issue": rec.get("issue", ""), "pages": rec.get("pages", ""),
        "type": ", ".join(ptypes), "flags": flags,
    }


def crossref_by_title(title, author, year, email):
    q = {"query.bibliographic": f"{title} {author or ''} {year or ''}".strip(), "rows": "5"}
    if email:
        q["mailto"] = email
    items = http_json("https://api.crossref.org/works?" + urllib.parse.urlencode(q), email)["message"]["items"]
    scored = []
    for it in items:
        s = summarize_crossref(it)
        s["match_score"] = round(sim(title, s["title"]), 2)
        scored.append(s)
    return sorted(scored, key=lambda x: -x["match_score"])


def unpaywall(doi, email):
    if not email:
        return {"oa": "email required for Unpaywall (--email)"}
    d = http_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi, safe='/')}?email={urllib.parse.quote(email)}", email)
    best = d.get("best_oa_location") or {}
    return {"is_oa": d.get("is_oa"), "oa_status": d.get("oa_status"),
            "pdf": best.get("url_for_pdf"), "landing": best.get("url")}


def report(rec, claimed_title=None, claimed_year=None, claimed_author=None):
    verdict = "FOUND"
    notes = []
    if claimed_title:
        s = sim(claimed_title, rec["title"])
        if s < 0.85:
            verdict = "FOUND-MISMATCH"
            notes.append(f"title similarity only {s:.2f}")
    if claimed_year and rec.get("year") and str(claimed_year) != str(rec["year"]):
        verdict = "FOUND-MISMATCH"
        notes.append(f"year differs (claimed {claimed_year}, record {rec['year']}; online vs print year can differ by 1)")
    if claimed_author and rec.get("authors"):
        if norm(claimed_author) not in norm(" ".join(rec["authors"])):
            verdict = "FOUND-MISMATCH"
            notes.append(f"author '{claimed_author}' not among record authors")
    print(f"[{verdict}] via {rec['source']}")
    print(f"  Title:   {rec['title']}")
    print(f"  Authors: {', '.join(rec['authors'][:6])}{' ...' if len(rec['authors']) > 6 else ''}")
    print(f"  Journal: {rec['journal']} ({rec['year']}) vol {rec['volume']} issue {rec['issue']} pages {rec['pages']}")
    print(f"  DOI: {rec.get('doi')}  PMID: {rec.get('pmid', '-')}  Type: {rec['type']}")
    for f in rec["flags"]:
        print(f"  !! FLAG: {f}")
    for n in notes:
        print(f"  note: {n}")
    return verdict


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doi"); ap.add_argument("--pmid")
    ap.add_argument("--title"); ap.add_argument("--author"); ap.add_argument("--year")
    ap.add_argument("--claimed-title", help="Title the user/AI claimed, to compare against the record")
    ap.add_argument("--file", help="File with one DOI or 'pmid:123' per line")
    ap.add_argument("--email"); ap.add_argument("--oa", action="store_true", help="Also look up legal OA link (Unpaywall)")
    a = ap.parse_args(argv)

    try:
        if a.file:
            code = 0
            for line in open(a.file, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                print("=" * 70 + f"\n{line}")
                if line.lower().startswith("pmid:"):
                    rec = pubmed_by_pmid(line.split(":", 1)[1].strip(), a.email)
                else:
                    rec = crossref_by_doi(re.sub(r"^(doi:|https?://(dx\.)?doi\.org/)", "", line, flags=re.I), a.email)
                    rec = summarize_crossref(rec) if rec else None
                if rec:
                    report(rec)
                else:
                    print("[NOT-FOUND]"); code = 1
            return code
        if a.doi:
            doi = re.sub(r"^(doi:|https?://(dx\.)?doi\.org/)", "", a.doi, flags=re.I)
            m = crossref_by_doi(doi, a.email)
            if not m:
                print("[NOT-FOUND] DOI not in Crossref (could be DataCite or a mistyped DOI). Try https://doi.org/" + doi)
                return 1
            rec = summarize_crossref(m)
            report(rec, a.claimed_title or a.title, a.year, a.author)
            if a.oa:
                print("  Open access:", json.dumps(unpaywall(doi, a.email)))
        elif a.pmid:
            rec = pubmed_by_pmid(a.pmid, a.email)
            if not rec:
                print("[NOT-FOUND] PMID not in PubMed"); return 1
            report(rec, a.claimed_title or a.title, a.year, a.author)
            if a.oa and rec.get("doi"):
                print("  Open access:", json.dumps(unpaywall(rec["doi"], a.email)))
        elif a.title:
            cands = crossref_by_title(a.title, a.author, a.year, a.email)
            if not cands or cands[0]["match_score"] < 0.6:
                print("[NOT-FOUND] no close title match in Crossref. Also check PubMed: "
                      f"\"{a.title}\"[ti]. Do NOT treat the reference as real.")
                return 1
            for c in cands[:3]:
                print(f"--- candidate (title similarity {c['match_score']})")
                report(c, None, a.year, a.author)
        else:
            ap.error("give --doi, --pmid, --title or --file")
    except urllib.error.URLError as e:
        sys.exit(f"Network error: {e}\nNo internet here? Verify manually: https://doi.org/<DOI>, "
                 "https://pubmed.ncbi.nlm.nih.gov/<PMID>/ (see references/08).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
