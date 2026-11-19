# Crop Coefficients (FAO-56) for Irrigation Scheduling

Source: FAO Irrigation and Drainage Paper 56, crop coefficient tables. The
values below are the standard single-crop-coefficient entries used by the
irrigation engine (`ETc = Kc × ET0`). Confirm each against FAO-56 Table 12
before use, and replace with locally calibrated values where the zone package
provides them.

| Crop | Kc ini | Kc mid | Kc end | Notes |
| --- | ---: | ---: | ---: | --- |
| Wheat | 0.40 | 1.15 | 0.30 | Kc end varies with harvest state |
| Rice (paddy) | 1.05 | 1.20 | 0.90 | Ponded water changes the water balance; use a paddy-specific model |
| Maize | 0.30 | 1.20 | 0.50 | Kc end 0.35 for field maize at physiological maturity |
| Sugarcane | 0.40 | 1.25 | 0.75 | Long duration; stage lengths from the zone package |
| Mustard | 0.35 | 1.10 | 0.35 | |
| Gram (chickpea) | 0.40 | 1.05 | 0.35 | |
| Potato | 0.50 | 1.15 | 0.75 | |
| Lentil | 0.40 | 1.10 | 0.30 | |
| Pea | 0.50 | 1.15 | 1.10 | Fresh market |
| Berseem | 0.40 | 1.15 | 1.10 | Multiple cuts change mid-season values |

## Engine rules

- Stage lengths come from the reference tables, not from FAO default lengths,
  wherever the zone package provides them.
- ET0 comes from Open-Meteo's `et0_fao_evapotranspiration` daily value.
- Effective rainfall uses an 80% factor on forecast `precipitation_sum` in the
  MVP, replaced by a soil-water-balance model once plot data allows it.
- Paddy must not use the upland water balance; it needs a ponded-water model or
  an explicit "irrigate to maintain standing water" rule.

## Verification status

Values are from FAO-56 as generally published; re-check against the paper's
Table 12 and cite the page in the reference row before shipping.
