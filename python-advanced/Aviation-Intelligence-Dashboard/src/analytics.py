import pandas as pd


def kpi_cards(df: pd.DataFrame) -> dict:
    total_flights = df["arr_flights"].sum() if "arr_flights" in df.columns else 0
    total_delay = df["arr_delay"].sum() if "arr_delay" in df.columns else 0
    total_cancelled = df["arr_cancelled"].sum() if "arr_cancelled" in df.columns else 0

    cancellation_rate = (total_cancelled / total_flights) if total_flights else 0

    # Weather delay share among delay components (if available)
    component_cols = ["weather_ct", "nas_ct", "security_ct", "late_aircraft_ct", "carrier_ct"]
    available = [c for c in component_cols if c in df.columns]
    weather_share = 0
    if "weather_ct" in df.columns and available:
        denom = df[available].sum().sum()
        weather_share = (df["weather_ct"].sum() / denom) if denom else 0

    return {
        "total_flights": total_flights,
        "total_delay": total_delay,
        "total_cancelled": total_cancelled,
        "cancellation_rate": cancellation_rate,
        "weather_share": weather_share,
    }


def airline_leaderboards(df: pd.DataFrame, top_n: int = 10) -> dict:
    # Delays by airline
    delays = (
        df.groupby("carrier_name")["arr_delay"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    # Cancellations by airline
    cancellations = (
        df.groupby("carrier_name")["arr_cancelled"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    # Market share by flights
    market = (
        df.groupby("carrier_name")["arr_flights"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    market["market_share"] = market["arr_flights"] / (market["arr_flights"].sum() or 1)

    return {"delays": delays, "cancellations": cancellations, "market": market}


def airport_leaderboards(df: pd.DataFrame, top_n: int = 10) -> dict:
    busiest = (
        df.groupby("airport_name")["arr_flights"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    most_delayed = (
        df.groupby("airport_name")["arr_delay"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return {"busiest": busiest, "most_delayed": most_delayed}


def yearly_delay_trend(df: pd.DataFrame, agg: str = "sum") -> pd.DataFrame:
    if agg == "avg":
        s = df.groupby("year")["arr_delay"].mean()
    else:
        s = df.groupby("year")["arr_delay"].sum()
    return s.reset_index(name="arr_delay")


def cancellation_analysis(df: pd.DataFrame) -> dict:
    by_airline = (
        df.groupby("carrier_name")["arr_cancelled"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    by_time = (
        df.groupby(["year", "month"])["arr_cancelled"].sum().reset_index()
    )
    return {"by_airline": by_airline, "by_time": by_time}


def weather_delay_analysis(df: pd.DataFrame) -> dict:
    # Weather delay over years (sum)
    if "weather_delay" in df.columns:
        by_year = df.groupby("year")["weather_delay"].sum().reset_index(name="weather_delay")
    elif "weather_ct" in df.columns:
        by_year = df.groupby("year")["weather_ct"].sum().reset_index(name="weather_delay")
    else:
        by_year = pd.DataFrame({"year": [], "weather_delay": []})

    # Correlation among available numeric cols
    numeric = df.select_dtypes(include=["number"])
    corr = numeric.corr(numeric_only=True)

    return {"by_year": by_year, "corr": corr}


def delay_heatmaps(df: pd.DataFrame) -> dict:
    """Return delay heatmap pivot (month x year).

    This function is defensive: if required columns are missing or the pivot is empty,
    it returns an empty DataFrame pivot.
    """

    if df is None or df.empty:
        return {"monthly_year": pd.DataFrame()}

    required = {"month", "year", "arr_delay"}
    if not required.issubset(set(df.columns)):
        return {"monthly_year": pd.DataFrame()}

    # Monthly x Year heatmap for delay
    month_order = sorted(df["month"].dropna().unique().tolist())
    pivot = df.pivot_table(values="arr_delay", index="month", columns="year", aggfunc="sum")

    if pivot is None:
        return {"monthly_year": pd.DataFrame()}

    if month_order:
        pivot = pivot.reindex(month_order)

    return {"monthly_year": pivot}


