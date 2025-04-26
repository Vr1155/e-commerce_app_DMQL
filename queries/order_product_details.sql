SELECT oi.order_id, oi.product_id, p.product_category_name, oi.price
FROM ecommerce.order_items oi
JOIN ecommerce.products p ON oi.product_id = p.product_id;
