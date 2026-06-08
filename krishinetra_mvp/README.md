# KrishiNetra - AI-Powered Precision Agriculture

Built for Maharashtra Agrihackathon 2026 (May 17)

## Quick Start

```powershell
# Activate venv (from repo root)
..\krishinetra_venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## Demo

Select a demo scenario from the sidebar:
- **A: Cotton Farm Stress - Vidarbha** — NDVI stress analysis
- **B: Onion Fields - Nashik** — Mixed vegetation health
- **C: Land Document Verification - Pune** — AI document extraction

## Structure

```
krishinetra_mvp/
├── app.py                 # Main app
├── modules/               # Python modules
│   ├── map_viz.py         # Folium map
│   ├── ndvi_loader.py     # NDVI PNG loader
│   ├── crop_predictor.py  # Lookup crop classifier
│   ├── stress_detector.py # Threshold stress zones
│   ├── area_calculator.py # Shapely area math
│   └── doc_extractor.py   # Gemini PDF extractor
├── data/
│   ├── ndvi_overlays/     # Pre-computed NDVI PNGs
│   ├── sample_documents/  # Demo land record PDF
│   └── crop_lookup.json   # Coordinate→crop map
├── .env                   # Gemini API key (optional)
└── requirements.txt
```

## Gemini API (Optional)

For document AI, add your key to `.env`:
```
GEMINI_API_KEY=your_key_here
```
Without it, the app uses fallback demo data.
