SELECT p.product_id,
       SUM(oi.price * oi.freight_value) AS total_revenue
FROM ecommerce.order_items oi
JOIN ecommerce.products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;
