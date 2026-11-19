# KhetSathi 360 — Data Source and API Catalog

Every external source the advisory engines may consume, with its access path,
licence, observed limits, verification status, and fallback. Status vocabulary:

- **Verified** — endpoint, parameters or access path confirmed directly in this
  session, with the observation quoted.
- **Documented** — official documentation read, not exercised end to end.
- **Blocked** — access attempted and refused, unreachable, or the portal is
  JavaScript-only and could not be read programmatically.
- **To obtain** — a document or key a human must collect before the feed works.

No adapter may be built against a **Blocked** or **To obtain** row. The
fallback column in the decision matrix says what the product does meanwhile.

---

## 1. Weather — Open-Meteo

| Field | Detail |
| --- | --- |
| Status | **Verified** |
| Licence | CC BY 4.0; attribution and indication of modification are mandatory |
| Cost | Free for non-commercial use, no API key. Commercial use requires a paid plan and a key on `customer-api.open-meteo.com` |
| Forecast endpoint | `https://api.open-meteo.com/v1/forecast` |
| Historical access | Historical Weather API; archive and climate APIs are paid-tier features |

Observed free-tier limits (`open-meteo.com/en/pricing`, read this session):
600 calls/min, 5,000 calls/hour, 10,000 calls/day, 300,000 calls/month, with no
uptime guarantee and no commercial use.

Daily variables the engine requires (names verified against the docs page):

| Purpose | Parameter |
| --- | --- |
| Max / min temperature | `temperature_2m_max`, `temperature_2m_min` |
| Rain total | `precipitation_sum` |
| Rain probability | `precipitation_probability_max` |
| Reference evapotranspiration | `et0_fao_evapotranspiration` |
| Wind (spray window) | `wind_speed_10m_max`, `wind_gusts_10m_max` |
| Radiation | `shortwave_radiation_sum` |

Hourly soil moisture (hourly only; not available in the daily block):
`soil_moisture_0_to_1cm`, `soil_moisture_1_to_3cm`, `soil_moisture_3_to_9cm`,
`soil_moisture_9_to_27cm`, `soil_moisture_27_to_81cm`.

Rules: `timezone` is mandatory when `daily` is used; `forecast_days` 0–16;
`past_days` 0–92. One request counts as more than one call if it exceeds ten
variables or two weeks for one location, so batch by grid cell, not by farmer.

**Cache policy**: round coordinates to 0.05°, cache for 6 hours, serve stale
with an age warning when upstream fails.
**Fallback**: NASA POWER (free, keyless, point daily rainfall and temperature)
for retrospective climatology only; no live fallback for forecast.

**Attribution text** (render in the UI footer): "Weather data by
Open-Meteo.com (CC BY 4.0), modified for local advisory."

---

## 2. Mandi prices — Agmarknet 2.0 and the OGD mirror

| Field | Detail |
| --- | --- |
| Status | **Blocked** for direct API; **To obtain** for a live resource ID |
| Official API | None published. Agmarknet is a report portal, not an API service |
| Current platform | Agmarknet 2.0. All 251 agricultural mandis in Uttar Pradesh were reported connected by September 2026 |
| Practical route | OGD mirror: "Current Daily Price of Various Commodities from Various Markets (Mandi)" on `data.gov.in`, consumed through `api.data.gov.in` |
| Portal behaviour | `agmarknet.gov.in` returns a thin 2.0 shell (about 1 KB) to a plain HTTP client; report access is browser-driven |

**data.gov.in contract (verified by behaviour, documented by platform):**

- A keyless request to a resource endpoint returned
  `{"error": "Authorization field missing"}` — a key is mandatory.
- A request carrying an unrecognised key returned
  `{"error": "Rate limit exceeded"}`, so the platform rejects before serving.
- Documented pattern:
  `https://api.data.gov.in/resource/<resource-id>?api-key=<KEY>&format=json&limit=100&offset=0`
  with `filters[field]=value` and `fields=` for projection.
- Formats: JSON, XML, CSV.

**To obtain before building the adapter**: the current resource ID for the mandi
price dataset (OGD reissues IDs; the widely circulated
`9ef84268-d588-465a-a308-a864a43d0070` could not be confirmed live this
session), and a personal API key from a registered `data.gov.in` account.

**Design consequence**: mandi is a *Should* capability, so the product must be
complete without it. If no clean daily feed exists by prototype freeze, the
price card is removed rather than shipped stale, and the scheme card absorbs
the "market awareness" job with a link to Agmarknet's public report page.

**Fallback**: cached snapshots with a visible date, hidden after 7 days; never
scrape inside a request path.

---

## 3. Soil — Soil Health Card

| Field | Detail |
| --- | --- |
| Status | **Blocked** (portal is JavaScript-only) / **To obtain** (aggregate tables) |
| Portal | `soilhealth.dac.gov.in` (Department of Agriculture and Farmers Welfare) |
| Observed | Root and all probed report paths return the same ~650-byte shell; content is rendered client-side, so nothing can be read by a script |
| What farmers get | A printed card per sample: pH, EC, organic carbon, available N, P, K, S and micronutrients (Zn, B, Fe, Mn, Cu), with a fertilizer recommendation |
| What the app needs | (a) the farmer's own card values, typed in; (b) block or district nutrient baselines for farmers without a card |
| Route for (b) | District and block summaries from the portal's report section, transcribed by a human into `data/reference/`, or a state soil-testing dataset if UP publishes one |

National context: about 25 crore cards issued and ₹1,706 crore released for the
scheme; UP is a covered state. The widely reported critique is that
recommendations are blanket rather than site-specific, which is exactly the gap
the soil-test-adjusted engine targets.

