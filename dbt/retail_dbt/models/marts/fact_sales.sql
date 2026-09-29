{{ config(materialized='table') }}

SELECT
    oi.order_item_id,
    o.order_id,
    o.order_date,
    o.customer_id,
    o.store_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    oi.quantity * oi.unit_price AS gross_amount,
    (oi.quantity * oi.unit_price) - oi.discount AS net_amount,
    o.order_status,
    o.payment_method
FROM {{ ref('stg_order_items') }} oi
INNER JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
