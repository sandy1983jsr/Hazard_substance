import streamlit as st
import pandas as pd
import requests
import random

# Try to get backend URL from secrets, else set to None
BACKEND_URL = st.secrets.get("BACKEND_URL", None)

def is_backend_available():
    if not BACKEND_URL:
        return False
    try:
        r = requests.get(f"{BACKEND_URL}/substances/", timeout=3)
        return r.ok
    except Exception:
        return False

def post_substances(df):
    results = []
    if not is_backend_available():
        st.warning("Backend not available: data will only be shown locally.")
        return None
    for _, row in df.iterrows():
        d = row.to_dict()
        # Convert regulatory_tags from string to dict if needed
        if "regulatory_tags" in d and isinstance(d["regulatory_tags"], str):
            import ast
            try:
                d["regulatory_tags"] = ast.literal_eval(d["regulatory_tags"])
            except Exception:
                d["regulatory_tags"] = {}
        resp = requests.post(f"{BACKEND_URL}/substances/", json=d)
        results.append(resp.status_code)
    return results

st.header("Compliance Substance Registry")

tab1, tab2 = st.tabs(["Upload CSV", "Use Sample Data"])

with tab1:
    st.subheader("Upload Substances CSV")
    st.write("CSV columns: name, cas_number, supplier, hazard_class, regulatory_tags (as dict-string)")
    csv_file = st.file_uploader("Choose a CSV file", type="csv", key="registry_csv")
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)
        if is_backend_available() and st.button("Upload to Backend"):
            codes = post_substances(df)
            st.success(f"Uploaded {sum([c==200 or c==201 for c in codes])} substances.")
        elif not is_backend_available():
            st.info("Backend not available — data shown locally only.")

with tab2:
    st.subheader("Generate & Use Sample Data")
    N = st.number_input("Number of random substances", 1, 20, 5, key="registry_n")
    if st.button("Generate Sample Data"):
        sample_names = ["Acetone", "Benzene", "Toluene", "Methanol", "Phenol", "Hexane", "Xylene", "Chloroform", "Formaldehyde", "Aniline"]
        sample_suppliers = ["ChemCo", "IndusChem", "GlobalChem", "ChemEx"]
        sample_hazards = ["Flammable liquid", "Carcinogen", "Corrosive", "Toxic", "Irritant"]
        sample_data = []
        for i in range(N):
            name = random.choice(sample_names)
            cas_number = f"{random.randint(10,999)}-{random.randint(10,99)}-{random.randint(1,9)}"
            supplier = random.choice(sample_suppliers)
            hazard = random.choice(sample_hazards)
            regulatory_tags = {
                "REACH": {"status": random.choice(["Candidate", "Not Listed"])},
                "Prop65": {"status": random.choice(["Listed", "Not Listed"])},
                "TSCA": {"status": random.choice(["Active", "Not Active"])},
                "CDSCO_INDIA": {"status": random.choice(["Listed", "Not Listed"])}
            }
            sample_data.append({
                "name": name,
                "cas_number": cas_number,
                "supplier": supplier,
                "hazard_class": hazard,
                "regulatory_tags": regulatory_tags
            })
        df_sample = pd.DataFrame(sample_data)
        st.dataframe(df_sample)
        if is_backend_available():
            codes = post_substances(df_sample)
            st.success(f"Uploaded {sum([c==200 or c==201 for c in codes])} sample substances.")
        else:
            st.info("Sample data only (backend not connected).")

# --- Show all substances registered ---
st.subheader("Registered Substances")
if is_backend_available():
    try:
        resp = requests.get(f"{BACKEND_URL}/substances/")
        if resp.ok:
            df = pd.DataFrame(resp.json())
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("No substances registered yet.")
        else:
            st.error(f"Backend error: {resp.status_code}")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
else:
    st.info("Backend not available — only sample data shown above.")
