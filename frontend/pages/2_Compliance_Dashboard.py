import streamlit as st
import pandas as pd
import requests
import random

BACKEND_URL = st.secrets.get("BACKEND_URL", None)

def is_backend_available():
    if not BACKEND_URL:
        return False
    try:
        r = requests.get(f"{BACKEND_URL}/dashboard/compliance", timeout=3)
        return r.ok
    except Exception:
        return False

st.header("Compliance Dashboard")

tab1, tab2 = st.tabs(["Upload CSV", "Use Sample Data"])

with tab1:
    st.subheader("Upload Compliance Summary CSV")
    st.write("CSV columns: Regulation, Total, At Risk")
    csv_file = st.file_uploader("Choose a CSV file", type="csv", key="compliance_csv")
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)

with tab2:
    st.subheader("Generate & View Sample Compliance Data")
    region_list = [
        "REACH", "Prop65", "TSCA", "CDSCO_INDIA"
    ]
    N = st.number_input("Number of regulations", 1, 10, 4, key="compliance_n")
    if st.button("Generate Sample Compliance Data"):
        sample_data = []
        for i in range(int(N)):
            region = region_list[i % len(region_list)]
            total = random.randint(1, 30)
            at_risk = random.randint(0, total)
            sample_data.append({"Regulation": region, "Total": total, "At Risk": at_risk})
        df_sample = pd.DataFrame(sample_data)
        st.dataframe(df_sample)

st.subheader("Current Compliance Summary")
if is_backend_available():
    try:
        summary = requests.get(f"{BACKEND_URL}/dashboard/compliance").json()
        df = pd.DataFrame([
            {"Regulation": k, "Total": v["count"], "At Risk": v["at_risk"]}
            for k, v in summary.items()
        ])
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No compliance data available.")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
else:
    st.info("Backend not available — only sample data above.")
