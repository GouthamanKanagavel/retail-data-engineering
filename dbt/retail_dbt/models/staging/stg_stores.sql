{{ config(materialized='table') }}

SELECT
    store_id,
    TRIM(store_name) AS store_name,
    TRIM(city) AS city,
    TRIM(state) AS state,
    TRIM(region) AS region,
    TRIM(store_type) AS store_type
FROM {{ source('retail_raw', 'RAW_STORES') }}
WHERE store_id IS NOT NULL
