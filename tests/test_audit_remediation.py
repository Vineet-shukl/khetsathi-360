"""
tests/test_audit_remediation.py
Automated regression tests verifying all security, XSS sanitization, parameter validation,
bilingual parity, and DOM contract remediations from the code audit.
"""

import html
import re
from pathlib import Path
import unittest
from fastapi.testclient import TestClient

from app.api import app
from app.seed_store_service import get_nearby_government_seed_stores


class TestAuditRemediation(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.html_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        self.assertTrue(self.html_path.exists())
        self.html_content = self.html_path.read_text(encoding="utf-8")

    def test_api_parameter_guardrails(self):
        """API endpoints must reject invalid inputs with HTTP 422."""
        # 1. Invalid crop pattern (e.g. script tags, SQL injection, spaces)
        res1 = self.client.get("/api/v1/crop/alternative-and-machinery?crop=<script>alert(1)</script>&area_ha=1.0")
        self.assertEqual(res1.status_code, 422)

        # 2. Out of bounds area_ha (> 500 Ha)
        res2 = self.client.get("/api/v1/crop/alternative-and-machinery?crop=wheat&area_ha=9999.0")
        self.assertEqual(res2.status_code, 422)

        # 3. Invalid language code
        res3 = self.client.get("/api/v1/crop/alternative-and-machinery?crop=wheat&area_ha=1.0&lang=fr")
        self.assertEqual(res3.status_code, 422)

        # 4. Certified seed endpoint parameter validation
        res4 = self.client.get("/api/v1/seed/certified-and-stores?crop=wheat;DROP+TABLE&area_ha=1.0")
        self.assertEqual(res4.status_code, 422)

    def test_seed_store_xss_sanitization(self):
        """Seed store directory must sanitize reflected district names against XSS."""
        malicious_district = '<script>alert("xss")</script>Ghazipur'
        stores = get_nearby_government_seed_stores(district=malicious_district)
        for store in stores:
            # Must not contain raw unescaped script tag
            self.assertNotIn("<script>", store["name"])
            self.assertNotIn("<script>", store["address"])
            self.assertNotIn("<script>", store["id"])

    def test_frontend_escape_html_present(self):
        """Frontend script must define escapeHtml utility function."""
        self.assertIn("function escapeHtml(str)", self.html_content)

    def test_no_orphan_plot_area_ids(self):
        """Script must never query non-existent plot-area or plot-unit IDs."""
        scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', self.html_content)
        all_js = "\n".join(scripts)
        bad_matches = re.findall(r'getEl\([\'"]plot-(?:area|unit)[\'"]\)', all_js)
        self.assertEqual(bad_matches, [], f"Found orphaned element IDs: {bad_matches}")

    def test_html_tag_balance(self):
        """HTML must have perfectly matched container tags."""
        div_open = len(re.findall(r'<div\b', self.html_content))
        div_close = len(re.findall(r'</div>', self.html_content))
        self.assertEqual(div_open, div_close, f"Div mismatch: {div_open} open vs {div_close} close")

        btn_open = len(re.findall(r'<button\b', self.html_content))
        btn_close = len(re.findall(r'</button>', self.html_content))
        self.assertEqual(btn_open, btn_close, f"Button mismatch: {btn_open} open vs {btn_close} close")

    def test_bilingual_idmap_coverage(self):
        """All critical DOM labels must be wired to idMap for Hindi and English toggle."""
        required_labels = [
            "lbl-alt-popup-title",
            "lbl-view-machinery",
            "lbl-apply-alt-crop",
            "lbl-soil-benefits-title",
            "lbl-org-vc-title",
            "lbl-org-jeeva-title",
            "lbl-org-neem-title",
            "lbl-benefit-bio-desc",
            "lbl-benefit-water-desc",
            "lbl-benefit-carbon-desc",
            "map-measure-hint",
            "lbl-apply-area",
            "lbl-clear-measure",
            "map-overlay-title",
        ]
        for lbl in required_labels:
            self.assertIn(f'"{lbl}":', self.html_content, f"Missing idMap mapping for: {lbl}")

    def test_touch_target_accessibility(self):
        """Interactive controls in map and popup must meet WCAG 2.2 touch target minimums (44px)."""
        controls = [
            "btn-detect-gps-inline",
            "btn-toggle-map",
            "btn-toggle-coord-nudge",
            "btn-minimize-alt-popup",
            "btn-close-alt-popup",
            "btn-apply-alt-crop",
            "btn-view-machinery-plan",
        ]
        for c in controls:
            pattern = rf'id="{c}"[^>]*class="[^"]*min-h-\[44px\]'
            match = re.search(pattern, self.html_content)
            self.assertIsNotNone(match, f"Control {c} lacks min-h-[44px] touch target class")


if __name__ == "__main__":
    unittest.main()
