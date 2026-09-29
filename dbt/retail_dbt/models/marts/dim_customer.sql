{{ config(materialized='table') }}

SELECT
    customer_id,
    customer_name,
    email,
    phone,
    city,
    state,
    country,
    registration_date
FROM {{ ref('stg_customers') }}
