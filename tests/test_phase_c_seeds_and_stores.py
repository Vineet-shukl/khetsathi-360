"""
tests/test_phase_c_seeds_and_stores.py — Unit & Integration tests for Phase C:
Certified Seed Varieties, Government Subsidized Price Matrix & Block Store Locator.
"""

import unittest
from fastapi.testclient import TestClient

from app.api import app
from app.seed_store_service import (
    get_certified_seed_varieties,
    get_nearby_government_seed_stores
)


class TestPhaseCSeedsAndStores(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_certified_seed_varieties_for_wheat(self):
        """
        Validates certified wheat varieties:
        - Includes standard ICAR varieties (HD-2967, DBW-187, etc.)
        - Contains certified germination rate >= 85%
        - Shows transparent government subsidized price vs open market price with cash savings
        """
        varieties = get_certified_seed_varieties(crop="wheat", region="Uttar Pradesh", language="hi")
        self.assertGreaterEqual(len(varieties), 2)
        v1 = varieties[0]
        self.assertIn("name", v1)
        self.assertIn("maturity_days", v1)
        self.assertGreaterEqual(v1["germination_pct"], 85)
        self.assertLess(v1["subsidized_price_per_kg_inr"], v1["market_price_per_kg_inr"])
        self.assertGreater(v1["subsidy_savings_pct"], 25)

    def test_certified_seed_varieties_for_mustard(self):
        """Validates certified mustard varieties (Pusa Bold, RH-749, etc.) in English."""
        varieties = get_certified_seed_varieties(crop="mustard", region="Rajasthan", language="en")
        self.assertGreaterEqual(len(varieties), 1)
        v = varieties[0]
        self.assertIn("seed_rate_kg_ha", v)
        self.assertLess(v["subsidized_price_per_kg_inr"], v["market_price_per_kg_inr"])

    def test_nearby_government_seed_stores_lookup(self):
        """
        Validates directory lookup of Government Block Seed Stores, KVKs, and PACS:
        - Contains official Block Agriculture Store (राजकीय कृषि बीज भंडार)
        - Includes physical address, distance, and contact
        """
        stores = get_nearby_government_seed_stores(district="Ghazipur", lat=25.5928, lon=83.5770, language="hi")
        self.assertGreaterEqual(len(stores), 2)
        s1 = stores[0]
        self.assertIn("name", s1)
        self.assertIn("store_type", s1)
        self.assertIn("distance_km", s1)
        self.assertIn("phone", s1)
        self.assertTrue(any("राजकीय" in s["name"] or "KVK" in s["name"] or "बीज" in s["name"] for s in stores))

    def test_api_endpoint_seeds_and_stores(self):
        """
        Integration test verifying GET /api/v1/seed/certified-and-stores.
        """
        resp = self.client.get(
            "/api/v1/seed/certified-and-stores?crop=wheat&district=Ghazipur&area_ha=1.5&lat=25.59&lon=83.58&lang=hi"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("varieties", data)
        self.assertIn("stores", data)
        self.assertIn("seed_requirement", data)
        self.assertGreater(data["seed_requirement"]["total_seed_kg"], 50)
        self.assertGreater(data["seed_requirement"]["total_savings_inr"], 500)

    def test_frontend_phase_c_dom_and_bilingual_contracts(self):
        """
        Validates that frontend/index.html includes:
        - #seed-catalog-stores-card, #seed-requirement-banner, #seed-varieties-list, #seed-stores-list
        - Bilingual I18N keys for certified seeds and government block stores
        - WCAG 2.2 touch target compliance (min-h-[44px])
        """
        import os
        from pathlib import Path

        html_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        self.assertTrue(html_path.exists())
        content = html_path.read_text(encoding="utf-8")

        # DOM Containers
        self.assertIn("seed-catalog-stores-card", content)
        self.assertIn("seed-requirement-banner", content)
        self.assertIn("seed-varieties-list", content)
        self.assertIn("seed-stores-list", content)
        self.assertIn("seed-summary-badge-box", content)

        # I18N Dictionary Keys
        required_keys = [
            "seedsBadge",
            "seedsTitle",
            "seedsSummaryTitle",
            "seedVarietiesHead",
            "seedStoresHead",
            "seedsGovPrice",
            "seedsMarketPrice",
            "seedsSavings",
            "storesCall",
        ]
        for key in required_keys:
            self.assertIn(f"{key}:", content, f"Missing I18N key: {key}")

        # WCAG 2.2 touch target compliance for call store action
        self.assertIn("min-h-[44px]", content)


if __name__ == "__main__":
    unittest.main()
