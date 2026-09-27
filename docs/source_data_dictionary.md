# Source Data Dictionary

## CUSTOMERS

| Column | Data Type | Description |
|---|---|---|
| customer_id | INTEGER | Unique customer identifier |
| customer_name | VARCHAR | Customer full name |
| email | VARCHAR | Customer email |
| phone | VARCHAR | Customer phone number |
| city | VARCHAR | Customer city |
| state | VARCHAR | Customer state |
| country | VARCHAR | Customer country |
| registration_date | DATE | Customer registration date |

---

## PRODUCTS

| Column | Data Type | Description |
|---|---|---|
| product_id | INTEGER | Unique product identifier |
| product_name | VARCHAR | Product name |
| category | VARCHAR | Product category |
| subcategory | VARCHAR | Product subcategory |
| brand | VARCHAR | Product brand |
| unit_price | DECIMAL | Current unit price |

---

## STORES

| Column | Data Type | Description |
|---|---|---|
| store_id | INTEGER | Unique store identifier |
| store_name | VARCHAR | Store name |
| city | VARCHAR | Store city |
| state | VARCHAR | Store state |
| region | VARCHAR | Business region |
| store_type | VARCHAR | Physical or online store |

---

## ORDERS

| Column | Data Type | Description |
|---|---|---|
| order_id | INTEGER | Unique order identifier |
| customer_id | INTEGER | Customer identifier |
| store_id | INTEGER | Store identifier |
| order_date | TIMESTAMP | Order creation timestamp |
| order_status | VARCHAR | Current order status |
| payment_method | VARCHAR | Payment method |

---

## ORDER_ITEMS

| Column | Data Type | Description |
|---|---|---|
| order_item_id | INTEGER | Unique order item identifier |
| order_id | INTEGER | Order identifier |
| product_id | INTEGER | Product identifier |
| quantity | INTEGER | Quantity purchased |
| unit_price | DECIMAL | Price at time of sale |
| discount | DECIMAL | Discount amount |
| line_amount | DECIMAL | Total line amount |

---

## PAYMENTS

| Column | Data Type | Description |
|---|---|---|
| payment_id | INTEGER | Unique payment identifier |
| order_id | INTEGER | Order identifier |
| payment_date | TIMESTAMP | Payment timestamp |
| payment_method | VARCHAR | Payment method |
| payment_amount | DECIMAL | Payment amount |
| payment_status | VARCHAR | Payment status |