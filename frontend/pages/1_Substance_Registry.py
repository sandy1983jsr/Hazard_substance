import streamlit as st
import requests
import pandas as pd

st.header("Substance Registry")
resp = requests.get("http://localhost:8000/substances/")
subs = resp.json()
st.dataframe(pd.DataFrame(subs))
