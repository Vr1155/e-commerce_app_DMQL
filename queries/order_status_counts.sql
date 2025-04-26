SELECT order_status, COUNT(*) AS total_orders
FROM ecommerce.orders
GROUP BY order_status
ORDER BY total_orders DESC;
