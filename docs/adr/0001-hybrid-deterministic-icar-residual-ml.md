# ADR-0001: Hybrid Deterministic ICAR Baseline with Bounded Residual Machine Learning

**Date**: 2026-11-15  
**Status**: accepted  
**Deciders**: KhetSathi Engineering & Agronomy Core  

## Context

Smallholder farmers in India operate under tight financial margins where fertilizer input costs dictate seasonal viability. Pure end-to-end black-box Machine Learning models (such as deep neural networks predicting raw N-P-K dosages directly from soil inputs) suffer from hallucination and out-of-distribution unpredictability. In agronomy, recommending an excess of 40 kg N/ha can cause lodging, vegetative overgrowth, high susceptibility to fungal pathogens, and groundwater nitrate poisoning. Conversely, purely static general recommendations fail to account for hyper-local micro-climate variance, temporal yield trends, and soil chemistry interactions.

## Decision

We adopt a **two-tier Hybrid Agronomic Decision Architecture**:
1. **Tier 1 (Deterministic Core)**: Compute state-notified Indian Council of Agricultural Research (ICAR) Package of Practices base recommendations adjusted deterministically for Soil Health Card nutrient classes (Low, Medium, High) and target yields.
2. **Tier 2 (Bounded Residual ML)**: Train a gradient-boosted decision tree (LightGBM) strictly on the **residual error** ($\Delta N = N_{\text{observed}} - N_{\text{ICAR\_base}}$) using historical district panel data, weather features, and soil parameters.
3. **Safety Envelope**: The ML residual adjustment is mathematically bounded to $\pm 15\%$ of the base recommendation:
   $$\text{Adjustment} = \max(-0.15 \times N_{\text{base}}, \min(0.15 \times N_{\text{base}}, \hat{\Delta N}))$$
   This guarantees that the ML model can refine the dose for local efficiency but can *never* prescribe a lethal or non-agronomic fertilizer volume.

## Alternatives Considered

### Alternative 1: Pure End-to-End Deep Neural Network (MLP / TabNet)
- **Pros**: Can learn non-linear interactions across high-dimensional feature spaces without feature engineering.
- **Cons**: Unexplainable black-box; can output wildly unsafe fertilizer rates for edge-case soil inputs; impossible to provide an auditable arithmetic trail for Indian agricultural extension officers.
- **Why not**: Fails zero-hallucination safety requirements and ICAR regulatory compliance.

### Alternative 2: Pure Rule-Based Static Lookup Table (Traditional Extension Sheets)
- **Pros**: 100% deterministic, easy to audit, zero compute overhead.
- **Cons**: Coarse district-wide averages ignore micro-climatic weather shifts, multi-year yield trajectory shifts, and soil texture subtleties, resulting in sub-optimal fertilizer use efficiency.
- **Why not**: Sacrifices a 59.6% MAE improvement demonstrated on historical holdout partitions.

## Consequences

### Positive
- **Guaranteed Agronomic Safety**: No model output can violate ICAR physical sanity thresholds.
- **High Accuracy**: Achieves 1.245 kg N/ha MAE on temporal holdout validation (59.6% improvement over baseline).
- **Auditability**: Every advisory returns both the base ICAR value and the ML residual delta, giving extension officers full visibility.
- **Ultra-low Latency**: In-memory LightGBM residual evaluation takes under 0.05 ms ($p95$).

### Negative
- Requires maintaining two parallel evaluation logic pathways (deterministic engine + ML pipeline).
- Model retraining requires curated residual target preparation.

### Risks & Mitigations
- **Risk**: ML model drift during extreme anomalous weather years.
- **Mitigation**: Automated promotion gates in `ml_pipeline/evaluate.py` require $\ge 25\%$ MAE improvement on holdout test partitions; if gates fail, the engine falls back gracefully to pure deterministic mode.
