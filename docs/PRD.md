# KhetSathi 360 — Product Requirements Document

> **Status: DRAFT — not yet validated.** The evidence base is preliminary. The
> field-validation milestone (10–15 farmer interviews in Ghazipur) is incomplete,
> so the problem statements below rest on the owner's observations, not on
> collected data. Sections marked *Assumption* must not be treated as findings.
> Source of record: the 1M1B project workbook (Dashboard, Overview, Work Tracker,
> Farmer Research, Milestone Tracker sheets). Timing lives in that tracker; this
> document is deliberately date-free.

- Program: 1M1B Green Internship — YIRP
- Owner: Vineet Shukla
- Domain: Agriculture / Environment / Sustainable Development
- Field area: Ghazipur district and eastern Uttar Pradesh
- Product: software-based agricultural decision-support platform (AgriTech)

---

## Problem Statement

Smallholder and marginal farmers in eastern Uttar Pradesh make four
high-consequence decisions every season with almost no local, scientific
information: what their soil lacks, which seed variety fits their land and
water, when weather will break their plan, and how much fertilizer and water to
apply. The cost of not solving this is paid twice: lower yields from the wrong
crop, variety, or timing, and inflated input bills from over-applied urea and
DAP that acidify soil and reduce nutrient-use efficiency. Public guidance
exists (Soil Health Cards, ICAR package of practices, IMD bulletins, scheme
portals) but it is fragmented, printed, generic, or behind portals a smallholder
does not use.

## Evidence

| ID | Observation | Status |
| --- | --- | --- |
| OBS-01 | Soil health cards are rarely used; farmers lack timely access to testing labs and cannot interpret the card. | Under Investigation — 0 interviews completed |
| OBS-02 | Seed choice is driven by local agro-dealers, not agro-climatic suitability or certified seed. | Under Investigation — 0 interviews completed |
| OBS-03 | Unseasonal rain and delayed monsoon cause recurring yield loss; no micro-climate alerts reach farmers. | Under Investigation — 0 interviews completed |
| OBS-04 | Over-reliance on urea and DAP causes nutrient imbalance and inflated input spend. | Under Investigation — 0 interviews completed |

**Assumption — needs validation** through the 10–15 structured interviews
defined in `docs/FIELD-RESEARCH-PROTOCOL.md`. Until those are coded, every
"farmer wants X" sentence in this PRD is a hypothesis, not a requirement.
Secondary evidence that the problem class is real (not specific to these
villages): documented critique of blanket, non-site-specific Soil Health Card
recommendations and low card-interpretation rates in Indian policy literature.

## Proposed Solution

A Hindi-first web application and installable PWA that turns four inputs — the
farmer's village, plot size and irrigation source, a soil test (the farmer's own
Soil Health Card values, a lab report, or a block-level baseline), and the
season — into one explainable advisory: ranked crops and notified varieties for
the agro-climatic zone, a fertilizer plan expressed in bags of named products
split across growth stages, an irrigation calendar driven by reference
evapotranspiration and forecast rainfall, a 7–16 day weather alert feed, local
mandi price context, and a scheme eligibility checklist including PMFBY.

The differentiator is not the data; it is the translation. Every recommendation
displays the arithmetic, the rule, and the source it came from, so a farmer or
an extension worker can check it. The platform sells nothing, so its advice is
not steered toward a particular input dealer.

## Key Hypothesis

We believe a soil-test-driven, zone-specific, explainable advisory will change
fertilizer and variety decisions for Ghazipur smallholders.
We will know we are right when, in the pilot cohort, at least 60% of farmers can
restate their recommended fertilizer dose unaided two weeks after receiving it,
and at least 30% report changing one input decision in the following season.

## What We Are NOT Building

- **Input marketplace or dealer ordering** — the advisory must stay neutral; a
  sales channel would compromise that and is a different business.
- **Credit, lending, or insurance distribution** — the navigator explains PMFBY
  eligibility and enrolment channels; it does not sell cover.
- **Image-based disease diagnosis** — Plantix-class computer vision needs a
  labelled image corpus we do not have; v1 covers nutrient and water disorders
  only through rule logic.
- **Satellite yield prediction or remote sensing analytics** — high cost, low
  explainability for a farmer, outside MVP.
- **Own soil testing lab** — we consume test results; we do not produce them.
- **Its own weather model** — we consume open forecast APIs.

## Success Metrics

| Metric | Target | How Measured |
| --- | --- | --- |
| Advisory agreement with ICAR/state package of practices | ≥ 90% on a 50-case golden set | Expert review of engine outputs against `data/reference` tables |
| Farmer comprehension of the fertilizer plan | ≥ 60% restate dose unaided after 2 weeks | Follow-up structured interview |
| Behaviour change | ≥ 30% report one changed input decision in one season | Season-end survey |
| Advisory generation latency (cached) | p95 under 800 ms | API metrics |
| Field-validation target | 10–15 interviews coded | `docs/FIELD-RESEARCH-PROTOCOL.md` |

