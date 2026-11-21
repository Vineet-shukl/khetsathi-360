import unittest

from fastapi.testclient import TestClient

from app.api import app


class TestFutureOrganicHub(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_future_endpoint_served(self):
        """Verifies /future endpoint serves the next-generation organic hub."""
        resp = self.client.get("/future")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers["content-type"])
        html = resp.text
        self.assertIn("KhetSathi", html)
        self.assertIn("अमृत माटी", html)
        self.assertIn("years-slider", html)
        self.assertIn("Jeevamrit", html)
        self.assertIn("Beejamrit", html)
        self.assertIn("Neemastra", html)

    def test_organic_alias_endpoint_served(self):
        """Verifies /organic alias routes to the same future organic interface."""
        resp = self.client.get("/organic")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers["content-type"])
        self.assertIn("अमृत माटी", resp.text)

    def test_working_root_unaffected(self):
        """Ensures the working production root UI at / and /ui remains 100% operational."""
        resp_root = self.client.get("/")
        self.assertEqual(resp_root.status_code, 200)
        self.assertIn("text/html", resp_root.headers["content-type"])
        self.assertIn("KhetSathi 360", resp_root.text)
        self.assertIn("किसान सलाहकार", resp_root.text)

        resp_ui = self.client.get("/ui")
        self.assertEqual(resp_ui.status_code, 200)


if __name__ == "__main__":
    unittest.main()
