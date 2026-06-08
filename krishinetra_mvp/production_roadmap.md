# Roadmap: Scaling KrishiNetra from MVP to Production

Moving from a hackathon demo to a "real" application requires transitioning from static, pre-computed data to dynamic, real-time intelligence.

## Phase 0 — Engineering Fundamentals (Foundation)
**Target: Solid, testable, reproducible codebase. Do this first.**

- [ ] **Refactor code** — Add structured error handling, logging, type hints. Remove silent fallbacks. Split `app.py` into controller/pages.
- [ ] **Testing** — Unit tests for all modules (pytest). Integration tests for API-dependent paths.
- [ ] **Dockerize** — `Dockerfile` + `docker-compose.yml` with Streamlit + Redis + PostgreSQL.
- [ ] **CI/CD** — GitHub Actions for lint, test, build.
- [ ] **Security** — Input validation, rate limiting, `.env`→secrets manager.
- [ ] **Monitoring** — Sentry for error tracking, structured logging (structlog).

## Phase 1 — Production Infrastructure
**Target: Multi-user, persistent, scalable platform.**

- [ ] **PostgreSQL + PostGIS** — Replace JSON/file storage. Spatial queries for farm boundaries.
- [ ] **User Auth** — OAuth/Google login, session management, per-user field history.
- [ ] **Celery + Redis** — Async background workers for satellite/doc processing. UI stays fast.
- [ ] **Cloud Deployment** — Deploy on AWS/GCP behind load balancer.

## Phase 2 — Core Features (Live Data)
**Target: Real intelligence, not mocked.**

- [ ] **GEE Satellite Pipeline** — Live Sentinel-2 composites. On-the-fly NDVI/EVI/NDWI. Time-series health charts.
- [ ] **Advanced Document AI** — Google Document AI OCR for handwritten records. PDF data ↔ GPS cross-validation. Batch upload for cooperatives.

## Phase 3 — Advanced Intelligence
**Target: Predictive, not just descriptive. (Skip for MVP/pilot.)**

- [ ] **Deep Learning Crop Model** — Train ResNet/ViT on 13-band Sentinel-2 data. Temporal growth curve analysis.
- [ ] **Weather API Integration** — Hyper-local forecasts → actionable irrigation advice.
- [ ] **IoT Integration** — LoRaWAN soil sensor feeds.
- [ ] **Ground Truth Feedback Loop** — Farmer photo uploads → model retraining.

---

## Technical Shift Summary
| Component | MVP (Demo) | Production (Real) |
| :--- | :--- | :--- |
| **Satellite Data** | Pre-computed PNG Overlays | Live GEE/Sentinel Hub API |
| **Crop Prediction** | Coordinate Lookup Table | Multispectral Deep Learning Model |
| **Area Calculation** | Static Shapely Math | Multi-temporal Polygon Monitoring |
| **Document AI** | PDF Extract with fallback | OCR + LLM + Govt API Validation |
| **Storage** | Local JSON Files | PostGIS Spatial Database |
| **Compute** | Local CPU | Distributed Cloud GPU Workers |

---

## Time Estimates (Single Developer, Sequential)

| Phase | Time | Parallelizable? |
| :--- | :--- | :--- |
| Phase 0 — Engineering | ~3 hours | Yes (CI/CD + Docker parallel) |
| Phase 1 — Infrastructure | ~3 hours | Partially |
| Phase 2 — Core Features | ~4 hours | GEE + Doc AI can be parallel |
| Phase 3 — Advanced | ~5 hours | Depends on data availability |
| **Total** | **~15 hours** | **~8 hours parallelized** |
