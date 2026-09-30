SELECT
    raw_rows,
    raw_distinct_order_items,
    staged_rows,
    validated_rows,
    fact_rows,
    rejected_rows,
    rejected_order_items,
    fact_reconciliation_status
FROM {{ ref('int_s3_sales_quality_audit') }}
WHERE fact_reconciliation_status != 'PASS'
   OR validated_rows != fact_rows
