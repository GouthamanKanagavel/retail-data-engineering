{% macro ingest_s3_sales() %}

COPY INTO {{ target.database }}.RAW.RAW_S3_SALES_INGEST
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
