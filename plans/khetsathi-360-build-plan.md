# KhetSathi 360 — Construction Blueprint

Objective: take KhetSathi 360 from validated requirements to a deployed MVP that
returns two trustworthy advisories — fertilizer plan and crop/variety
recommendation — plus a weather feed, in Hindi, for Ghazipur smallholders.

Pre-flight: git repo exists (main), GitHub remote `Vineet-shukl/khetsathi-360`
exists and is reachable, `gh` authenticated with `repo` scope. No CI configured
yet, so step 1 creates it. This plan assumes the validation phase is running;
steps 4 and 5 depend on reference tables, not on interview outcomes, so
implementation can start before validation closes, but no field test may run
before it does.

Conventions: every step is one pull request, one branch, one review. A step is
done only when its verification commands pass and its exit criteria are met.
Rollback for every step is `git revert` of the merge commit plus a cache flush;
no step is irreversible, and no step deletes farmer data.

---

## Dependency Graph

```
S1 scaffold+CI
 └── S2 reference tables
      ├── S3 weather adapter ──┬── S4 fertilizer engine ──┬── S7 API layer ── S8 intake UI ── S9 advisory UI ── S10 deploy
      │                        └── S5 crop/variety engine ┘
      └── S6 mandi + schemes ──────────────────────────────┘
```

Parallel groups: S4 and S5 run in parallel after S3. S6 runs in parallel with S4
and S5. S7 requires S4, S5, and S6. Nothing else parallelizes because S8 onward
share the frontend tree.

---

## Steps

### S1 — Repository scaffold and CI

**Context brief**: Empty repo except docs. Create the monorepo layout
(`src/api`, `src/engine`, `src/adapters`, `src/web`, `tests`), Python project
with `pyproject.toml`, FastAPI app factory, health endpoint, and a GitHub
Actions workflow running ruff, mypy, and pytest on push and PR.

**Tasks**
1. Create directory skeleton and `pyproject.toml` with pinned dependencies.
2. Add FastAPI app factory, `/healthz`, settings loader reading environment.
3. Add `ruff`, `mypy`, `pytest` configuration.
4. Add `.github/workflows/ci.yml` running lint, types, tests on Python 3.12.
5. Add `Dockerfile` for the API and a `docker-compose.yml` with Postgres.

**Verification**
```bash
pytest -q
ruff check src tests
mypy src
docker compose config
```

**Exit criteria**: CI green on the PR; `docker compose up` serves `/healthz`.

**Model tier**: default. **Rollback**: revert PR.

---

### S2 — Reference data tables and loader

**Context brief**: Engines must never hard-code agronomy. Create versioned
reference tables under `data/reference/` (fertilizer grades, FAO-56 Kc values,
eastern-UP crop calendar, zone package rows for rice, wheat, sugarcane, mustard,
gram, potato) with a `source_citation` and `version` per row, and a loader that
seeds PostgreSQL and fails loudly on a row without a citation. Draft tables
already exist in `data/reference/`; this step completes and versions them.

**Tasks**
1. Define the table schema (Markdown source of truth plus a JSON export).
2. Transcribe the eastern plain zone package rows for the six MVP crops from
   the published package-of-practices documents; record page numbers.
3. Write the loader with citation enforcement.
4. Add a validation test: every row has source, version, and plausible ranges.

**Verification**
```bash
python -m src.reference.load --dry-run
pytest tests/reference -q
```

**Exit criteria**: Loader seeds the database; a row missing a citation raises;
golden-set reviewer signs off the transcribed rows.

**Model tier**: default, with expert (mentor/agronomist) review of rows.
**Rollback**: revert PR and re-seed.

---

### S3 — Weather adapter with cache and fallback

**Context brief**: Wrap Open-Meteo. Required daily variables:
`precipitation_sum`, `temperature_2m_max`, `temperature_2m_min`,
`et0_fao_evapotranspiration`, `precipitation_probability_max`,
`wind_speed_10m_max`; hourly `soil_moisture_0_to_1cm`. Round coordinates to a
0.05° grid, cache for 6 hours in `weather_cache`, timeout at 8 seconds, and
serve stale data with an age warning when the upstream fails.

