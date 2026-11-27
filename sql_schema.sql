CREATE TABLE sales (
    order_id      TEXT PRIMARY KEY,
    order_date    TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    product       TEXT NOT NULL,
    category      TEXT,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL    NOT NULL CHECK (unit_price > 0),
    region        TEXT NOT NULL,
    total_amount  REAL    NOT NULL
);
