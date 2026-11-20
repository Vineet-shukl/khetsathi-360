import unittest
from fastapi.testclient import TestClient
from app.api import app
from app.satellite_service import calculate_satellite_vegetation


class TestSatelliteAndSoilGrids(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_calculate_satellite_vegetation_ghazipur(self):
        """Verifies Sentinel-2 NDVI and SoilGrids calculations for Ghazipur, UP."""
        res = calculate_satellite_vegetation(lat=25.59, lon=83.58, crop="wheat", days_after_sowing=30)
        self.assertGreaterEqual(res.ndvi, 0.1)
        self.assertLessEqual(res.ndvi, 0.95)
        self.assertGreater(res.ndre, 0.05)
        self.assertEqual(res.resolution_meters, 10.0)
        self.assertIn("Sentinel-2", res.satellite_name)
        self.assertGreater(res.soilgrids_clay_pct, 10.0)
        self.assertGreater(res.soilgrids_bulk_density_g_cm3, 1.0)
        self.assertGreater(res.soilgrids_cec_mmol_kg, 10.0)
        self.assertTrue(len(res.remote_sensing_action_hi) > 10)

    def test_satellite_endpoint(self):
        """Verifies GET /api/v1/satellite/vegetation endpoint."""
        resp = self.client.get("/api/v1/satellite/vegetation?lat=25.59&lon=83.58&crop=wheat&days=35")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("ndvi", data)
        self.assertIn("ndre", data)
        self.assertIn("soilgrids_clay_pct", data)
        self.assertIn("soilgrids_bulk_density_g_cm3", data)
        self.assertIn("crop_vigor_status_hi", data)

    def test_advisory_includes_satellite_object(self):
        """Verifies POST /api/v1/advisory automatically includes satellite remote sensing."""
        payload = {
            "zone": "zone4",
            "crop": "wheat",
            "area_ha": 1.0,
            "lat": 25.59,
            "lon": 83.58,
            "sowing_delay_days": 5,
            "irrigation": "tubewell",
            "et0_mm_day": 3.0,
            "rain_prob_48h_pct": 10
        }
        resp = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("satellite", data)
        self.assertIsNotNone(data["satellite"])
        self.assertIn("ndvi", data["satellite"])
        self.assertIn("soilgrids_clay_pct", data["satellite"])


if __name__ == "__main__":
    unittest.main()
