# Crop Calendar — Eastern Uttar Pradesh (Indicative)

Ghazipur district sits in UP agro-climatic Zone IV (eastern plain) and in the
North Eastern Plains Zone for wheat. The windows below are indicative for
planning the advisory engine; every row must be replaced or confirmed by the
official package of practices for the zone (NDUAT Kumarganj / UP Agriculture
Department) before it drives an advisory.

| Crop | Season | Sowing / planting | Harvest | Typical duration (days) | Notes |
| --- | --- | --- | --- | ---: | --- |
| Rice (paddy) | Kharif | Nursery June; transplant late June–mid July | October–November | 110–140 | Depends on variety duration class |
| Maize | Kharif | June–July | September–October | 90–110 | Also grown in rabi in some blocks |
| Pigeonpea | Kharif | June–July | November–December | 150–180 | Rainfed |
| Urd / moong | Kharif | June–July | August–September | 60–80 | Short duration |
| Wheat | Rabi | Late October–November | March–April | 120–145 | Late sowing after paddy shifts the window |
| Mustard | Rabi | October | February–March | 100–130 | |
| Gram | Rabi | October–November | February–March | 95–120 | |
| Lentil | Rabi | October–November | February–March | 100–120 | |
| Potato | Rabi | October–November | January–February | 75–100 | |
| Pea | Rabi | October–November | December–February | 60–90 | |
| Berseem (fodder) | Rabi | October–November | Multiple cuts to April | — | |
| Sugarcane | Annual | Autumn September–October; spring February–March | October–March (12-month crop) | 300–365 | Ratoon cycles follow |

## Advisory implications

- A crop recommendation must check that the crop's harvest window does not
  collide with the next crop's sowing window on the same plot.
- Wheat after late paddy is a different agronomic situation from timely-sown
  wheat; the engine needs a "previous crop" field on the plot.
- Sugarcane occupies the plot for a full year; it must be treated as an
  exclusive constraint, not a normal rotation member.

## Verification status

Unverified for this session. Source to obtain: the eastern plain zone package of
practices, then record document, edition, and page per row.
