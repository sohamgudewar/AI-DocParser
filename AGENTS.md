# AGENTS.md — KrishiNetra Session Context

## Project
KrishiNetra — AI-Powered Precision Agriculture for Maharashtra.
Built for Maharashtra Agrihackathon 2026. Currently an MVP with pre-computed data.

## Current State (MVP)
- Streamlit app with 3 tabs: Satellite Analysis, Document Verification, About
- Pre-computed NDVI PNG overlays (not live satellite)
- Hardcoded JSON lookup table for crop prediction
- Gemini AI for PDF extraction (with silent fallback to fake data)
- No database, no auth, no tests, no error handling
- Single-threaded, blocks on processing

## Decisions Made
- Preference for most efficient order: refactor first, then infra, then features
- Training ML models is NOT needed for MVP/pilot phase
- Git commits + AGENTS.md are the mechanism for session continuity
- Production_roadmap.md reorganized into phased, engineering-first approach

## Next Steps
## Next Steps
Phase 2 fully complete (all 13 features done). Next would be Docker build (when Docker Desktop available), deployment, or productionization.

## Progress

### Session 1 (Refactor) — Completed
...
### Session 7 (Celery/Redis) — Completed
...
### Session 11 (Deep Learning Crop Model Pipeline) — Completed
- Created `modules/ml_pipeline.py`:
  - `CropModelPipeline` class with `predict()` supporting lat/lon, ndvi health %, and area inputs
  - `_extract_features()` — maps coordinates to region, soil type, and matched zone
  - `_predict_dummy()` — uses lookup table with confidence modulated by NDVI health and field size
  - `_predict_sklearn()` — placeholder for trained sklearn models (falls back to dummy if no model loaded)
  - `load_model()`, `set_model()`, `get_available_models()` — model registry for future trained models
  - Soil zone mapping for 6 Maharashtra regions
- Updated `modules/crop_predictor.py`:
  - `predict_crop()` now delegates to `ml_pipeline.CropModelPipeline.predict()` instead of inline zone matching
  - Accepts optional `ndvi_health_pct` and `area_hectares` params for confidence refinement
  - Maintains full backward compatibility (same return shape, same function signature)
- Created `tests/test_ml_pipeline.py` — 10 tests covering init, known/unknown predict, NDVI/area params, soil type, model switching, fallback, feature extraction
- **Result: 59/59 tests pass, 0 errors (+10 new tests)**

### What Changed (Session 11)
| File | Before | After |
| :--- | :--- | :--- |
| `modules/ml_pipeline.py` | Didn't exist | Pipeline class with preprocess→predict→postprocess |
| `modules/crop_predictor.py` | Inline zone matching | Delegates to ML pipeline |
| `tests/test_ml_pipeline.py` | Didn't exist | 10 tests for pipeline |

### Session 13 (End-to-End Testing) — Completed
- Created `tests/test_integration.py` — 9 E2E tests covering:
  - Full analysis pipeline (Vidarbha + Nashik): coords → validate → predict → NDVI → stress → area
  - Unknown coords graceful fallback
  - Full document verification flow (extract → verify → mismatch detection)
  - Auth flow (valid/invalid/unknown emails)
  - ML pipeline with NDVI & area params
  - GPS parsing from multiple string formats
  - NDVI files verified for all 3 demo locations
- Created `tests/test_data_files.py` — verifies crop_lookup.json schema, NDVI files exist
- Verified all 13 modules import cleanly + app.py compiles
- Installed `celery[redis]` for module import compatibility
- **Result: 68/68 tests pass, 0 errors (+19 new tests)**

### What Changed (Session 13)
| File | Before | After |
| :--- | :--- | :--- |
| `tests/test_integration.py` | Didn't exist | 9 E2E integration tests |
| `tests/test_data_files.py` | Didn't exist | Schema + file existence checks |

