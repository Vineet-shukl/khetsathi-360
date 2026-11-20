import io
import unittest
from fastapi.testclient import TestClient
from app.api import app


class TestSHCVisionOCR(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_shc_ocr_upload_endpoint(self):
        """Verifies multimodal Soil Health Card OCR upload endpoint returns 12 parameters."""
        dummy_image = io.BytesIO(b"fake-image-bytes-representing-a-soil-health-card-scan")
        resp = self.client.post(
            "/api/v1/shc/ocr-upload",
            files={"file": ("soil_health_card.jpg", dummy_image, "image/jpeg")},
            params={"district": "Ghazipur"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("n_kg_ha", data)
        self.assertIn("p_kg_ha", data)
        self.assertIn("k_kg_ha", data)
        self.assertIn("oc_pct", data)
        self.assertIn("ph", data)
        self.assertIn("zn_ppm", data)
        self.assertGreater(data["confidence_pct"], 80.0)
        self.assertIn("extracted_via", data)

    def test_shc_ocr_upload_empty_file(self):
        """Verifies empty uploaded file returns 422."""
        empty_file = io.BytesIO(b"")
        resp = self.client.post(
            "/api/v1/shc/ocr-upload",
            files={"file": ("empty.jpg", empty_file, "image/jpeg")}
        )
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
