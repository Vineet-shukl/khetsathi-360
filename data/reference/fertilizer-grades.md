# Fertilizer Grades Reference

Product composition used by the fertilizer engine to convert elemental nutrient
doses into bags a farmer can buy. Values are standard Indian fertilizer grade
compositions; confirm against the FCO schedule and the product label before
using in any advisory.

| Product | N (%) | P2O5 (%) | K2O (%) | Other | Bag size (kg) |
| --- | ---: | ---: | ---: | --- | ---: |
| Urea | 46 | 0 | 0 | — | 45 |
| DAP (di-ammonium phosphate) | 18 | 46 | 0 | — | 50 |
| MOP (muriate of potash) | 0 | 0 | 60 | — | 50 |
| SSP (single super phosphate) | 0 | 16 | 0 | ~11% S, ~19% Ca | 50 |
| NPK 10-26-26 | 10 | 26 | 26 | — | 50 |
| NPK 12-32-16 | 12 | 32 | 16 | — | 50 |
| NPK 20-20-0 | 20 | 20 | 0 | — | 50 |
| Ammonium sulphate | 21 | 0 | 0 | ~24% S | 50 |
| CAN (calcium ammonium nitrate) | 26 | 0 | 0 | ~8% Ca | 50 |

## Conversion rule the engine applies

1. Compute elemental requirement: N, P2O5, K2O in kg for the plot.
2. Fill phosphorus first with DAP when P is required, because DAP also carries
   N. Deduct that N credit from the urea requirement.
3. Fill potassium with MOP.
4. Fill remaining N with urea.
5. Convert kg to bags by the bag size above and round to half bags for display,
   keeping exact kg in the arithmetic trail.

Worked example (illustration only, not a recommendation): 1 ha wheat needing
120 kg N, 60 kg P2O5, 40 kg K2O. DAP for 60 kg P2O5 = 60 / 0.46 = 130.4 kg DAP,
which carries 130.4 × 0.18 = 23.5 kg N. Remaining N = 96.5 kg → urea =
96.5 / 0.46 = 209.8 kg. MOP for 40 kg K2O = 40 / 0.60 = 66.7 kg.

## Notes

- SSP is preferred where sulphur deficiency is documented; its P2O5 is lower per
  kg, so the arithmetic differs.
- Never present a product quantity without the elemental dose and the source
  rule beside it.
- Bag weights vary by manufacturer; the engine stores bag size as data, not a
  constant.
