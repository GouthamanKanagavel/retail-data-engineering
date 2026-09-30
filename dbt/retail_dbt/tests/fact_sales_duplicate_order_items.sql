SELECT
    order_item_id,
    COUNT(*) AS row_count
FROM {{ ref('fact_sales') }}
GROUP BY order_item_id
HAVING COUNT(*) > 1
