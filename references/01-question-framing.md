# 01. Question Framing

A search is only as good as the question behind it. Spend a few minutes here to save hours later.

## Contents
1. Choose a framework
2. Turn a topic into concepts
3. Synonym harvesting
4. Scope decisions
5. Worked examples

## 1. Choose a framework

| Framework | Use for | Elements |
|---|---|---|
| **PICO** | Clinical effectiveness/therapy | Population, Intervention, Comparator, Outcome |
| **PICOS / PICOTS** | Reviews needing design/time | + Study design, Timeframe |
| **PECO** | Exposures, risk, environmental | Population, Exposure, Comparator, Outcome |
| **PEO** | Qualitative, experiences | Population, Exposure, Outcome |
| **SPIDER** | Qualitative/mixed methods | Sample, Phenomenon of Interest, Design, Evaluation, Research type |
| **SPICE** | Services, social science | Setting, Perspective, Intervention, Comparison, Evaluation |
| **PCC** | Scoping reviews (JBI) | Population, Concept, Context |
| **PIRD** | Diagnostic accuracy | Population, Index test, Reference standard, Diagnosis |
| **PFO** | Prognosis | Population, Prognostic Factor, Outcome |
| **ECLIPSE** | Health policy/management | Expectation, Client group, Location, Impact, Professionals, Service |

If the topic is not clinical (e.g., machine learning, materials), skip the framework and list concepts directly: **object, method, application, context**.

## 2. Turn a topic into concepts

Vague: "Does coffee affect heart health?"

| Concept | Terms |
|---|---|
| Exposure | coffee, caffeine, caffeinated beverages |
| Outcome | cardiovascular disease, myocardial infarction, stroke, blood pressure, arrhythmia |
| Population (optional) | adults, general population |
| Design (optional) | cohort, meta-analysis |

Rules of thumb:
- **2 to 3 concepts** is the sweet spot. Each added `AND` shrinks results and risks missing relevant papers.
- For a broad review, search exposure + outcome and filter population and design at screening; this is more sensitive.
- Skip concepts that are poorly indexed (e.g., "adults", "quality of life") in the strategy and apply them at screening.

## 3. Synonym harvesting

For each concept, gather:

- **Controlled vocabulary**: MeSH (PubMed/MEDLINE/Cochrane), Emtree (Embase), APA Thesaurus (PsycINFO), CINAHL Headings
- **Synonyms and near-synonyms**: myocardial infarction / heart attack / MI
- **Acronyms and abbreviations**: T2DM, COPD (check ambiguity: "MS" = multiple sclerosis or mass spectrometry)
- **Spelling variants**: randomized/randomised, tumor/tumour, anemia/anaemia, pediatric/paediatric
- **Plurals and endings**: use truncation (`diabet*`) carefully
- **Older/newer terminology**: historical terms vs current ones (e.g., "mental retardation" vs "intellectual disability")
- **Brand vs generic drug names**: Lipitor / atorvastatin
- **Narrower terms**: MeSH explodes narrower terms by default in PubMed

Where to find terms fast:
1. Look up the term in the **MeSH Database** and read "Entry Terms".
2. Read the title, abstract, and keywords of 3 to 5 known relevant papers.
3. Check published search filters and strategies for the topic (Cochrane, InterTASC ISSG).
4. Ask the user for seed papers.

## 4. Scope decisions (decide before searching)

Write these down; they become inclusion/exclusion criteria (see `07`):

- Date range (justify; do not cut arbitrarily)
- Languages (English-only introduces bias; say so if used)
- Study designs
- Populations (age, setting, species: human vs animal)
- Publication status (peer-reviewed only, or preprints and gray literature)
- Minimum sample size or quality (state explicitly if used)

## 5. Worked examples

**Clinical (PICO)**
Question: In adults with knee osteoarthritis, does intra-articular hyaluronic acid reduce pain compared with placebo?
- P: knee osteoarthritis, adults
- I: intra-articular hyaluronic acid (viscosupplementation)
- C: placebo or saline
- O: pain (VAS, WOMAC)
Search concepts: P AND I (outcome and comparator handled at screening; design filter optional)

**Qualitative (SPIDER)**
Question: How do nurses experience moral distress in ICUs?
- S: nurses; P: moral distress; D: interviews, focus groups; E: experiences, perceptions; R: qualitative

**Non-clinical**
Question: What deep learning methods detect defects in solar panels?
Concepts: (deep learning OR CNN OR "neural network*") AND (defect OR fault OR crack) AND ("solar panel*" OR photovoltaic)

## Output of this step

A short block to paste into the search log:
```
Question: ...
Framework: ...
Concepts: 1) ... 2) ... 3) ...
Scope: dates ..., languages ..., designs ...
Seed papers (known relevant): ...
```
