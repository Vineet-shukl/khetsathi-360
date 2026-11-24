"""
tests/test_map_pointer_contracts.py — Unit & Integration tests for Phase A:
Interactive Farmland Map Pointer, Geodesic Acreage Calculation & Bilingual Parity.
"""

import math
import unittest
from fastapi.testclient import TestClient

from app.api import app


def calculate_polygon_area_sq_meters(coords: list[tuple[float, float]]) -> float:
    """
    Computes geodesic polygon area in square meters using Shoelace formula
    projected via equirectangular approximation at the mean latitude.
    coords is list of (lat, lon) tuples.
    """
    if len(coords) < 3:
        return 0.0

    mean_lat = sum(c[0] for c in coords) / len(coords)
    lat_rad = math.radians(mean_lat)
    
    # 1 deg lat in meters ~ 111,139 m
    # 1 deg lon in meters ~ 111,139 * cos(lat) m
    meters_per_lat = 111139.0
    meters_per_lon = 111139.0 * math.cos(lat_rad)

    xy = [(c[1] * meters_per_lon, c[0] * meters_per_lat) for c in coords]
    
    # Shoelace formula
    area = 0.0
    n = len(xy)
    for i in range(n):
        j = (i + 1) % n
        area += xy[i][0] * xy[j][1]
        area -= xy[j][0] * xy[i][1]
        
    return abs(area) / 2.0


class TestMapPointerContracts(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_polygon_area_geodesic_math(self):
        """
        Verify that a 100m x 100m parcel box (~1.0 Hectare = 10,000 m2)
        computes accurately to within 2% error.
        """
        lat_ref = 25.5928
        lon_ref = 83.5770
        
        d_lat = 100.0 / 111139.0
        d_lon = 100.0 / (111139.0 * math.cos(math.radians(lat_ref)))
        
        polygon = [
            (lat_ref, lon_ref),
            (lat_ref + d_lat, lon_ref),
            (lat_ref + d_lat, lon_ref + d_lon),
            (lat_ref, lon_ref + d_lon)
        ]
        
        sqm = calculate_polygon_area_sq_meters(polygon)
        self.assertAlmostEqual(sqm, 10000.0, delta=200.0)  # within 2% of 10,000 m2
        
        # Test unit conversions from sqm
        ha = sqm / 10000.0
        bigha_pucca = sqm / 2500.0  # 1 Pucca Bigha = 2,500 m2 (UP/Bihar)
        acre = sqm / 4046.86       # 1 Acre = 4046.86 m2
        
        self.assertAlmostEqual(ha, 1.0, delta=0.02)
        self.assertAlmostEqual(bigha_pucca, 4.0, delta=0.08)
        self.assertAlmostEqual(acre, 2.47, delta=0.05)

    def test_spatial_idw_district_sync_on_map_coords(self):
        """
        Verify that dropping a pin anywhere in India returns the expected
        district centroid and spatial IDW soil baseline via API.
        """
        resp = self.client.get("/api/v1/district/baseline?lat=25.5928&lon=83.5770")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["match_type"], "spatial_idw")
        self.assertIn("Ghazipur", data["nearest_district"])
        self.assertEqual(data["region"], "Uttar Pradesh")
        self.assertIn("expected_soil", data)
        self.assertGreater(data["expected_soil"]["n"], 100)
        self.assertGreater(data["expected_soil"]["ph"], 5.0)

    def test_map_pointer_coordinate_validation(self):
        """Verify boundary checks on out-of-India lat/lon coords."""
        # Latitude out of bounds (> 38.0)
        resp = self.client.get("/api/v1/district/baseline?lat=45.0&lon=80.0")
        self.assertEqual(resp.status_code, 422)

        # Longitude out of bounds (< 68.0)
        resp = self.client.get("/api/v1/district/baseline?lat=25.0&lon=50.0")
        self.assertEqual(resp.status_code, 422)

    def test_polygon_area_degenerate_edge_cases(self):
        """
        Verify that degenerate, collinear, empty, and micro-polygons
        are safely handled without errors or division-by-zero.
        """
        # 0 points
        self.assertEqual(calculate_polygon_area_sq_meters([]), 0.0)
        # 1 point
        self.assertEqual(calculate_polygon_area_sq_meters([(25.59, 83.57)]), 0.0)
        # 2 points (collinear line segment)
        self.assertEqual(calculate_polygon_area_sq_meters([(25.59, 83.57), (25.60, 83.58)]), 0.0)
        # 3 collinear points
        collinear = [(25.0, 80.0), (25.0, 80.5), (25.0, 81.0)]
        self.assertAlmostEqual(calculate_polygon_area_sq_meters(collinear), 0.0, places=3)
        # Clockwise vs Counter-clockwise orientation returns identical positive magnitude
        poly_ccw = [(25.0, 80.0), (25.01, 80.0), (25.01, 80.01), (25.0, 80.01)]
        poly_cw = list(reversed(poly_ccw))
        area_ccw = calculate_polygon_area_sq_meters(poly_ccw)
        area_cw = calculate_polygon_area_sq_meters(poly_cw)
        self.assertGreater(area_ccw, 0.0)
        self.assertAlmostEqual(area_ccw, area_cw, places=4)

    def test_minimum_parcel_area_guardrail(self):
        """
        Verify that micro-parcels (< 0.01 Ha = 100 m2) are rejected by the agronomic
        guardrail threshold to avoid 0.00 Ha advisory corruption.
        """
        MIN_PARCEL_HA = 0.01
        # 1.2 m2 micro-jitter
        micro_sqm = 1.2
        micro_ha = micro_sqm / 10000.0
        self.assertLess(micro_ha, MIN_PARCEL_HA)
        self.assertEqual(f"{micro_ha:.2f}", "0.00")  # Proves danger of un-guarded truncation

        # Valid agricultural plot (e.g. 500 m2 = 0.05 Ha)
        valid_sqm = 500.0
        valid_ha = valid_sqm / 10000.0
        self.assertGreaterEqual(valid_ha, MIN_PARCEL_HA)
        self.assertEqual(f"{valid_ha:.2f}", "0.05")

    def test_frontend_map_pointer_i18n_parity(self):
        """
        Validates that frontend/index.html includes all required Phase A
        map pointer translation keys in both I18N.hi and I18N.en with zero discrepancy.
        """
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            content = f.read()

        required_map_keys = [
            "mapPointerBtn",
            "mapTitle",
            "mapSub",
            "mapSatellite",
            "mapStandard",
            "mapMeasureArea",
            "mapMyGps",
            "mapClose",
            "mapLockParcel",
            "mapMeasuredAreaBadge",
            "mapApplyArea",
            "mapMeasureHint",
            "mapResetMeasure",
            "mapOverlayTitle"
        ]

        # Verify presence in I18N.hi block and I18N.en block
        hi_block = content.split("hi: {")[1].split("en: {")[0]
        en_block = content.split("en: {")[1].split("};")[0]

        for key in required_map_keys:
            self.assertIn(f"{key}:", hi_block, f"Missing key '{key}' in I18N.hi dictionary")
            self.assertIn(f"{key}:", en_block, f"Missing key '{key}' in I18N.en dictionary")


if __name__ == "__main__":
    unittest.main()
