# ML System Architecture

This document describes the AI/ML & Optimization intelligence layer for the SIH 26027 project: **AI-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways**.

## 1. Overall System Architecture

The project architecture clearly separates the operational backend (FastAPI, SQLAlchemy) from the machine learning and optimization logic.

```mermaid
flowchart TD
    subgraph Operational Backend
        DB[(PostgreSQL/SQLite)]
        Models[SQLAlchemy Models]
        API[FastAPI Endpoints]
    end

    subgraph Intelligence Layer
        Extractor[Data Extractor]
        Validator[Data Validator]
        FeatureEng[Feature Engineering]
        ML[ML Models (Risk/Impact)]
        Opt[OR-Tools CP-SAT]
    end

    DB --> Extractor
    Extractor --> Validator
    Validator --> FeatureEng
    FeatureEng --> ML
    ML --> Opt
    Opt --> API
```

## 2. Existing Backend Components

The system is built on top of an existing backend repository:
- **Web Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Data Schemas:** Pydantic
- **Entities:**
  - `Train`: Represents rolling stock.
  - `TrainSchedule`: Represents expected passing times for trains across sections.
  - `Section`: Represents physical railway tracks between stations.
  - `Asset`: Represents track/S&T/OHE assets requiring maintenance.
  - `Block`: Represents scheduled maintenance windows.
  - `MaintenanceTask`: Represents work to be done.

## 3. Data Integration Pipeline (app/ml/data)

The `app/ml/data` module handles reading raw data from the operational backend without mutating it.
1. **Extractor:** Queries the database using standard SQLAlchemy sessions and converts raw models into pandas DataFrames.
2. **Validator:** Uses logic to ensure no null deadlines, positive durations, and valid IDs.
3. **Transformer:** Joins `MaintenanceTask` with `Asset` and `Section` to form an ML-ready dataset row.

## 4. Machine Learning & Optimization Pipeline (Future Phases)

- **Feature Engineering:** Derives synthetic/temporal features like `asset_age`, `days_overdue`, and `train_density`.
- **Maintenance Risk Model:** Predicts urgency/risk scores.
- **Optimization Engine:** Uses Google OR-Tools (CP-SAT) to generate candidate windows, evaluate hard constraints (e.g., Train conflicts), and coordinate maintenance tasks into optimal combined blocks.
