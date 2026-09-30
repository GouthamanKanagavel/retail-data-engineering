{{ config(materialized='table') }}

WITH rejection_metrics AS (

    SELECT
        COUNT(*) AS rejected_rows,
        COUNT(DISTINCT order_item_id) AS rejected_order_items,

        COUNT_IF(rejection_reason = 'INVALID_QUANTITY')
            AS invalid_quantity_rows,

        COUNT_IF(rejection_reason = 'INVALID_UNIT_PRICE')
            AS invalid_unit_price_rows,

        COUNT_IF(rejection_reason = 'INVALID_DISCOUNT')
            AS invalid_discount_rows,

        COUNT_IF(rejection_reason = 'MISSING_ORDER')
            AS missing_order_rows,

        COUNT_IF(rejection_reason = 'MISSING_PRODUCT')
            AS missing_product_rows

    FROM {{ ref('int_s3_sales_all_rejected') }}
),

pipeline_metrics AS (

    SELECT
        (SELECT COUNT(*)
         FROM {{ source('retail_raw', 'RAW_S3_SALES_INGEST') }}
        ) AS raw_rows,

        (SELECT COUNT(DISTINCT order_item_id)
         FROM {{ source('retail_raw', 'RAW_S3_SALES_INGEST') }}
        ) AS raw_distinct_order_items,

        (SELECT COUNT(*)
         FROM {{ ref('stg_s3_sales') }}
        ) AS staged_rows,

        (SELECT COUNT(*)
         FROM {{ ref('int_s3_sales_validated') }}
        ) AS validated_rows,

        (SELECT COUNT(*)
         FROM {{ ref('fact_sales') }}
        ) AS fact_rows
)

SELECT
    CURRENT_TIMESTAMP() AS audit_timestamp,

    p.raw_rows,
    p.raw_distinct_order_items,
    p.staged_rows,
    p.validated_rows,
    p.fact_rows,

    r.rejected_rows,
    r.rejected_order_items,

    r.invalid_quantity_rows,
    r.invalid_unit_price_rows,
    r.invalid_discount_rows,
    r.missing_order_rows,
    r.missing_product_rows,

    CASE
        WHEN p.validated_rows = p.fact_rows
        THEN 'PASS'
        ELSE 'FAIL'
    END AS FACT_RECONCILIATION_STATUS

FROM pipeline_metrics p
CROSS JOIN rejection_metrics r
