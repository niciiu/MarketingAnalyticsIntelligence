import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine
from pathlib import Path
from datetime import datetime
import numpy as np

#PAGE CONFIG
st.set_page_config(
    page_title="Marketing Campaign Intelligence",
    page_icon="📊",
    layout="wide"
)

css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

#DB CONNECTION 
engine = create_engine("sqlite:///data/ads_analytics.db", future=True)

@st.cache_data
def q(sql: str) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

@st.cache_data
def load_stability(path: str = "data/roi_stability_summary.csv") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    # month_id ke datetime untuk filter
    if "month_id" in df.columns:
        df["month_id"] = pd.to_datetime(df["month_id"])
    return df

#LOAD DATA
kpi_df     = q("SELECT * FROM vw_marketing_kpi ORDER BY dt;")
monthly_df = q("SELECT * FROM vw_campaign_monthly ORDER BY month_id, channel;")
roi_map    = q("SELECT * FROM vw_campaign_roi_map ORDER BY roi_avg DESC;")
stab_df    = load_stability()

#DATE FILTER 
if not kpi_df.empty:
    kpi_df["dt"] = pd.to_datetime(kpi_df["dt"])
    min_dt = kpi_df["dt"].min()
    max_dt = kpi_df["dt"].max()
else:
    min_dt = datetime(2021, 1, 1)
    max_dt = datetime(2021, 12, 31)

default_start = max_dt - pd.DateOffset(months=2)

