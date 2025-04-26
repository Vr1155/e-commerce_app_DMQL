SELECT c.customer_unique_id,
       COUNT(*) AS order_count
FROM ecommerce.orders o
JOIN ecommerce.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id
ORDER BY order_count DESC
LIMIT 10;
