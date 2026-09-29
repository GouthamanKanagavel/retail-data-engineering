{{ config(materialized='table') }}

SELECT
    DATEADD(day, SEQ4(), '2026-01-01'::DATE) AS date_day,
    YEAR(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS year,
    MONTH(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS month,
    MONTHNAME(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS month_name,
    DAY(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS day,
    DAYOFWEEK(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS day_of_week,
    DAYNAME(DATEADD(day, SEQ4(), '2026-01-01'::DATE)) AS day_name
FROM TABLE(GENERATOR(ROWCOUNT => 365))