## Open Questions

- [ ] Do farmers value an explainable advisory over a simple "do this" card?
  Comprehension and trust may pull in opposite directions.
- [ ] Which soil input is realistic at scale: Soil Health Card values, paid lab
  tests, or block-level baselines? This decides the accuracy ceiling.
- [ ] Is a smartphone PWA reachable for the target user, or is SMS/IVR the real
  channel? Shared-device and literacy constraints are unresolved.
- [ ] Can Agmarknet/mandi data be obtained reliably without scraping?
- [ ] What is the liability posture when advice is wrong? What disclaimer and
  escalation path does the mentor require?

---

## Users & Context

**Primary User**
- **Who**: A smallholder with 0.5–2 ha in Ghazipur district, eastern UP,
  growing rice, wheat, and often sugarcane; Hindi or Bhojpuri speaker; buys
  inputs from the village dealer on credit.
- **Current behavior**: Asks the dealer, copies a neighbour, applies urea on
  habit, ignores the Soil Health Card, checks rain by looking up.
- **Trigger**: Sowing window opens, the soil card arrives, a weather warning is
  heard on TV, or a crop shows yellowing.
- **Success state**: Holds a plan for the season that names the variety, the
  fertilizer bags and dates, and the irrigation days, and can explain why.

**Job to Be Done**
When a season starts and money for inputs is short, I want a plan tailored to my
own soil and water so I can spend on the right inputs and not lose the crop to a
preventable mistake.

**Non-Users**
Large commercial farms and agribusinesses (different economics, already served).
Export-oriented horticulture. FPO managers are a secondary user at most, not a
v1 design target.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
| --- | --- | --- |
| Must | Farmer and plot profile (village, area, irrigation source) | Every advisory is location- and water-dependent |
| Must | Soil test entry and interpretation, with SHC fallback to block baseline | Without soil values the fertilizer engine is generic, which is the failure mode we exist to fix |
| Must | Fertilizer plan in named products and bags, split by stage, with arithmetic shown | Highest-cost decision, clearest waste, most checkable output |
| Must | Crop and variety recommendation by zone, season, water, and soil constraints | Second-highest consequence decision; uses published zone packages |
| Must | 7–16 day weather forecast and threshold alerts | Cheap to deliver, high perceived value, protects spraying and irrigation timing |
| Must | Hindi UI with plain-language agronomy terms | Target user cannot use an English interface |
| Should | Irrigation scheduler from Kc × ET0 minus effective rainfall | High value, needs plot-level water balance to be trustworthy |
| Should | Mandi price context for the chosen crop near the farmer | Reduces distress selling; depends on data access |
| Should | Scheme navigator (PMFBY and state schemes) with eligibility checklist | Unclaimed benefits are a documented gap |
| Should | Offline-capable PWA with cached last advisory | Rural connectivity is intermittent |
| Could | WhatsApp or SMS delivery of stage reminders | Matches real usage; needs a gateway and cost model |
| Could | Voice input/output in Hindi/Bhojpuri | Literacy barrier is real; heavy to build |
| Could | Disease diagnosis from photos | Needs a labelled corpus and expert validation |
| Won't (v1) | Marketplace, credit, insurance sales, satellite analytics, own weather model | Out of scope; see "What We Are NOT Building" |

### MVP Scope

The minimum to test the hypothesis: a single farmer can enter a plot and soil
values, pick a season, and receive (a) a crop and variety recommendation and (b)
a fertilizer plan with product quantities and arithmetic, in Hindi, plus a
weather forecast. Irrigation, mandi, and schemes can follow once the core two
advisories are trusted.

### User Flow

1. Open the PWA, choose village (search by name or pin on map).
2. Enter plot: area, irrigation source, current or planned crop.
3. Enter soil: type in Soil Health Card values, upload a lab report photo for
   manual transcription, or accept the block baseline (clearly labelled as an
   estimate).
4. Receive advisory card: crop and variety ranked, fertilizer bags by stage,
   the rule and source behind each number.
5. Save, print, or share the card; receive stage reminders if a channel is
   enabled.
6. Return at the next stage; the plan updates with weather and price context.

---

## Technical Approach

**Feasibility**: HIGH for the MVP as specified, MEDIUM for advisory accuracy.
The data sources are mostly open, the agronomic rules are published, and the
engineering is conventional. The accuracy ceiling is set by soil-input quality
and by how faithfully published zone packages are transcribed.

**Architecture Notes**
- React PWA frontend, FastAPI backend, PostgreSQL, nightly ingestion worker.
  Full design in `docs/ARCHITECTURE.md`.
