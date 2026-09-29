{{ config(materialized='table') }}

SELECT
    product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    TRIM(subcategory) AS subcategory,
    unit_price
FROM {{ source('retail_raw', 'RAW_PRODUCTS') }}
WHERE product_id IS NOT NULL
  AND unit_price >= 0
