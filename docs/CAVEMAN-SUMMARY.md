# KhetSathi 360 — Caveman Summary

Terse. Load-bearing facts exact.

## What

KhetSathi 360. Agri decision support. Smallholder farmers. Ghazipur, eastern UP.
1M1B Green Internship YIRP. Owner Vineet Shukla.

## Problem

Farmer guess soil, seed, weather, fertilizer. Public data exist. Scattered.
Printed. Generic. Farmer not use.

## Product

Hindi PWA. Input: village, plot, soil test, season.
Output: crop + variety, fertilizer bags by stage, weather alerts, mandi hint,
scheme checklist.
Every number show rule + source. Platform sell nothing.

## Stack

React + Vite PWA. FastAPI. PostgreSQL 16. Docker Compose. One VM. No Kubernetes.
Weather: Open-Meteo. Free. No key. 16 day. Verified.
Mandi: data.gov.in OGD. API key. Resource ID unresolved.
Package of practices: PDFs. Transcribe by hand. Cite page.

## Not Building

Marketplace. Credit. Insurance sales. Photo disease AI. Satellite yield. Own
weather model. Own soil lab.

## Key Hypothesis

Explainable soil-first advisory change input decisions.
Right when 60% farmers restate fertilizer dose unaided after 2 weeks.
AND 30% change one decision next season.

## Hard Rules

1. No advisory without `source_citation`.
2. No agronomic constant outside `data/reference`.
3. No external API in request path without timeout + cache.
4. Hindi in farmer path. English only developer side.
5. Golden set 50 cases. 90% agreement. Else no ship.

## Gaps. Honest.

Interviews: 0 done. Problem unvalidated.
OGD page: sandbox placeholder. Need real resource ID.
PMFBY portal: JS only. Human must read.
Zone package PDFs: not obtained. Blocker for S2.
Competitors: unsourced. Need citations.

## Build Order

S1 scaffold+CI → S2 reference tables → S3 weather adapter.
Then S4 fertilizer ∥ S5 cropfit ∥ S6 mandi+schemes.
Then S7 API → S8 intake UI → S9 advisory UI → S10 deploy.

S4 hardest. Staff strongest.

## Files

`docs/PRD.md`. `docs/ARCHITECTURE.md`. `docs/API-CATALOG.md`.
`docs/FIELD-RESEARCH-PROTOCOL.md`. `docs/SCHOLAR-EVALUATION.md`.
`plans/khetsathi-360-build-plan.md`. `data/reference/*.md`.
