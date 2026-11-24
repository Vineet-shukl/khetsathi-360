# ADR-0006: Farmer-First Endgame Vision Architecture

## Status
Accepted

## Context
KhetSathi 360 has evolved from an ICAR/FAO-56 deterministic calculator into a production-grade national agricultural decision system. The project founder has established an overarching vision and foundational roadmap to make KhetSathi 360 a global benchmark in agricultural software engineering, targeting smallholder farmers with diverse educational backgrounds (including farmers with primary school education).

## Decision
We formally adopt the **Farmer-First 8-Pillar Endgame Vision Architecture** as the binding direction of KhetSathi 360:

1. **Interactive Farmland Geolocation**: Farmers can pinpoint their parcel using an interactive map pointer (Leaflet/Bhuvan/OSM tile layer) in addition to 1-Click GPS and Blinkit-style village autocomplete.
2. **Certified Seed Variety & Subsidized Store Locator**: Recommend certified climate-resilient varieties and connect farmers to nearby Government Block Seed Stores (राजकीय बीज भंडार), KVKs, and authorized dealers with transparent price subsidies.
3. **Smart Geological Weather & Minimized Alternate Crop Suggestion Pop-up**:
   - Live NWP weather with rainfall leaching protection.
   - A non-intrusive, floating, minimizable recommendation pop-up in the top-right corner that intelligently suggests more profitable, water-efficient alternative crops suited to upcoming season trends.
   - Comprehensive cultivation roadmap covering machinery and tools tailored to small vs large acreages.
4. **Dual-Track Soil Health Intelligence**: Strict multimodal SHC OCR parser paired with a 695-district geostatistical baseline fallback.
5. **Organic Mode ("अमृत माटी") & Direct Buyer Marketplaces**: Instant toggle between chemical and organic modes with comparative profit ledgers, bio-input recipes (Jeevamrit, Beejamrit, Neemastra), and direct buyer contacts.
6. **Ultra-Fast Performance & Skeleton UI**: High-speed, low-bandwidth footprint with skeleton loaders, offline PWA caching, and compatibility with budget 4G mobile devices.
7. **Accessible Class-5 Farmer UX Benchmark**: Large tactile visual components, voice narration (TTS), WCAG 2.2 AA contrast, and 100% bilingual parity (Hindi ⇄ English).
8. **Permanent Core Rulebook**: These principles are codified in `docs/PROJECT_FOUNDATION.md` and cannot be altered or degraded during incremental development.

## Consequences
- **Positive**: Provides a single, unambiguous architectural North Star. Ensures developer and agent alignment across all future turns. Guarantees that cutting-edge agronomic science remains intuitively accessible to grassroots farmers.
- **Implementation Strategy**: Each feature will be introduced incrementally without disrupting the currently deployed, live-tested production endpoints.
