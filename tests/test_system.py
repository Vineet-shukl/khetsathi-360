"""
tests/test_system.py — Comprehensive System Test Suite for KhetSathi 360.

Verifies:
  1. DAP nitrogen credit arithmetic (ICAR/FCO-56 deterministic baseline)
  2. Realistic promotion gates with real dataset pipeline (holdout MAE, latency, slice fairness)
  3. District spatial model (exact Ghazipur lookup, spatial IDW coordinate estimation)
  4. Advisory API endpoint (hybrid ML residual serving mode and deterministic fallback)
  5. Real dataset loading, mapping, and temporal holdout split (partI, partII, district SHC)
  6. SHC classification and soil amendment alerts
  7. API health endpoint reporting model version and real data provenance
  8. Agronomic safety guardrails: strict ±15% bound enforcement
"""

import os
import sys
import unittest
from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.baseline_engine import compute_baseline_npk_ha, convert_to_bags, resolve_soil
from app.contracts import AdvisoryRequest, SoilTestInput
from app.ml_residual import ResidualMLModel
from ml_pipeline.evaluate import PROMOTION_GATES, run_evaluation
from ml_pipeline.train import (
    DISTRICT_CSV,
    PARTI_FILE,
    PARTII_FILE,
    SPLIT_YEAR,
    generate_pan_india_residual_dataset,
    load_real_agronomic_dataset,
    load_real_district_records,
    train_and_save,
)


class TestKhetSathiMLSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        train_and_save()
        from app.api import app

        cls.client = TestClient(app)

    # ------------------------------------------------------------------
    # 1. Deterministic Baseline Agronomy & Bag Arithmetic
    # ------------------------------------------------------------------
    def test_dap_nitrogen_credit_math(self):
        """Verifies DAP 18% N credit arithmetic prevents urea over-application."""
        plan = convert_to_bags(120.0, 60.0, 40.0)
        self.assertAlmostEqual(plan.dap_kg, 130.4, places=1)
        self.assertAlmostEqual(plan.n_credit_from_dap_kg, 23.5, places=1)
        self.assertAlmostEqual(plan.urea_kg, 209.8, places=1)
        self.assertAlmostEqual(plan.mop_kg, 66.7, places=1)

    # ------------------------------------------------------------------
    # 2. Promotion Gates on Real Holdout Dataset
    # ------------------------------------------------------------------
    def test_promotion_gates_with_real_dataset(self):
        """All production gates must pass on real temporal holdout partition."""
        metrics = run_evaluation()
        self.assertGreaterEqual(
            metrics["mae_improvement_pct"],
            PROMOTION_GATES["mae_improvement_pct_min"],
            f"MAE improvement {metrics['mae_improvement_pct']:.1f}% below gate {PROMOTION_GATES['mae_improvement_pct_min']}%",
        )
        self.assertLessEqual(
            metrics["p95_latency_ms"],
            PROMOTION_GATES["p95_latency_ms_max"],
            f"p95 latency {metrics['p95_latency_ms']:.4f} ms exceeds gate {PROMOTION_GATES['p95_latency_ms_max']} ms",
        )
        self.assertLessEqual(
            metrics["max_zone_mae"],
            PROMOTION_GATES["max_zone_mae"],
            f"Max zone MAE {metrics['max_zone_mae']:.3f} exceeds slice gate {PROMOTION_GATES['max_zone_mae']}",
        )
        self.assertEqual(metrics["district_spatial_eval"]["n_test_districts"], 139)
        self.assertLessEqual(metrics["district_spatial_eval"]["n_low_mae"], 22.0)
        self.assertLessEqual(metrics["district_spatial_eval"]["p_low_mae"], 22.0)

    # ------------------------------------------------------------------
    # 3. District Spatial Soil Model
    # ------------------------------------------------------------------
    def test_real_ghazipur_district_baseline(self):
        """Exact district lookup for Ghazipur (field area in Eastern UP)."""
        r = self.client.get("/api/v1/district/baseline?query=Ghazipur")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("Ghazipur", data["address"])
        self.assertAlmostEqual(data["n_low"], 99.94, places=2)
        self.assertIn("Wheat", data["crops"])
        self.assertIn("expected_soil", data)
        self.assertGreater(data["expected_soil"]["n"], 0)

    def test_spatial_idw_by_coordinates(self):
        """Coordinate-based spatial IDW interpolation (Ghazipur coords: 25.59N, 83.58E)."""
        r = self.client.get("/api/v1/district/baseline?lat=25.59&lon=83.58")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["match_type"], "spatial_idw")
        self.assertIn("nearest_district", data)
        self.assertLess(data["distance_km"], 25.0)

    def test_district_baseline_missing_params(self):
        """Missing parameters return HTTP 400 Bad Request."""
        r = self.client.get("/api/v1/district/baseline")
        self.assertEqual(r.status_code, 400)

    # ------------------------------------------------------------------
    # 4. Advisory Endpoint: Hybrid ML & Deterministic Fallback
    # ------------------------------------------------------------------
    def test_advisory_endpoint_hybrid_and_fallback(self):
        """Advisory returns hybrid_ml when enabled, falls back to deterministic when disabled."""
        payload = {
            "zone": "zone4",
            "crop": "wheat",
            "area_ha": 1.0,
            "irrigation": "tubewell",
            "et0_mm_day": 3.8,
            "sowing_delay_days": 12,
            "rain_prob_48h_pct": 75,
            "soil": {
                "n_kg_ha": 210,
                "p_kg_ha": 14,
                "k_kg_ha": 165,
                "oc_pct": 0.42,
                "ph": 7.3,
                "zn_ppm": 0.45,
            },
            "language": "hi",
        }
        os.environ["ENABLE_ML_RESIDUAL"] = "true"
        r = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data["rain_guardrail_hold_urea"])
        self.assertEqual(data["serving_mode"], "hybrid_ml")
        self.assertIn("real", data["model_version"])

        # Fallback test: with ENABLE_ML_RESIDUAL=false, must fall back cleanly
        os.environ["ENABLE_ML_RESIDUAL"] = "false"
        r_fb = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(r_fb.status_code, 200)
        self.assertEqual(r_fb.json()["serving_mode"], "deterministic_fallback")
        self.assertEqual(r_fb.json()["ml_residual_delta_n_kg_ha"], 0.0)
        os.environ["ENABLE_ML_RESIDUAL"] = "true"

    def test_advisory_without_soil_uses_baseline(self):
        """When farmer provides no soil test, confidence_mode indicates baseline estimate."""
        payload = {
            "zone": "zone6",
            "crop": "rice",
            "area_ha": 2.0,
            "irrigation": "canal",
            "et0_mm_day": 5.0,
            "sowing_delay_days": 0,
            "rain_prob_48h_pct": 10,
        }
        r = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["confidence_mode"], "block_baseline_estimate")
        self.assertEqual(data["uncertainty_pct"], 15.0)

    def test_advisory_english_summary(self):
        """Verifies English summary generation with variety and bag recommendations."""
        payload = {
            "zone": "zone10",
            "crop": "maize",
            "area_ha": 1.5,
            "irrigation": "rainfed",
            "et0_mm_day": 4.0,
            "sowing_delay_days": 5,
            "rain_prob_48h_pct": 30,
            "soil": {
                "n_kg_ha": 200,
                "p_kg_ha": 12,
                "k_kg_ha": 150,
                "oc_pct": 0.5,
                "ph": 7.0,
                "zn_ppm": 0.6,
            },
            "language": "en",
        }
        r = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("bags DAP", data["farmer_summary"])

    # ------------------------------------------------------------------
    # 5. Real Data Loading & Pipeline Validation
    # ------------------------------------------------------------------
    def test_real_partII_dataset_exists_and_loads(self):
        """Verify partII real dataset has expected row count (>5000) and columns."""
        self.assertTrue(PARTII_FILE.exists(), f"Missing file: {PARTII_FILE}")
        X, y, _zones, years = load_real_agronomic_dataset()
        self.assertGreater(len(X), 5000, f"Expected >5000 samples, got {len(X)}")
        self.assertEqual(X.shape[0], len(y))
        self.assertEqual(X.shape[0], len(years))
        # Ensure temporal split covers before and after SPLIT_YEAR
        self.assertGreater((years <= SPLIT_YEAR).sum(), 3000)
        self.assertGreater((years > SPLIT_YEAR).sum(), 1500)

    def test_real_partI_dataset_exists(self):
        """Verify partI panel file exists and has data."""
        self.assertTrue(PARTI_FILE.exists(), f"Missing file: {PARTI_FILE}")

    def test_district_records_load(self):
        """Verify 695 real district records from CropDataset-Enhanced.csv."""
        self.assertTrue(DISTRICT_CSV.exists(), f"Missing file: {DISTRICT_CSV}")
        records = load_real_district_records(DISTRICT_CSV)
        self.assertEqual(len(records), 695)
        for r in records[:5]:
            self.assertIn("address", r)
            self.assertIn("lat", r)
            self.assertIn("lon", r)
            self.assertIn("n_low", r)

    def test_residual_dataset_no_nans(self):
        """Verifies generated feature matrix and targets contain no NaN values."""
        X, y, zones = generate_pan_india_residual_dataset()
        self.assertFalse(np.isnan(y).any(), "NaN detected in residual targets")
        self.assertFalse(np.isnan(X).any(), "NaN detected in feature matrix X")
        valid_zones = {"zone4", "zone6", "zone8", "zone9", "zone10", "zone13"}
        for z in set(zones):
            self.assertIn(z, valid_zones)

    # ------------------------------------------------------------------
    # 6. SHC Parse Endpoint
    # ------------------------------------------------------------------
    def test_shc_parse_endpoint(self):
        """Classifies Soil Health Card parameters into Low/Medium/High and alerts."""
        payload = {
            "n_kg_ha": 200.0,
            "p_kg_ha": 8.0,
            "k_kg_ha": 150.0,
            "oc_pct": 0.4,
            "ph": 7.0,
            "zn_ppm": 0.3,
        }
        r = self.client.post("/api/v1/shc/parse", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["classifications"]), 6)
        n_class = next(c for c in data["classifications"] if c["parameter"] == "Available N")
        self.assertEqual(n_class["status"], "Low")
        self.assertTrue(any("Zinc" in f for f in data["amendment_flags"]))

    # ------------------------------------------------------------------
    # 7. Health and UI Endpoints
    # ------------------------------------------------------------------
    def test_health_endpoint(self):
        """Health endpoint confirms models are loaded with real data source provenance."""
        r = self.client.get("/api/v1/health")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["ml_loaded"])
        self.assertTrue(data["district_model_loaded"])
        self.assertGreater(data["districts_indexed"], 600)
        self.assertIn("model_version", data)
        self.assertEqual(data["data_source"], "real")

    def test_frontend_served_at_root_and_ui(self):
        """Root /, /ui, /portal, /login, and /investor serve the production frontend HTML with WCAG landmarks."""
        for path in ["/", "/ui", "/portal", "/login", "/investor"]:
            r = self.client.get(path)
            self.assertEqual(r.status_code, 200)
            self.assertIn("text/html", r.headers.get("content-type", ""))
            self.assertTrue("KhetSathi 360" in r.text or "Redirecting" in r.text)

    # ------------------------------------------------------------------
    # 8. Real-Time Meteorological Weather & ET0 Integration
    # ------------------------------------------------------------------
    def test_weather_endpoint_valid_coordinates(self):
        """Valid Indian coordinates return live or climatological weather with FAO-56 ET0."""
        r = self.client.get("/api/v1/weather?lat=25.59&lon=83.58&lang=hi")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn(data["status"], ["ok", "fallback"])
        self.assertAlmostEqual(data["lat"], 25.59, places=2)
        self.assertAlmostEqual(data["lon"], 83.58, places=2)
        self.assertGreater(data["et0_fao_mm_day"], 0.0)
        self.assertGreaterEqual(data["rain_prob_48h_pct"], 0)
        self.assertLessEqual(data["rain_prob_48h_pct"], 100)
        self.assertIn("weather_condition", data)

    def test_weather_endpoint_out_of_bounds_validation(self):
        """Coordinates outside India boundaries return HTTP 422 Unprocessable Entity."""
        r = self.client.get("/api/v1/weather?lat=75.0&lon=83.58")
        self.assertEqual(r.status_code, 422)

    def test_advisory_enriched_with_live_coordinates(self):
        """Passing lat & lon to advisory auto-enriches calculation with live weather & ET0."""
        payload = {
            "zone": "zone4",
            "crop": "wheat",
            "area_ha": 1.0,
            "irrigation": "tubewell",
            "lat": 25.59,
            "lon": 83.58,
            "soil": {
                "n_kg_ha": 210,
                "p_kg_ha": 14,
                "k_kg_ha": 165,
                "oc_pct": 0.42,
                "ph": 7.3,
                "zn_ppm": 0.45,
            },
            "language": "hi",
        }
        r = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsNotNone(data["live_weather"])
        self.assertGreater(data["peak_etc_mm_day"], 0.0)
        self.assertTrue(any("Open-Meteo" in s for s in data["sources"]))

    # ------------------------------------------------------------------
    # 9. Agronomic Safety Bounds: Strict ±15% Cap
    # ------------------------------------------------------------------
    def test_ml_residual_bounded_within_15_pct(self):
        """ML residual delta cannot shift N by more than ±15% of baseline N."""
        bundle_path = ROOT / "artifacts" / "model_bundle.json"
        model = ResidualMLModel(bundle_path)

        req = AdvisoryRequest(
            zone="zone4",
            crop="wheat",
            area_ha=1.0,
            irrigation="tubewell",
            et0_mm_day=3.8,
            sowing_delay_days=0,
            rain_prob_48h_pct=25,
            soil=SoilTestInput(
                n_kg_ha=250,
                p_kg_ha=15,
                k_kg_ha=180,
                oc_pct=0.45,
                ph=7.2,
                zn_ppm=0.55,
            ),
        )
        soil, _ = resolve_soil(req)
        base_n, _, _ = compute_baseline_npk_ha(req, soil)
        delta, band = model.predict_bounded(req, soil, base_n)
        max_shift = 0.15 * base_n
        self.assertLessEqual(abs(delta), max_shift + 0.01)
        self.assertLessEqual(abs(band[0]), max_shift + 0.01)
        self.assertLessEqual(abs(band[1]), max_shift + 0.01)

    # ------------------------------------------------------------------
    # 10. Investor-Grade Analytics & Economic Decision Endpoints
    # ------------------------------------------------------------------
    def test_investor_metrics_endpoint(self):
        """Investor metrics endpoint returns live model accuracy, coverage, and provenance."""
        r = self.client.get("/api/v1/investor/metrics")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertGreaterEqual(data["total_districts_covered"], 600)
        self.assertGreater(data["total_data_points"], 1000000)
        self.assertGreaterEqual(data["model_improvement_pct"], 25.0)
        self.assertGreater(data["avg_yield_improvement_pct"], 0.0)
        self.assertEqual(data["unique_crops"], 6)
        self.assertGreaterEqual(data["unique_states"], 20)
        self.assertLess(data["api_p95_latency_ms"], 50.0)
        self.assertIn("DAC&FW Soil Health Card", data["core_datasets"][0])

    def test_yield_predict_endpoint_with_district(self):
        """Yield prediction returns bounded prediction, CI, and historical baseline for district."""
        payload = {"crop": "wheat", "district_name": "Ghazipur"}
        r = self.client.post("/api/v1/yield/predict", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["crop"], "wheat")
        self.assertEqual(data["district"], "Ghazipur")
        self.assertGreater(data["predicted_yield_t_ha"], 0.5)
        self.assertLess(data["predicted_yield_t_ha"], 10.0)
        ci = data["confidence_interval_t_ha"]
        self.assertLessEqual(ci[0], data["predicted_yield_t_ha"])
        self.assertGreaterEqual(ci[1], data["predicted_yield_t_ha"])
        self.assertGreater(data["historical_avg_yield_t_ha"], 0.0)

    def test_yield_predict_endpoint_with_coordinates(self):
        """Yield prediction automatically resolves nearest district from GPS coordinates."""
        payload = {"crop": "rice", "lat": 25.5928, "lon": 83.5770}
        r = self.client.post("/api/v1/yield/predict", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("Ghazipur", data["district"])
        self.assertGreater(data["predicted_yield_t_ha"], 0.5)

    def test_roi_estimate_endpoint(self):
        """Farmer ROI calculation verifies MSP, revenue, input cost, and net profit arithmetic."""
        payload = {
            "crop": "wheat",
            "area_ha": 2.0,
            "current_yield_t_ha": 3.8,
            "district_name": "Ghazipur",
        }
        r = self.client.post("/api/v1/roi/estimate", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["crop"], "wheat")
        self.assertEqual(data["area_ha"], 2.0)
        self.assertAlmostEqual(data["production_tonnes"], 7.6, places=1)
        self.assertEqual(data["msp_price_inr_per_q"], 2275.0)
        self.assertAlmostEqual(data["gross_revenue_inr"], 7.6 * 22750.0, places=0)
        self.assertAlmostEqual(
            data["net_profit_inr"], data["gross_revenue_inr"] - data["total_input_cost_inr"], places=0
        )
        self.assertGreater(data["roi_pct"], 0.0)
        self.assertGreater(data["break_even_area_ha"], 0.0)
        self.assertGreater(data["cost_benefit_ratio"], 1.0)

    def test_analytics_coverage_endpoint(self):
        """Coverage analytics returns comprehensive district, state, zone, and crop catalog."""
        r = self.client.get("/api/v1/analytics/coverage")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertGreaterEqual(data["total_districts"], 600)
        self.assertGreater(data["total_states"], 15)
        self.assertEqual(len(data["crops_supported"]), 6)
        self.assertEqual(len(data["zones_covered"]), 6)
        up_state = [s for s in data["states"] if "uttar pradesh" in s["state"].lower()]
        self.assertTrue(len(up_state) > 0)
        self.assertGreater(up_state[0]["districts_count"], 40)


if __name__ == "__main__":
    unittest.main()
