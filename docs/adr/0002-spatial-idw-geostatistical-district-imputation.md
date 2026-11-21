# ADR-0002: Spatial IDW Geostatistical District Imputation

**Date**: 2026-11-16  
**Status**: accepted  
**Deciders**: KhetSathi Engineering & GIS Core  

## Context

Over 85% of Indian smallholders do not possess a recent physical Soil Health Card (SHC) testing laboratory slip for their plot. When a farmer opens KhetSathi and enables GPS or enters their village/district, the platform must immediately supply a scientifically sound, statistically robust soil nutrient baseline (Nitrogen, Phosphorus, Potassium, Organic Carbon, pH, Zinc) rather than blocking the user or requiring manual lab entry.

## Decision

We implement a **Spatial Inverse Distance Weighting (IDW) Geostatistical Interpolator** coupled with a pre-computed Pan-India centroid matrix covering all **695 agricultural districts**:
1. When exact GPS coordinates $(\text{lat}, \text{lon})$ are provided, the system identifies the $k$-nearest district centroids (default $k=3$) within a bounding radius.
2. Nutrient levels are interpolated using power parameter $p=2.0$:
   $$\hat{Z}(x_0) = \frac{\sum_{i=1}^k d(x_0, x_i)^{-p} Z(x_i)}{\sum_{i=1}^k d(x_0, x_i)^{-p}}$$
3. If GPS is unavailable, the system executes an exact localized district fallback indexed against the official DAC&FW district macro/micronutrient soil database.

## Alternatives Considered

### Alternative 1: Remote Sensing Only (Satellite NDVI/SoilGrids API on every request)
- **Pros**: Continuous spatial grid down to 250m resolution.
- **Cons**: High network latency (1.2–3.5 seconds per external API query); frequent upstream throttling and downtime; requires internet connectivity that fails in deep rural farms.
- **Why not**: Latency budget exceeds the 200 ms target for real-time mobile advisory.

### Alternative 2: Nearest-Neighbor District Hard Assignment (Voronoi Polygons)
- **Pros**: Trivial lookup speed ($O(1)$).
- **Cons**: Severe boundary discontinuity: a farmer sitting 500 meters across a district border experiences an unnatural step-change in recommended nutrients.
- **Why not**: Fails geostatistical continuity and causes farmer distrust along district borders.

## Consequences

### Positive
- **Smooth Spatial Gradients**: Border plots receive blended nutrient profiles representing actual continuous soil horizons.
- **Instant Response Time**: Entire centroid bundle resides in-memory (`artifacts/district_soil_bundle.json`), completing spatial lookup in under 1.5 ms.
- **100% Pan-India Coverage**: Seamlessly handles all 695 districts across India.

### Negative
- Requires periodic batch regeneration of the spatial centroid cache whenever official DAC&FW soil survey datasets are updated.

### Risks & Mitigations
- **Risk**: Distortion in extreme terrain (e.g., steep Himalayan valleys).
- **Mitigation**: Spatial coordinates outside national agro-climatic boundaries trigger input validation errors (`HTTP 422`).
