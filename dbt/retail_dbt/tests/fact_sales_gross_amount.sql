SELECT
    order_item_id,
    quantity,
    unit_price,
    gross_amount
FROM {{ ref('fact_sales') }}
WHERE ROUND(gross_amount, 2) <> ROUND(quantity * unit_price, 2)
