"""
tests/test_fpo_realtime.py — Tests for Real-Time Mandi Prices, FPO SQLite Records, and Closed-Loop Events.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app
from app.mandi_service import _AGMARKNET_CACHE


class TestFPORealtimeSystem(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / "test_fpo.db"
        self.prev_db = os.environ.get("KHETSATHI_FPO_DB")
        self.prev_gov_key = os.environ.get("DATA_GOV_IN_API_KEY")
        os.environ["KHETSATHI_FPO_DB"] = str(self.db_path)
        os.environ.pop("DATA_GOV_IN_API_KEY", None)
        _AGMARKNET_CACHE.clear()
        self.client = TestClient(app)

    def tearDown(self):
        if self.prev_db is not None:
            os.environ["KHETSATHI_FPO_DB"] = self.prev_db
        else:
            os.environ.pop("KHETSATHI_FPO_DB", None)
        if self.prev_gov_key is not None:
            os.environ["DATA_GOV_IN_API_KEY"] = self.prev_gov_key
        else:
            os.environ.pop("DATA_GOV_IN_API_KEY", None)
        _AGMARKNET_CACHE.clear()
        self.tmpdir.cleanup()

    def test_mandi_prices_benchmark_and_spot_quote_override(self):
        res = self.client.get("/api/v1/fpo/mandi-prices?crop=mustard")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["crop"], "mustard")
        self.assertEqual(data["cacp_msp_inr_per_q"], 6200.0)
        self.assertEqual(len(data["zones"]), 6)
        self.assertFalse(data["live_feed_connected"])

        # Persist a live spot mandi quote for Zone 4 and verify live update
        quote_res = self.client.post(
            "/api/v1/fpo/mandi-prices/quote",
            json={
                "crop": "mustard",
                "zone": "zone4",
                "market_hub": "Varanasi APMC",
                "min_price_inr_per_q": 6350,
                "modal_price_inr_per_q": 6650,
                "max_price_inr_per_q": 6850,
            },
        )
        self.assertEqual(quote_res.status_code, 200)
        updated = quote_res.json()
        self.assertTrue(updated["live_feed_connected"])
        z4 = next(z for z in updated["zones"] if z["zone"] == "zone4")
        self.assertEqual(z4["price_source"], "fpo_spot_quote")
        self.assertEqual(z4["market_hub"], "Varanasi APMC")
        self.assertEqual(z4["modal_price_inr_per_q"], 6650.0)
        self.assertEqual(z4["msp_delta_inr_per_q"], 450.0)

    def test_mandi_prices_agmarknet_live_connector(self):
        os.environ["DATA_GOV_IN_API_KEY"] = "test-demo-key"

        class _MockResp:
            def read(self):
                return json.dumps(
                    {
                        "records": [
                            {
                                "state": "Uttar Pradesh",
                                "district": "Ghazipur",
                                "market": "Ghazipur",
                                "min_price": "2610",
                                "modal_price": "2740",
                                "max_price": "2820",
                                "arrival_date": "26/11/2026",
                            }
                        ]
                    }
                ).encode("utf-8")

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        with patch("app.mandi_service.urllib.request.urlopen", return_value=_MockResp()):
            res = self.client.get("/api/v1/fpo/mandi-prices?crop=wheat&refresh=true")

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["live_feed_connected"])
        z4 = next(z for z in data["zones"] if z["zone"] == "zone4")
        self.assertEqual(z4["price_source"], "agmarknet_live")
        self.assertEqual(z4["modal_price_inr_per_q"], 2740.0)
        self.assertEqual(z4["market_hub"], "Ghazipur APMC")

    def test_fpo_records_crud_valuation_and_filters(self):
        initial = self.client.get("/api/v1/fpo/records")
        self.assertEqual(initial.status_code, 200)
        payload = initial.json()
        self.assertGreaterEqual(payload["summary"]["total_records"], 6)
        self.assertGreater(payload["summary"]["estimated_cluster_revenue_inr"], 0)

        # Create a new farmer record
        created = self.client.post(
            "/api/v1/fpo/records",
            json={
                "farmer_name": "Sunita Devi",
                "village": "Karanda",
                "district": "Ghazipur",
                "zone": "zone4",
                "crop": "mustard",
                "area_ha": 2.0,
                "n_kg_ha": 190.0,
                "p_kg_ha": 12.0,
                "k_kg_ha": 160.0,
                "oc_pct": 0.42,
                "ph": 7.4,
                "zn_ppm": 0.48,
                "soil_source": "ocr_scan",
                "lot_status": "growing",
            },
        )
        self.assertEqual(created.status_code, 200)
        rec = created.json()
        rec_id = rec["id"]
        self.assertEqual(rec["farmer_name"], "Sunita Devi")
        self.assertGreater(rec["estimated_value_inr"], 100000)

        # Filter by search query
        searched = self.client.get("/api/v1/fpo/records?q=Sunita")
        self.assertEqual(searched.status_code, 200)
        self.assertEqual(len(searched.json()["records"]), 1)

        # Update lot status
        patched = self.client.patch(f"/api/v1/fpo/records/{rec_id}", json={"lot_status": "ready_to_sell"})
        self.assertEqual(patched.status_code, 200)
        self.assertEqual(patched.json()["lot_status"], "ready_to_sell")

        # Delete record
        deleted = self.client.delete(f"/api/v1/fpo/records/{rec_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertTrue(deleted.json()["deleted"])

    def test_fpo_assimilation_events_persistence(self):
        ev = self.client.post(
            "/api/v1/fpo/events",
            json={
                "event_type": "yellowing",
                "note": "Plot 4 lower leaves pale",
                "district": "Ghazipur",
                "crop": "wheat",
            },
        )
        self.assertEqual(ev.status_code, 200)
        created = ev.json()
        self.assertEqual(created["event_type"], "yellowing")
        self.assertIn("Zinc Sulphate", created["action_summary_en"])

        listing = self.client.get("/api/v1/fpo/events?limit=5")
        self.assertEqual(listing.status_code, 200)
        events = listing.json()
        self.assertTrue(any(e["id"] == created["id"] for e in events))
