import os

from dashboard.alert import get_alert, extract_transactions
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from rag.investigator import generate_report
import warnings
warnings.filterwarnings("ignore")

if "supabase_url" in st.secrets:

    SUPABASE_URL = st.secrets["supabase_url"]

    SUPABASE_KEY = st.secrets["supabase_key"]

else:

    from dotenv import load_dotenv

    load_dotenv()

    SUPABASE_URL = os.getenv("supabase_url")

    SUPABASE_KEY = os.getenv("supabase_key")
# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
page_title="Fraud Detection Dashboard",
page_icon="🚨",
layout="wide"
)

# -------------------------------------------------------
# CUSTOM STYLING
# -------------------------------------------------------

st.markdown("""

<style>

.stApp {
    background-color: #0F172A;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

h1 {
    color: white !important;
    text-align: center;
    font-size: 3rem !important;
}

h2, h3 {
    color: white !important;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>

""", unsafe_allow_html=True)

# -------------------------------------------------------
# KPI CARD FUNCTION
# -------------------------------------------------------

def kpi_card(title, value, color):
    card_html = f"""
    <div style="
        background:{color};
        border-radius:15px;
        padding:20px;
        text-align:center;
        height:120px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.3);
    ">
        <div style="
            color:white;
            font-size:20px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            {title}
        </div>
        <div style="
            color:white;
            font-size:42px;
            font-weight:800;
        ">
            {value}
        </div>
    </div>
    """
    components.html(card_html, height=130)

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------

st.title("🚨 Fraud Detection Dashboard")
st.caption("Real-Time Fraud Monitoring")

# -------------------------------------------------------
# DATA
# -------------------------------------------------------

alerts = get_alert()
transactions = extract_transactions()

# -------------------------------------------------------
# FILTERS
# -------------------------------------------------------

left,right = st.columns([3,1])

with left:
    threshold = st.slider(
    "Risk Score Threshold",
    0,
    150,
    50
    )

with right:
    if st.button("🔄 Refresh Alerts"):
        alerts = get_alert()

# -------------------------------------------------------

# ALERT SECTION

# -------------------------------------------------------

if isinstance(alerts, list) and len(alerts) > 0:


    alert_df = pd.DataFrame(alerts)

    alert_df = alert_df[alert_df["score"] >= threshold]

    total_alerts = len(alert_df)

    avg_score = (round(alert_df["score"].mean(),2) if len(alert_df) else 0)

    max_score = (alert_df["score"].max() if len(alert_df) else 0)

    fraud_count = len(alert_df[alert_df["score"] >= 50])

# ---------------------------------------------------
# KPI ROW
# ---------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    kpi_card( "🚨 Alerts",total_alerts,  "#DC2626")

with c2:
    kpi_card( "📈 Avg Risk",avg_score, "#2563EB")
       

with c3:
    kpi_card("🔥 Max Risk", max_score, "#7C3AED")


with c4:
    kpi_card("⚠️ Fraud Alerts",fraud_count, "#EA580C")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# ALERT TABLE + COUNTRY CHART
# ---------------------------------------------------

left,right = st.columns([2,1])

with left:

    st.subheader("Current Alerts")

    display_df = alert_df.copy()

    if "id" in display_df.columns:
        display_df = display_df.drop(columns=["id"])
    

    st.dataframe( display_df,height=250,width=800)

with right:

    st.subheader("Alerts By Country")

    country_counts = (alert_df["country"].value_counts())

    st.bar_chart(country_counts,height=300,width = 'stretch')

# ---------------------------------------------------
# INVESTIGATION SECTION
# ---------------------------------------------------

st.subheader("🔍 Alert Investigation")

selected_row = st.selectbox("Select Alert",alert_df.index)

selected_alert = alert_df.loc[selected_row]

c1,c2,c3 = st.columns(3)

with c1:
    kpi_card("Risk Score",selected_alert["score"],"#DC2626")

with c2:
    kpi_card("Country",selected_alert["country"],"#2563EB")

with c3:
    kpi_card("Amount",f"${selected_alert['amount']}", "#16A34A")

st.markdown(
    f"""
    <div style="
    background:#1E293B;
    padding:15px;
    border-radius:12px;
    color:white;
    margin-top:10px;
    ">
    <h4>Explanation</h4>
    {selected_alert['reasons']}
    </div>
    """,
    unsafe_allow_html=True
)

if isinstance(transactions, list) and len(transactions) > 0:

    tx_df = pd.DataFrame(transactions)

    # ── clean up mixed-vintage data ──────────────────────────
    tx_df["ml_probability"] = pd.to_numeric(tx_df["ml_probability"], errors="coerce")
    tx_df["final_score"]    = pd.to_numeric(tx_df["final_score"],    errors="coerce")
    tx_df["fraud_detected"] = tx_df["fraud_detected"].fillna(False).astype(bool)

    st.markdown("---")
    st.header("📊 Transaction Analytics")

    valid_ml    = tx_df[tx_df["ml_probability"].notna()]
    valid_score = tx_df[tx_df["final_score"].notna()]
    ml_records  = len(valid_ml)

    kpi_card("ML Scored", ml_records, "#0891B2")

    avg_ml       = round(valid_ml["ml_probability"].mean(), 2) if ml_records > 0 else 0
    avg_final    = round(valid_score["final_score"].mean(),  2) if len(valid_score) > 0 else 0
    fraud_count_tx = int(tx_df["fraud_detected"].sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Transactions", len(tx_df),       "#2563EB")
    with c2: kpi_card("Avg ML",       avg_ml,           "#7C3AED")
    with c3: kpi_card("Avg Score",    avg_final,        "#16A34A")
    with c4: kpi_card("Frauds",       fraud_count_tx,   "#DC2626")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    # ── Top Risk Table ────────────────────────────────────────
    with left:
        st.subheader("Top Risk Transactions")

        top_risk = tx_df.sort_values(
            "final_score", ascending=False, na_position="last"
        ).head(10).copy()

        # human-readable columns
        top_risk["fraud_detected"] = top_risk["fraud_detected"].map(
            {True: "✅ Yes", False: "❌ No"}
        )
        top_risk["ml_probability"] = top_risk["ml_probability"].fillna("N/A")
        top_risk["final_score"]    = top_risk["final_score"].fillna("N/A")

        st.dataframe(
            top_risk[["user_id", "amount", "country", "risk_score",
                       "ml_probability", "final_score", "fraud_detected"]],
            height=250,
            use_container_width=True
        )

    # ── ML Distribution ───────────────────────────────────────
    with right:
        st.subheader("ML Distribution")

        if ml_records > 0:
            fig = px.histogram(valid_ml, x="ml_probability", nbins=20,
                               title=f"{ml_records} scored records")
            fig.update_layout(
                height=250,
                paper_bgcolor="#0F172A",
                plot_bgcolor="#0F172A",
                font_color="white",
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No ML-scored records yet.")

st.markdown("GenAI-Powered Investigation")
if st.button("Gen AI Report"):
    report = generate_report(selected_alert['reasons'])
    st.markdown(
        f"""
        <div style="
        background:#1E293B;
        padding:15px;
        border-radius:12px;
        color:white;
        margin-top:10px;
        ">
        <h4>GenAI Report</h4>
        {report}
        </div>
        """,
        unsafe_allow_html=True
    )


