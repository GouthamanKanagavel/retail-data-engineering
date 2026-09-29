SELECT
    order_item_id,
    gross_amount,
    discount,
    net_amount
FROM {{ ref('fact_sales') }}
WHERE ROUND(net_amount, 2) <> ROUND(gross_amount - discount, 2)
