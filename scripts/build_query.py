#!/usr/bin/env python3
"""
build_query.py - Turn concept blocks into ready-to-paste search strings for
PubMed, Scopus, Web of Science, Embase, Ovid MEDLINE, Cochrane, EBSCO (CINAHL),
ScienceDirect, Europe PMC and Google Scholar.   Standard library only.

Usage
  python build_query.py \
     --block "diabetes=type 2 diabet*;T2DM;NIDDM" \
     --block "exercise=exercis*;physical activity;training" \
     --block "outcome=HbA1c;glycated hemoglobin" \
     --mesh  "diabetes=Diabetes Mellitus, Type 2" \
     --mesh  "exercise=Exercise" \
     --emtree "diabetes=non insulin dependent diabetes mellitus" \
     --years 2015-2025 --lang english --design rct --platform all

  --block  "name=term1;term2;..."   free-text terms (use * for truncation)
  --mesh   "name=Heading;Heading"   MeSH headings (PubMed, Ovid, Cochrane, EBSCO uses as CINAHL heading guess)
  --emtree "name=term;term"         Emtree headings (Embase)
  --design rct|sr|none              optional study-design filter
  --platform all or comma list: pubmed,scopus,wos,embase,ovid,cochrane,ebsco,sciencedirect,europepmc,scholar
  --json                            machine-readable output

IMPORTANT: output is a starting point. Controlled-vocabulary names differ by
database, so check each heading in the platform's thesaurus. Run the query,
test it against known papers, and log the final version.
"""
import argparse
import json
import sys


def parse_kv(items):
    out = {}
    for it in items or []:
        if "=" not in it:
            sys.exit(f"Bad argument (need name=a;b;c): {it}")
        k, v = it.split("=", 1)
        out[k.strip()] = [t.strip() for t in v.split(";") if t.strip()]
    return out


def quote(t):
    return f'"{t}"' if " " in t or "-" in t else t


def has_trunc(t):
    return "*" in t