**Design consequence**: the soil input path is three-tier (own card, lab report,
block baseline), and every advisory must display which tier produced it. A block
baseline is an estimate and is labelled as one.

---

## 4. Schemes — PMFBY and state programmes

| Field | Detail |
| --- | --- |
| Status | **Documented** (mechanics), **Blocked** (portal), **To obtain** (UP season window) |
| Portal | `pmfby.gov.in` returns a title-only document to a plain client; content is rendered by script |
| Farmer premium share | 2% of sum insured for kharif food and oilseed crops; 1.5% for rabi food and oilseed crops; 5% for annual commercial and horticultural crops. The remainder is subsidised by Centre and State |
| Enrolment channels | PMFBY portal "Farmer Corner", banks, Common Service Centres, the NCIP self-registration app |

**Critical operational fact**: enrolment cut-offs are set state by state and
crop by crop. Evidence this session: Andhra Pradesh ran Kharif 2026 with RWBCIS
closing 31 July and PMFBY paddy closing 15 August. Therefore **no national
deadline may be shown to a farmer**. The UP rabi window must be read from the
UP Agriculture Department notification or `pmfby.gov.in` each season and
entered as dated data, never hard-coded.

**Design consequence**: each scheme row carries `window_note`, `verified_on`,
and `source_url`. The UI shows "checked on <date>" and a link; it never asserts
a closing date the data does not carry.

**Fallback**: if the season window is unknown, show eligibility and documents
only, with "confirm the last date at your bank or CSC".

---

## 5. Language — Bhashini (Hindi voice, phase 2)

| Field | Detail |
| --- | --- |
| Status | **Documented** |
| Provider | MeitY, Digital India Bhashini Division (National Language Translation Mission) |
| Capability | ASR, machine translation, TTS, OCR, transliteration across the 22 Eighth-Schedule languages |
| Access | API key through the Bhashini/ULCA developer route; free sandbox access for developers |
| Precedent | Kisan e-Mitra, the ministry's farmer chatbot, is Bhashini-powered. The pattern is ASR → translate → retrieval over a curated knowledge base → translate back → TTS, deliberately retrieval-first to limit hallucination on entitlement details |

**Design consequence**: voice is a *Could*, not a *Must*. If built, the language
layer wraps the deterministic advisory text, and any LLM only rephrases; it
never invents a dose, a date, or an entitlement.

---

## 6. Agronomy reference — package of practices and FAO-56

| Field | Detail |
| --- | --- |
| Status | **To obtain** (zone package), **Documented** (FAO-56) |
| Zone | Ghazipur sits in UP agro-climatic Zone IV (eastern plain); wheat falls in the North Eastern Plains Zone |
| Nodal institutions | NDUAT Kumarganj (zone university), UP Council of Agricultural Research, state Department of Agriculture |
| Format | PDFs and printed *Krishak Mitra*-style publications; no API, no machine-readable edition |
| What must be transcribed | Recommended N-P₂O₅-K₂O per crop, stage splits, the notified variety list with sowing windows and seed rates, and irrigation critical stages |

**Cost is real**: hand transcription with a page citation per row is a
multi-day task and the single largest error source in the product. The build
plan makes it a blocking step (S2) with citation enforcement and expert review
for exactly this reason.

**FAO-56**: crop coefficients in `data/reference/fao56-kc-values.md` follow the
single-crop-coefficient method, `ETc = Kc × ET0`. Confirm each row against the
published tables and cite the page before shipping. Paddy needs a ponded-water
rule, not the upland balance.

**ML crop recommendation datasets**: the public Kaggle "Crop Recommendation"
set (N, P, K, temperature, humidity, pH, rainfall; 2,200 rows; 22 crops at 100
each) reports 98–99% accuracy with tree ensembles. Treat that as a saturation
artefact of near-disjoint synthetic class ranges, not as evidence of field
accuracy. It may inform a fallback ranking prior only; it may never override a
cited zone recommendation.

---

## 7. Decision matrix

| Capability | Source | Status | Ships in MVP | If the source fails |
| --- | --- | --- | --- | --- |
| Weather forecast and alerts | Open-Meteo | Verified | Yes | Stale cache with age warning |
| Fertilizer plan | Zone package transcribed + FAO-56 | To obtain | Blocked until S2 | Do not ship the engine; show soil interpretation only |
| Crop and variety | Zone package | To obtain | Blocked until S2 | Show the general zone list marked "verify locally" |
| Soil interpretation | Farmer card, lab report, block baseline | Blocked portal | Yes, via farmer input | Block baseline, labelled as an estimate |
| Mandi price | OGD/Agmarknet | Blocked | No (Should) | Hide the price card; link to the Agmarknet report |
| Scheme navigator | PMFBY mechanics + UP notification | Documented | Yes, with conditional dates | Eligibility and documents only |
| Hindi voice | Bhashini | Documented | No (Could) | Text UI only |

---

## 8. Standing rules for every adapter

1. Timeout, retry with backoff, and a cache in front. No live call in a request
   path without all three.
2. Record `source`, `fetched_at`, and `licence` with every stored payload.
3. Attribution rendered wherever the data surfaces, not only on an about page.
4. A key lives in the environment, never in the repository or the PWA bundle.
5. Contract tests run against recorded fixtures; CI never calls a live API.
6. If a row above says Blocked, the adapter does not exist yet. Build the
   fallback instead.

---

*Compiled from sources exercised and read during this session. Re-verify every
row marked Documented at build time; portals change without notice.*
