{% macro ingest_s3_sales() %}

COPY INTO {{ target.database }}.RAW.RAW_S3_SALES_INGEST
(
    ORDER_ITEM_ID,
    ORDER_ID,
    PRODUCT_ID,
    QUANTITY,
    UNIT_PRICE,
    DISCOUNT,
    LINE_AMOUNT,
    SOURCE_FILE,
    INGESTED_AT
)
FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        METADATA$FILENAME,
        CURRENT_TIMESTAMP()
    FROM @{{ target.database }}.RAW.RETAIL_SALES_S3_STAGE
)
FILE_FORMAT = (
    FORMAT_NAME = '{{ target.database }}.RAW.CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';

{% endmacro %}