**Tasks**
1. Client with typed response models.
2. Grid rounding and cache read/write.
3. Stale-serve policy and warning field.
4. Recorded-fixture contract tests; no live calls in CI.

**Verification**
```bash
pytest tests/adapters/weather -q
curl -s localhost:8000/v1/weather/1 | jq .alerts
```

**Exit criteria**: Forecast returned offline from cache; stale warning present
when the fixture simulates an upstream 500.

**Model tier**: default. **Rollback**: revert PR; cache rows expire naturally.

---

### S4 — Fertilizer engine

**Context brief**: Deterministic engine per `docs/ARCHITECTURE.md` §5.1. Inputs:
crop, soil test values or block baseline with a quality flag, plot area, target
yield class. Outputs: elemental N, P2O5, K2O; product quantities in kg and bags
(urea 46-0-0, DAP 18-46-0, MOP 0-0-60, SSP 0-16-0); stage split; arithmetic
trail; citations. STCR equations only where a reviewed zone equation exists.

**Tasks**
1. Implement class-based recommendation tables adjusted by soil class.
2. Implement product conversion with DAP N credit deducted from urea.
3. Implement stage split and the arithmetic trail data structure.
4. Build the 50-case golden set from `data/reference` and test agreement.
5. Enforce that every output carries `source_citation`.

**Verification**
```bash
pytest tests/engine/test_fertilizer.py -q
pytest tests/engine/test_golden_set.py -q
```

**Exit criteria**: Golden set ≥ 90% agreement; DAP urea-credit case correct;
no output without a citation.

