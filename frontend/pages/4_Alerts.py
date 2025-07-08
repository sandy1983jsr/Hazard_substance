import streamlit as st
import pandas as pd
import random

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
