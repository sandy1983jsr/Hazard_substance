# Hazardous Substance Compliance Tool – Frontend

This React dashboard displays regulatory compliance for substances across multiple regions (EU, US, India, and more).

## Features

- Substance table with per-region regulatory status columns (REACH, Prop 65, TSCA, CDSCO India, etc.)
- Compliance overview dashboard by region
- Alerts for regulatory risks and SDS expiry
- SDS uploading interface

## Extending

- Add more regions: add their code to the `REGIONS` array in `SubstanceList.js` and `REGION_LABELS` in `Dashboard.js`.
- Backend must supply `regulatory_tags` field for each substance in the API.

## Usage

```
npm install
npm start
```

Backend (FastAPI) should be running at the same host/port or proxied.
