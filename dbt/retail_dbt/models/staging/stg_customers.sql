{{ config(materialized='table') }}

SELECT
    customer_id,
    TRIM(customer_name) AS customer_name,
    LOWER(TRIM(email)) AS email,
    TRIM(phone) AS phone,
    TRIM(city) AS city,
    TRIM(state) AS state,
    TRIM(country) AS country,
    registration_date
FROM {{ source('retail_raw', 'RAW_CUSTOMERS') }}
