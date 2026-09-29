{{ config(materialized='table') }}

SELECT
    product_id,
    product_name,
    category,
    subcategory,
    unit_price
FROM {{ ref('stg_products') }}
