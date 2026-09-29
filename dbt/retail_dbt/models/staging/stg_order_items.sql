{{ config(materialized='table') }}

SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    oi.line_amount
FROM {{ source('retail_raw', 'RAW_ORDER_ITEMS') }} oi
INNER JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
WHERE oi.quantity > 0
  AND oi.unit_price >= 0
  AND oi.discount >= 0
  AND oi.product_id IN (
      SELECT product_id
      FROM {{ source('retail_raw', 'RAW_PRODUCTS') }}
  )
