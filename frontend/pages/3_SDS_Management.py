import streamlit as st
import requests

st.header("SDS Management")

substance_id = st.number_input("Substance ID", min_value=1, step=1)
uploaded_file = st.file_uploader("Upload SDS for Substance", type=["pdf", "docx"])

if st.button("Upload SDS") and uploaded_file and substance_id:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    resp = requests.post(
        f"http://localhost:8000/sds/upload/{int(substance_id)}",
        files=files
    )
    if resp.status_code == 200:
        st.success("SDS uploaded successfully")
    else:
        st.error("Upload failed")
