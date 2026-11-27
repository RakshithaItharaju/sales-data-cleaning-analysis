"""Step 1: Clean and validate raw sales data.

Bad rows are rejected (not silently "fixed") and written to
output/rejected_rows.csv with a reason, so data quality stays visible.
"""
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw_sales.csv")
CLEAN_PATH = Path("output/clean_sales.csv")
REJECTED_PATH = Path("output/rejected_rows.csv")

REQUIRED = ["order_id", "order_date", "customer_name", "product",
            "quantity", "unit_price", "region"]


def clean(df: pd.DataFrame):
    report = {"raw_rows": len(df)}
    df = df.copy()

    # 1. Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    # 2. Standardise text (trim spaces, consistent casing)
    for col in ["customer_name", "product", "category", "region"]:
        df[col] = df[col].astype("string").str.strip()
    df["product"] = df["product"].str.title()
    df["region"] = df["region"].str.title()

    # 3. Keep originals to tell "missing" apart from "invalid", then convert types
    raw_qty, raw_price, raw_date = df["quantity"], df["unit_price"], df["order_date"]
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")

    # 4. Validation rules -> a reason for every rejected row
    df["reject_reason"] = ""

    def flag(mask, reason):
        df.loc[mask, "reject_reason"] += reason + "; "

    for col in REQUIRED:
        flag(df[col].isna(), f"missing {col}") if col not in ("quantity", "unit_price", "order_date") \
            else flag(df[col].isna() & {"quantity": raw_qty, "unit_price": raw_price,
                                        "order_date": raw_date}[col].isna(), f"missing {col}")
    flag(df["quantity"].isna() & raw_qty.notna(), "invalid quantity (not a number)")
    flag(df["unit_price"].isna() & raw_price.notna(), "invalid unit_price (not a number)")
    flag(df["order_date"].isna() & raw_date.notna(), "invalid order_date (expected YYYY-MM-DD)")
    flag(df["quantity"] <= 0, "quantity must be > 0")
    flag(df["unit_price"] <= 0, "unit_price must be > 0")

    rejected = df[df["reject_reason"] != ""].copy()
    clean_df = df[df["reject_reason"] == ""].drop(columns="reject_reason").copy()

    # 5. Derived column + final types
    clean_df["quantity"] = clean_df["quantity"].astype(int)
    clean_df["total_amount"] = clean_df["quantity"] * clean_df["unit_price"]
    clean_df["order_date"] = clean_df["order_date"].dt.strftime("%Y-%m-%d")

    # 6. Same order_id appearing twice with different details -> keep first
    dup_ids = clean_df["order_id"].duplicated(keep="first")
    report["duplicate_order_ids_removed"] = int(dup_ids.sum())
    clean_df = clean_df[~dup_ids]

    report["rejected_rows"] = len(rejected)
    report["clean_rows"] = len(clean_df)
    return clean_df, rejected, report


def main():
    CLEAN_PATH.parent.mkdir(exist_ok=True)
    raw = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False).replace("", pd.NA)

    clean_df, rejected, report = clean(raw)
    clean_df.to_csv(CLEAN_PATH, index=False)
    rejected.to_csv(REJECTED_PATH, index=False)

    print("=== Data Quality Report ===")
    for k, v in report.items():
        print(f"{k:30s}: {v}")
    print(f"\nClean data    -> {CLEAN_PATH}")
    print(f"Rejected rows -> {REJECTED_PATH}")


if __name__ == "__main__":
    main()
