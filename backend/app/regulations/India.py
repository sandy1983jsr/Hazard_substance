import requests
from bs4 import BeautifulSoup
from app.crud import get_all_substances, update_substance_regulation

CDSCO_URL = "https://cdsco.gov.in/opencms/opencms/en/Chemical-List/"

def scrape_cdsco_cas_numbers():
    resp = requests.get(CDSCO_URL, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")
    cas_numbers = set()
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 1:
            cas_cell = cells[1].get_text(strip=True)
            if cas_cell and any(c.isdigit() for c in cas_cell):
                cas_numbers.add(cas_cell)
    return cas_numbers

def update_india(db):
    try:
        cas_numbers = scrape_cdsco_cas_numbers()
    except Exception:
        cas_numbers = set()
    for sub in get_all_substances(db):
        if sub.cas_number in cas_numbers:
            update_substance_regulation(db, sub.id, "CDSCO_INDIA", {"status": "Listed"})
        else:
            update_substance_regulation(db, sub.id, "CDSCO_INDIA", {"status": "Not Listed"})
