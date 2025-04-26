SELECT g.geolocation_state, COUNT(DISTINCT s.seller_id) AS seller_count
FROM ecommerce.sellers s
JOIN ecommerce.geolocation g ON s.seller_zip_code_prefix = g.geolocation_zip_code_prefix
GROUP BY g.geolocation_state
ORDER BY seller_count DESC;
