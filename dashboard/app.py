
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
HIST_PATH = BASE_DIR / "data" / "raw" / "ethiopia.csv"
FCST_PATH = BASE_DIR / "data" / "processed" / "forecast_results.csv"


st.set_page_config(layout="wide")
st.title("Financial Inclusion Dashboard")

@st.cache_data
def load_data():
    hist = pd.read_csv(HIST_PATH)
    fcst = pd.read_csv(FCST_PATH)
    return hist, fcst

hist, fcst = load_data()


st.subheader("Historical Trends")

indicator = st.selectbox("Select Indicator", hist.indicator_code.unique())
hist_df = hist[hist.indicator_code == indicator]

if not hist_df.empty:
    fig = px.line(hist_df, x="observation_date", y="value_numeric", title=f"{indicator} Over Time")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No historical data for {indicator}")

st.subheader("Forecast Projections")

indicator_fcst = st.selectbox("Select Forecast Indicator", fcst.indicator.unique())
scenario = st.selectbox("Scenario", ["base_with_events", "optimistic", "pessimistic"])
fcst_df = fcst[fcst.indicator == indicator_fcst]

if not fcst_df.empty:
    fig2 = px.line(fcst_df, x="year", y=scenario, title=f"{indicator_fcst} Forecast ({scenario})")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning(f"No forecast data for {indicator_fcst}")


st.download_button("Download Historical Data", hist.to_csv(index=False), "historical.csv")
st.download_button("Download Forecasts", fcst.to_csv(index=False), "forecasts.csv")