SELECT *
FROM ecommerce.order_payments
WHERE payment_value > (
    SELECT AVG(payment_value)
    FROM ecommerce.order_payments
);
