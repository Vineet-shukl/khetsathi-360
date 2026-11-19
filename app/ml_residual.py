import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

from app.contracts import AdvisoryRequest
from app.baseline_engine import CROPS, ZONES

ZONE_KEYS = list(ZONES.keys())
CROP_KEYS = list(CROPS.keys())
IRR_KEYS = ["tubewell", "canal", "rainfed"]


def extract_features(req: AdvisoryRequest, soil: Dict[str, float]) -> np.ndarray:
    """Shared train/serve feature transform to guarantee zero train-serve skew."""
    feats: List[float] = [
        soil["n"] / 500.0,
        soil["p"] / 50.0,
        soil["k"] / 400.0,
        soil["oc"],
        (soil["ph"] - 7.0) / 2.0,
        req.sowing_delay_days / 30.0,
        req.et0_mm_day / 10.0,
        req.rain_prob_48h_pct / 100.0,
    ]
    for z in ZONE_KEYS:
        feats.append(1.0 if req.zone == z else 0.0)
    for c in CROP_KEYS:
        feats.append(1.0 if req.crop == c else 0.0)
    for irr in IRR_KEYS:
        feats.append(1.0 if req.irrigation == irr else 0.0)
    return np.array(feats, dtype=np.float64)


class ResidualMLModel:
    """Loads versioned Ridge + bootstrap uncertainty bundle and enforces ±15% safety bounds."""

    def __init__(self, bundle_path: Path):
        data = json.loads(bundle_path.read_text(encoding="utf-8"))
        self.version: str = data["model_version"]
        self.mean = np.array(data["feature_mean"], dtype=np.float64)
        self.std = np.array(data["feature_std"], dtype=np.float64)
        self.weights = np.array(data["weights"], dtype=np.float64)
        self.bias: float = float(data["bias"])
        self.boot_weights = np.array(data["boot_weights"], dtype=np.float64)
        self.boot_biases = np.array(data["boot_biases"], dtype=np.float64)

    def predict_bounded(
        self, req: AdvisoryRequest, soil: Dict[str, float], baseline_n_ha: float
    ) -> Tuple[float, List[float]]:
        x = extract_features(req, soil)
        x_norm = (x - self.mean) / np.where(self.std < 1e-8, 1.0, self.std)

        raw_delta = float(np.dot(x_norm, self.weights) + self.bias)
        boot_preds = self.boot_weights @ x_norm + self.boot_biases
        low_q = float(np.percentile(boot_preds, 10))
        high_q = float(np.percentile(boot_preds, 90))

        # Hard agronomic safety guardrail: ML residual cannot shift N more than ±15% of baseline
        max_shift = 0.15 * baseline_n_ha
        bounded_delta = float(np.clip(raw_delta, -max_shift, max_shift))
        bounded_low = float(np.clip(low_q, -max_shift, max_shift))
        bounded_high = float(np.clip(high_q, -max_shift, max_shift))
        return round(bounded_delta, 2), [round(bounded_low, 2), round(bounded_high, 2)]
