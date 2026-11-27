# Sales Data Cleaning and Analysis

A small data engineering project: a **Python pipeline** cleans and validates messy sales
data, loads only the valid records into **SQLite**, and **SQL queries** analyse revenue.

**Tech:** Python (pandas), SQL, SQLite

## Pipeline

```
data/raw_sales.csv  ->  clean_sales.py  ->  load_to_sqlite.py  ->  run_analysis.py
   (messy input)        (validate/clean)     (SQLite storage)      (SQL aggregations)
```

1. **Clean and validate** (`src/clean_sales.py`)
   - Removes exact duplicate rows
   - Trims whitespace and standardises casing (`" laptop "` -> `Laptop`, `NORTH` -> `North`)
   - Rejects rows with missing required fields, non-numeric values, invalid dates,
     or quantity / price <= 0
   - Writes rejected rows with a reason to `output/rejected_rows.csv`
   - Adds `total_amount = quantity * unit_price`
2. **Load** (`src/load_to_sqlite.py`): creates the `sales` table (with `PRIMARY KEY`,
   `NOT NULL` and `CHECK` constraints in `sql/schema.sql`) and inserts the clean records.
3. **Analyse** (`src/run_analysis.py`): runs the queries in `sql/analysis_queries.sql`.

## Project structure

```
sales-data-cleaning/
├── data/raw_sales.csv           # messy input data
├── sql/
│   ├── schema.sql               # table definition with constraints
│   └── analysis_queries.sql     # SQL aggregations
├── src/
│   ├── generate_raw_data.py     # (optional) regenerates the messy dataset
│   ├── clean_sales.py
│   ├── load_to_sqlite.py
│   └── run_analysis.py
├── main.py                      # runs the whole pipeline
└── requirements.txt
```

## How to run

```bash
pip install -r requirements.txt
python main.py
```

Outputs are created in `output/`: `clean_sales.csv`, `rejected_rows.csv`, `sales.db`.

## Sample result (data quality report)

| Metric | Count |
|---|---|
| Raw rows | 96 |
| Duplicates removed | 6 |
| Rejected (missing / invalid) | 15 |
| Clean rows loaded | 75 |

## SQL analysis included

- Revenue by product
- Revenue by region
- Monthly revenue
- Top 5 customers by spend
- Products with above-average order value (subquery + `HAVING`)

## Possible improvements

- Add unit tests for the validation rules (pytest)
- Load data in an `INSERT OR REPLACE` incremental mode
- Add a chart of monthly revenue
