"""
ETL Script: Load Clean Marketing Campaign Data into SQLite Database

- Read cleaned marketing dataset (CSV)
- Load into SQLite DB with structured schema
- Ensure idempotent (safe to rerun)
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parents[1]
CLEAN_CSV = ROOT / "data" / "marketing_campaign_performance.csv"
DB_PATH   = ROOT / "data" / "ads_analytics.db"
ENGINE_URL = f"sqlite:///{DB_PATH}"

print("📦 Loading dataset from:", CLEAN_CSV)
df = pd.read_csv(CLEAN_CSV, parse_dates=["date"])

# Create engine
engine = create_engine(ENGINE_URL, future=True)

# Define table schema
with engine.begin() as conn:
    conn.exec_driver_sql("""
    CREATE TABLE IF NOT EXISTS campaign_performance (
        date TEXT,
        campaign_id INTEGER,
        company TEXT,
        campaign_type TEXT,
        target_audience TEXT,
        duration TEXT,
        channel TEXT,
        conversion_rate REAL,
        spend REAL,
        roi REAL,
        location TEXT,
        language TEXT,
        clicks INTEGER,
        impressions INTEGER,
        engagement_score INTEGER,
        customer_segment TEXT,
        ctr REAL,
        cpc REAL,
        cpm REAL,
        engagement_rate REAL
    );
    """)
    conn.exec_driver_sql("DELETE FROM campaign_performance;")
    df.to_sql("campaign_performance", conn, if_exists="append", index=False)

print(f"Loaded {len(df):,} rows into {DB_PATH}")
print("Table name: campaign_performance")
