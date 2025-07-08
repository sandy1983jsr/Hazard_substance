import streamlit as st
import requests
import pandas as pd

st.header("Alerts & Regulatory Risks")
alerts = requests.get("http://localhost:8000/dashboard/alerts").json()
if alerts:
    df = pd.DataFrame(alerts)
    st.dataframe(df)
else:
    st.success("No current alerts.")
