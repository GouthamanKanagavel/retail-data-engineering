SELECT
    rejected_order_items
FROM {{ ref('int_s3_sales_quality_audit') }}
WHERE rejected_order_items > 1000
