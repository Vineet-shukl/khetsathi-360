import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.api import app

MOCK_NEURAL_MP3 = b"ID3\x03\x00\x00\x00\x00\x00\x00" + b"\xff\xfb\x90d\x00" * 150


class TestTTSEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.tts_service.synthesize_neural_speech", new_callable=AsyncMock)
    def test_tts_synthesize_hindi(self, mock_synth):
        """Verifies zero-cost Neural TTS synthesis in Hindi returns audio/mpeg."""
        mock_synth.return_value = MOCK_NEURAL_MP3
        resp = self.client.get("/api/v1/tts/synthesize?text=नमस्कार किसान भाई, खेत में डीएपी डालें&lang=hi")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("content-type"), "audio/mpeg")
        self.assertGreater(len(resp.content), 500)
        self.assertIn("inline", resp.headers.get("content-disposition", ""))
        mock_synth.assert_awaited_once_with(text="नमस्कार किसान भाई, खेत में डीएपी डालें", lang="hi", voice=None)

    @patch("app.tts_service.synthesize_neural_speech", new_callable=AsyncMock)
    def test_tts_synthesize_english(self, mock_synth):
        """Verifies Neural TTS synthesis in Indian English."""
        mock_synth.return_value = MOCK_NEURAL_MP3
        resp = self.client.get("/api/v1/tts/synthesize?text=Hello farmer, your advisory is ready&lang=en")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("content-type"), "audio/mpeg")
        self.assertGreater(len(resp.content), 500)
        mock_synth.assert_awaited_once_with(text="Hello farmer, your advisory is ready", lang="en", voice=None)

    def test_tts_empty_text_validation(self):
        """Verifies empty or whitespace-only text returns 422."""
        resp = self.client.get("/api/v1/tts/synthesize?text=&lang=hi")
        self.assertEqual(resp.status_code, 422)

    @patch("app.tts_service.synthesize_neural_speech", new_callable=AsyncMock)
    def test_tts_upstream_failure_handling(self, mock_synth):
        """Verifies external TTS service failure returns HTTP 500 gracefully."""
        mock_synth.side_effect = RuntimeError("Edge TTS upstream timeout")
        resp = self.client.get("/api/v1/tts/synthesize?text=Sample+text&lang=hi")
        self.assertEqual(resp.status_code, 500)
        self.assertIn("Speech synthesis error", resp.json().get("detail", ""))


if __name__ == "__main__":
    unittest.main()
