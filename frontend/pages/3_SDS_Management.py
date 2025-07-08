import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

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
