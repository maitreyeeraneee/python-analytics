import os
from typing import Any, Dict, Optional

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

# Expected model input order (must match training)
FEATURES = [
    "arr_flights",
    "carrier_ct",
    "weather_ct",
    "nas_ct",
    "security_ct",
    "late_aircraft_ct",
]


def _default_model_path() -> str:
    # CWD-independent path resolution
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "models", "delay_prediction_model.pkl")


MODEL_PATH = _default_model_path()


@st.cache_resource(show_spinner=False)
def load_model(path: str = MODEL_PATH) -> Any:
    """Load the trained ML model.

    Raises:
        FileNotFoundError: if the model artifact does not exist
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found at: {path}. "
            "Ensure 'models/delay_prediction_model.pkl' exists."
        )

    model = joblib.load(path)

    # Basic interface validation
    if not hasattr(model, "predict"):
        raise TypeError("Loaded model does not expose a 'predict' method.")

    return model


def _coerce_inputs(user_inputs: Dict[str, Any]) -> list[list[float]]:
    row = []
    for f in FEATURES:
        v = user_inputs.get(f, 0)
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = 0.0
        row.append(v)

    return [row]


def predict_delay(model: Any, user_inputs: dict) -> float:
    """Predict arrival delay (minutes) using the trained model."""

    if model is None or not hasattr(model, "predict"):
        raise ValueError("Model is not loaded or invalid.")

    x = _coerce_inputs(user_inputs)
    pred = model.predict(x)

    # Model may return ndarray; normalize to float
    try:
        return float(pred[0])
    except Exception as e:
        raise RuntimeError(f"Unexpected prediction output format: {type(pred)}") from e


def feature_importance_plot(model: Any) -> Optional[Any]:
    """Return a Plotly figure for feature importances (if supported by model)."""

    if not hasattr(model, "feature_importances_"):
        return None

    importance = getattr(model, "feature_importances_", None)
    if importance is None:
        return None

    fi = pd.DataFrame({"Feature": FEATURES, "Importance": importance}).sort_values(
        "Importance", ascending=False
    )

    fig = px.bar(
        fi,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Model Feature Importance",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


