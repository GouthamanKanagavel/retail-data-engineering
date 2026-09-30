{{ config(
    materialized='incremental',
    unique_key='order_item_id',
    incremental_strategy='merge'
) }}

SELECT
    s.order_item_id,
    s.order_id,
    s.order_date,
    s.customer_id,
    s.store_id,
    s.product_id,
    s.quantity,
    s.unit_price,
    s.discount,
    s.quantity * s.unit_price AS gross_amount,
    s.line_amount AS net_amount,
    s.order_status,
    s.payment_method

FROM {{ ref('int_s3_sales_validated') }} s

{% if is_incremental() %}

WHERE s.order_item_id NOT IN (
    SELECT order_item_id
    FROM {{ this }}
)

{% endif %}
