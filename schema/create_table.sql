-- Create schema
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Geolocation table: zip prefix should be INT, not VARCHAR
CREATE TABLE ecommerce.geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city VARCHAR(255),
    geolocation_state VARCHAR(2),
    PRIMARY KEY (geolocation_zip_code_prefix, geolocation_city, geolocation_state)  -- composite key because zip codes can repeat in different cities/states
);

-- Product category translation
CREATE TABLE ecommerce.product_category_translation (
    product_category_name VARCHAR(255) PRIMARY KEY,
    product_category_name_english VARCHAR(255)
);

-- Customers table
CREATE TABLE ecommerce.customers (
    customer_id VARCHAR(40) PRIMARY KEY,
    customer_unique_id VARCHAR(40) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(255),
    customer_state VARCHAR(2)
    -- Skipping FK to geolocation because geolocation has duplicates and would fail constraint
);

-- Sellers table
CREATE TABLE ecommerce.sellers (
    seller_id VARCHAR(40) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(255),
    seller_state VARCHAR(2)
    -- Skipping FK to geolocation for same reason as customers
);

-- Products table
CREATE TABLE ecommerce.products (
    product_id VARCHAR(40) PRIMARY KEY,
    product_category_name VARCHAR(255),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT,
    FOREIGN KEY (product_category_name) REFERENCES ecommerce.product_category_translation(product_category_name)
);

-- Orders table
CREATE TABLE ecommerce.orders (
    order_id VARCHAR(40) PRIMARY KEY,
    customer_id VARCHAR(40),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES ecommerce.customers(customer_id) ON DELETE CASCADE
);

-- Order items
CREATE TABLE ecommerce.order_items (
    order_id VARCHAR(40),
    order_item_id INT,
    product_id VARCHAR(40),
    seller_id VARCHAR(40),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES ecommerce.orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES ecommerce.products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES ecommerce.sellers(seller_id) ON DELETE CASCADE
);

-- Order payments
CREATE TABLE ecommerce.order_payments (
    order_id VARCHAR(40),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(10,2),
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES ecommerce.orders(order_id) ON DELETE CASCADE
);

-- Order reviews
CREATE TABLE ecommerce.order_reviews (
    review_id VARCHAR(40) PRIMARY KEY,
    order_id VARCHAR(40),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES ecommerce.orders(order_id) ON DELETE CASCADE
);