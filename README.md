# 🌿 KrishiNetra: AI-Powered Precision Agriculture

**KrishiNetra** is an end-to-end MVP designed to empower farmers and agricultural stakeholders with data-driven insights. Built for the **Maharashtra Agrihackathon 2026**, it combines satellite imagery analysis with Generative AI to bridge the gap between complex data and actionable farming decisions.

## 🚀 Key Features
- **🛰️ Satellite NDVI Analysis:** Visualizes vegetation health using pre-computed NDVI overlays to identify high-stress zones.
- **📄 AI Document Extraction:** Uses Google Gemini to automatically parse and verify complex PDF land records (7/12 extracts).
- **🌾 Crop Prediction:** Context-aware crop identification based on geographic coordinates and local lookup data.
- **📍 Interactive Mapping:** Built with Streamlit and Folium for a seamless, location-based user experience.
- **🛡️ Stress Detection:** Automated calculation of "at-risk" farm areas to prioritize irrigation and intervention.

## 🛠️ Quick Start

```powershell
# Navigate to the MVP directory
cd krishinetra_mvp

# Activate venv (from repo root)
..\krishinetra_venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 📂 Project Structure

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

## 🤖 Gemini API (Optional)

For document AI, add your key to `.env`:
```
GEMINI_API_KEY=your_key_here
```
Without it, the app uses fallback demo data.

---

## 📸 Demo Scenarios

Select a demo scenario from the sidebar:
- **A: Cotton Farm Stress - Vidarbha** — NDVI stress analysis
- **B: Onion Fields - Nashik** — Mixed vegetation health
- **C: Land Document Verification - Pune** — AI document extraction
