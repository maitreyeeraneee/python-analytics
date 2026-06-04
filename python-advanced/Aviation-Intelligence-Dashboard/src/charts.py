import plotly.express as px
import folium
import pandas as pd


def plot_airline_market_share(market_df):
    # If too many airlines, keep top 10
    df = market_df.copy()
    if "market_share" in df.columns and len(df) > 10:
        df = df.sort_values("arr_flights", ascending=False).head(10)

    fig = px.pie(df, values="arr_flights", names="carrier_name", title="Airline Market Share")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_top_delayed_airports(df_airports):
    fig = px.bar(
        df_airports,
        x="arr_delay",
        y="airport_name",
        orientation="h",
        title="Top Delayed Airports",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_top_busiest_airports(df_airports):
    fig = px.bar(
        df_airports,
        x="arr_flights",
        y="airport_name",
        orientation="h",
        title="Top Busiest Airports",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_yearly_delay_trend(trend_df, agg_label: str):
    fig = px.line(trend_df, x="year", y="arr_delay", markers=True, title=f"Yearly Delay Trend ({agg_label})")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_cancellation_by_airline(df_airline):
    fig = px.bar(
        df_airline.head(15),
        x="arr_cancelled",
        y="carrier_name",
        orientation="h",
        title="Cancellations by Airline",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_cancellation_heatmap(df_by_time):
    # Convert to month name labels if desired; keep numeric for simplicity
    pivot = df_by_time.pivot_table(values="arr_cancelled", index="month", columns="year", aggfunc="sum")
    fig = px.imshow(pivot, title="Cancellation Heatmap (Month x Year)", aspect="auto", color_continuous_scale="Viridis")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def plot_delay_heatmap(pivot, title: str):
    """Plot month x year heatmap.

    If pivot is empty, return a simple placeholder figure.
    """

    if pivot is None or getattr(pivot, "empty", True):
        fig = px.imshow(
            [[0]],
            title=title,
            aspect="auto",
            color_continuous_scale="Blues",
        )
        fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
        return fig

    fig = px.imshow(
        pivot,
        title=title,
        aspect="auto",
        color_continuous_scale="Blues",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig



def plot_correlation_heatmap(corr_df, title: str = "Correlation Heatmap"):
    fig = px.imshow(corr_df, title=title, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig


def make_airport_map(airport_df):
    """Create an airport map.

    Dataset-driven only: if lat/lon are missing or empty, no markers are rendered.
    """

    if airport_df is None or airport_df.empty:
        return folium.Map(location=[39.5, -98.35], zoom_start=4)

    # Try common lat/lon column names.
    lat_col = None
    lon_col = None
    for c in airport_df.columns:
        cl = c.lower()
        if cl in {"lat", "latitude"}:
            lat_col = c
        if cl in {"lon", "lng", "longitude"}:
            lon_col = c

    m = folium.Map(location=[39.5, -98.35], zoom_start=4)

    if not (lat_col and lon_col):
        return m

    label_col = "airport_name" if "airport_name" in airport_df.columns else None

    for _, row in airport_df.iterrows():
        if pd.isna(row.get(lat_col)) or pd.isna(row.get(lon_col)):
            continue

        lat = float(row[lat_col])
        lon = float(row[lon_col])

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            popup=str(row[label_col]) if label_col else "",
            color="blue",
            fill=True,
        ).add_to(m)

    return m