# HERO + RANGE PICKER
with st.container():
    st.markdown('<div class="bi-hero">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            '<div class="bi-title">Marketing Campaign Intelligence Dashboard</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bi-sub">End-to-end marketing performance, ROI diagnostics, and channel efficiency insights.</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.write("")  # spacer
        date_range = st.date_input(
            "Date range",
            value=(default_start.date(), max_dt.date()),
            min_value=min_dt.date(),
            max_value=max_dt.date(),
            format="YYYY-MM-DD",
            label_visibility="collapsed"
        )
    st.markdown('</div>', unsafe_allow_html=True)

start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

# filter utama
kpi_f = kpi_df[(kpi_df["dt"] >= start_dt) & (kpi_df["dt"] <= end_dt)].copy()
monthly_df["month_id"] = pd.to_datetime(monthly_df["month_id"])
monthly_f = monthly_df[(monthly_df["month_id"] >= start_dt) & (monthly_df["month_id"] <= end_dt)].copy()

#KPI CARDS
def period_delta(series: pd.Series) -> float:
    if series.empty or len(series) < 2:
        return 0.0
    n = len(series)
    half = max(n // 2, 1)
    cur = series.iloc[-half:].mean()
    prev = series.iloc[:half].mean()
    if prev == 0:
        return 0.0
    return (cur - prev) / prev

col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

if not kpi_f.empty:
    ctr_delta  = period_delta(kpi_f["ctr"])
    cpc_delta  = period_delta(kpi_f["cpc_avg"])
    cpm_delta  = period_delta(kpi_f["cpm_avg"])
    roi_delta  = period_delta(kpi_f["roi_avg"])
    spend_mean = kpi_f["spend"].mean()

    def kpi_card(container, label, value_str, delta):
        sign = "up" if delta >= 0 else "down"
        arrow = "▲" if delta >= 0 else "▼"
        container.markdown(
            f"""
            <div class="kpi">
              <div class="label">{label}</div>
              <div class="value">{value_str}</div>
              <div class="delta {sign}">{arrow} {abs(delta):.1%}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    kpi_card(col_k1, "Avg ROI", f"{kpi_f['roi_avg'].mean():.2f}", roi_delta)
    kpi_card(col_k2, "CTR", f"{kpi_f['ctr'].mean():.2%}", ctr_delta)
    kpi_card(col_k3, "CPC (avg)", f"{kpi_f['cpc_avg'].mean():.2f}", cpc_delta)
    kpi_card(col_k4, "CPM (avg)", f"{kpi_f['cpm_avg'].mean():.2f}", cpm_delta)
    kpi_card(col_k5, "Avg Daily Spend", f"${spend_mean:,.0f}", 0.0)

#ROW 1: Spend trend, ROI trend, Donut share
left, mid, right = st.columns([2.2, 2, 1.6])

if not kpi_f.empty:
    spend_line = alt.Chart(kpi_f).mark_area(opacity=0.5).encode(
        x=alt.X("dt:T", title=None),
        y=alt.Y("spend:Q", title="Spend"),
        tooltip=["dt", "spend"]
    ).properties(height=220)

    roi_line = alt.Chart(kpi_f).mark_line(point=True).encode(
        x=alt.X("dt:T", title=None),
        y=alt.Y("roi_avg:Q", title="ROI"),
        tooltip=["dt", "roi_avg"]
    ).properties(height=220)

    left.markdown('<div class="card"><b>Spend Over Time</b>', unsafe_allow_html=True)
    left.altair_chart(spend_line, use_container_width=True)
    left.markdown('</div>', unsafe_allow_html=True)

    mid.markdown('<div class="card"><b>ROI Trend Over Time</b>', unsafe_allow_html=True)
    mid.altair_chart(roi_line, use_container_width=True)
    mid.markdown('</div>', unsafe_allow_html=True)

# donut share by channel (pakai spend monthly)
share = monthly_f.groupby("channel", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
if not share.empty:
    donut = alt.Chart(share).mark_arc(innerRadius=60).encode(
        theta="spend:Q",
        color=alt.Color("channel:N", legend=None),
        tooltip=["channel", "spend"]
    ).properties(height=220)
    right.markdown('<div class="card"><b>Spend Share by Channel</b>', unsafe_allow_html=True)
    right.altair_chart(donut, use_container_width=True)
    right.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2: Mini performance charts ----------
st.markdown("#### Performance Signals")
g1, g2, g3, g4 = st.columns(4)

if not kpi_f.empty:
    charts = [
        ("Impressions", "impressions"),
        ("Clicks", "clicks"),
        ("CTR", "ctr"),
        ("ROI", "roi_avg"),
    ]
    cols = [g1, g2, g3, g4]
    for (title, col_name), c in zip(charts, cols):
        c.markdown(f'<div class="card"><b>{title}</b>', unsafe_allow_html=True)
        ch = alt.Chart(kpi_f).mark_bar().encode(
            x=alt.X("dt:T", title=None),
            y=alt.Y(f"{col_name}:Q", title=None),
            tooltip=["dt", col_name]
        ).properties(height=180)
        c.altair_chart(ch, use_container_width=True)
        c.markdown('</div>', unsafe_allow_html=True)

#ROW 3: ROI vs Spend Quadrant + Stability Table
q_left, q_right = st.columns([1.6, 2])

# Quadrant ROI vs Spend ( roi_map)
if not roi_map.empty:
    df_q = roi_map.copy()
    med_spend = df_q["spend"].median()
    med_roi = df_q["roi_avg"].median()

    def quad(row):
        if row["spend"] >= med_spend and row["roi_avg"] >= med_roi:
            return "High Scale • High ROI"
        elif row["spend"] >= med_spend and row["roi_avg"] < med_roi:
            return "High Scale • Low ROI"
        elif row["spend"] < med_spend and row["roi_avg"] >= med_roi:
            return "Low Scale • High ROI"
        else:
            return "Low Scale • Low ROI"

    df_q["quadrant"] = df_q.apply(quad, axis=1)

    base = alt.Chart(df_q)

    points = base.mark_circle(size=140).encode(
        x=alt.X("spend:Q", title="Spend (total)"),
        y=alt.Y("roi_avg:Q", title="ROI (avg)"),
        color=alt.Color("quadrant:N", legend=alt.Legend(title="Quadrant")),
        tooltip=["channel", "spend", "roi_avg", "n_rows", "quadrant"]
    )

    vline = base.mark_rule(strokeDash=[4,4]).encode(
        x=alt.datum(med_spend)
    )
    hline = base.mark_rule(strokeDash=[4,4]).encode(
        y=alt.datum(med_roi)
    )

    quad_chart = (points + vline + hline).properties(
        height=280,
        title="ROI vs Spend Quadrant (Channel-Level)"
    )

    q_left.markdown('<div class="card"><b>ROI vs Spend Quadrant</b>', unsafe_allow_html=True)
    q_left.altair_chart(quad_chart, use_container_width=True)
    q_left.markdown('</div>', unsafe_allow_html=True)

# Stability table (roi_stability_summary.csv)
if not stab_df.empty:
    # filter by selected period
    stab_f = stab_df.copy()
    if "month_id" in stab_f.columns:
        stab_f = stab_f[(stab_f["month_id"] >= start_dt) & (stab_f["month_id"] <= end_dt)]

    stable_rank = (stab_f.groupby("channel", as_index=False)
                   .agg(
                       total_spend=("spend", "sum"),
                       roi_mean=("roi_mean", "mean"),
                       roi_cv=("roi_cv", "mean"),
                       months=("month_id", "nunique")
                   ))
    stable_rank = stable_rank.sort_values(["roi_cv", "roi_mean"], ascending=[True, False])

    q_right.markdown('<div class="card"><b>Channel Stability (ROI CV & Coverage)</b>', unsafe_allow_html=True)
    q_right.dataframe(
        stable_rank,
        use_container_width=True,
        hide_index=True
    )
    q_right.markdown('</div>', unsafe_allow_html=True)

#Monthly detail table
st.markdown("#### Monthly Performance (Detail)")
st.dataframe(
    monthly_f.sort_values(["month_id", "channel"]),
    use_container_width=True,
    hide_index=True
)
st.caption("Note: All KPIs are computed from the cleaned dataset via SQLite views and stability diagnostics.")
