## Source to Target Mapping

# Customers

Oracle.CUSTOMERS
        ↓
Snowflake.RAW_CUSTOMERS
        ↓
STG_CUSTOMERS
        ↓
DIM_CUSTOMER

# Products

Oracle.PRODUCTS
        ↓
Snowflake.RAW_PRODUCTS
        ↓
STG_PRODUCTS
        ↓
DIM_PRODUCT

# Stores

Oracle.STORES
        ↓
Snowflake.RAW_STORES
        ↓
STG_STORES
        ↓
DIM_STORE

# Orders

Oracle.ORDERS
        ↓
Snowflake.RAW_ORDERS
        ↓
STG_ORDERS
        ↓
FACT_SALES

# Order Items

S3 / Oracle.ORDER_ITEMS
        ↓
Snowflake.RAW_ORDER_ITEMS
        ↓
STG_ORDER_ITEMS
        ↓
FACT_SALES

# Payments

S3 / Oracle.PAYMENTS
        ↓
Snowflake.RAW_PAYMENTS
        ↓
STG_PAYMENTS
        ↓
Payment Analytics

## Transformation Rules

# Gross Amount
gross_amount = quantity × unit_price

# Discount Amount
discount_amount = discount

# Net Amount
net_amount = gross_amount - discount_amount

# Data Quality
The pipeline must identify:

Null customer IDs
Null product IDs
Duplicate orders
Duplicate order items
Invalid dates
Negative quantities
Negative prices
Missing customers
Missing products
Missing stores


---

# Step 22 — Create realistic data-quality scenarios

This is important for your project.

We're **intentionally going to create bad data**.

That allows you to demonstrate actual data engineering skills.

We'll eventually have examples such as:

# Duplicate
order_id = 10025
order_id = 10025

# Missing customer
order_id = 10030
customer_id = 999999

where customer 999999 doesn't exist.

# Late-arriving data

An order belonging to September 10 may arrive on September 12.

# Updated record
Customer:
    city = Chennai
later becomes:
    city = Kanchipuram