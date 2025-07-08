import streamlit as st
import requests
import pandas as pd

st.header("Compliance Dashboard")
summary = requests.get("http://localhost:8000/dashboard/compliance").json()
df = pd.DataFrame([
    {"Regulation": k, "Total": v["count"], "At Risk": v["at_risk"]}
    for k, v in summary.items()
])
st.dataframe(df)
