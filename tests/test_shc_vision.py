import io
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.api import app

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "shc_samples"


class TestSHCVisionOCR(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_shc_ocr_upload_endpoint(self):
        """Verifies multimodal Soil Health Card OCR upload endpoint returns 12 parameters."""
        dummy_image = io.BytesIO(b"fake-image-bytes-representing-a-soil-health-card-scan")
        resp = self.client.post(
            "/api/v1/shc/ocr-upload",
            files={"file": ("soil_health_card.jpg", dummy_image, "image/jpeg")},
            params={"district": "Ghazipur"},
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
        resp = self.client.post("/api/v1/shc/ocr-upload", files={"file": ("empty.jpg", empty_file, "image/jpeg")})
        self.assertEqual(resp.status_code, 422)

    def test_shc_ocr_rejects_resume_document(self):
        """Guardrail: Non-SHC resume document must be rejected with 422."""
        resume_path = FIXTURES_DIR / "sample_resume_document.png"
        self.assertTrue(resume_path.exists(), f"Fixture missing: {resume_path}")

        with open(resume_path, "rb") as f:
            resume_bytes = f.read()

        resp = self.client.post(
            "/api/v1/shc/ocr-upload",
            files={"file": ("software_engineer_resume.png", resume_bytes, "image/png")},
        )
        self.assertEqual(resp.status_code, 422)
        detail = resp.json().get("detail", "")
        self.assertTrue(
            "अमान्य" in detail or "Invalid" in detail or "Resume" in detail or "मृदा स्वास्थ्य कार्ड नहीं" in detail,
            f"Unexpected detail: {detail}",
        )

    def test_shc_ocr_rejects_invoice_document(self):
        """Guardrail: Non-SHC tax invoice document must be rejected with 422."""
        invoice_path = FIXTURES_DIR / "sample_invoice_document.png"
        self.assertTrue(invoice_path.exists(), f"Fixture missing: {invoice_path}")

        with open(invoice_path, "rb") as f:
            invoice_bytes = f.read()

        resp = self.client.post(
            "/api/v1/shc/ocr-upload",
            files={"file": ("tax_invoice_march.png", invoice_bytes, "image/png")},
        )
        self.assertEqual(resp.status_code, 422)
        detail = resp.json().get("detail", "")
        self.assertTrue("अमान्य" in detail or "Invalid" in detail, f"Unexpected detail: {detail}")

    def test_shc_ocr_rejects_resume_filename_pattern(self):
        """Guardrail: Filenames clearly denoting resumes/cvs are rejected immediately."""
        fake_bytes = b"X" * 200
        for bad_name in ["Vineet_Kumar_Resume.pdf", "curriculum_vitae_2026.png", "monthly_payslip_oct.pdf"]:
            resp = self.client.post(
                "/api/v1/shc/ocr-upload",
                files={"file": (bad_name, fake_bytes, "application/pdf")},
            )
            self.assertEqual(resp.status_code, 422, f"Failed to reject bad filename: {bad_name}")

    def test_shc_ocr_accepts_authentic_shc_samples(self):
        """Accuracy benchmark: Public authentic SHC samples must extract valid soil parameters."""
        shc_samples = [
            ("real_soil_health_card_1.jpg", "image/jpeg"),
            ("sample_hindi_shc.png", "image/png"),
        ]

        for filename, mime in shc_samples:
            sample_path = FIXTURES_DIR / filename
            self.assertTrue(sample_path.exists(), f"Fixture missing: {sample_path}")

            with open(sample_path, "rb") as f:
                sample_bytes = f.read()

            resp = self.client.post(
                "/api/v1/shc/ocr-upload",
                files={"file": (filename, sample_bytes, mime)},
                params={"district": "Varanasi"},
            )
            self.assertEqual(resp.status_code, 200, f"Failed on sample {filename}: {resp.text}")
            data = resp.json()

            # Verify physical bounds according to DAC&FW guidelines
            self.assertGreaterEqual(data["n_kg_ha"], 10.0)
            self.assertLessEqual(data["n_kg_ha"], 1000.0)
            self.assertGreaterEqual(data["p_kg_ha"], 1.0)
            self.assertLessEqual(data["p_kg_ha"], 200.0)
            self.assertGreaterEqual(data["k_kg_ha"], 10.0)
            self.assertLessEqual(data["k_kg_ha"], 1000.0)
            self.assertGreaterEqual(data["ph"], 4.0)
            self.assertLessEqual(data["ph"], 10.5)
            self.assertGreaterEqual(data["oc_pct"], 0.05)
            self.assertLessEqual(data["oc_pct"], 3.0)


if __name__ == "__main__":
    unittest.main()