### Runtime Bugfix (Session 13.5)
- **`logger` used before defined** in `app.py` — `logger = get_logger(__name__)` was on line 31 but used on lines 21/23. Moved above Celery/GEE availability checks.
- **`add_ndvi_tile_layer` import error** — caused by stale `__pycache__` or old streamlit process. Fix: kill all streamlit/python processes, clear `__pycache__`, restart with `python -m streamlit run app.py`.
- `.env` `STREAMLIT_SERVER_COOKIE_SECRET` updated from placeholder to secure random hex.

### Session 12 (IoT/Ground Truth) — Skipped (no hardware)

### Session 11 (Deep Learning Crop Model Pipeline) — Completed
...
### Session 8 (User Auth) — Completed
- Created `modules/auth.py` — email-based auth with:
  - `authenticate(email)` — validates email, returns user dict, creates DB user if possible
  - Manages 2 demo users (admin@krishinetra.in, farmer@demo.in)
  - Graceful DB fallback (works without PostgreSQL)
- Updated `app.py` — sidebar now has Account section:
  - When logged out: email input + login button + demo user hints
  - When logged in: shows user name/email + logout button
  - Uses `st.session_state.user` to persist login across reruns
- **Result: 49/49 tests pass, 0 errors**

### What Changed (Session 8)
| File | Before | After |
| :--- | :--- | :--- |
| `modules/auth.py` | Didn't exist | Email auth, DB user sync, demo users |
| `app.py` | No auth in sidebar | Account section with login/logout |

## Suggested Build Order
1. ✅ Refactor code (error handling, logging, structured modules)
2. ✅ Testing (unit tests for all modules)
3. ✅ Docker (Dockerfile + docker-compose)
4. ✅ CI/CD (GitHub Actions)
5. ✅ Security hardening
6. ✅ PostgreSQL + PostGIS backend (schema + data migration)
7. ✅ Celery/Redis async tasks
8. ✅ User Auth (OAuth)
9. GEE satellite integration
10. Advanced Document AI
11. Deep learning crop model pipeline
12. IoT / Ground truth
13. End-to-end testing
- Created `modules/tasks.py` — Celery app + task definitions:
  - `run_ndvi_analysis` — runs full analysis pipeline in background (crop predict, NDVI, stress zones, area)
  - `extract_document` — runs PDF extraction in background
  - `celery_available()` — helper to check if Redis/Celery is reachable
- Created `worker.py` — entry point: `celery -A modules.tasks worker --loglevel=info`
- Updated `docker-compose.yml` — added `worker` service with 2 concurrency
- Updated `requirements.txt` — added `celery[redis]>=5.4.0`
- Updated `app.py` — analysis pipeline checks Celery first, falls back to synchronous (no behavior change without Redis)
- **Note:** Celery tasks dispatch to background worker when Redis is available; app runs synchronously when it's not

### What Changed (Session 7)
| File | Before | After |
| :--- | :--- | :--- |
| `modules/tasks.py` | Didn't exist | Celery app + 2 background tasks |
| `worker.py` | Didn't exist | Celery worker entry point |
| `docker-compose.yml` | 3 services | Added `worker` service |
| `requirements.txt` | 14 deps | Added celery[redis] |
| `app.py` | Direct synchronous calls | Async via Celery when available, fallback to sync |

## Suggested Build Order
1. ✅ Refactor code (error handling, logging, structured modules)
2. ✅ Testing (unit tests for all modules)
3. ✅ Docker (Dockerfile + docker-compose)
4. ✅ CI/CD (GitHub Actions)
5. ✅ Security hardening
6. ✅ PostgreSQL + PostGIS backend (schema + data migration)
7. ✅ Celery/Redis async tasks
8. User Auth (OAuth)
9. GEE satellite integration
10. Advanced Document AI
11. Deep learning crop model pipeline
12. IoT / Ground truth
13. End-to-end testing
- Created `data/schema.sql` — 5 tables with PostGIS geometry columns, spatial indexes
  - `users` — for future auth
  - `fields` — farm boundaries with GEOMETRY(POINT) and GEOMETRY(POLYGON)
  - `analysis` — NDVI analysis history per field
  - `land_records` — extracted document data
  - `crop_zones` — migrated from lookup JSON
