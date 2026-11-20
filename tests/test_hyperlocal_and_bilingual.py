"""
tests/test_hyperlocal_and_bilingual.py — Unit & Integration tests for
Blinkit-style hyper-local location search and weather irregularity detection.
"""
import unittest
from fastapi.testclient import TestClient
from app.api import app
from app.weather_service import evaluate_weather_irregularities, search_pinpoint_locations


class TestHyperLocalAndBilingual(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_location_search_endpoint(self):
        """Verifies Blinkit/Swiggy style location search endpoint across Indian localities."""
        resp = self.client.get("/api/v1/location/search?query=Ghazipur")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(any("Ghazipur" in item["display_name"] for item in data))
        first = data[0]
        self.assertIn("lat", first)
        self.assertIn("lon", first)
        self.assertIn("display_name", first)
        self.assertIn("source", first)

    def test_location_search_minimum_length(self):
        """Short query returns 422 Unprocessable Entity."""
        resp = self.client.get("/api/v1/location/search?query=a")
        self.assertEqual(resp.status_code, 422)

    def test_weather_irregularity_heavy_rain(self):
        """Evaluates heavy rain irregularity (>60% rain prob) triggers urea hold."""
        hold, heat, et0, rh, irs = evaluate_weather_irregularities(
            current_temp_c=25.0,
            relative_humidity_pct=70.0,
            et0_fao_mm_day=2.5,
            rain_prob_48h_pct=75,
            precipitation_sum_mm=18.0,
            language="hi",
        )
        self.assertTrue(hold)
        self.assertFalse(heat)
        self.assertFalse(et0)
        self.assertEqual(len(irs), 1)
        self.assertEqual(irs[0].code, "heavy_rain")
        self.assertIn("यूरिया", irs[0].title_hi)
        self.assertIn("Urea", irs[0].title_en)

    def test_weather_irregularity_heat_and_et0(self):
        """Evaluates heatwave (temp >= 35°C) and high evaporative deficit (ET0 >= 5.0)."""
        hold, heat, et0, rh, irs = evaluate_weather_irregularities(
            current_temp_c=38.5,
            relative_humidity_pct=25.0,
            et0_fao_mm_day=5.8,
            rain_prob_48h_pct=5,
            precipitation_sum_mm=0.0,
            language="hi",
        )
        self.assertFalse(hold)
        self.assertTrue(heat)
        self.assertTrue(et0)
        codes = [i.code for i in irs]
        self.assertIn("heat_stress", codes)
        self.assertIn("high_et0", codes)

    def test_weather_irregularity_high_humidity(self):
        """Evaluates high humidity (RH >= 80%) fungal pathogen incubation risk."""
        hold, heat, et0, rh, irs = evaluate_weather_irregularities(
            current_temp_c=26.0,
            relative_humidity_pct=88.0,
            et0_fao_mm_day=2.8,
            rain_prob_48h_pct=20,
            precipitation_sum_mm=0.0,
            language="en",
        )
        self.assertTrue(rh)
        codes = [i.code for i in irs]
        self.assertIn("high_humidity", codes)
        self.assertIn("Disease", irs[0].title_en)
        self.assertIn("fungal", irs[0].message_en.lower())

    def test_advisory_hyperlocal_coordinates_integration(self):
        """Passing exact village coordinates enriches advisory with live weather & baseline."""
        payload = {
            "zone": "zone4",
            "crop": "wheat",
            "area_ha": 1.0,
            "lat": 25.4196,  # Zamania village, Ghazipur
            "lon": 83.5579,
            "language": "hi",
        }
        resp = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNotNone(data.get("live_weather"))
        self.assertIn("product_plan", data)
        self.assertGreater(data["product_plan"]["dap_bags_50kg"], 0)


if __name__ == "__main__":
    unittest.main()
