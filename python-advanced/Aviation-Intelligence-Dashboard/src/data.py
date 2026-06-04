import os

import pandas as pd
import streamlit as st

def _default_data_path() -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "dataset", "flights.csv")


DATA_PATH = _default_data_path()


@st.cache_data(show_spinner=False)
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load and lightly normalize the flights dataset."""

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset file not found at: {path}. Ensure dataset/flights.csv exists."
        )

    df = pd.read_csv(path)

    # Basic cleanup / type coercion safety
    # (Keep it lightweight; assume dataset already mostly clean.)
    for col in [
        "year",
        "month",
        "arr_flights",
        "arr_delay",
        "arr_cancelled",
        "carrier_ct",
        "weather_ct",
        "nas_ct",
        "security_ct",
        "late_aircraft_ct",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep rows with delay target present for modeling/analytics
    if "arr_delay" in df.columns:
        df = df.dropna(subset=["arr_delay"])
    return df


def apply_filters(
    df: pd.DataFrame,
    year_range,
    airlines,
    airports,
    month,
) -> pd.DataFrame:
    out = df.copy()

    if year_range is not None and len(year_range) == 2:
        out = out[(out["year"] >= year_range[0]) & (out["year"] <= year_range[1])]

    if airlines is not None and len(airlines) > 0:
        out = out[out["carrier_name"].isin(airlines)]

    if airports is not None and len(airports) > 0:
        out = out[out["airport_name"].isin(airports)]

    if month is not None:
        out = out[out["month"] == month]

    return out

