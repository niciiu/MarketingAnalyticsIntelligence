from sqlalchemy import create_engine
from pathlib import Path

SQL_FILES = [
    "sql_views/vw_marketing_kpi.sql",
    "sql_views/vw_campaign_monthly.sql",
    "sql_views/vw_campaign_roi_map.sql",
]

def apply_views_sqlite(engine, sql_path):
    raw = engine.raw_connection()       # ambil koneksi mentah
    try:
        with open(sql_path, "r", encoding="utf-8") as f:
            script = f.read()
        raw.executescript(script)       # jalankan multi-statement
        raw.commit()
        print(f"Applied: {sql_path}")
    finally:
        raw.close()                     # pastikan koneksi ditutup

def main():
    engine = create_engine("sqlite:///data/ads_analytics.db", future=True)
    for sql_path in SQL_FILES:
        apply_views_sqlite(engine, sql_path)
    print("All SQL views created successfully.")

if __name__ == "__main__":
    main()
