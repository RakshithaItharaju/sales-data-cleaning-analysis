"""Step 3: Run the SQL analysis queries and print the results."""
import re
import sqlite3
from pathlib import Path

DB_PATH = Path("output/sales.db")
QUERY_FILE = Path("sql/analysis_queries.sql")


def main():
    blocks = re.split(r"-- name: ", QUERY_FILE.read_text())[1:]
    with sqlite3.connect(DB_PATH) as conn:
        for block in blocks:
            title, sql = block.split("\n", 1)
            cur = conn.execute(sql)
            cols = [c[0] for c in cur.description]
            print(f"\n=== {title.strip()} ===")
            print(" | ".join(f"{c:>15}" for c in cols))
            for row in cur.fetchall():
                print(" | ".join(f"{str(v):>15}" for v in row))


if __name__ == "__main__":
    main()
