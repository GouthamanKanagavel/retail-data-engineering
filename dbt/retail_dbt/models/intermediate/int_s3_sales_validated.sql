{{ config(materialized='table') }}

SELECT
    s.order_item_id,
    s.order_id,
    o.order_date,
    o.customer_id,
    o.store_id,
    s.product_id,
    s.quantity,
    s.unit_price,
    s.discount,
    s.line_amount,
    o.order_status,
    o.payment_method,
    s.source_file,
    s.ingested_at

FROM {{ ref('stg_s3_sales') }} s

INNER JOIN {{ ref('stg_orders') }} o
    ON s.order_id = o.order_id

INNER JOIN {{ ref('stg_products') }} p
    ON s.product_id = p.product_id