- Rules first, ML later: the fertilizer and variety engines are deterministic
  and explainable; a learned model may sit on top once field outcomes exist.
- Every output carries `rule_id`, `source`, and `engine_version` so an expert
  can audit it.
- Open-Meteo is the primary weather source (no key, documented variables);
  data.gov.in (OGD) is the primary path for mandi and IMD-derived datasets.
  Source-by-source verification status is in `docs/API-CATALOG.md`.

**Technical Risks**

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Zone package tables transcribed with errors | M | Golden-set review against source PDFs; cite page numbers |
| Open data API changes or rate limits | M | Cache in Postgres; adapter layer with a second source per feed |
| Soil input missing or garbage | H | Explicit input quality flag; degrade to block baseline with a visible warning |
| Farmer cannot use a smartphone UI | M | Hindi-first, large touch targets, printable card as the fallback artifact |
| Advice causes loss and blame follows | L | Position as guidance with the arithmetic shown; disclaimers; no pesticide dosing in v1 |

---

## Implementation Phases

Status values follow the tracker vocabulary (pending / in progress / complete).
Phases are ordered by dependency; dates are intentionally omitted.

| # | Phase | Description | Status | Parallel | Depends |
| --- | --- | --- | --- | --- | --- |
| 1 | Validation | Farmer interviews, coding, problem confirmation | in progress | - | - |
| 2 | Requirements | This PRD signed off; personas and scope fixed | in progress | - | 1 |
| 3 | Data and architecture | Source verification, reference tables, architecture spec | in progress | with 2 | 1 |
| 4 | Prototype | Engine, API, and Hindi intake UI for the two core advisories | pending | - | 3 |
| 5 | Field testing | Demo to 5+ farmers and mentor; usability and accuracy fixes | pending | - | 4 |
| 6 | Deployment | Live deployment, user guide, internship report | pending | - | 5 |

### Phase Details

**Phase 1: Validation**
- **Goal**: Replace assumption-level observations with coded interview data.
- **Scope**: 10–15 interviews per `docs/FIELD-RESEARCH-PROTOCOL.md`; validation
  verdict per observation.
- **Success signal**: At least 60% of respondents independently report the
  pain behind OBS-01 to OBS-04, or the scope is revised to match what they do
  report.

**Phase 4: Prototype**
- **Goal**: Two trustworthy advisories end to end, in Hindi.
- **Scope**: Fertilizer engine and crop/variety recommender, weather adapter,
  intake flow, advisory card, golden-set tests.
- **Success signal**: 50-case golden set at 90% agreement with published
  package of practices.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
| --- | --- | --- | --- |
| Weather source | Open-Meteo primary | IMD paid feed, OpenWeatherMap, NASA POWER | Documented, keyless for non-commercial use, 16-day horizon, soil moisture included; IMD has no self-serve open API |
| Advisory engine | Deterministic rules with citations | ML-first recommendation | Explainability and auditability beat marginal accuracy at this stage; no training outcomes exist yet |
| Frontend | React PWA (Vite) | Next.js, native app | Offline caching and low payload matter more than SSR; install-free |
| Language | Hindi first | English first, bilingual | Target user; English UI would invalidate the usability test |
| Soil input | SHC values plus block baseline fallback | Require lab test | Requiring a lab test would exclude most target users |
| Mandi data | OGD/Agmarknet mirror with cached snapshots | Live scraping, eNAM partner access | Scraping is fragile; eNAM access is restricted |

---

## Research Summary

**Market Context**
Government and private advisory tools exist and each leaves a gap this product
targets. Kisan Suvidha aggregates services but offers shallow, generic advice and
dated UX. Plantix excels at photo diagnosis but not at soil or fertilizer
arithmetic. DeHaat and AgroStar bundle advice with input retail, which creates a
neutrality question and a purchase-volume threshold that marginal farmers may
not clear. Krishify is peer-to-peer, fast and vernacular, but unverified. The
open position is a public-good, explainable, soil-first advisory that sells
nothing.

**Technical Context**
Open-Meteo's forecast API was verified this session: keyless non-commercial use,
16-day horizon, `precipitation_sum`, `temperature_2m_max/min`,
`et0_fao_evapotranspiration`, hourly soil moisture. The OGD platform
(`data.gov.in`) documents an API-key REST pattern but its API listing page
currently serves a sandbox placeholder, so resource identifiers must be resolved
individually. Agmarknet publishes no official REST API; the OGD mirror is the
practical route. District agromet bulletins exist as pages, not feeds. ICAR and
state package-of-practices documents are PDFs that must be transcribed by hand
into reference tables, which is a real cost and a source of error.

---

*Drafted from the 1M1B project workbook. Status: DRAFT — needs field validation
and mentor sign-off.*
