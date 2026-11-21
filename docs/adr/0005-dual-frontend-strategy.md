# ADR-0005: Dual Frontend Architecture for Farmer vs Enterprise Modalities

**Date**: 2026-11-20  
**Status**: accepted  
**Deciders**: KhetSathi Frontend & Architecture Core  

## Context

KhetSathi 360 serves two fundamentally distinct user cohorts:
1. **Field Farmers & Extension Officers**: Require instant mobile page load on 3G/4G networks, extreme battery efficiency, complete Devanagari Hindi support, high-contrast readable cards, and zero JavaScript hydration delay or bundler overhead.
2. **FPO Managers, Agritech Partners & Investors**: Require complex data visualizations, multi-district cohort analytics, unit economics calculators, interactive sliders, and componentized state management.

Initial attempts to replace the entire frontend with a single heavy React bundle introduced bundle bloat, hydration delays on budget Android devices, and deployment fragility.

## Decision

We establish a **Dual Frontend Architecture**:
1. **Primary Root UI (`/` and `/ui`)**:
   - Built as a self-contained, high-performance HTML/CSS/Vanilla JS PWA located at `frontend/index.html`.
   - Zero compilation or node build dependencies required at deployment time.
   - Operates with sub-100ms first contentful paint (FCP) and full offline resilience.
2. **Enterprise & Investor Client (`/react`)**:
   - Modern React 19 + TypeScript + Tailwind CSS application located in `client/`.
   - Engineered for complex interactive dashboards: Organic transition economics, investor cohort analytics, multi-district coverage maps.
   - Built to `client/dist/` and deployed to `frontend/index_react.html` via `client/scripts/deploy-react.js`, strictly isolated from the root farmer interface.

## Alternatives Considered

### Alternative 1: Single Monolithic Single-Page App (React-Only)
- **Pros**: Single component library, uniform codebase.
- **Cons**: 300+ KB JS bundle requires parsing and hydration on low-end MediaTek/Spreadtrum smartphone processors, degrading first-input responsiveness for farmers.
- **Why not**: Harms primary mission of serving rural smallholders with maximum speed.

### Alternative 2: Server-Side Rendered (Next.js / Remix)
- **Pros**: Fast initial paint with React ecosystem.
- **Cons**: Adds Node.js runtime container complexity and memory overhead alongside the FastAPI Python ML service; complicates simple single-container VM deployments.
- **Why not**: Violates simplicity principles for the Python-first agronomy core.

## Consequences

### Positive
- **Maximum Farmer Reliability**: The primary farmer interface has zero build pipeline dependencies; a Python-only server can serve it directly.
- **Enterprise Power**: Partners and investors get modern React 19 interactive features without compromising farmer page speeds.
- **Isolated Failure Domains**: A syntax or dependency issue in the React bundle can never break the root farmer advisory UI.

### Negative
- Requires maintaining design language consistency across both vanilla and React implementations.

### Risks & Mitigations
- **Risk**: Drift between the two interfaces.
- **Mitigation**: Shared API client contracts (`app/contracts.py` & `client/src/api/client.ts`) and unified design tokens ensure identical agronomic outputs across both interfaces.
