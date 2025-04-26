SELECT r.review_id, r.review_score, o.order_id, o.order_status
FROM ecommerce.order_reviews r
JOIN ecommerce.orders o ON r.order_id = o.order_id
WHERE r.review_score = 1;
