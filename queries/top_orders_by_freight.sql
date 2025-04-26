SELECT order_id, product_id, freight_value
FROM ecommerce.order_items
ORDER BY freight_value DESC
LIMIT 5;
