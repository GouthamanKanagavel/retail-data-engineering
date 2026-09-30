{{ config(materialized='table') }}

WITH valid_s3_sales AS (

    SELECT
        s.order_item_id,
        s.order_id,
        s.product_id,
        s.quantity,
        s.unit_price,
        s.discount,
        s.line_amount,
        s.source_file

    FROM {{ ref('stg_s3_sales') }} s

    INNER JOIN {{ ref('stg_orders') }} o
        ON s.order_id = o.order_id

    INNER JOIN {{ ref('stg_products') }} p
        ON s.product_id = p.product_id
)

SELECT
    s.order_item_id,

    CASE
        WHEN f.order_item_id IS NULL THEN 'NEW_TO_FACT'

        WHEN
            s.order_id != f.order_id
            OR s.product_id != f.product_id
            OR s.quantity != f.quantity
            OR s.unit_price != f.unit_price
            OR s.discount != f.discount
            OR s.line_amount != f.net_amount
        THEN 'VALUE_MISMATCH'

        ELSE 'MATCH'
    END AS reconciliation_status,

    s.order_id AS s3_order_id,
    f.order_id AS fact_order_id,

    s.product_id AS s3_product_id,
    f.product_id AS fact_product_id,

    s.quantity AS s3_quantity,
    f.quantity AS fact_quantity,

    s.unit_price AS s3_unit_price,
    f.unit_price AS fact_unit_price,

    s.discount AS s3_discount,
    f.discount AS fact_discount,

    s.line_amount AS s3_line_amount,
    f.net_amount AS fact_net_amount,

    s.source_file

FROM valid_s3_sales s

LEFT JOIN {{ ref('fact_sales') }} f
    ON s.order_item_id = f.order_item_id
