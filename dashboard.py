"""
BBIM713 Capstone: Interactive Beverage Analytics Web Dashboard
Run using: py -3.11 -m streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Beverage Intelligence Dashboard",
    page_icon="🍾",
    layout="wide"
)

# Custom Header Styling
st.markdown("""
    <style>
    .main-title {font-size:30px; font-weight:700; color:#1E3A8A; margin-bottom:0px;}
    .sub-title {font-size:14px; color:#4B5563; margin-bottom:15px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🍾 AI-Driven Alcoholic Beverage Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title"><b>BBIM713 Capstone Project (DA)</b> | <i>Gurpreet Singh, Harsimran, Sukhbir</i></p>', unsafe_allow_html=True)

csv_path = "data/processed/master_beverage_catalog.csv"
metrics_path = "data/processed/pipeline_metrics.json"

if not os.path.exists(csv_path) or not os.path.exists(metrics_path):
    st.error("⚠️ Generated data files not found. Please run `py -3.11 main.py` in your terminal first!")
    st.stop()

# -------------------------------------------------------------
# 1. LOAD PROCESSED DATA
# -------------------------------------------------------------
df = pd.read_csv(csv_path)
with open(metrics_path, "r", encoding="utf-8") as f:
    pipeline_metrics = json.load(f)

# -------------------------------------------------------------
# 2. EXECUTIVE KPI CARDS
# -------------------------------------------------------------
mode = pipeline_metrics.get("extractor_mode", "unknown")
if mode != "real_llm_key":
    st.warning("Extractor mode: FALLBACK PARSER. The 'LLM' scores below come from the backup parser, not a real model.")
if pipeline_metrics.get("run_mode") == "snapshot_replay":
    st.info("Data source: replay of saved retailer pages (repeatable benchmark snapshot), not a live crawl.")

f1_llm = pipeline_metrics["metrics_llm"]["macro_overall"]["f1_score"]
f1_rule = pipeline_metrics["metrics_rule"]["macro_overall"]["f1_score"]
f1_gap = (f1_llm - f1_rule) * 100  # percentage points

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Canonical Products", len(df), f"{df['merchant_name'].nunique()} retailers")
col2.metric("Excluded Items", pipeline_metrics.get("total_excluded", 0), "Accessories dropped")
col3.metric("Average Price", f"${df['price'].mean():.2f} NZD", f"Range: \\${df['price'].min():.2f} - \\${df['price'].max():.2f}")
col4.metric("Average Strength", f"{df['abv'].mean():.1f}% ABV", f"Min {df['abv'].min():.1f}% - Max {df['abv'].max():.1f}%")
col5.metric("Extractor Macro F1", f"{f1_llm:.4f}", f"{f1_gap:+.1f} pts vs rule baseline")

st.divider()

# -------------------------------------------------------------
# 3. INTERACTIVE SEARCH & FILTERS
# -------------------------------------------------------------
st.subheader("🔍 Product Catalog Explorer")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    cat_list = ["All"] + sorted(df["category"].dropna().unique().tolist())
    sel_cat = st.selectbox("Filter by Category:", cat_list)

with f_col2:
    country_list = ["All"] + sorted(df["country_of_origin"].dropna().unique().tolist())
    sel_country = st.selectbox("Filter by Country:", country_list)

with f_col3:
    priced = df["price"].dropna()
    price_min, price_max = float(priced.min()), float(priced.max())
    sel_price = st.slider("Filter by Price Range ($ NZD):", price_min, price_max, (price_min, price_max))

filtered_df = df.copy()
if sel_cat != "All":
    filtered_df = filtered_df[filtered_df["category"] == sel_cat]
if sel_country != "All":
    filtered_df = filtered_df[filtered_df["country_of_origin"] == sel_country]
filtered_df = filtered_df[(filtered_df["price"].isna()) | ((filtered_df["price"] >= sel_price[0]) & (filtered_df["price"] <= sel_price[1]))]

st.dataframe(filtered_df, use_container_width=True)

st.divider()

# -------------------------------------------------------------
# 4. VISUAL ANALYTICS SECTION (CHARTS & DISTRIBUTIONS)
# -------------------------------------------------------------
st.subheader("📊 Visual Analytics & Market Breakdown")

v_col3, v_col4 = st.columns(2)

with v_col3:
    st.markdown("#### Alcohol Strength (ABV %) vs. Retail Price ($ NZD)")
    st.scatter_chart(data=df, x="abv", y="price", color="category")

with v_col4:
    st.markdown("#### Average Retailer Price Comparison ($ NZD)")
    merchant_avg_price = df.groupby("merchant_name")["price"].mean().sort_values(ascending=False)
    st.bar_chart(merchant_avg_price)

st.divider()

# -------------------------------------------------------------
# 6. EMPIRICAL BENCHMARK EVALUATION (VISUAL 6 - RQ2)
# -------------------------------------------------------------
st.subheader("🧪 Model Performance Benchmark (RQ2 Comparison)")
st.caption("Empirical Precision, Recall, and Macro F1 comparison on ground truth.")

m_llm = pipeline_metrics["metrics_llm"]
m_rule = pipeline_metrics["metrics_rule"]

bench_df = pd.DataFrame({
    "Metric": ["Overall Precision", "Overall Recall", "Macro F1-Score"],
    "Rule-Based Baseline": [
        m_rule["macro_overall"]["precision"],
        m_rule["macro_overall"]["recall"],
        m_rule["macro_overall"]["f1_score"]
    ],
    "Proposed LLM Extractor": [
        m_llm["macro_overall"]["precision"],
        m_llm["macro_overall"]["recall"],
        m_llm["macro_overall"]["f1_score"]
    ]
}).set_index("Metric")

st.dataframe(bench_df.style.format("{:.4f}"), use_container_width=True)
# Side-by-side bars, one group per metric, with a fixed 0 to 1 axis so no bar is clipped.
import altair as alt
chart_df = bench_df.reset_index().melt(id_vars="Metric", var_name="Method", value_name="Score")
bench_chart = (
    alt.Chart(chart_df)
    .mark_bar()
    .encode(
        x=alt.X("Method:N", axis=None),
        y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 1]), title="Score (0 to 1)"),
        color=alt.Color("Method:N", title=None),
        column=alt.Column("Metric:N", title=None),
        tooltip=["Metric", "Method", alt.Tooltip("Score:Q", format=".4f")],
    )
    .properties(width=180, height=280)
)
st.altair_chart(bench_chart, use_container_width=False)