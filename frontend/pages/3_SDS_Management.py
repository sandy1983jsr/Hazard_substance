import streamlit as st
import pandas as pd
import requests
import random
from datetime import date, timedelta

BACKEND_URL = st.secrets.get("BACKEND_URL", None)

def is_backend_available():
    if not BACKEND_URL:
        return False
    try:
        r = requests.get(f"{BACKEND_URL}/substances/", timeout=3)
        return r.ok
    except Exception:
        return False

st.header("SDS Management")

tab1, tab2 = st.tabs(["Upload CSV", "Use Sample Data"])

with tab1:
    st.subheader("Upload SDS Registry CSV")
    st.write("CSV columns: substance_id, substance_name, sds_path, sds_expiry")
    csv_file = st.file_uploader("Choose a CSV file", type="csv", key="sds_csv")
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)

with tab2:
    st.subheader("Generate & View Sample SDS Data")
    N = st.number_input("Number of SDS records", 1, 20, 4, key="sds_n")
    if st.button("Generate Sample SDS Data"):
        sample_names = ["Acetone", "Benzene", "Toluene", "Phenol"]
        sample_data = []
        for i in range(int(N)):
            substance_id = i + 1
            name = random.choice(sample_names)
            sds_path = f"sds/{name.lower()}_{substance_id}.pdf"
            expiry = date.today() + timedelta(days=random.randint(10, 365))
            sample_data.append({
                "substance_id": substance_id,
                "substance_name": name,
                "sds_path": sds_path,
                "sds_expiry": expiry
            })
        df_sample = pd.DataFrame(sample_data)
        st.dataframe(df_sample)

st.subheader("Registered SDS Information")
if is_backend_available():
    try:
        resp = requests.get(f"{BACKEND_URL}/substances/")
        if resp.ok:
            df = pd.DataFrame(resp.json())
            if not df.empty and 'sds_path' in df.columns:
                df_sds = df[['id', 'name', 'sds_path', 'sds_expiry']].rename(
                    columns={'id': 'substance_id', 'name': 'substance_name'}
                )
                st.dataframe(df_sds)
            else:
                st.info("No SDS records available.")
        else:
            st.error(f"Backend error: {resp.status_code}")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
else:
    st.info("Backend not available — only sample data above.")