# ------------------------------------------------------------ per platform --
def pubmed(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        items = [f'"{h}"[mh]' for h in mesh.get(name, [])]
        for t in terms:
            items.append(f'{quote(t)}[tiab]' if (" " not in t and "-" not in t) else f'"{t}"[tiab]')
        parts.append("(" + " OR ".join(items) + ")")
    if design == "rct":
        parts.append('(randomized controlled trial[pt] OR randomized[tiab] OR randomised[tiab] OR placebo[tiab])')
    elif design == "sr":
        parts.append('(systematic[sb] OR meta-analysis[pt] OR "systematic review"[tiab] OR "meta-analysis"[tiab])')
    if years:
        a, b = years
        parts.append(f"{a}:{b}[dp]")
    if lang:
        parts.append(f"{lang}[la]")
    return "\n AND ".join(parts)


def scopus(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        parts.append("(" + " OR ".join(f'"{t}"' if " " in t else t for t in terms) + ")")
    core = "TITLE-ABS-KEY(" + " AND ".join(parts) + ")"
    extra = []
    if design == "rct":
        extra.append("TITLE-ABS-KEY(random* OR placebo OR \"controlled trial\")")
    elif design == "sr":
        extra.append("TITLE-ABS-KEY(\"systematic review\" OR \"meta-analysis\" OR \"meta analysis\")")
    if years:
        a, b = years
        extra.append(f"PUBYEAR > {a - 1} AND PUBYEAR < {b + 1}")
    if lang:
        extra.append(f"LANGUAGE({lang})")
    return "\n AND ".join([core] + extra)


def wos(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        parts.append("(" + " OR ".join(f'"{t}"' if " " in t else t for t in terms) + ")")
    out = ["TS=(" + " AND ".join(parts) + ")"]
    if design == "rct":
        out.append("TS=(random* OR placebo OR \"controlled trial\")")
    elif design == "sr":
        out.append("TS=(\"systematic review\" OR \"meta-analysis\" OR \"meta analysis\")")
    if years:
        out.append(f"PY=({years[0]}-{years[1]})")
    if lang:
        out.append(f"LA={lang.capitalize()}")
    return "\n AND ".join(out)


def embase(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        items = [f"'{h}'/exp" for h in emtree.get(name, [])]
        for t in terms:
            tt = f"'{t}'" if " " in t else t
            items.append(f"{tt}:ti,ab,kw")
        parts.append("(" + " OR ".join(items) + ")")
    if design == "rct":
        parts.append("([randomized controlled trial]/lim OR random*:ti,ab,kw OR placebo:ti,ab,kw)")
    elif design == "sr":
        parts.append("([systematic review]/lim OR [meta analysis]/lim OR 'systematic review':ti,ab,kw)")
    if years:
        parts.append(f"[{years[0]}-{years[1]}]/py")
    if lang:
        parts.append(f"[{lang}]/lim")
    return "\n AND ".join(parts)


def ovid(blocks, mesh, emtree, years, lang, design):
    lines, ids = [], []
    n = 0
    for name, terms in blocks.items():
        block_ids = []
        for h in mesh.get(name, []):
            n += 1
            lines.append(f"{n}. exp {h}/")
            block_ids.append(n)
        n += 1
        lines.append(f"{n}. (" + " or ".join(terms) + ").ti,ab,kf.")
        block_ids.append(n)
        if len(block_ids) > 1:
            n += 1
            lines.append(f"{n}. " + " or ".join(str(i) for i in block_ids))
        ids.append(n)
    if len(ids) > 1:
        n += 1
        lines.append(f"{n}. " + " and ".join(str(i) for i in ids))
    last = n
    if design == "rct":
        n += 1
        lines.append(f"{n}. {last} and (randomized controlled trial.pt. or random*.ti,ab. or placebo.ti,ab.)")
        last = n
    elif design == "sr":
        n += 1
        lines.append(f"{n}. {last} and (meta-analysis.pt. or systematic review.pt. or (systematic review or meta-analysis).ti,ab.)")
        last = n
    lim = []
    if lang:
        lim.append(f"{lang} language")
    if years:
        lim.append(f'yr="{years[0]}-{years[1]}"')
    if lim:
        n += 1
        lines.append(f"{n}. limit {last} to (" + " and ".join(lim) + ")")
    return "\n".join(lines)


def cochrane(blocks, mesh, emtree, years, lang, design):
    lines, ids = [], []
    n = 0
    for name, terms in blocks.items():
        items = [f'[mh "{h}"]' for h in mesh.get(name, [])]
        items += [f'{quote(t)}:ti,ab,kw' for t in terms]
        n += 1
        lines.append(f"#{n} " + " OR ".join(items))
        ids.append(n)
    n += 1
    suffix = f" with Publication Year from {years[0]} to {years[1]}" if years else ""
    lines.append(f"#{n} " + " AND ".join(f"#{i}" for i in ids) + suffix)
    return "\n".join(lines)


def ebsco(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        items = [f'MH "{h}+"' for h in mesh.get(name, [])]
        tq = " OR ".join(f'"{t}"' if " " in t else t for t in terms)
        items += [f"TI({tq})", f"AB({tq})"]
        parts.append("(" + " OR ".join(items) + ")")
    out = " AND ".join(parts)
    note = "\n(Set Published Date and Language limiters in the sidebar; CINAHL headings may differ from MeSH, verify in the CINAHL thesaurus.)"
    return out + note


def sciencedirect(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        parts.append("(" + " OR ".join(f'"{t}"' if " " in t else t for t in terms) + ")")
    q = " AND ".join(parts)
    note = ["Field: 'Title, abstract or author-specified keywords'", q,
            "(ScienceDirect allows roughly 8 Boolean operators per field; split the query if it is longer.)"]
    if years:
        note.append(f"Years: {years[0]}-{years[1]}")
    if design == "rct":
        note.append("Article type: Research articles")
    elif design == "sr":
        note.append("Article type: Review articles")
    return "\n".join(note)


def europepmc(blocks, mesh, emtree, years, lang, design):
    parts = []
    for name, terms in blocks.items():
        parts.append("(" + " OR ".join(f'TITLE_ABS:"{t}"' if " " in t else f"TITLE_ABS:{t}" for t in terms) + ")")
    if design == "rct":
        parts.append('(PUB_TYPE:"Randomized Controlled Trial" OR TITLE_ABS:randomized OR TITLE_ABS:placebo)')
    elif design == "sr":
        parts.append('(PUB_TYPE:"Systematic Review" OR PUB_TYPE:"Meta-Analysis" OR TITLE_ABS:"systematic review")')
    if years:
        parts.append(f"PUB_YEAR:[{years[0]} TO {years[1]}]")
    if lang:
        parts.append('LANG:"eng"' if lang.lower().startswith("eng") else f'LANG:"{lang}"')
    return "\n AND ".join(parts)


def scholar(blocks, mesh, emtree, years, lang, design):
    # Google Scholar has no truncation or nested Boolean: give simple variants
    names = list(blocks)
    prim = [quote(blocks[n][0]).replace("*", "") for n in names]
    lines = ["Variant 1 (core terms): " + " ".join(prim)]
    if len(names) >= 2:
        alts = " OR ".join(quote(t).replace("*", "") for t in blocks[names[0]][:3])
        rest = " ".join(prim[1:])
        lines.append("Variant 2 (synonyms for concept 1): " + alts + " " + rest)
    lines.append("Notes: no truncation or nesting; set the date range in the sidebar; review first 100 to 300 results; log it.")
    if design == "sr":
        lines.append("Add: review OR meta-analysis")
    return "\n".join(lines)


PLATFORMS = {
    "pubmed": ("PubMed", pubmed), "scopus": ("Scopus", scopus), "wos": ("Web of Science Core Collection", wos),
    "embase": ("Embase (embase.com)", embase), "ovid": ("Ovid MEDLINE", ovid), "cochrane": ("Cochrane Library", cochrane),
    "ebsco": ("EBSCOhost (CINAHL)", ebsco), "sciencedirect": ("ScienceDirect", sciencedirect),
    "europepmc": ("Europe PMC", europepmc), "scholar": ("Google Scholar", scholar),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--block", action="append", required=True)
    ap.add_argument("--mesh", action="append")
    ap.add_argument("--emtree", action="append")
    ap.add_argument("--years", help="e.g. 2015-2025")
    ap.add_argument("--lang", help="e.g. english")
    ap.add_argument("--design", choices=["rct", "sr", "none"], default="none")
    ap.add_argument("--platform", default="all")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    blocks, mesh, emtree = parse_kv(a.block), parse_kv(a.mesh), parse_kv(a.emtree)
    years = None
    if a.years:
        try:
            y1, y2 = a.years.split("-")
            years = (int(y1), int(y2))
        except ValueError:
            sys.exit("--years must look like 2015-2025")
    sel = list(PLATFORMS) if a.platform == "all" else [p.strip() for p in a.platform.split(",")]
    for p in sel:
        if p not in PLATFORMS:
            sys.exit(f"Unknown platform {p}. Choose from: {', '.join(PLATFORMS)}")

    results = {p: PLATFORMS[p][1](blocks, mesh, emtree, years, a.lang, a.design) for p in sel}
    if a.json:
        print(json.dumps({PLATFORMS[p][0]: v for p, v in results.items()}, indent=2, ensure_ascii=False))
    else:
        for p in sel:
            print(f"### {PLATFORMS[p][0]}\n```\n{results[p]}\n```\n")
        if "embase" in sel and not emtree:
            print("Note: no --emtree headings given, so the Embase query uses free text only. Look up Emtree terms for better recall.\n")
        if any(len(t) < 4 and has_trunc(t) for ts in blocks.values() for t in ts):
            print("Warning: PubMed needs at least 4 characters before a truncation asterisk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
