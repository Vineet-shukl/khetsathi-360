import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np

STATE_TO_ZONE: Dict[str, str] = {
    "uttar pradesh": "zone4", "bihar": "zone4", "jharkhand": "zone4", "west bengal": "zone4", "odisha": "zone4",
    "punjab": "zone6", "haryana": "zone6", "delhi": "zone6", "uttarakhand": "zone6", "himachal pradesh": "zone6", "jammu and kashmir": "zone6",
    "madhya pradesh": "zone8", "chhattisgarh": "zone8", "rajasthan": "zone8",
    "maharashtra": "zone9", "goa": "zone9",
    "karnataka": "zone10", "andhra pradesh": "zone10", "telangana": "zone10",
    "tamil nadu": "zone10", "kerala": "zone10", "puducherry": "zone10",
    "gujarat": "zone13",
}


def haversine_km(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = np.radians(lat2)
    dp = np.radians(lat2 - lat1)
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2.0) ** 2 + math.cos(p1) * np.cos(p2) * np.sin(dl / 2.0) ** 2
    return 2.0 * r * np.arcsin(np.minimum(1.0, np.sqrt(a)))


class DistrictSoilModel:
    """Real-data spatial IDW estimator + exact lookup across 695 Indian districts (soilhealth.dac.gov.in)."""

    def __init__(self, bundle_path: Path):
        data = json.loads(bundle_path.read_text(encoding="utf-8"))
        self.version: str = data["model_version"]
        self.k_neighbors: int = int(data["k_neighbors"])
        self.power: float = float(data["idw_power"])
        self.records: List[Dict] = data["records"]
        self.lats = np.array([r["lat"] for r in self.records], dtype=np.float64)
        self.lons = np.array([r["lon"] for r in self.records], dtype=np.float64)
        self.targets = np.array(
            [[r["n_low"], r["n_med"], r["n_high"], r["p_low"], r["p_med"], r["p_high"], r["k_low"], r["k_med"], r["k_high"], r["ph_acid"], r["ph_neut"], r["ph_alk"]] for r in self.records],
            dtype=np.float64,
        )

    def lookup_by_name(self, query: str) -> Optional[Dict]:
        q = query.strip().lower()
        for r in self.records:
            if q in r["address"].lower():
                zone = STATE_TO_ZONE.get(r.get("region", "").strip().lower(), "zone4")
                return dict(r, zone=zone)
        return None

    def predict_by_coords(self, lat: float, lon: float) -> Dict:
        dists = haversine_km(lat, lon, self.lats, self.lons)
        idx = np.argsort(dists)[: self.k_neighbors]
        d_k = np.maximum(dists[idx], 1.0)
        w = 1.0 / (d_k ** self.power)
        w = w / np.sum(w)
        pred = w @ self.targets[idx]
        nearest = self.records[int(idx[0])]
        zone = STATE_TO_ZONE.get(nearest.get("region", "").strip().lower(), "zone4")
        return {
            "source_mode": "spatial_idw_k" + str(self.k_neighbors),
            "nearest_district": nearest["address"],
            "distance_km": round(float(dists[idx[0]]), 1),
            "region": nearest["region"],
            "zone": zone,
            "crops": nearest["crops"],
            "n_low": round(float(pred[0]), 2),
            "n_med": round(float(pred[1]), 2),
            "n_high": round(float(pred[2]), 2),
            "p_low": round(float(pred[3]), 2),
            "p_med": round(float(pred[4]), 2),
            "p_high": round(float(pred[5]), 2),
            "k_low": round(float(pred[6]), 2),
            "k_med": round(float(pred[7]), 2),
            "k_high": round(float(pred[8]), 2),
            "ph_acid": round(float(pred[9]), 2),
            "ph_neut": round(float(pred[10]), 2),
            "ph_alk": round(float(pred[11]), 2),
        }

    @staticmethod
    def dist_to_expected_soil(dist_probs: Dict) -> Dict[str, float]:
        """Convert SHC Low/Med/High % distribution into expected kg/ha & pH for baseline engine."""
        exp_n = (dist_probs["n_low"] * 190.0 + dist_probs["n_med"] * 420.0 + dist_probs["n_high"] * 600.0) / 100.0
        exp_p = (dist_probs["p_low"] * 7.0 + dist_probs["p_med"] * 17.5 + dist_probs["p_high"] * 32.0) / 100.0
        exp_k = (dist_probs["k_low"] * 85.0 + dist_probs["k_med"] * 200.0 + dist_probs["k_high"] * 340.0) / 100.0
        exp_ph = (dist_probs["ph_acid"] * 5.6 + dist_probs["ph_neut"] * 6.9 + dist_probs["ph_alk"] * 8.2) / 100.0
        return {
            "n": round(exp_n, 1),
            "p": round(exp_p, 1),
            "k": round(exp_k, 1),
            "oc": 0.45,
            "ph": round(exp_ph, 2),
            "zn": 0.50,
        }
