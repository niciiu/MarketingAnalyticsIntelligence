# 📊 Marketing Campaign Intelligence Platform

### Enterprise-Grade Performance Analytics • KPI Engine • ROI Efficiency Modeling • Executive Intelligence Dashboard

This repository provides an **enterprise-class Marketing Intelligence Platform** designed to operationalize advertising performance, ROI stability, and channel-level efficiency through a scalable analytics pipeline supported by **SQLite, SQL views, and a high-fidelity Streamlit Business Intelligence Dashboard**.

The system is built to meet the needs of modern data teams: **transparent transformations, reproducible metrics, SQL-backed business rules, and real-time visualization** with minimal infrastructure overhead.

---

## 🔥 Executive Summary

Modern marketing organizations require consistent, auditable, and scalable analytics systems to track multi-channel performance.
This project delivers:

*   A unified **data processing pipeline**
*   Standardized **KPI computation** across campaigns
*   A **SQL semantic layer** to centralize business definitions
*   A **Streamlit executive dashboard** for insight delivery
*   Robust **ROI diagnostic engines**, including
    *   Efficiency vs scale mapping (Quadrant Analysis)
    *   Stability modeling via Coefficient of Variation
    *   Multi-period trend analytics

The entire stack is **container-free, dependency-light, and cloud-deployable**, making it ideal for rapid prototyping or enterprise integration.

---

# 🧱 Architecture Overview

A modular, layered BI architecture:

```
           ┌────────────────────────────────────────┐
           │             Data Sources                │
           │     Multi-channel Marketing Dataset     │
           └────────────────────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────┐
          │      Data Preparation & Governance       │
          │  - Cleansing                             │
          │  - Type normalization                    │
          │  - Currency / KPI standardization        │
          │  - Outlier handling                      │
          └─────────────────────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────┐
          │            Analytics Database            │
          │           (SQLite, SQLAlchemy)           │
          │  Centralized metric layer for BI usage   │
          └─────────────────────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────┐
          │               Semantic Layer             │
          │       SQL Views for KPI Consistency      │
          │  vw_marketing_kpi                        │
          │  vw_campaign_monthly                     │
          │  vw_campaign_roi_map                     │
          └─────────────────────────────────────────┘
                              │
                              ▼
          ┌─────────────────────────────────────────┐
          │            BI & Insight Delivery         │
          │        Streamlit Executive Dashboard     │
          │  KPI tiles • Trends • Quadrants • Tables │
          └─────────────────────────────────────────┘
```

This mirrors the structure of enterprise BI systems such as Looker, Tableau Semantic Layer, and Adobe Analytics Workspace.

---

# 📁 System Components

## 1. **Data Layer**

*   200,000-row marketing dataset
*   Standardized schema packaged into `ads_analytics.db`
*   Raw and clean data separation for governance

## 2. **ETL Layer**

*   `load_to_sqlite.py`
    Loads the cleaned dataset into SQLite and enforces consistent data types.

*   `apply_sql_views.py`
    Constructs SQL views that unify KPI logic for all downstream consumption.

This ensures **metric consistency**, one of the core principles of enterprise BI governance.

## 3. **Semantic Layer (SQL Views)**

Three analytical views support the dashboard:

| View Name             | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| `vw_marketing_kpi`    | Daily metrics with CTR, CPC, CPM, ROI aggregation |
| `vw_campaign_monthly` | Monthly performance by channel/campaign           |
| `vw_campaign_roi_map` | KPI foundation for ROI Quadrants and Stability    |

This layer decouples business logic from code — aligning with enterprise BI standards.

## 4. **Analytics & Modeling**

The system performs advanced marketing diagnostics:

### ✓ ROI Stability Modeling

*   Coefficient of Variation (CV)
*   Multi-period smoothing
*   Consistency ranking across channels

### ✓ Efficiency vs Scale Analysis

*   ROI vs Spend Quadrants
*   Identifying high-scale / high-ROI channels
*   Budget reallocation insights

### ✓ Trend Analytics

*   Multi-period ROI trend
*   Spend/CTR dynamics
*   Engagement signal monitoring

---

# 🖥 Executive Dashboard

The Streamlit BI dashboard provides a high-fidelity analytical interface inspired by enterprise BI design principles:

### 📌 Features

*   **KPI Tiles** with directional deltas
*   **Daily Spend Trend**
*   **ROI Trend Line**
*   **Spend Distribution Donut Chart**
*   **Mini Performance Signal Cards**
*   **ROI vs Spend Quadrant (Scale vs Efficiency)**
*   **Channel Stability Table** using CV
*   **Full Monthly Performance Table**

### 🎯 Design Principles

*   Decision-first visualization
*   Minimal cognitive load
*   High information density
*   Clear performance contrasts
*   Consistent value formatting
*   Smooth UX for senior-level consumption

---

# 🛠 Technology Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| Data Processing | Python (Pandas, NumPy)   |
| Database        | SQLite + SQLAlchemy      |
| Transformation  | SQL Views                |
| Modeling        | Statistical CV Framework |
| Visualization   | Altair                   |
| BI Interface    | Streamlit                |
| Development     | VS Code, virtualenv      |

Enterprise-ready. Lightweight. Reproducible.

---

# 🚀 Running in Local Environment

### 1. Clone Repository

```bash
git clone https://github.com/niciiu/MarketingAnalyticsIntelligence.git
cd MarketingAnalyticsIntelligence
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate```

### 3. Install Packages

```bash
pip install -r requirements.txt
```

### 4. Run ETL

```bash
python etl/load_to_sqlite.py
python etl/apply_sql_views.py
```

### 5. Launch Enterprise BI Dashboard

```bash
streamlit run streamlit/streamlit_app.py
```

---

# 📈 Strategic Business Value

This platform enables organizations to:

### **1. Standardize KPI Computation Across Teams**

Centralizing KPI definitions reduces metric fragmentation — a common enterprise BI challenge.

### **2. Identify High-Impact Channels Efficiently**

Quadrant analysis enables strategic budget shifting from low-efficiency to high-efficiency channels.

### **3. Monitor ROI Stability for Long-Term Planning**

Channels with high volatility require creative refinement or allocation safeguards.

### **4. Reduce Time-to-Insight**

Analysts, managers, and executives can access consistent data without manual processing.

---

# 🔮 Next Steps (Enterprise Roadmap)

| Enhancement                   | Description                                    |
| ----------------------------- | ---------------------------------------------- |
| Automated ingestion pipelines | Scheduled refresh, Airflow/Prefect integration |
| Statistical anomaly detection | Identify abrupt KPI shifts                     |
| Predictive ROI modeling       | Prophet / ARIMA / Gradient boosting            |
| Campaign segmentation         | Cluster analysis (KMeans / LDA)                |
| MMM (Media Mix Modeling)      | Incremental lift attribution                   |
| Multi-touch attribution       | Path-based ROI contribution                    |

---

# 👤 Author

**Nicki Utomo**
Marketing Analytics • Business Intelligence • Data Engineering
GitHub: [https://github.com/niciiu](https://github.com/niciiu)
Portfolio-ready enterprise analytics solutions.
