SELECT c.customer_id, g.geolocation_city, g.geolocation_state
FROM ecommerce.customers c
JOIN ecommerce.geolocation g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
LIMIT 10;
