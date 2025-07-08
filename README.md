# Hazardous Substance Compliance Tool

## Features

- Central registry of hazardous substances and SDS
- Regulatory compliance tracking (EU REACH, US Prop65/TSCA, India CDSCO)
- Alerts for at-risk substances and SDS expiry
- Streamlit dashboard (ready for [Streamlit Community Cloud](https://streamlit.io/cloud))
- Modular, easily extended for more jurisdictions

## Usage

1. **Run with Docker Compose** (recommended for local/dev):

    ```
    docker-compose up --build
    ```

2. **Or run each part manually:**

    - Start PostgreSQL
    - Start FastAPI backend: `uvicorn app.main:app --reload`
    - Start Streamlit frontend: `streamlit run Home.py`

3. **Deploy on Streamlit Community Cloud:**

    - Push only the `frontend/` folder to a new public GitHub repo
    - Set up the backend API (hosted or via cloud VM)
    - Set your backend API URL in the Streamlit Python files (currently `"http://localhost:8000"`)
    - [See Streamlit docs](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app) for full deployment steps

## Extending

- Add new region modules under `backend/app/regulations/`
- Add extra dashboard pages to `frontend/pages/`

## License

MIT
