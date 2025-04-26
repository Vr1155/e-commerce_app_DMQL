SELECT *
FROM ecommerce.orders
WHERE order_purchase_timestamp >= NOW() - INTERVAL '10 years'
ORDER BY order_purchase_timestamp DESC
LIMIT 100;
