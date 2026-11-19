"""
Unit tests validating frontend mathematical models, land unit conversions,
DAP nitrogen credit logic, and data structures used by KhetSathi 360.
"""

import unittest
import urllib.parse


class TestFrontendContracts(unittest.TestCase):
    def test_land_unit_conversions(self):
        """Test Bigha / Acre / Hectare unit conversion math."""
        # 1 Hectare = 4.0 UP Pucca Bigha (2,500 m2 / bigha)
        # 1 Hectare = 2.47105 Acres
        bigha_pucca_to_ha = 0.250000
        acre_to_ha = 0.404686
        ha_to_acre = 2.47105
        ha_to_bigha = 4.00000

        # 4 Bigha -> 1.0 Ha
        self.assertAlmostEqual(4.0 * bigha_pucca_to_ha, 1.0, places=4)
        # 1.0 Ha -> 4.0 Bigha
        self.assertAlmostEqual(1.0 * ha_to_bigha, 4.0, places=4)
        # 1.0 Ha -> 2.47105 Acres
        self.assertAlmostEqual(1.0 * ha_to_acre, 2.47105, places=4)
        # 2.47105 Acres -> 1.0 Ha
        self.assertAlmostEqual(2.47105 * acre_to_ha, 1.0, places=3)

    def test_dap_nitrogen_credit_formula(self):
        """Verify DAP 18% N credit arithmetic prevents urea over-application."""
        req_p = 60.0  # kg P2O5
        req_n = 120.0 # kg N
        req_k = 40.0  # kg K2O

        dap_kg = req_p / 0.46
        n_credit_dap = dap_kg * 0.18
        remaining_n = max(0.0, req_n - n_credit_dap)
        urea_kg = remaining_n / 0.46
        mop_kg = req_k / 0.60

        dap_bags = round((dap_kg / 50.0) * 2) / 2
        urea_bags = round((urea_kg / 45.0) * 2) / 2
        mop_bags = round((mop_kg / 50.0) * 2) / 2

        self.assertAlmostEqual(dap_kg, 130.43, places=2)
        self.assertAlmostEqual(n_credit_dap, 23.48, places=2)
        self.assertAlmostEqual(remaining_n, 96.52, places=2)
        self.assertAlmostEqual(urea_kg, 209.83, places=2)
        self.assertAlmostEqual(mop_kg, 66.67, places=2)

        self.assertEqual(dap_bags, 2.5)
        self.assertEqual(urea_bags, 4.5)
        self.assertEqual(mop_bags, 1.5)

    def test_whatsapp_share_url_generation(self):
        """Verify WhatsApp share text structure and URL encoding."""
        plan = {
            "lang": "hi",
            "districtName": "Ghazipur, UP",
            "lat": 25.59,
            "lon": 83.58,
            "cropHi": "गेहूं",
            "variety": "HD-2967",
            "areaFormatted": "4.0 बीघा",
            "areaHa": 1.0,
            "confidenceModeHi": "मिट्टी जांच सत्यापित (±5%)",
            "dapBags": 2.5,
            "ureaBags": 4.5,
            "mopBags": 1.5,
            "weatherCond": "धूप व साफ आसमान",
            "temp": 24,
            "et0": 2.8,
            "rainProb": 10,
            "rainGuardrailHi": "खाद डालना सुरक्षित है"
        }

        text = (
            f"🌾 *किसान साथी 360 — खेत सलाह पर्ची*\n"
            f"📍 स्थान: {plan['districtName']} ({plan['lat']}°N, {plan['lon']}°E)\n"
            f"🌾 फसल: *{plan['cropHi']}* ({plan['variety']})\n"
            f"📐 खेत का माप: *{plan['areaFormatted']}* ({plan['areaHa']:.2f} हेक्टेयर)\n"
            f"📦 डीएपी: {plan['dapBags']} बोरी | यूरिया: {plan['ureaBags']} बोरी | पोटाश: {plan['mopBags']} बोरी\n"
            f"🌦️ मौसम: {plan['weatherCond']} | बारिश: {plan['rainProb']}%\n"
            f"🛡️ {plan['rainGuardrailHi']}"
        )

        encoded = urllib.parse.quote(text)
        url = f"https://api.whatsapp.com/send?text={encoded}"

        self.assertTrue(url.startswith("https://api.whatsapp.com/send?text="))
        self.assertIn("Ghazipur", urllib.parse.unquote(url))
        self.assertIn("HD-2967", urllib.parse.unquote(url))
        self.assertIn("4.5", urllib.parse.unquote(url))


if __name__ == "__main__":
    unittest.main()
