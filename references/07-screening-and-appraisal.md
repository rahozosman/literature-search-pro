# 07. Screening and Critical Appraisal

Finding papers is half the job. Deciding which ones to trust, and how much, is the other half.

## Contents
1. Inclusion and exclusion criteria
2. Two-stage screening
3. Evidence hierarchy
4. Study design identification
5. Risk-of-bias and quality tools
6. Red flags checklist
7. Grading certainty (GRADE)
8. Quick appraisal template

## 1. Inclusion and exclusion criteria

Write them **before** viewing results. Template:

| Domain | Include | Exclude |
|---|---|---|
| Population | Adults ≥18 with T2DM | Type 1, gestational, animal studies |
| Intervention/exposure | Supervised aerobic or resistance exercise ≥8 weeks | Single-session studies |
| Comparator | Usual care or no exercise | None required for single-arm studies? (decide) |
| Outcome | HbA1c reported | No glycemic outcome |
| Design | RCTs, controlled trials | Case reports, editorials |
| Language/date | English, 2010 to 2025 | Other |
| Status | Peer-reviewed | Preprints, conference abstracts (decide) |

Reasons for exclusion at full-text stage must be recorded (needed for PRISMA).

## 2. Two-stage screening

1. **Title and abstract**: be inclusive; exclude only clear misses. Mark: Include / Exclude / Maybe.
2. **Full text**: apply all criteria. Record one primary exclusion reason (wrong population, wrong design, wrong outcome, duplicate, no full text, etc.).

For formal reviews, use **two independent reviewers** with a third to resolve conflicts; report agreement (Cohen's kappa). When Claude acts as a single screener, state that clearly and flag borderline items for human review.

## 3. Evidence hierarchy (therapy/intervention questions)

1. Systematic reviews and meta-analyses of RCTs
2. Individual randomized controlled trials
3. Non-randomized controlled studies and cohort studies
4. Case-control studies
5. Cross-sectional studies, case series
6. Case reports
7. Mechanistic/animal/in vitro studies and expert opinion

The hierarchy shifts with the question:
- **Prognosis/etiology**: well-conducted cohorts can be top-tier.
- **Diagnostic accuracy**: cross-sectional with reference standard (QUADAS-2).
- **Qualitative experience**: qualitative syntheses (CASP, JBI).
- **Rare harms**: observational/pharmacovigilance data.
A flawed RCT can be weaker than a good cohort. Level does not replace appraisal.

## 4. Identifying study design (do not trust labels blindly)

| If you see | It is likely |
|---|---|
| Random allocation + control group | RCT (check method of randomization) |
| Groups assigned by clinician/patient choice, no randomization | Non-randomized/quasi-experimental |
| Follow people forward by exposure, measure outcomes | Prospective cohort |
| Start from outcome, compare past exposure | Case-control |
| One time point, prevalence | Cross-sectional |
| Systematic methods, PRISMA flow, search strategy | Systematic review |
| Narrative summary with no methods | Narrative review (lower rigor) |
| Pooled estimate with heterogeneity | Meta-analysis |
| Pre-registered protocol, scoping aims, no pooled effect | Scoping review |
| Single patient/family | Case report |
| "Pilot", "feasibility" | Small, not powered for efficacy |

Authors mislabel designs ("prospective study" that is a retrospective chart review; "randomized" with inadequate allocation). Read Methods.

## 5. Risk-of-bias and quality tools

| Design | Tool |
|---|---|
| RCT | **Cochrane RoB 2**; Jadad (older, limited) |
| Non-randomized interventions | **ROBINS-I** |
| Cohort / case-control | **Newcastle-Ottawa Scale**, JBI checklists |
| Cross-sectional | **JBI**, AXIS |
| Diagnostic accuracy | **QUADAS-2** |
| Prognostic | **PROBAST** |
| Systematic reviews | **AMSTAR 2**, **ROBIS** |
| Qualitative | **CASP**, JBI Qualitative, COREQ/SRQR for reporting |
| Animal studies | **SYRCLE** |
| Case reports | JBI case report checklist, CARE |
| Economic evaluations | CHEERS, Drummond |
| Reporting standards (not quality tools) | CONSORT (RCT), STROBE (observational), PRISMA (SR), STARD (diagnostic), TRIPOD (prediction), ARRIVE (animal) |

**RoB 2 domains (RCT)**: randomization process; deviations from intended interventions; missing outcome data; measurement of outcome; selection of reported result. Overall: low / some concerns / high.

## 6. Red flags checklist

- [ ] Tiny sample with large claimed effect; no power calculation
- [ ] No pre-registration (RCTs should be registered; check ClinicalTrials.gov/ISRCTN) or outcomes differ from registry
- [ ] Surrogate outcomes only, selective reporting, many subgroup analyses
- [ ] p-values just under 0.05 everywhere; no effect sizes or confidence intervals
- [ ] High or unbalanced attrition, no intention-to-treat analysis
- [ ] Industry funding or conflicts not disclosed; spin in the abstract versus results
- [ ] Conclusions beyond data (causal language from observational data)
- [ ] Journal red flags: unusually fast peer review, no editorial board, not in DOAJ/MEDLINE/Scopus, aggressive solicitation (see `08`)
- [ ] Retracted or has an expression of concern (see `08`)
- [ ] Duplicate or salami publication from the same dataset
- [ ] Animal or in vitro result presented as human evidence

## 7. Grading certainty (GRADE)

Start RCT evidence high, observational low. **Downgrade** for risk of bias, inconsistency, indirectness, imprecision, publication bias. **Upgrade** observational for large effect, dose-response, plausible confounding that would reduce the effect. Final levels: **High, Moderate, Low, Very low**. When summarizing a body of evidence, state the certainty explicitly and the reasons.

## 8. Quick appraisal template (per article)

```
Design: ...
Sample/setting: n=..., ...
Key result: effect size (95% CI), p
Risk of bias: Low / Some concerns / High (domains: ...)
Limitations stated: ...
Limitations I see: ...
Funding/COI: ...
Applicability to the user's question: High / Medium / Low
Verdict: Rely / Use with caution / Background only / Exclude
```
