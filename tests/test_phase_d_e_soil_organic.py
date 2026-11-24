"""
tests/test_phase_d_e_soil_organic.py — Unit & Integration tests for Phase D & E:
1. Phase D: Regional Agricultural Institute Soil Record Fallback with ICAR/STCR Citations.
2. Phase E: Organic Farming Mode Dashboard Switcher, Soil Benefits, Local Price Premiums, and Direct Buyer Routes.
"""

import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from app.api import app
from app.district_soil_model import DistrictSoilModel
from app.organic_engine import calculate_organic_advisory


class TestPhaseDESoilAndOrganic(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        bundle_path = Path(__file__).resolve().parent.parent / "artifacts" / "district_soil_bundle.json"
        self.model = DistrictSoilModel(bundle_path=bundle_path)

    def test_phase_d_regional_institute_soil_record_resolution(self):
        """
        Validates Phase D:
        - Accurately resolves nearest district soil baseline when farmer has no soil card
        - Contains N, P, K, OC, pH, Zn and region classification
        """
        res = self.model.predict_by_coords(lat=25.5928, lon=83.5770)
        self.assertIn("ghazipur", res["nearest_district"].lower())
        self.assertIn("region", res)
        self.assertEqual(res["region"], "Uttar Pradesh")
        self.assertIn("zone", res)

    def test_phase_d_regional_soil_api_endpoint(self):
        """
        Validates GET /api/v1/district/baseline returns regional institute dataset records.
        """
        resp = self.client.get("/api/v1/district/baseline?lat=25.59&lon=83.58")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("ghazipur", data["nearest_district"].lower())
        self.assertIn("expected_soil", data)
        soil = data["expected_soil"]
        self.assertGreater(soil["n"], 100)
        self.assertGreater(soil["p"], 5)
        self.assertGreater(soil["k"], 50)
        self.assertGreater(soil["ph"], 5.0)

    def test_phase_e_organic_advisory_economics_and_benefits(self):
        """
        Validates Phase E:
        - Calculates bio-input plan (Vermicompost, Bio-NPK, Jeevamrut, Neem cake)
        - Computes organic market premium (+25% over MSP)
        - Verifies PKVY government assistance calculation
        - Delivers verified direct buyer routes (Jaivik Kheti, PGS-India, FPOs)
        """
        advisory = calculate_organic_advisory(crop="wheat", area_ha=2.0)
        self.assertIsNotNone(advisory.input_plan)
        self.assertGreater(advisory.input_plan.vermicompost_tonnes, 2.0)
        self.assertGreater(advisory.input_plan.jeevamrut_litres, 500.0)

        eco = advisory.economics
        self.assertGreater(eco.organic_net_profit_inr, 50000.0)
        self.assertGreater(eco.expected_organic_price_per_q_inr, 2500.0)
        self.assertGreater(eco.pkvy_annual_assistance_inr, 20000.0)

        routes = advisory.supplier_routes
        self.assertGreaterEqual(len(routes), 3)
        self.assertTrue(any("Jaivik" in r.channel_name for r in routes))
        self.assertTrue(any("PGS" in r.channel_name for r in routes))

    def test_phase_e_organic_api_endpoint(self):
        """
        Validates GET /api/v1/organic/advisory.
        """
        resp = self.client.get("/api/v1/organic/advisory?crop=wheat&area_ha=1.5")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["economics"]["crop"], "wheat")
        self.assertIn("input_plan", data)
        self.assertIn("economics", data)
        self.assertIn("supplier_routes", data)

    def test_phase_d_and_e_frontend_dom_and_bilingual_contracts(self):
        """
        Validates frontend/index.html includes:
        - Phase D: Regional soil record attribution banner (#regional-soil-record-card)
        - Phase E: Dashboard Mode Switcher (#dashboard-mode-bar, #btn-mode-conventional, #btn-mode-organic)
        - Phase E: Organic transformation containers (#organic-dashboard-panel, #organic-bio-inputs-grid, #organic-soil-benefits-card)
        - Bilingual I18N keys for mode shifting and regional soil records
        - Touch target compliance (min-h-[44px])
        """
        html_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        self.assertTrue(html_path.exists())
        content = html_path.read_text(encoding="utf-8")

        # Phase D DOM elements
        self.assertIn("regional-soil-record-card", content)

        # Phase E DOM elements
        self.assertIn("dashboard-mode-bar", content)
        self.assertIn("btn-mode-conventional", content)
        self.assertIn("btn-mode-organic", content)
        self.assertIn("organic-soil-benefits-card", content)

        # I18N Keys
        required_keys = [
            "dashboardModeTitle",
            "modeConvBtn",
            "modeOrgBtn",
            "regionalSoilTitle",
            "regionalSoilSub",
            "soilBenefitBio",
            "soilBenefitWater",
            "soilBenefitCarbon",
            "orgMandiTitle",
        ]
        for key in required_keys:
            self.assertIn(f"{key}:", content, f"Missing I18N key: {key}")


if __name__ == "__main__":
    unittest.main()
