"""Generates a small, intentionally messy sales dataset (data/raw_sales.csv).

The mess is deliberate so the cleaning pipeline has real problems to fix:
duplicates, missing values, negative/zero numbers, bad dates, inconsistent text.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

PRODUCTS = {
    "Laptop": (55000, "Electronics"),
    "Smartphone": (22000, "Electronics"),
    "Headphones": (2500, "Accessories"),
    "Keyboard": (1500, "Accessories"),
    "Mouse": (800, "Accessories"),
    "Monitor": (12000, "Electronics"),
    "Printer": (9000, "Office"),
    "Office Chair": (7000, "Furniture"),
}
REGIONS = ["North", "South", "East", "West"]
CUSTOMERS = ["Anil Kumar", "Priya Sharma", "Ravi Teja", "Sneha Reddy",
             "Karthik Rao", "Meena Iyer", "Arjun Das", "Divya Nair"]

rows = []
start = date(2025, 1, 1)
for i in range(1, 91):
    product = random.choice(list(PRODUCTS))
    price, category = PRODUCTS[product]
    rows.append({
        "order_id": f"ORD{1000 + i}",
        "order_date": (start + timedelta(days=random.randint(0, 330))).isoformat(),
        "customer_name": random.choice(CUSTOMERS),
        "product": product,
        "category": category,
        "quantity": random.randint(1, 5),
        "unit_price": price,
        "region": random.choice(REGIONS),
    })

# ---- inject mess ----
for r in random.sample(rows, 8):                      # inconsistent text
    r["product"] = random.choice([r["product"].upper(), f"  {r['product'].lower()} "])
    r["region"] = random.choice([r["region"].lower(), r["region"].upper()])
for r in random.sample(rows, 5):                      # missing values
    r[random.choice(["customer_name", "product", "quantity", "unit_price"])] = ""
for r in random.sample(rows, 4):                      # negative / zero numbers
    r["quantity"] = random.choice([-2, 0])
for r in random.sample(rows, 3):                      # non-numeric price
    r["unit_price"] = random.choice(["N/A", "abc", "free"])
for r in random.sample(rows, 4):                      # bad / alternate dates
    r["order_date"] = random.choice(["2025-13-45", "not a date", "15/03/2025"])
rows += random.sample(rows, 6)                        # exact duplicate rows
random.shuffle(rows)

Path("data").mkdir(exist_ok=True)
with open("data/raw_sales.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} raw rows to data/raw_sales.csv")
