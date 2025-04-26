README.md

E-Commerce Database Management System (Team-24)

Project Overview

This project creates a relational database for an E-Commerce platform, based on the Brazilian e-commerce public dataset by Olist (sourced from Kaggle). The system manages data about customers, orders, products, sellers, reviews, payments, and geolocation.

It is designed to:

Efficiently store, update, and query large-scale e-commerce transactional data.

Ensure referential integrity, data normalization (BCNF), and scalability.

Support complex queries and optimize query performance.

The database supports both querying and updating operations.

Team Members

Vaibhav Vinay Ranashoor (UB ID: vranasho)

Mahmood Ali Khan (UB ID: mahmood7)

Nivedhithaa Karunanidhi (UB ID: nkarunan)

Files Provided

create.sql : SQL script to create the database schema.

Milestone 2 Report.pdf : Detailed report describing project tasks, E/R diagrams, BCNF analysis, queries, indexing, and optimization.

How to Run

Create the database:

CREATE DATABASE ecommerce_db;

Execute the schema creation:

Run the create.sql script in your PostgreSQL environment (e.g., PgAdmin, psql).

Load sample data:

Manually insert small test datasets (around 10 entries per table) to debug easily.

For production, load cleaned CSV data using PostgreSQL's import features.

Execute queries:

Run various SELECT, INSERT, UPDATE, DELETE queries (examples are given in the project report).

Database Schema

Main Tables:

geolocation

product_category_translation

customers

sellers

products

orders

order_items

order_payments

order_reviews

Key Design Features

All relations are in Boyce-Codd Normal Form (BCNF).

Referential integrity enforced with primary and foreign keys.

Indexes created on foreign keys and frequently filtered columns to improve performance.

Dataset supports analytical queries like joins, subqueries, GROUP BY, and aggregations.

Datasets Used

Kaggle: Brazilian E-Commerce Public Dataset by Olist

Example Queries (Provided in Report)

Aggregate orders by status

Find top customers by number of orders

Revenue calculation per seller

Payment analysis using subqueries

Challenges Faced

Slow queries on large datasets (~600K+ rows).

Solved by creating targeted indexes and using EXPLAIN ANALYZE for query planning.

Recommended partitioning and materialized views for very large tables.

Bonus

Building a web interface to visualize and interact with the database.

Links

[Google Drive Links in Report]

End of README.md