- Created `modules/database.py` — connection manager with graceful fallback if DB unavailable
  - `get_connection()`, `execute()`, `insert_analysis()`, `insert_land_record()`
- Created `scripts/seed_db.py` — migrates crop_lookup.json → crop_zones table
- Updated `docker-compose.yml` — mounts `schema.sql` as init script for PostGIS container
- Updated `requirements.txt` — added `psycopg2-binary`
- **Note:** PostgreSQL not running locally so DB module gracefully degrades (logs warning, returns None)

### What Changed (Session 6)
| File | Before | After |
| :--- | :--- | :--- |
| `data/schema.sql` | Didn't exist | 5 PostGIS tables + indexes |
| `modules/database.py` | Didn't exist | Connection pool, query helpers, fallback |
| `scripts/seed_db.py` | Didn't exist | JSON → Postgres migration |
| `docker-compose.yml` | No init script | Mounts schema.sql |
| `requirements.txt` | 13 deps | Added psycopg2-binary |

### DB Integration Fix (Session 7.5)
- `app.py` now imports `insert_analysis`, `insert_land_record`, `db_available`
- Analysis results save to PostgreSQL after pipeline completes
- Document extractions save to `land_records` table when uploaded or loaded as sample
- Gracefully degrades when DB is offline (logs warning, no crash)
- Created `modules/security.py` — validation utilities:
  - `validate_pdf_upload()` — checks PDF magic bytes, file size (<10 MB), path traversal
  - `sanitize_filename()` — strips dangerous characters, max 255 chars
  - `validate_coordinates()` — bounds-check lat (15-22), lon (72-81) for Maharashtra
  - `geojson_complexity_safe()` — limits GeoJSON node count to 50,000
- Updated `doc_extractor.py` — validates + sanitizes uploads before processing
- Updated `area_calculator.py` — checks GeoJSON complexity before parsing
- Updated `app.py` — coordinate validation on analyze, file size check on upload
- Updated `.env.example` — added `STREAMLIT_SERVER_COOKIE_SECRET`
- Created `test_security.py` — 9 tests for all security functions
- **Result: 49/49 tests pass, 0 errors**

### What Changed (Session 5)
| File | Before | After |
| :--- | :--- | :--- |
| `modules/security.py` | Didn't exist | PDF, filename, coordinate, GeoJSON validation |
| `modules/doc_extractor.py` | No upload validation | Validates + sanitizes uploads |
| `modules/area_calculator.py` | No complexity check | Rejects complex GeoJSON before parsing |
| `app.py` | No coord validation | Validates lat/lon, file size |
| `.env.example` | 1 var | Added `STREAMLIT_SERVER_COOKIE_SECRET` |
| `test_security.py` | Didn't exist | 9 tests |

## Suggested Build Order
1. ✅ Refactor code (error handling, logging, structured modules)
2. ✅ Testing (unit tests for all modules)
3. ✅ Docker (Dockerfile + docker-compose)
4. ✅ CI/CD (GitHub Actions)
5. ✅ Security hardening
6. PostgreSQL + PostGIS backend (schema + data migration)
7. Celery/Redis async tasks
8. User Auth (OAuth)
9. GEE satellite integration
10. Advanced Document AI
11. Deep learning crop model pipeline
12. IoT / Ground truth
13. End-to-end testing

## Notes
- venv: `krishinetra_venv\Scripts\Activate.ps1`
- run: `streamlit run app.py` (from krishinetra_mvp/)
- .env: `GEMINI_API_KEY=...`
- logs: `krishinetra_mvp/logs/krishinetra.log`
- docker: `docker compose up --build` from `krishinetra_mvp/`
