{{ config(materialized='table') }}

WITH ranked_sales AS (
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

        ROW_NUMBER() OVER (
            PARTITION BY order_item_id
            ORDER BY source_file DESC, ingested_at DESC
        ) AS rn

    FROM {{ source('retail_raw', 'RAW_S3_SALES_INGEST') }}

    WHERE order_item_id IS NOT NULL
      AND order_id IS NOT NULL
      AND product_id IS NOT NULL
      AND quantity > 0
      AND unit_price >= 0
      AND discount >= 0
)

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    line_amount,
    source_file,
    ingested_at

FROM ranked_sales
WHERE rn = 1