-- name: Revenue by product
SELECT product,
       SUM(quantity)               AS units_sold,
       ROUND(SUM(total_amount), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;

-- name: Revenue by region
SELECT region,
       COUNT(*)                    AS orders,
       ROUND(SUM(total_amount), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- name: Monthly revenue
SELECT substr(order_date, 1, 7)    AS month,
       ROUND(SUM(total_amount), 2) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- name: Top 5 customers by spend
SELECT customer_name,
       COUNT(*)                    AS orders,
       ROUND(SUM(total_amount), 2) AS total_spent
FROM sales
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 5;

-- name: Products above average order value
SELECT product,
       ROUND(AVG(total_amount), 2) AS avg_order_value
FROM sales
GROUP BY product
HAVING AVG(total_amount) > (SELECT AVG(total_amount) FROM sales)
ORDER BY avg_order_value DESC;
