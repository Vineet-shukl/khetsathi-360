import unittest

from fastapi.testclient import TestClient

from app.api import app


class TestOrganicEngine(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_organic_advisory_wheat(self):
        """Verifies organic bio-input plan, economics, and supplier routes for wheat."""
        resp = self.client.get("/api/v1/organic/advisory?crop=wheat&area_ha=1.0")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Bio-inputs verification
        inp = data["input_plan"]
        self.assertGreater(inp["vermicompost_tonnes"], 1.0)
        self.assertGreater(inp["bio_npk_consortia_litres"], 1.0)
        self.assertGreater(inp["jeevamrut_litres"], 200.0)
        self.assertGreater(inp["neem_cake_kg"], 100.0)

        # Economics verification
        eco = data["economics"]
        self.assertGreater(eco["input_cost_savings_inr"], 3000.0)
        self.assertGreater(eco["expected_organic_price_per_q_inr"], 2275.0)
        self.assertGreater(eco["organic_net_profit_inr"], eco["conventional_net_profit_inr"])
        self.assertEqual(eco["pkvy_annual_assistance_inr"], 16666.0)

        # Supplier routes verification
        routes = data["supplier_routes"]
        self.assertGreaterEqual(len(routes), 4)
        names = [r["channel_name"] for r in routes]
        self.assertTrue(any("Jaivik Kheti" in n for n in names))
        self.assertTrue(any("PGS-India" in n for n in names))

    def test_organic_advisory_mustard(self):
        """Verifies organic bio-input plan for mustard."""
        resp = self.client.get("/api/v1/organic/advisory?crop=mustard&area_ha=2.0")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["economics"]["crop"], "mustard")
        self.assertEqual(data["economics"]["area_ha"], 2.0)


if __name__ == "__main__":
    unittest.main()