**Model tier**: strongest available (this is the product's core claim).
**Rollback**: revert PR; engine version bump prevents stale advisories.

---

### S5 — Crop and variety engine

**Context brief**: Constraint filter then explainable ranking per
`docs/ARCHITECTURE.md` §5.2. Hard filters: season, zone, water class, pH/EC
limits, duration versus the next sowing window. Ranking factors must be
returned with weights.

**Tasks**
1. Encode zone eligibility for the six MVP crops and their notified varieties.
2. Implement filters and weighted ranking.
3. Return factor breakdown with each recommendation.
4. Test rejection cases (wrong season, unsuitable pH, duration overflow).

**Verification**
```bash
pytest tests/engine/test_cropfit.py -q
```

**Exit criteria**: All rejection cases pass; every ranked variety has a citation.

**Model tier**: default. **Rollback**: revert PR.

---

### S6 — Mandi and scheme adapters

**Context brief**: OGD mandi prices and a curated scheme table. Mandi: daily
worker pull by commodity and district, stored as snapshots; if the newest
snapshot is older than 7 days, the API reports `stale: true` and the UI hides
the price card. Schemes: PMFBY eligibility and enrolment channels from the
official portal, with a "verify on portal" note and season-checked dates.

**Tasks**
1. OGD client with API key from environment; fixture-based tests.
2. Snapshot table and staleness policy.
3. Scheme seed data with source links.
4. Endpoint tests.

**Verification**
```bash
pytest tests/adapters/test_mandi.py tests/engine/test_schemes.py -q
```

**Exit criteria**: Stale snapshot never shown as current; scheme rows carry a
source link and a season tag.

**Model tier**: default. **Rollback**: revert PR.

---

### S7 — API layer and OTP auth

**Context brief**: Expose v1 endpoints from `docs/ARCHITECTURE.md` §7 behind OTP
auth. Rate-limit OTP (5 per hour per number), hash phone numbers for lookup,
record consent, and use the single error envelope with Hindi and English
messages.

**Tasks**
1. Auth router, JWT issue and verify, rate limiter.
2. Farmer, plot, soil-test routers with ownership checks.
3. Advisory router composing S4, S5, and S6.
4. Error envelope and OpenAPI examples.
5. Tests for authorization boundaries.

**Verification**
```bash
pytest tests/api -q
```

**Exit criteria**: A second farmer cannot read another's advisory; OTP rate
limit enforced; OpenAPI renders with examples.

**Model tier**: default. **Rollback**: revert PR.

---

### S8 — Frontend intake flow (Hindi)

**Context brief**: React PWA with village search, plot entry, and soil entry
(SHC values, lab photo for manual transcription, or block baseline with a
visible estimate warning). Hindi strings in a JSON catalog; no hard-coded copy.
Large targets, 360 px baseline.

**Tasks**
1. Scaffold Vite React app with routing and i18n catalog.
2. Village search against a static table; plot form with validation.
3. Soil form with three input paths and the quality flag surfaced.
4. PWA manifest and service worker caching the shell.
5. Component tests for validation and the estimate warning.

**Verification**
```bash
npm --prefix src/web test -- --run
npm --prefix src/web run build
```

**Exit criteria**: A farmer can complete intake in Hindi; offline reload shows
the cached shell; no English string in the farmer path.

**Model tier**: default. **Rollback**: revert PR.

---

### S9 — Advisory UI with arithmetic trail

**Context brief**: Render the advisory card: ranked crops and varieties, the
fertilizer plan in bags by stage, the arithmetic trail expandable, weather strip
with alerts, and a print stylesheet so the card can be carried to the dealer.

**Tasks**
1. Advisory card components and print CSS.
2. Expandable "why this number" panel sourced from `sources_json`.
3. Weather strip and alert banners in Hindi.
4. Accessibility pass (contrast, focus order, text scaling).
5. Snapshot tests for the card.

**Verification**
```bash
npm --prefix src/web test -- --run
npm --prefix src/web run build
npx playwright test
```

**Exit criteria**: Card prints on one A4 page; every number finds its citation
in one tap; Playwright happy path green.

**Model tier**: default. **Rollback**: revert PR.

---

### S10 — Deployment and field-test instrumentation

**Context brief**: Ship the MVP to a live URL and instrument it for the field
test. Docker Compose on a single VM behind Caddy with TLS; nightly database
backup; privacy-respecting event log (advisory generated, viewed, printed) with
no content beyond ids and engine version.

**Tasks**
1. Compose stack with api, web, worker, db, caddy; environment template.
2. Backup job and one restore rehearsal.
3. Event instrumentation and a simple admin query for the field test.
4. Runbook: deploy, rollback, rotate secrets.
5. Field-test link and QR for the mentor and farmer sessions.

**Verification**
```bash
docker compose -f docker-compose.prod.yml config
curl -s https://<host>/healthz
```

**Exit criteria**: Live URL serves the intake flow; rollback rehearsed once;
backup restore verified.

**Model tier**: default. **Rollback**: previous image tag redeploy.

---

## Invariants (checked after every step)

1. No advisory output without `source_citation`.
2. No agronomic constant outside `data/reference`.
3. No external API call in the request path without timeout and cache.
4. All tests and lint green before merge.
5. Hindi in the farmer path; English allowed only in developer surfaces.

## Adversarial Review Pass

Performed against this plan before commit. Findings applied:

| Finding | Severity | Resolution |
| --- | --- | --- |
| Plan had no accuracy harness, so "MVP works" would be untestable | High | Golden-set tasks and thresholds added to S4 and S5 |
| Reference transcription was one bullet with no review gate | High | Citation enforcement plus expert review in S2 exit criteria |
| Weather adapter had no failure policy | High | Stale-serve policy and fixture tests in S3 |
| Privacy and consent absent | Medium | OTP hashing and consent record in S7; DPDP note in architecture |
| Hindi copy could ship unreviewed | Medium | S8 exit criterion "no English in farmer path"; native-speaker review before S10 |
| Deployment had no rollback rehearsal | Medium | Rollback rehearsal added to S10 |

Not fixed, deliberately: no load testing (pilot scale is tens of users) and no
multi-region (irrelevant at this stage).

## Mutation Protocol

A step may be split, reordered, skipped, or abandoned only by editing this file
with a dated note in the change description. A skipped step leaves its invariants
in force. A new step must declare its dependencies and its verification command.

---

*Blueprint for the 1M1B internship prototype. Execution starts at S1; S4 is the
highest-risk step and the one to staff most carefully.*
