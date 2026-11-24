# Architecture Decision Records (ADRs)

This directory documents the foundational architectural and agronomic decisions shaping **KhetSathi 360**. Each record outlines the operational context, alternatives evaluated, technical trade-offs, and downstream consequences.

## Index

| ADR | Title | Status | Date | Primary Driver |
|:---:|:------|:------:|:----:|:---------------|
| [0001](0001-hybrid-deterministic-icar-residual-ml.md) | Hybrid Deterministic ICAR Baseline with Bounded Residual ML | **Accepted** | 2026-11-15 | Agronomic safety & zero-hallucination |
| [0002](0002-spatial-idw-geostatistical-district-imputation.md) | Spatial IDW Geostatistical District Imputation | **Accepted** | 2026-11-16 | 695-district GPS & baseline coverage |
| [0003](0003-multimodal-gemini-shc-guardrails.md) | Multimodal Vision OCR with Pre-Validation Document Guardrails | **Accepted** | 2026-11-20 | Rejection of non-SHC files (resumes, bills) |
| [0004](0004-pwa-network-first-offline-resilience.md) | Progressive Web App with Network-First Navigation Caching | **Accepted** | 2026-11-20 | Zero-connectivity rural field resilience |
| [0005](0005-dual-frontend-strategy.md) | Dual Frontend Architecture for Farmer vs Enterprise Modalities | **Accepted** | 2026-11-20 | Speed for farmers (`/`) + Analytics (`/react`) |
| [0006](0006-farmer-first-endgame-vision-architecture.md) | Farmer-First Endgame Vision Architecture (8 Inviolable Pillars) | **Accepted** | 2026-11-24 | Class-5 accessible UX, map pointing, subsidized seeds, smart crop pop-up & machinery |

---

## Guidelines for New ADRs
To propose a new architectural decision:
1. Copy [template.md](template.md) to `NNNN-[short-title].md`.
2. State the problem context, alternatives considered, and measurable consequences.
3. Update this index table upon approval.
