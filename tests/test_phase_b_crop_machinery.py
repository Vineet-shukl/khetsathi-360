"""
tests/test_phase_b_crop_machinery.py — Unit & Integration tests for Phase B:
Smart Floating Alternative Crop Suggestion Engine & Plot-Scale Machinery Lifecycle.
"""

import unittest
from fastapi.testclient import TestClient

from app.api import app
from app.crop_machinery_service import (
    evaluate_alternative_crop,
    get_plot_scaled_machinery_plan,
    get_cultivation_lifecycle_stages
)


class TestPhaseBCropMachinery(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_alternative_crop_wheat_in_dry_conditions(self):
        """
        When Wheat is selected in dry microclimates (rain_prob < 20% or high ET0),
        engine recommends Mustard (सरसों) with positive water savings and margin boost.
        """
        alt = evaluate_alternative_crop(
            crop="wheat",
            area_ha=1.0,
            rain_prob_48h_pct=10,
            et0_fao_mm_day=4.5,
            language="hi"
        )
        self.assertTrue(alt["has_alternative"])
        self.assertEqual(alt["suggested_crop"], "mustard")
        self.assertGreaterEqual(alt["water_saving_pct"], 50)
        self.assertGreater(alt["profit_difference_inr_ha"], 10000)
        self.assertIn("सरसों", alt["reason"])

    def test_alternative_crop_rice_in_water_deficit(self):
        """
        When Rice is selected in low rainfall / high water deficit,
        engine suggests Maize or Pulses (Gram) with >= 60% water reduction.
        """
        alt = evaluate_alternative_crop(
            crop="rice",
            area_ha=1.5,
            rain_prob_48h_pct=15,
            et0_fao_mm_day=5.2,
            language="en"
        )
        self.assertTrue(alt["has_alternative"])
        self.assertIn(alt["suggested_crop"], ["maize", "gram"])
        self.assertGreaterEqual(alt["water_saving_pct"], 60)
        self.assertIn("water", alt["reason"].lower())

    def test_plot_scaled_machinery_tiers(self):
        """
        Validates machinery recommendations scale by plot size:
        - Smallholder (< 0.5 Ha / < 2 Bigha): manual/bullock tools
        - Medium (0.5 to 2.5 Ha): mini-tractor / power tiller
        - Commercial (> 2.5 Ha): heavy tractor, rotavator, combine
        """
        # Smallholder: 0.25 Ha (1 Bigha)
        small = get_plot_scaled_machinery_plan(area_ha=0.25, language="hi")
        self.assertEqual(small["tier"], "smallholder")
        self.assertTrue(any("बैल" in t["name"] or "मैनुअल" in t["name"] or "स्प्रेयर" in t["name"] for t in small["tools"]))

        # Medium: 1.0 Ha (4 Bigha)
        med = get_plot_scaled_machinery_plan(area_ha=1.0, language="en")
        self.assertEqual(med["tier"], "medium")
        self.assertTrue(any("tiller" in t["name"].lower() or "drill" in t["name"].lower() for t in med["tools"]))

        # Large: 3.5 Ha (14 Bigha)
        large = get_plot_scaled_machinery_plan(area_ha=3.5, language="hi")
        self.assertEqual(large["tier"], "commercial")
        self.assertTrue(any("रोटावेटर" in t["name"] or "कंबाइन" in t["name"] or "ट्रैक्टर" in t["name"] for t in large["tools"]))

    def test_cultivation_stages_structure(self):
        """
        Validates 5 chronological cultivation stages with days, tools, and actions.
        """
        stages = get_cultivation_lifecycle_stages(crop="wheat", area_ha=1.0, language="hi")
        self.assertEqual(len(stages), 5)
        stage_names = [s["stage_num"] for s in stages]
        self.assertEqual(stage_names, [1, 2, 3, 4, 5])
        self.assertIn("बुवाई", stages[0]["title"])
        self.assertIn("tools", stages[0])

    def test_api_endpoint_alternative_and_machinery(self):
        """
        Integration test verifying GET /api/v1/crop/alternative-and-machinery.
        """
        resp = self.client.get(
            "/api/v1/crop/alternative-and-machinery?crop=wheat&area_ha=1.0&lat=25.59&lon=83.58&rain_prob_pct=10&et0=4.5&lang=hi"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("alternative", data)
        self.assertIn("machinery", data)
        self.assertIn("lifecycle_stages", data)
        self.assertEqual(data["alternative"]["suggested_crop"], "mustard")
        self.assertEqual(data["machinery"]["tier"], "medium")
        self.assertEqual(len(data["lifecycle_stages"]), 5)


if __name__ == "__main__":
    unittest.main()
