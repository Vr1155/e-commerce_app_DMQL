SELECT oi.seller_id, SUM(oi.price) AS total_revenue
FROM ecommerce.order_items oi
GROUP BY oi.seller_id
ORDER BY total_revenue DESC;
