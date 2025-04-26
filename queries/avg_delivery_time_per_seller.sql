SELECT oi.seller_id,
       AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))) / 3600 AS avg_delivery_hours
FROM ecommerce.order_items oi
JOIN ecommerce.orders o ON oi.order_id = o.order_id
GROUP BY oi.seller_id
ORDER BY avg_delivery_hours
LIMIT 10;
