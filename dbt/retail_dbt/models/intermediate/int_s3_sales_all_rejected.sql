{{ config(materialized='table') }}

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    line_amount,
    source_file,
    ingested_at,
    rejection_reason
FROM {{ ref('int_s3_sales_quality_rejected') }}

UNION ALL

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    line_amount,
    source_file,
    ingested_at,
    rejection_reason
FROM {{ ref('int_s3_sales_rejected') }}
