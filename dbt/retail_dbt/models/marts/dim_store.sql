{{ config(materialized='table') }}

SELECT
    store_id,
    store_name,
    city,
    state,
    region,
    store_type
FROM {{ ref('stg_stores') }}
