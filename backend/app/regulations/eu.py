import requests
from app.crud import get_all_substances, update_substance_regulation

REACH_CANDIDATE_LIST_URL = "https://echa.europa.eu/documents/10162/2743446/candidate_list_en.json"

def update_reach(db):
    resp = requests.get(REACH_CANDIDATE_LIST_URL, timeout=30)
    data = resp.json()
    candidate_cas = {item['cas_number'] for item in data['data'] if item.get('cas_number')}
    for sub in get_all_substances(db):
        if sub.cas_number in candidate_cas:
            update_substance_regulation(db, sub.id, "REACH", {"status": "Candidate"})
        else:
            update_substance_regulation(db, sub.id, "REACH", {"status": "Not Listed"})
