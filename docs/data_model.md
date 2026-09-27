# Retail Data Model

## Business Entities

The project will use the following primary entities:

### Customer

Stores customer master information.

Key:

- customer_id

Attributes:

- customer_name
- email
- phone
- city
- state
- country
- registration_date

### Product

Stores product master information.

Key:

- product_id

Attributes:

- product_name
- category
- subcategory
- brand
- unit_price

### Store

Stores store information.

Key:

- store_id

Attributes:

- store_name
- city
- state
- region
- store_type

### Order

Represents a customer transaction.

Key:

- order_id

Attributes:

- customer_id
- store_id
- order_date
- order_status
- payment_method

### Order Item

Represents individual products within an order.

Key:

- order_item_id

Attributes:

- order_id
- product_id
- quantity
- unit_price
- discount
- line_amount

---

## Analytical Model

### DIM_DATE

date_key
full_date
day
month
month_name
quarter
year
week
day_name

# DIM_CUSTOMER
customer_key
customer_id
customer_name
email
city
state
country
registration_date

# DIM_PRODUCT
product_key
product_id
product_name
category
subcategory
brand
unit_price

# DIM_STORE
store_key
store_id
store_name
city
state
region
store_type

# FACT_SALES
sales_key
order_id
order_item_id
date_key
customer_key
product_key
store_key
quantity
unit_price
discount
gross_amount
net_amount

# Relationships
DIM_DATE
    |
    |
    +--------- FACT_SALES ---------+
                  |                |
                  |                |
            DIM_CUSTOMER      DIM_PRODUCT
                  |
             DIM_STORE

The fact table contains measurable business events while dimension tables
contain descriptive attributes.