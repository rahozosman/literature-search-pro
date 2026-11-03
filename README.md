# Literature Search Pro

A deep, portable skill for finding, verifying, appraising, and documenting scientific articles across PubMed, Google Scholar, ScienceDirect, Scopus, Web of Science, Embase, Cochrane, Europe PMC, OpenAlex, arXiv, IEEE, and more. Every article can be saved as a structured Markdown file.

## What is inside

```
literature-search-pro/
├── SKILL.md                      Core workflow (the file the AI reads first)
├── PORTABLE-PROMPT.md            One-page version to paste anywhere
├── README.md                     This file
├── references/                   Deep guides, loaded only when needed
│   ├── 01-question-framing.md          PICO, PEO, SPIDER, PCC, synonym harvesting
│   ├── 02-pubmed.md                    Field tags, MeSH, filters, E-utilities API
│   ├── 03-google-scholar.md            Operators, snowballing, gray literature, limits
│   ├── 04-sciencedirect-scopus-wos-embase.md   Elsevier and other subscription platforms
│   ├── 05-other-databases.md           Europe PMC, OpenAlex, arXiv, Cochrane, registries, regional DBs, API recipes
│   ├── 06-syntax-translation.md        One strategy translated into 9 platforms
│   ├── 07-screening-and-appraisal.md   Criteria, study design, risk-of-bias tools, GRADE
│   ├── 08-verification-and-integrity.md  Anti-fabrication checks, retractions, predatory journals
│   ├── 09-markdown-article-records.md  The MD record format and folder layout
│   ├── 10-systematic-review-prisma.md  PRISMA 2020, PRISMA-S, dedup, extraction, synthesis
│   ├── 11-output-templates.md          Shapes for answers, reading lists, reviews
│   └── 12-troubleshooting.md           Too many/few results, access, API errors
├── templates/                    article-record.md, search-log.md, evidence-table.md, prisma-flow.md
├── scripts/                      Python 3.8+, no dependencies
│   ├── pubmed_search.py                Search PubMed, write one MD file per article + INDEX.md + CSV
│   ├── build_query.py                  Concept blocks to ready-to-paste queries for 10 platforms
│   └── verify_citation.py              Verify DOI/PMID/title via Crossref, PubMed, Unpaywall
└── examples/worked-example.md    A full run-through
```

## Install

**Claude (claude.ai or app):** Settings, Capabilities, Skills, upload `literature-search-pro.skill` (or the zip). In Claude Code, copy the folder to `~/.claude/skills/literature-search-pro/` (personal) or `.claude/skills/` (project). Then say: "Find recent RCTs on X in PubMed."

**ChatGPT:** (a) Create a Custom GPT: paste `PORTABLE-PROMPT.md` into Instructions and upload the `references/` and `templates/` files as Knowledge; enable web browsing and Code Interpreter if available. (b) Or paste `PORTABLE-PROMPT.md` into a Project's instructions and add the other files to the project.

**Gemini, Copilot, Perplexity, local LLMs:** use `PORTABLE-PROMPT.md` as the system prompt or Gem/Space instructions; attach the reference files if the tool supports files.

**Use the scripts yourself (no AI needed):**
```
python scripts/build_query.py --block "dx=type 2 diabet*;T2DM" --block "tx=exercis*;physical activity" --mesh "dx=Diabetes Mellitus, Type 2" --years 2015-2025 --design rct
python scripts/pubmed_search.py --query '"type 2 diabetes"[tiab] AND exercise[tiab]' --max 50 --out literature --email you@example.com
python scripts/verify_citation.py --doi 10.1038/nature12373 --email you@example.com --oa
```
Set `NCBI_EMAIL` and `NCBI_API_KEY` environment variables to avoid retyping.

## Design principles

1. **No fabricated references.** Mode detection (live, code-only, chat-only) and verification labels keep the AI honest.
2. **Progressive disclosure.** The AI reads a short SKILL.md and opens only the reference file it needs, so it stays fast.
3. **Reproducible.** Every search is logged with the exact string, date, filters, and counts.
4. **Portable.** Plain Markdown and standard-library Python; no vendor lock-in.

## Honest limits

- Paywalled platforms (ScienceDirect, Scopus, WoS, Embase) need institutional access; the skill prepares queries and exports but cannot log in for you.
- Google Scholar has no API; the skill uses it manually or via open alternatives.
- Database interfaces change. The syntax here reflects documentation known at writing time; confirm in the platform's help pages when something errors.
- The scripts were tested for parsing and query generation offline; live API behavior depends on your network and the services' current terms and rate limits.
- AI-assisted screening and appraisal support, but do not replace, dual human review for formal systematic reviews.
