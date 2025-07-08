import requests
import pandas as pd
from io import BytesIO
from app.crud import get_all_substances, update_substance_regulation

PROP65_URL = "https://oehha.ca.gov/media/downloads/proposition-65/p65list112223.xlsx"
TSCA_API_URL = "https://comptox.epa.gov/dashboard/api/chemical_lists/TSCA_ACTIVE"

def update_prop65(db):
    resp = requests.get(PROP65_URL, timeout=30)
    xls = pd.read_excel(BytesIO(resp.content), engine='openpyxl')
    cas_list = set(xls['CAS No.'].dropna().astype(str).str.strip())
    for sub in get_all_substances(db):
        if sub.cas_number in cas_list:
            update_substance_regulation(db, sub.id, "Prop65", {"status": "Listed"})
        else:
            update_substance_regulation(db, sub.id, "Prop65", {"status": "Not Listed"})

def update_tsca(db):
    resp = requests.get(TSCA_API_URL, timeout=30)
    data = resp.json()
    cas_list = {item['casrn'] for item in data['results']} if 'results' in data else set()
    for sub in get_all_substances(db):
        if sub.cas_number in cas_list:
            update_substance_regulation(db, sub.id, "TSCA", {"status": "Active"})
        else:
            update_substance_regulation(db, sub.id, "TSCA", {"status": "Not Active"})
