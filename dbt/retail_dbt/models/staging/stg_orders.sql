{{ config(materialized='table') }}

WITH ranked_orders AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY order_date
        ) AS rn
    FROM {{ source('retail_raw', 'RAW_ORDERS') }}
)

SELECT
    order_id,
    customer_id,
    store_id,
    order_date,
    order_status,
    payment_method
FROM ranked_orders
WHERE rn = 1
  AND order_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND store_id IS NOT NULL
  AND customer_id IN (
      SELECT customer_id
      FROM {{ source('retail_raw', 'RAW_CUSTOMERS') }}
  )
  AND store_id IN (
      SELECT store_id
      FROM {{ source('retail_raw', 'RAW_STORES') }}
  )
