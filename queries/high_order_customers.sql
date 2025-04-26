SELECT c.customer_id, g.geolocation_city, g.geolocation_state
FROM ecommerce.customers c
JOIN ecommerce.geolocation g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
WHERE c.customer_id IN (
    SELECT customer_id
    FROM ecommerce.orders
    GROUP BY customer_id
    HAVING COUNT(*) >= 1
)
LIMIT 10;
