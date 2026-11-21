# ADR-0003: Multimodal Vision OCR with Pre-Validation Document Guardrails

**Date**: 2026-11-20  
**Status**: accepted  
**Deciders**: KhetSathi Engineering Core  

## Context

Farmers who do have a physical Soil Health Card often struggle to manually key in 12 complex laboratory parameters (N, P, K in kg/ha, OC in %, pH, Zn in ppm, EC in dS/m). We integrated multimodal vision to extract these values directly from smartphone camera photos. However, initial testing revealed that when non-agricultural documents (such as resumes, tax invoices, electricity bills, or selfies) were uploaded, the system previously attempted extraction or silently fell back to regional sample presets, giving the false impression that non-soil documents were valid Soil Health Cards.

## Decision

We implement a **Three-Stage Document Authenticity Guardrail Pipeline**:
1. **Stage 1 (Deterministic Byte & Hash Filter)**:
   - Size sanity check: files $< 30\text{ bytes}$ or $> 20\text{ MB}$ rejected immediately.
   - Known non-SHC SHA-256 fingerprint matching rejects test mockups and dummy non-soil files.
2. **Stage 2 (Lexical & Filename Pattern Inspection)**:
   - File names denoting non-agricultural documents (`resume`, `cv`, `curriculum`, `biodata`, `invoice`, `bill`, `receipt`, `salary`, `payslip`) without agricultural tokens are rejected prior to any LLM call with `HTTP 422 Unprocessable Entity`.
   - For PDFs, PyMuPDF (`fitz`) extracts embedded text; documents containing career or billing keywords without soil nutrients are rejected with zero external token expenditure.
3. **Stage 3 (Vision Model Authenticity Classification)**:
   - Gemini 1.5 Flash Vision system prompt enforces mandatory Step 1 Authenticity verification:
     $$\text{is\_soil\_health\_card} \in \{\text{true}, \text{false}\}$$
   - Non-SHC uploads return `{"is_soil_health_card": false, "rejection_reason": "..."}`, translated into bilingual Hindi/English error messages.
   - Frontend explicitly halts scanning and alerts the farmer; **silent fallback to sample presets is strictly forbidden**.

## Alternatives Considered

### Alternative 1: Traditional Tesseract / PaddleOCR Pipeline
- **Pros**: Fully self-hosted, zero external API dependency.
- **Cons**: Severe degradation on wrinkled, stained, low-contrast physical paper cards photographed in harsh outdoor sunlight; fails on Devanagari Hindi tables.
- **Why not**: Accuracy on real Indian farm cards dropped below 45% in field tests.

### Alternative 2: Unfiltered LLM Prompting
- **Pros**: Simple single-step prompt.
- **Cons**: Burns paid LLM tokens on accidental user uploads; risks LLM hallucinating plausible-sounding soil values for resumes or non-soil text.
- **Why not**: Direct cause of the resume-acceptance bug observed in earlier iterations.

## Consequences

### Positive
- **Zero Token Waste**: Inappropriate uploads are rejected at Stage 1 or Stage 2 without triggering Gemini API calls.
- **Farmer Trust**: Clear bilingual rejection messages guide the user to upload genuine DAC&FW cards.
- **Bounded Output**: Extracted values are clamped to physical agronomic ranges (e.g., pH 4.0–10.5, N 10–1000 kg/ha).

### Negative
- Requires maintaining negative token lists and PDF inspection utilities.

### Risks & Mitigations
- **Risk**: Edge case where a card photo has an unusual filename like `IMG_001.jpg`.
- **Mitigation**: Stage 2 only flags explicit non-SHC filename patterns; general camera filenames pass cleanly to Stage 3 for visual classification.
