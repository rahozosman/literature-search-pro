#!/usr/bin/env python3
"""
pubmed_search.py - Search PubMed via NCBI E-utilities and save every article
as a Markdown record (YAML front matter) plus INDEX.md, results.csv and a
search-log entry.  Standard library only (Python 3.8+).

Examples
  python pubmed_search.py --query '"type 2 diabetes"[tiab] AND exercise[tiab] AND randomized controlled trial[pt]' \
      --max 50 --out literature --email you@example.com
  python pubmed_search.py --pmids 12345678,23456789 --out literature
  python pubmed_search.py --query 'asthma[mh]' --mindate 2024/01/01 --maxdate 2026/12/31 --datetype edat

Needs internet access to eutils.ncbi.nlm.nih.gov. NCBI rate limit: 3 requests/s
without an API key, 10/s with one (--api-key). Please set --email.

The script only extracts metadata and the abstract. It does NOT judge study
quality, relevance, or inclusion; those fields are left blank for a reviewer.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "literature-search-pro"


# ----------------------------------------------------------------- HTTP ----
class Client:
    def __init__(self, email=None, api_key=None):
        self.email = email
        self.api_key = api_key
        self.delay = 0.12 if api_key else 0.35
        self._last = 0.0

    def _params(self, params):
        p = dict(params)
        p["tool"] = TOOL
        if self.email:
            p["email"] = self.email
        if self.api_key:
            p["api_key"] = self.api_key
        return p

    def get(self, endpoint, params, post=False, retries=3):
        data = urllib.parse.urlencode(self._params(params)).encode()
        for attempt in range(retries):
            wait = self.delay - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            try:
                if post:
                    req = urllib.request.Request(BASE + endpoint, data=data)
                else:
                    req = urllib.request.Request(BASE + endpoint + "?" + data.decode())
                with urllib.request.urlopen(req, timeout=60) as r:
                    self._last = time.time()
                    return r.read()
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
            except urllib.error.URLError:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                raise
        raise RuntimeError("unreachable")


# ------------------------------------------------------------- PARSING -----
def _text(el):
    """All text inside an element, including nested tags (<i>, <sub>...)."""
    return "".join(el.itertext()).strip() if el is not None else ""


def _clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def parse_article(art):
    """Convert a <PubmedArticle> element into a plain dict."""
    mc = art.find("MedlineCitation")
    article = mc.find("Article")
    pmid = _text(mc.find("PMID"))

    title = _clean(_text(article.find("ArticleTitle")))

    abstract_parts = []
    for ab in article.findall("Abstract/AbstractText"):
        label = ab.get("Label")
        txt = _clean(_text(ab))
        abstract_parts.append(f"{label}: {txt}" if label else txt)
    abstract = "\n\n".join(p for p in abstract_parts if p)

    authors = []
    for a in article.findall("AuthorList/Author"):
        last = _text(a.find("LastName"))
        ini = _text(a.find("Initials"))
        coll = _text(a.find("CollectiveName"))
        if last:
            authors.append(f"{last} {ini}".strip())
        elif coll:
            authors.append(coll)

    journal = _clean(_text(article.find("Journal/Title")))
    iso = _clean(_text(article.find("Journal/ISOAbbreviation")))
    volume = _text(article.find("Journal/JournalIssue/Volume"))
    issue = _text(article.find("Journal/JournalIssue/Issue"))
    pages = _text(article.find("Pagination/MedlinePgn"))

    year = _text(article.find("Journal/JournalIssue/PubDate/Year"))
    if not year:
        medline_date = _text(article.find("Journal/JournalIssue/PubDate/MedlineDate"))
        m = re.search(r"(19|20)\d{2}", medline_date)
        year = m.group(0) if m else ""

    doi = ""
    for e in article.findall("ELocationID"):
        if e.get("EIdType") == "doi":
            doi = _text(e)
    pmcid = ""
    for i in art.findall("PubmedData/ArticleIdList/ArticleId"):
        t = i.get("IdType")
        if t == "doi" and not doi:
            doi = _text(i)
        elif t == "pmc":
            pmcid = _text(i)

    pubtypes = [_text(p) for p in article.findall("PublicationTypeList/PublicationType")]
    mesh = [_text(m) for m in mc.findall("MeshHeadingList/MeshHeading/DescriptorName")]
    keywords = [_text(k) for k in mc.findall("KeywordList/Keyword")]
    langs = [_text(l) for l in article.findall("Language")]

    notices = []
    for c in mc.findall("CommentsCorrectionsList/CommentsCorrections"):
        rt = c.get("RefType", "")
        if rt in ("RetractionIn", "ExpressionOfConcernIn", "ErratumIn", "UpdateIn"):
            notices.append(rt)
    retracted = "Retracted Publication" in pubtypes or "RetractionIn" in notices

    return {
        "pmid": pmid, "title": title, "abstract": abstract, "authors": authors,
        "journal": journal, "journal_iso": iso, "year": year, "volume": volume,
        "issue": issue, "pages": pages, "doi": doi, "pmcid": pmcid,
        "pubtypes": pubtypes, "mesh": mesh, "keywords": keywords,
        "languages": langs, "notices": notices, "retracted": retracted,
    }


def parse_xml(xml_bytes):
    root = ET.fromstring(xml_bytes)
    return [parse_article(a) for a in root.findall("PubmedArticle")]


# ---------------------------------------------------------- MD OUTPUT ------
def q(s):
    """YAML-safe double-quoted string."""
    return json.dumps(s if s is not None else "", ensure_ascii=False)


def guess_design(pubtypes):
    """Rough hint from PubMed publication types. A reviewer must confirm."""
    m = {
        "Randomized Controlled Trial": "RCT", "Meta-Analysis": "MA",
        "Systematic Review": "SR", "Case Reports": "case-report",
        "Review": "narrative-review", "Clinical Trial": "clinical-trial",
        "Observational Study": "observational", "Preprint": "preprint",
    }
    for k, v in m.items():
        if k in pubtypes:
            return v
    return ""


def slug(s, n=60):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:n]


def record_name(r):
    first = (r["authors"][0].split()[0] if r["authors"] else "Unknown")
    first = re.sub(r"[^A-Za-z]", "", first) or "Unknown"
    ident = f"PMID{r['pmid']}" if r["pmid"] else f"doi-{slug(r['doi'])}"
    return f"{first}{r['year'] or 'nd'}_{ident}"


def vancouver(r):
    au = r["authors"]
    a = ", ".join(au[:6]) + (", et al" if len(au) > 6 else "")
    tail = f"{r['year']}"
    if r["volume"]:
        tail += f";{r['volume']}"
        if r["issue"]:
            tail += f"({r['issue']})"
    if r["pages"]:
        tail += f":{r['pages']}"
    doi = f" doi:{r['doi']}" if r["doi"] else ""
    title = r["title"] if r["title"][-1:] in ".?!" else r["title"] + "."
    return f"{a}. {title} {r['journal_iso'] or r['journal']}. {tail}.{doi} PMID:{r['pmid']}"


def write_record(r, outdir, query_ref, today):
    status = "retracted" if r["retracted"] else ("preprint" if "Preprint" in r["pubtypes"] else "published")
    url = f"https://doi.org/{r['doi']}" if r["doi"] else f"https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/"
    fm = [
        "---",
        "type: article",
        f"title: {q(r['title'])}",
        "authors: " + json.dumps(r["authors"], ensure_ascii=False),
        f"year: {r['year'] or 'null'}",
        f"journal: {q(r['journal'])}",
        f"volume: {q(r['volume'])}",
        f"issue: {q(r['issue'])}",
        f"pages: {q(r['pages'])}",
        f"doi: {q(r['doi'])}",
        f"pmid: {q(r['pmid'])}",
        f"pmcid: {q(r['pmcid'])}",
        f"url: {q(url)}",
        f"study_design: {q(guess_design(r['pubtypes']))}   # hint from PubMed publication types; reviewer must confirm",
        f"status: {status}",
        f"publication_types: {json.dumps(r['pubtypes'], ensure_ascii=False)}",
        f"mesh_terms: {json.dumps(r['mesh'], ensure_ascii=False)}",
        f"keywords: {json.dumps(r['keywords'], ensure_ascii=False)}",
        f"language: {json.dumps(r['languages'])}",
        "sample_size: null",
        "risk_of_bias: not-assessed",
        "evidence_level: abstract-only",
        "verification: VERIFIED-DB",
        f"retraction_checked: true   # only PubMed's own flags were checked",
        f"retraction_flag: {'true' if r['retracted'] else 'false'}",
        f"notices: {json.dumps(r['notices'])}",
        "relevance: \"\"",
        "decision: \"\"",
        "exclusion_reason: \"\"",
        "source_database: [\"PubMed\"]",
        f"date_retrieved: {q(today)}",
        f"search_ref: {q(query_ref)}",
        "tags: []",
        "---",
    ]
    short = (r["authors"][0].split()[0] if r["authors"] else "Unknown")
    if len(r["authors"]) > 1:
        short += " et al"
    body = [
        f"# {short} {r['year']}",
        "",
        "## Citation",
        vancouver(r),
        "",
        "## Abstract (as retrieved from PubMed)",
        r["abstract"] or "_No abstract available in PubMed record._",
        "",
        "## Summary",
        "_To be written in your own words after reading._",
        "",
        "## Key findings",
        "- Primary outcome:",
        "- Secondary outcomes:",
        "- Harms:",
        "",
        "## Methods snapshot", "", "## Strengths", "", "## Limitations", "",
        "## Risk of bias notes", "", "## Relevance to the question", "",
        "## Notes and follow-ups", "",
    ]
    if r["retracted"]:
        body.insert(1, "> **WARNING: PubMed flags this record as retracted. Do not rely on its findings.**\n")
    path = os.path.join(outdir, "records", record_name(r) + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(fm) + "\n" + "\n".join(body))
    return path


def write_index(rows, outdir):
    path = os.path.join(outdir, "INDEX.md")
    lines = ["# Index of records", "",
             "| File | Authors Year | Journal | Hint: design | PMID | DOI | Retraction flag |",
             "|---|---|---|---|---|---|---|"]
    for r, p in rows:
        a = (r["authors"][0] if r["authors"] else "Unknown") + (" et al" if len(r["authors"]) > 1 else "")
        lines.append(f"| [[{os.path.basename(p)[:-3]}]] | {a} {r['year']} | {r['journal_iso'] or r['journal']} | "
                     f"{guess_design(r['pubtypes'])} | {r['pmid']} | {r['doi']} | {'YES' if r['retracted'] else ''} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(outdir, "results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pmid", "doi", "year", "first_author", "title", "journal", "design_hint", "retracted"])
        for r, _ in rows:
            w.writerow([r["pmid"], r["doi"], r["year"], r["authors"][0] if r["authors"] else "",
                        r["title"], r["journal"], guess_design(r["pubtypes"]), r["retracted"]])


def append_log(outdir, query, count, fetched, args, today):
    path = os.path.join(outdir, "search-log.md")
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write("# Search Log\n\n")
        f.write(f"## PubMed search, {today}\n- Interface: E-utilities (esearch/efetch) via pubmed_search.py\n"
                f"- Query:\n```\n{query}\n```\n"
                f"- Date limits: datetype={args.datetype or '-'} mindate={args.mindate or '-'} maxdate={args.maxdate or '-'}\n"
                f"- Sort: {args.sort}\n- Total hits in PubMed: {count}\n- Records fetched and saved: {fetched}\n\n")


# ---------------------------------------------------------------- MAIN -----
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", help="PubMed query string")
    ap.add_argument("--pmids", help="Comma-separated PMIDs (skips search)")
    ap.add_argument("--max", type=int, default=50, help="Max records to fetch (default 50)")
    ap.add_argument("--out", default="literature", help="Output folder (default ./literature)")
    ap.add_argument("--sort", default="relevance", choices=["relevance", "pub_date", "Author", "JournalName"])
    ap.add_argument("--datetype", choices=["pdat", "edat", "mdat"], help="Date type for mindate/maxdate")
    ap.add_argument("--mindate"); ap.add_argument("--maxdate")
    ap.add_argument("--email", default=os.environ.get("NCBI_EMAIL"))
    ap.add_argument("--api-key", default=os.environ.get("NCBI_API_KEY"))
    ap.add_argument("--count-only", action="store_true", help="Only report the hit count")
    ap.add_argument("--parse-file", help="(testing) parse a local efetch XML file instead of calling NCBI")
    args = ap.parse_args(argv)

    today = dt.date.today().isoformat()
    os.makedirs(os.path.join(args.out, "records"), exist_ok=True)

    if args.parse_file:
        with open(args.parse_file, "rb") as f:
            recs = parse_xml(f.read())
        query, total = "(local file)", len(recs)
    else:
        if not (args.query or args.pmids):
            ap.error("provide --query or --pmids")
        c = Client(args.email, args.api_key)
        try:
            if args.pmids:
                ids = [x.strip() for x in args.pmids.split(",") if x.strip()]
                query, total, webenv, qkey = "PMIDs: " + ",".join(ids), len(ids), None, None
            else:
                query = args.query
                p = {"db": "pubmed", "term": query, "retmax": min(args.max, 10000),
                     "retmode": "json", "sort": args.sort, "usehistory": "y"}
                if args.datetype and (args.mindate or args.maxdate):
                    p.update({"datetype": args.datetype, "mindate": args.mindate or "1800",
                              "maxdate": args.maxdate or "3000"})
                res = json.loads(c.get("esearch.fcgi", p))["esearchresult"]
                if "ERROR" in res:
                    sys.exit(f"PubMed error: {res['ERROR']}")
                total = int(res["count"])
                ids = res["idlist"]
                webenv, qkey = res.get("webenv"), res.get("querykey")
                tr = res.get("querytranslation")
                print(f"PubMed hits: {total}")
                if tr:
                    print(f"PubMed interpreted the query as:\n  {tr}")
                for w in res.get("warninglist", {}).get("outputmessages", []):
                    print(f"WARNING: {w}")
                for w in res.get("errorlist", {}).get("phrasesnotfound", []):
                    print(f"WARNING: phrase not found: {w}")
            if args.count_only:
                return 0
            recs = []
            for i in range(0, len(ids), 200):
                chunk = ids[i:i + 200]
                xml = c.get("efetch.fcgi", {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"}, post=True)
                recs.extend(parse_xml(xml))
                print(f"  fetched {len(recs)}/{len(ids)}")
        except urllib.error.URLError as e:
            sys.exit("Network error talking to NCBI: %s\n"
                     "No internet from this environment? Use the query in the web UI instead: "
                     "https://pubmed.ncbi.nlm.nih.gov/ (see references/02-pubmed.md)." % e)

    rows = []
    for r in recs[: args.max]:
        rows.append((r, write_record(r, args.out, "S-" + today, today)))
    write_index(rows, args.out)
    append_log(args.out, query, total, len(rows), args, today)
    flagged = sum(1 for r, _ in rows if r["retracted"])
    print(f"Saved {len(rows)} records to {args.out}/records (retraction-flagged: {flagged})")
    print(f"Index: {args.out}/INDEX.md | CSV: {args.out}/results.csv | Log: {args.out}/search-log.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
