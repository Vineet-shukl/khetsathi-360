import unittest
from fastapi.testclient import TestClient
from app.api import app


class TestTTSEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_tts_synthesize_hindi(self):
        """Verifies zero-cost Neural TTS synthesis in Hindi returns audio/mpeg."""
        resp = self.client.get("/api/v1/tts/synthesize?text=नमस्कार किसान भाई, खेत में डीएपी डालें&lang=hi")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("content-type"), "audio/mpeg")
        self.assertGreater(len(resp.content), 500)
        self.assertIn("inline", resp.headers.get("content-disposition", ""))

    def test_tts_synthesize_english(self):
        """Verifies Neural TTS synthesis in Indian English."""
        resp = self.client.get("/api/v1/tts/synthesize?text=Hello farmer, your advisory is ready&lang=en")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("content-type"), "audio/mpeg")
        self.assertGreater(len(resp.content), 500)

    def test_tts_empty_text_validation(self):
        """Verifies empty or whitespace-only text returns 422."""
        resp = self.client.get("/api/v1/tts/synthesize?text=&lang=hi")
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
