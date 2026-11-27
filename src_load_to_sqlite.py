"""Step 2: Load validated records into SQLite."""
import sqlite3
from pathlib import Path

import pandas as pd

CLEAN_PATH = Path("output/clean_sales.csv")
DB_PATH = Path("output/sales.db")
SCHEMA_PATH = Path("sql/schema.sql")


def main():
    df = pd.read_csv(CLEAN_PATH)
    DB_PATH.unlink(missing_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text())
        df.to_sql("sales", conn, if_exists="append", index=False)
        count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    print(f"Loaded {count} validated records into {DB_PATH}")


if __name__ == "__main__":
    main()
