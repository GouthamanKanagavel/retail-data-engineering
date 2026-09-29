SELECT
    order_item_id,
    line_amount,
    (quantity * unit_price) - discount AS expected_line_amount
FROM {{ ref('stg_s3_sales') }}
WHERE ABS(
    line_amount - ((quantity * unit_price) - discount)
) > 0.01