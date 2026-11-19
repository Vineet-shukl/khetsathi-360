# Scholar Evaluation: KhetSathi 360 PRD and Construction Blueprint

Artifact type: research-and-engineering proposal (product requirements document
plus architecture specification plus build blueprint).
Scope: comprehensive. Evaluator position: independent reviewer, not the author.

## Overall Assessment

- Overall score: 3 / 5
- Confidence: high
- Summary: The proposal is well structured, unusually honest about what it does
  not know, and its engineering plan is concrete and testable. Its central
  weakness is evidentiary: the problem it solves rests on four unvalidated field
  observations with zero interviews completed, and its competitive and agronomic
  claims lean on general knowledge rather than cited sources. The data-source
  catalog is careful enough to be usable, but several load-bearing sources were
  unreachable during drafting. As a proposal it is defensible; as a validated
  requirement document it is not yet ready, and it says so itself, which is the
  right posture.

## Dimension Scores

| Dimension | Score | Evidence | Revision priority |
| --- | ---: | --- | --- |
| Problem and question | 4 | Four observations mapped to four decisions (soil, seed, weather, fertilizer); scope boundaries explicit. Weakness: all observations carry "Under Investigation — 0 interviews" | Medium |
| Literature and context | 2 | Competitor sketch (Kisan Suvidha, Plantix, DeHaat, AgroStar, Krishify) is from general knowledge, no dates, no sources; Soil Health Card critique is asserted without citation | High |
| Methodology | 3 | Field protocol is well designed (consent, coding frame, verdict rules, stated biases). Not executed. Engine validation via golden set is sound in principle | High |
| Data and evidence | 2 | Zero primary data; Open-Meteo verified; OGD page served a sandbox placeholder; Agmarknet has no official API; PMFBY portal is JavaScript-only; package-of-practices PDFs not obtained | High |
| Analysis | 3 | STCR equation form stated correctly in general terms; fertilizer conversion arithmetic shown and checkable. No baseline, no sensitivity analysis, no error propagation from soil-test error | Medium |
| Results and interpretation | N/A | No results exist yet; not applicable to a pre-implementation proposal | - |
| Limitations | 4 | Limitations stated specifically: self-reported fertilizer amounts, facilitator sampling bias, one-district generalisation, accuracy ceiling set by soil input quality | Low |
| Writing and structure | 4 | Clear sectioning, decisions log, invariant list, mutation protocol. Occasional length | Low |
| Citations | 2 | Sources labelled by verification status, which is honest, but most scholarly and competitive claims lack references; FAO-56 tables cited by paper, not page | High |

## Critical Issues

1. **Unvalidated problem.** Every requirement descends from OBS-01 to OBS-04, and
   none has data behind it. The PRD mitigates this by labelling assumptions, but
   the build plan (S4, S5) can proceed without validation, so the product may be
   built for a problem the field does not confirm.
2. **Advisory accuracy depends on unretrieved documents.** The fertilizer and
   variety engines are only as good as the transcribed eastern-plain package of
   practices, and those documents were not obtained. The plan correctly makes S2
   a blocker, but the proposal should not claim 90% golden-set agreement before a
   source document exists.
3. **Neutrality claim is untested.** "The platform sells nothing" is a stated
   differentiator but has no evidence that farmers trust free advice more than
   dealer advice; the field protocol includes trust questions but the hypothesis
   is not wired into a metric.
4. **Data availability risks are under-costed.** OGD returned a sandbox
   placeholder, Agmarknet lacks an API, and IMD has no self-serve feed. The
   mandi and scheme features are "Should", not "Must", which limits blast radius,
   but the PRD should state what the product looks like if mandi data never
   arrives cleanly.

## Recommended Revisions

1. Execute and code the 10–15 interviews before Phase 4; write verdicts into the
   Evidence table and revise or delete any requirement contradicted by them.
2. Obtain the zone package documents and record document, edition, and page per
   reference row; downgrade the 90% claim to "target pending source review".
3. Replace the competitor paragraph with dated, linked sources (company filings,
   app store listings, government scheme pages) or mark it explicitly as
   author's general knowledge.
4. Add a sensitivity note: how much does the fertilizer plan change if soil
   values are wrong by one class? This is the honest way to state accuracy.
5. Define the liability and disclaimer text with the mentor before field
   testing, since farmers will act on the output.
6. Add an explicit fallback specification: what the product does when mandi and
   scheme data are unavailable for a district.

## Evidence Checks Needed

- [ ] Farmer interview dataset, coded, with verdicts per observation.
- [ ] Zone package-of-practices PDF with page citations for each reference row.
- [ ] OGD mandi resource ID confirmed live, with response sample.
- [ ] PMFBY premium shares and UP enrolment window read from the portal by a human.
- [ ] At least one cited evaluation of Soil Health Card interpretation/adoption.
- [ ] Competitor claims (users served, business model) replaced with dated sources.

---

*Evaluation produced against the PRD, architecture specification, and build
blueprint as committed in this repository.*
