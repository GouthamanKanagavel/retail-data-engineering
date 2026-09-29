{{ config(materialized='table') }}

SELECT
    p.payment_id,
    p.order_id,
    p.payment_date,
    p.payment_method,
    p.payment_amount
FROM {{ source('retail_raw', 'RAW_PAYMENTS') }} p
INNER JOIN {{ ref('stg_orders') }} o
    ON p.order_id = o.order_id
WHERE p.payment_id IS NOT NULL
  AND p.order_id IS NOT NULL
  AND p.payment_amount >= 0
