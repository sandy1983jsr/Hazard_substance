import streamlit as st
import pandas as pd
import requests
import random

BACKEND_URL = st.secrets.get("BACKEND_URL", None)

def is_backend_available():
    if not BACKEND_URL:
        return False
    try:
        r = requests.get(f"{BACKEND_URL}/dashboard/alerts", timeout=3)
        return r.ok
    except Exception:
        return False

st.header("Alerts & Regulatory Risks")

tab1, tab2 = st.tabs(["Upload CSV", "Use Sample Data"])

with tab1:
    st.subheader("Upload Alerts CSV")
    st.write("CSV columns: substance, cas, alert")
    csv_file = st.file_uploader("Choose a CSV file", type="csv", key="alerts_csv")
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)

with tab2:
    st.subheader("Generate & View Sample Alerts")
    N = st.number_input("Number of alerts", 1, 20, 4, key="alerts_n")
    if st.button("Generate Sample Alerts"):
        sample_names = ["Acetone", "Benzene", "Toluene", "Phenol"]
        sample_alerts = [
            "Regulatory risk (Prop65)", "SDS expires soon", "Listed on REACH", "Carcinogen - Handle with care"
        ]
        sample_data = []
        for i in range(int(N)):
            name = random.choice(sample_names)
            cas = f"{random.randint(10,999)}-{random.randint(10,99)}-{random.randint(1,9)}"
            alert = random.choice(sample_alerts)
            sample_data.append({
                "substance": name,
                "cas": cas,
                "alert": alert
            })
        df_sample = pd.DataFrame(sample_data)
        st.dataframe(df_sample)

st.subheader("Current Alerts")
if is_backend_available():
    try:
        alerts = requests.get(f"{BACKEND_URL}/dashboard/alerts").json()
        if alerts:
            df = pd.DataFrame(alerts)
            st.dataframe(df)
        else:
            st.success("No current alerts.")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
else:
    st.info("Backend not available — only sample data above.")
