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

    CASE
        WHEN quantity IS NULL OR quantity <= 0
            THEN 'INVALID_QUANTITY'

        WHEN unit_price IS NULL OR unit_price < 0
            THEN 'INVALID_UNIT_PRICE'

        WHEN discount IS NULL OR discount < 0
            THEN 'INVALID_DISCOUNT'

        ELSE 'UNKNOWN'
    END AS rejection_reason

FROM {{ source('retail_raw', 'RAW_S3_SALES_INGEST') }}

WHERE quantity IS NULL
   OR quantity <= 0
   OR unit_price IS NULL
   OR unit_price < 0
   OR discount IS NULL
   OR discount < 0
