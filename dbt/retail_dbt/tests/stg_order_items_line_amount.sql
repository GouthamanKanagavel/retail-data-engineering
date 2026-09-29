SELECT
    order_item_id,
    quantity,
    unit_price,
    discount,
    line_amount
FROM {{ ref('stg_order_items') }}
WHERE ROUND(line_amount, 2) <> ROUND((quantity * unit_price) - discount, 2)