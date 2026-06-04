import streamlit as st
import plotly.express as px
from streamlit_folium import st_folium

from src.data import load_data, apply_filters
from src.analytics import (
    kpi_cards,
    airline_leaderboards,
    airport_leaderboards,
    yearly_delay_trend,
    cancellation_analysis,
    weather_delay_analysis,
    delay_heatmaps,
)
from src.charts import (
    make_airport_map,
    plot_airline_market_share,
    plot_cancellation_by_airline,
    plot_cancellation_heatmap,
    plot_correlation_heatmap,
    plot_delay_heatmap,
    plot_top_busiest_airports,
    plot_top_delayed_airports,
    plot_yearly_delay_trend,
)
from src.prediction import load_model, predict_delay, feature_importance_plot

st.set_page_config(
    page_title="Aviation Intelligence Dashboard",
    page_icon="✈️",
    layout="wide",
)

DARK_CSS = """
<style>
/*************** Streamlit dark professional theme ***************/
html, body, [class*="css"] { background-color: #0b1220; color: #e8eefc; }
.stApp { background: radial-gradient(900px circle at 10% 10%, rgba(86, 96, 255, 0.18), transparent 50%),
                   radial-gradient(900px circle at 90% 20%, rgba(0, 210, 255, 0.10), transparent 50%), #0b1220; }
.block-container { padding-top: 1.5rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(21, 33, 61, 0.9), rgba(11, 18, 32, 0.9));
  border-right: 1px solid rgba(255,255,255,0.06);
}

/* Metrics cards */
div[data-testid="stMetricWidget"] {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 14px;
}

/* Buttons */
button[kind="primary"] { background-color: #4f6bff !important; }

/* Charts background */
.js-plotly-plot .plotly { background: rgba(0,0,0,0) !important; }
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

st.title("✈️ Aviation Intelligence Dashboard")
st.caption("Production-style aviation analytics + ML delay prediction")

# Load data once (with UX feedback)
with st.spinner("Loading aviation dataset..."):
    raw_df = load_data()

# Validate required columns early to avoid downstream crashes
required_cols = {"year", "month", "carrier_name", "airport_name", "arr_flights", "arr_delay", "arr_cancelled"}
missing = required_cols.difference(set(raw_df.columns))
if missing:
    st.error(f"Dataset is missing required columns: {sorted(missing)}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

min_year = int(raw_df["year"].min())
max_year = int(raw_df["year"].max())
year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

airline_options = sorted(raw_df["carrier_name"].dropna().unique().tolist())
airlines = st.sidebar.multiselect(
    "Airlines",
    options=airline_options,
    default=airline_options,
)

airport_options = sorted(raw_df["airport_name"].dropna().unique().tolist())
airports = st.sidebar.multiselect(
    "Airports",
    options=airport_options,
    default=[],
    help="Leave empty to use all airports",
)

months = st.sidebar.multiselect(
    "Months",
    options=sorted(raw_df["month"].dropna().unique().tolist()),
    default=[],
)

# Apply month filter: if none selected -> keep all
# (dashboard uses a single-month filter; if multiple months selected -> keep all)
month_value = months[0] if len(months) == 1 else None

df = apply_filters(
    raw_df,
    year_range=year_range,
    airlines=airlines,
    airports=airports,
    month=month_value,
)


# KPI cards
kpis = kpi_cards(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Flights", f"{kpis['total_flights']:,.0f}")
c2.metric("Total Delays", f"{kpis['total_delay']:,.0f}")
c3.metric("Cancelled Flights", f"{kpis['total_cancelled']:,.0f}")
c4.metric("Cancellation Rate", f"{kpis['cancellation_rate']*100:.2f}%")

# Market share pie
leaderboards = airline_leaderboards(df, top_n=10)
fig_market = plot_airline_market_share(leaderboards["market"])
st.plotly_chart(fig_market, use_container_width=True)

# -----------------------------
# Main analytics sections
# -----------------------------

st.subheader("Airline Analytics")

colA, colB = st.columns(2)

with colA:
    fig_delays = px.bar(
        leaderboards["delays"].head(10),
        x="arr_delay",
        y="carrier_name",
        orientation="h",
        title="Top Airlines by Total Delays",
    )
    fig_delays.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_delays, use_container_width=True)

with colB:
    fig_cxl = px.bar(
        leaderboards["cancellations"].head(10),
        x="arr_cancelled",
        y="carrier_name",
        orientation="h",
        title="Top Airlines by Total Cancellations",
    )
    fig_cxl.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_cxl, use_container_width=True)

st.subheader("Airport Analytics")

airport_l = airport_leaderboards(df, top_n=10)

colC, colD = st.columns([1.2, 1.0])
with colC:
    fig_busiest = plot_top_busiest_airports(airport_l["busiest"])
    st.plotly_chart(fig_busiest, use_container_width=True)

with colD:
    fig_delayed_airports = plot_top_delayed_airports(airport_l["most_delayed"])
    st.plotly_chart(fig_delayed_airports, use_container_width=True)

# Folium map
st.markdown("### Airport Location Map")
# Folium map (dataset-driven)
# Build a minimal dataframe with airport_name + lat/lon columns if present.
airport_map_df = df.groupby("airport_name").agg(
    lat=("lat", "mean") if "lat" in df.columns else ("airport_name", "first"),
    lon=("lon", "mean") if "lon" in df.columns else ("lng", "mean") if "lng" in df.columns else ("airport_name", "first"),
).reset_index()

airport_map = make_airport_map(airport_map_df)
st_folium(airport_map, width=1000, height=520)



# -----------------------------
# Trends & heatmaps
# -----------------------------

st.subheader("Delay Trends & Heatmaps")

t1, t2 = st.columns(2)

with t1:
    agg = st.selectbox("Yearly trend aggregation", options=["sum", "avg"], index=0, key="agg_year")
    yearly = yearly_delay_trend(df, agg=agg)
    fig_trend = plot_yearly_delay_trend(yearly, agg_label=agg)
    st.plotly_chart(fig_trend, use_container_width=True)

with t2:
    heat = delay_heatmaps(df)["monthly_year"]
    fig_h = plot_delay_heatmap(heat, title="Monthly Delay Heatmap (Month x Year)")
    st.plotly_chart(fig_h, use_container_width=True)

# Cancellation analysis
st.subheader("Cancellation Analysis")

ca, cb = st.columns(2)

with ca:
    cxl = cancellation_analysis(df)["by_airline"]
    st.plotly_chart(plot_cancellation_by_airline(cxl), use_container_width=True)

with cb:
    by_time = cancellation_analysis(df)["by_time"]
    st.plotly_chart(plot_cancellation_heatmap(by_time), use_container_width=True)

# Weather delay analysis
st.subheader("Weather Delay Analysis")

wa, wb = st.columns(2)

with wa:
    w = weather_delay_analysis(df)["by_year"]
    fig_w = px.line(w, x="year", y="weather_delay", markers=True, title="Weather Delays Over Years")
    fig_w.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_w, use_container_width=True)

with wb:
    corr = weather_delay_analysis(df)["corr"]
    # keep only columns related to delays if present
    st.plotly_chart(plot_correlation_heatmap(corr), use_container_width=True)

# -----------------------------
# AI PREDICTION SYSTEM
# -----------------------------

st.subheader("AI Flight Delay Prediction System")

try:
    model = load_model()

    arr_flights = st.number_input(
        "Number of Flights",
        value=1000.0,
        min_value=0.0,
    )

    carrier_ct = st.number_input(
        "Carrier Delay Count",
        value=50.0,
        min_value=0.0,
    )

    weather_ct = st.number_input(
        "Weather Delay Count",
        value=20.0,
        min_value=0.0,
    )

    nas_ct = st.number_input(
        "NAS Delay Count",
        value=30.0,
        min_value=0.0,
    )

    security_ct = st.number_input(
        "Security Delay Count",
        value=5.0,
        min_value=0.0,
    )

    late_aircraft_ct = st.number_input(
        "Late Aircraft Count",
        value=40.0,
        min_value=0.0,
    )

    if st.button("Predict Delay"):
        user_inputs = {
            "arr_flights": arr_flights,
            "carrier_ct": carrier_ct,
            "weather_ct": weather_ct,
            "nas_ct": nas_ct,
            "security_ct": security_ct,
            "late_aircraft_ct": late_aircraft_ct,
        }
        prediction = predict_delay(model, user_inputs)
        st.success(f"Predicted Flight Delay: {prediction:.2f} minutes")

    # Optional: show feature importance if model exposes it
    fi_fig = feature_importance_plot(model)
    if fi_fig is not None:
        with st.expander("Model Feature Importance"):
            st.plotly_chart(fi_fig, use_container_width=True)

except Exception as e:
    st.error(f"Prediction System Error: {e}")
    