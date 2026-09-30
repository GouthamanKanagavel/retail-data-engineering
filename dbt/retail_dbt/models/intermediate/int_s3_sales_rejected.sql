{{ config(materialized='table') }}

SELECT
    s.order_item_id,
    s.order_id,
    s.product_id,
    s.quantity,
    s.unit_price,
    s.discount,
    s.line_amount,
    s.source_file,
    s.ingested_at,

    CASE
        WHEN o.order_id IS NULL THEN 'MISSING_ORDER'
        WHEN p.product_id IS NULL THEN 'MISSING_PRODUCT'
        ELSE 'UNKNOWN'
    END AS rejection_reason

FROM {{ ref('stg_s3_sales') }} s

LEFT JOIN {{ ref('stg_orders') }} o
    ON s.order_id = o.order_id

LEFT JOIN {{ ref('stg_products') }} p
    ON s.product_id = p.product_id

WHERE o.order_id IS NULL
   OR p.product_id IS NULL
