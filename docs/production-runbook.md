# Retail Data Engineering — Production Runbook

**Project:** `retail-data-engineering`  
**Repository:** `GouthamanKanagavel/retail-data-engineering`  
**Primary branch:** `main`

## 1. Purpose

This runbook defines how to operate, monitor, troubleshoot, recover, and validate the Retail Data Engineering production pipeline.

Pipeline:

```text
AWS S3
   ↓
Snowflake External Stage
   ↓
Snowflake RAW
   ↓
dbt STAGING
   ↓
dbt INTERMEDIATE / QUALITY
   ↓
dbt ANALYTICS
   ↓
Production Data Quality Checks
```

Airflow orchestration:

```text
ingest_s3_sales
       ↓
   dbt_build
       ↓
 quality_checks
```

The objective is to ingest S3 sales data safely, transform it through dbt, reject invalid records without corrupting the fact table, validate data quality, and provide a repeatable recovery procedure.

## 2. Production Components

Repository:

```text
retail-data-engineering/
├── airflow/
│   ├── dags/retail_dbt_pipeline.py
│   └── config/dbt/profiles.yml
├── dbt/retail_dbt/
│   ├── models/
│   ├── macros/
│   ├── tests/
│   ├── dbt_project.yml
│   └── packages.yml
├── docker/docker-compose.airflow.yml
├── python/ops/retail_pipeline_health.py
└── .github/workflows/ci.yml
```

## 3. AWS Environment

Region:

```text
ap-south-1
```

Production S3 bucket:

```text
retail-data-engineering-1790670224
```

Sales prefix:

```text
sales/
```

Verify AWS identity:

```bash
aws sts get-caller-identity
```

List sales files:

```bash
aws s3 ls s3://retail-data-engineering-1790670224/sales/
```

Recursive listing:

```bash
aws s3 ls s3://retail-data-engineering-1790670224/sales/ --recursive
```

Do not delete production S3 objects during troubleshooting unless explicitly approved.

## 4. Snowflake Environment

Database:

```text
RETAIL_DW
```

Primary schemas:

```text
RAW
STAGING
ANALYTICS
```

Development schema:

```text
DBT_DEV
```

CI schema:

```text
DBT_CI
```

Production storage integration:

```text
RETAIL_S3_INTEGRATION
```

Production stage:

```text
RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE
```

Production raw table:

```text
RETAIL_DW.RAW.RAW_S3_SALES_INGEST
```

Table structure:

```sql
CREATE OR REPLACE TABLE RETAIL_DW.RAW.RAW_S3_SALES_INGEST (
    ORDER_ITEM_ID NUMBER,
    ORDER_ID NUMBER,
    PRODUCT_ID NUMBER,
    QUANTITY NUMBER,
    UNIT_PRICE NUMBER(10,2),
    DISCOUNT NUMBER(12,2),
    LINE_AMOUNT NUMBER(12,2),
    SOURCE_FILE VARCHAR,
    INGESTED_AT TIMESTAMP_NTZ
);
```

Verify the stage:

```sql
LIST @RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE;
```

## 5. Airflow Production DAG

DAG ID:

```text
retail_dbt_pipeline
```

Source:

```text
airflow/dags/retail_dbt_pipeline.py
```

Task dependency:

```text
ingest_s3_sales
       ↓
   dbt_build
       ↓
 quality_checks
```

Schedule:

```text
0 2 * * *
```

The schedule is 02:00 according to Airflow's configured timezone. Airflow timestamps observed in this project were UTC, so do not call this 02:00 IST unless the Airflow timezone is explicitly verified.

Reliability settings:

```text
catchup=False
max_active_runs=1
dagrun_timeout=30 minutes
retries=2
retry_delay=2 minutes
task execution_timeout=15 minutes
```

## 6. Start Airflow

From the project root:

```bash
cd "/Users/gouthamankanagavel/Downloads/Banking Project/retail-data-engineering"
```

Start:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   up -d
```

Check:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   ps
```

Expected services include:

```text
postgres
airflow-init
airflow-scheduler
airflow-webserver
```

Scheduler logs:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   logs --tail=100 airflow-scheduler
```

Follow logs:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   logs -f airflow-scheduler
```

Stop following with `Ctrl+C`.

## 7. Verify DAG Registration

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list
```

Confirm:

```text
retail_dbt_pipeline
```

Validate source syntax:

```bash
python3 -m py_compile airflow/dags/retail_dbt_pipeline.py
```

If syntax validation fails, do not rerun production.

## 8. Production Health Check

Utility:

```text
python/ops/retail_pipeline_health.py
```

Run:

```bash
python3 python/ops/retail_pipeline_health.py
```

Healthy ending:

```text
Latest state: success
HEALTH CHECK: PASS
```

The script fails when Airflow cannot be queried, no DAG runs exist, the latest run cannot be parsed, or the latest run is not successful.

## 9. Inspect Recent Airflow Runs

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list-runs   -d retail_dbt_pipeline   -o table
```

Record:

- DAG run ID
- state
- execution date
- start time
- end time

Healthy state:

```text
success
```

Do not blindly rerun a failed run.

## 10. Airflow Failure Logging

The DAG failure callback logs:

```text
DAG_ID
TASK_ID
RUN_ID
EXECUTION_DATE
EXCEPTION
```

Preserve the original exception before changing anything.

## 11. Environment Variables and Secrets

Local Docker uses:

```text
.env
```

The dbt password is supplied through:

```text
DBT_PASSWORD
```

Safe diagnostic:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   sh -lc 'if [ -n "$DBT_PASSWORD" ]; then echo "DBT_PASSWORD=SET"; else echo "DBT_PASSWORD=MISSING"; fi'
```

Never print, commit, or hard-code the actual password.

## 12. S3 Ingestion

Airflow task:

```text
ingest_s3_sales
```

It invokes:

```text
dbt run-operation ingest_s3_sales
```

Macro:

```text
dbt/retail_dbt/macros/ingest_s3_sales.sql
```

The macro executes a Snowflake `COPY INTO` against:

```text
RETAIL_DW.RAW.RAW_S3_SALES_INGEST
```

with:

```text
ON_ERROR = 'ABORT_STATEMENT'
```

Flow:

```text
S3
 ↓
Snowflake Stage
 ↓
COPY INTO
 ↓
RAW_S3_SALES_INGEST
```

## 13. Verify S3 Ingestion

Stage:

```sql
LIST @RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE;
```

Raw table:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT ORDER_ITEM_ID) AS distinct_order_items,
    COUNT(DISTINCT SOURCE_FILE) AS source_files,
    MAX(ORDER_ITEM_ID) AS max_order_item_id
FROM RETAIL_DW.RAW.RAW_S3_SALES_INGEST;
```

The S3 ingestion process was tested for idempotency. Reprocessing already-loaded files should not create duplicate ingestion records.

A COPY reporting zero new files can be healthy.

## 14. dbt Build

Airflow task:

```text
dbt_build
```

Project:

```text
dbt/retail_dbt
```

Validate:

```bash
cd dbt/retail_dbt
dbt parse --no-partial-parse
```

Build:

```bash
dbt build --no-partial-parse
```

Tests:

```bash
dbt test --no-partial-parse
```

Targeted model:

```bash
dbt run --select <model_name>
```

Targeted test:

```bash
dbt test --select <test_name>
```

Do not disable production tests to obtain a green build.

## 15. dbt Data Flow

The S3 sales path is:

```text
RAW_S3_SALES_INGEST
        ↓
stg_s3_sales
        ↓
int_s3_sales_validated
        ├───────────────┐
        ↓               ↓
fact_sales       rejection models
```

Important rejection models:

```text
int_s3_sales_rejected
int_s3_sales_quality_rejected
int_s3_sales_all_rejected
```

## 16. Staging and Validation Rules

Physical validation includes:

```text
quantity > 0
unit_price >= 0
discount >= 0
```

The staging layer deduplicates using:

```text
order_item_id
```

Validated sales are checked against:

```text
sales → orders
sales → products
```

Records that fail required relationships are rejected rather than inserted into the fact table.

## 17. Fact Sales

The S3-backed fact model is incremental:

```text
materialized = incremental
unique_key = order_item_id
incremental_strategy = merge
```

Business key:

```text
ORDER_ITEM_ID
```

The model is intended to process new order items without rebuilding all historical data.

## 18. Data Quality Checks

The production quality task runs:

```text
s3_sales_fact_reconciliation
fact_sales_duplicate_order_items
s3_sales_rejection_threshold
```

A production run is not considered healthy until these checks pass.

### Reconciliation

Validates that the validated S3 population is correctly represented in the fact table.

Expected:

```text
PASS
```

### Duplicate detection

```sql
SELECT
    ORDER_ITEM_ID,
    COUNT(*) AS record_count
FROM RETAIL_DW.ANALYTICS.FACT_SALES
GROUP BY ORDER_ITEM_ID
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

### Rejection threshold

Protects against unexpectedly large rejection volumes.

Do not disable this test to make production green.

## 19. Rejection Types

Physical rejection reasons:

```text
INVALID_QUANTITY
INVALID_UNIT_PRICE
INVALID_DISCOUNT
```

Relationship rejection reasons:

```text
MISSING_ORDER
MISSING_PRODUCT
```

Relevant models:

```text
int_s3_sales_quality_rejected
int_s3_sales_rejected
int_s3_sales_all_rejected
```

A rejected record is not automatically an infrastructure failure.

## 20. Controlled Failure Test

A controlled test used:

```text
ORDER_ITEM_ID = 999999
ORDER_ID      = 100001
PRODUCT_ID    = 1
QUANTITY      = 2
UNIT_PRICE    = 100.00
DISCOUNT      = -5.00
LINE_AMOUNT   = 195.00
```

Expected classification:

```text
INVALID_DISCOUNT
```

Expected behavior:

```text
RAW
 ↓
quality classification
 ↓
INVALID_DISCOUNT
 ↓
rejected
 ↓
not inserted into fact_sales
```

The test data was removed and the production baseline restored.

## 21. Ingestion Macro Operational Lesson

The ingestion macro was corrected to explicitly execute generated SQL with:

```jinja
{% do run_query(sql) %}
```

Therefore:

> A successful `dbt run-operation` invocation alone does not prove that the intended SQL executed.

Always verify the Snowflake target state after ingestion.

## 22. Validated Baselines

The validated full dbt build had:

```text
18 models
88 data tests
7 sources
563 macros

PASS=106
WARN=0
ERROR=0
SKIP=0
NO-OP=0
REUSED=0
TOTAL=106
```

Validated raw baseline after controlled-test cleanup:

```text
ROW_COUNT              900763
DISTINCT_ORDER_ITEMS   300261
SOURCE_FILES           4
MAX_ORDER_ITEM_ID      300261
```

These are historical validation baselines, not permanent production thresholds. Legitimate new data will change them.

## 23. Troubleshooting S3

Check AWS:

```bash
aws sts get-caller-identity
aws s3 ls s3://retail-data-engineering-1790670224/sales/
```

Check Snowflake:

```sql
LIST @RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE;
```

Check RAW:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT ORDER_ITEM_ID) AS distinct_order_items,
    COUNT(DISTINCT SOURCE_FILE) AS source_files
FROM RETAIL_DW.RAW.RAW_S3_SALES_INGEST;
```

Investigate:

```text
S3
 ↓
IAM
 ↓
Snowflake storage integration
 ↓
Snowflake stage
 ↓
COPY INTO
 ↓
RAW
```

If a source file is missing, investigate the upstream producer. Do not fabricate data or repeatedly rerun ingestion.

## 24. Troubleshooting dbt

Start:

```bash
cd dbt/retail_dbt
```

Parse:

```bash
dbt parse --no-partial-parse
```

Build:

```bash
dbt build --no-partial-parse
```

For a specific model:

```bash
dbt run --select <model_name>
```

For a specific test:

```bash
dbt test --select <test_name>
```

Investigate the first meaningful compilation or database error.

## 25. Troubleshooting Airflow

Broad scheduler logs:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   logs --tail=200 airflow-scheduler
```

Task classification:

```text
ingest_s3_sales
    → S3 / Snowflake ingestion

dbt_build
    → dbt / SQL / transformation

quality_checks
    → data quality / reconciliation
```

Preserve the original error before remediation.

## 26. Reconciliation Failure

Investigate:

```text
RAW_S3_SALES_INGEST
        ↓
stg_s3_sales
        ↓
int_s3_sales_validated
        ↓
fact_sales
```

Compare:

- row counts
- distinct `ORDER_ITEM_ID`
- rejected rows
- duplicate rows
- incremental processing behavior

Do not manually insert missing fact rows until the root cause is known.

## 27. Rejection Threshold Failure

Determine whether the source actually contains an abnormal number of invalid records.

Inspect:

```text
INVALID_QUANTITY
INVALID_UNIT_PRICE
INVALID_DISCOUNT
MISSING_ORDER
MISSING_PRODUCT
```

If the source is genuinely invalid:

```text
Stop
Investigate upstream
Preserve evidence
Do not disable the threshold
```

## 28. Duplicate Fact Records

Run:

```sql
SELECT
    ORDER_ITEM_ID,
    COUNT(*) AS record_count
FROM RETAIL_DW.ANALYTICS.FACT_SALES
GROUP BY ORDER_ITEM_ID
HAVING COUNT(*) > 1;
```

If duplicates exist:

1. Stop downstream publication.
2. Investigate concurrent runs.
3. Investigate source duplication.
4. Investigate incremental logic.
5. Correct the pipeline.
6. Validate before remediation.

Do not simply delete duplicate records.

## 29. Safe Rerun Procedure

Never blindly rerun production.

Use:

```text
1. Identify failed DAG run
        ↓
2. Identify failed task
        ↓
3. Capture error
        ↓
4. Determine root cause
        ↓
5. Determine whether ingestion already completed
        ↓
6. Check Snowflake state
        ↓
7. Fix root cause
        ↓
8. Rerun the appropriate stage
        ↓
9. Validate recovery
```

Before rerunning ingestion:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT ORDER_ITEM_ID) AS distinct_order_items,
    COUNT(DISTINCT SOURCE_FILE) AS source_files
FROM RETAIL_DW.RAW.RAW_S3_SALES_INGEST;
```

Then:

```sql
LIST @RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE;
```

If ingestion already succeeded, do not automatically repeat it.

## 30. Recovery Verification

Check latest DAG:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list-runs   -d retail_dbt_pipeline   -o table
```

Latest run should be:

```text
success
```

Run:

```bash
python3 python/ops/retail_pipeline_health.py
```

Expected:

```text
HEALTH CHECK: PASS
```

Run quality checks:

```bash
cd dbt/retail_dbt

dbt test   --select   s3_sales_fact_reconciliation   fact_sales_duplicate_order_items   s3_sales_rejection_threshold   --no-partial-parse
```

## 31. Production Data Verification

Raw ingestion:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT ORDER_ITEM_ID) AS distinct_order_items,
    COUNT(DISTINCT SOURCE_FILE) AS source_files,
    MAX(ORDER_ITEM_ID) AS max_order_item_id
FROM RETAIL_DW.RAW.RAW_S3_SALES_INGEST;
```

Fact uniqueness:

```sql
SELECT
    ORDER_ITEM_ID,
    COUNT(*) AS record_count
FROM RETAIL_DW.ANALYTICS.FACT_SALES
GROUP BY ORDER_ITEM_ID
HAVING COUNT(*) > 1;
```

Expected duplicate query result:

```text
0 rows
```

## 32. Git Change Management

Check:

```bash
git status
```

Review:

```bash
git diff
```

Validate:

```bash
git diff --check
```

Never commit:

```text
.env
passwords
tokens
private keys
credentials
```

Use feature branches:

```bash
git checkout -b feature/<change-name>
```

Then:

```bash
git add <files>
git commit -m "<meaningful message>"
git push -u origin feature/<change-name>
```

Merge into `main` only after review and green CI.

## 33. CI/CD

Workflow:

```text
.github/workflows/ci.yml
```

CI validates:

```text
dbt project
Airflow DAG
operational health-check syntax
Snowflake dbt integration
```

Local validation:

```bash
python3 -m py_compile airflow/dags/retail_dbt_pipeline.py
python3 -m py_compile python/ops/retail_pipeline_health.py
cd dbt/retail_dbt
dbt parse --no-partial-parse
```

Snowflake integration uses GitHub secrets:

```text
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
SNOWFLAKE_ROLE
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_DATABASE
SNOWFLAKE_SCHEMA
```

Never hard-code these credentials.

## 34. CI Failure Procedure

1. Open the failing GitHub Actions job.
2. Identify the failing job.
3. Find the first meaningful error.
4. Reproduce locally where practical.
5. Fix the underlying issue.
6. Run local validation.
7. Commit and push.
8. Wait for CI to become green.
9. Merge only after required checks pass.

## 35. Docker Safety

Avoid destructive commands in production.

For example:

```bash
docker compose down -v
```

can remove volumes.

Before any destructive Docker command:

```text
STOP
CHECK
CONFIRM
UNDERSTAND STATE
THEN EXECUTE
```

Prefer targeted recovery such as:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   restart airflow-scheduler
```

when only the scheduler requires restart.

## 36. Incident Classification

Classify incidents as:

### Infrastructure

```text
Docker unavailable
Airflow scheduler stopped
Snowflake unavailable
AWS authentication failure
```

### Ingestion

```text
S3 file missing
stage inaccessible
COPY failure
invalid CSV structure
```

### Transformation

```text
dbt compilation error
SQL error
incremental model failure
schema mismatch
```

### Data Quality

```text
reconciliation failure
duplicate order items
rejection threshold exceeded
```

### Business Data

```text
unexpected product mapping
unexpected order relationship
abnormally high rejection rate
```

## 37. Incident Response Checklist

```text
[ ] Record incident start time
[ ] Identify latest Airflow DAG run
[ ] Record DAG run ID
[ ] Identify failed task
[ ] Capture error message
[ ] Determine incident category
[ ] Check S3
[ ] Check Snowflake RAW
[ ] Check dbt
[ ] Check data quality
[ ] Determine root cause
[ ] Apply smallest safe fix
[ ] Rerun appropriate stage
[ ] Validate DAG success
[ ] Validate reconciliation
[ ] Validate quality checks
[ ] Run health check
[ ] Record recovery time
[ ] Document root cause
```

## 38. Incident Documentation Template

```text
Incident:
Date:
Start time:
End time:

DAG:
Run ID:
Failed task:

Incident category:

Observed error:

Impact:

Root cause:

Corrective action:

Rerun performed:

Data validation:

Quality checks:

Health check:

Final status:

Follow-up action:
```

## 39. Common Scenario — DAG Missing

Run:

```bash
python3 -m py_compile airflow/dags/retail_dbt_pipeline.py
```

Then:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   logs --tail=200 airflow-scheduler
```

Look for import errors.

## 40. Common Scenario — Scheduler Down

Check:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   ps
```

If appropriate:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   restart airflow-scheduler
```

Then:

```bash
python3 python/ops/retail_pipeline_health.py
```

## 41. Common Scenario — Health Check Fails

Possible causes:

- Airflow command failed.
- No DAG runs exist.
- Latest run cannot be parsed.
- Latest run is not `success`.

Run:

```bash
python3 python/ops/retail_pipeline_health.py
```

Then:

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list-runs   -d retail_dbt_pipeline   -o table
```

## 42. Production Safety Rules

### Never

- Commit production passwords.
- Put Snowflake passwords in source code.
- Delete production S3 files to make tests pass.
- Delete Snowflake production records to make reconciliation pass.
- Disable data-quality tests to obtain a green build.
- Modify the fact table manually without understanding downstream impact.
- Repeatedly rerun ingestion without checking Snowflake state.
- Treat every rejected record as an infrastructure failure.
- Assume a successful dbt command proves the intended SQL executed.
- Merge failing CI.

### Always

- Investigate before rerunning.
- Preserve logs.
- Check Airflow state.
- Check task state.
- Check S3 state.
- Check Snowflake state.
- Check dbt state.
- Check data-quality state.
- Run the production health check.
- Verify reconciliation after recovery.
- Keep production changes version-controlled.

## 43. Standard Daily Operator Procedure

### Step 1 — Health check

```bash
python3 python/ops/retail_pipeline_health.py
```

### Step 2 — If PASS

No immediate investigation is required.

### Step 3 — If FAIL

Inspect the latest DAG run.

### Step 4

Identify the failed task.

### Step 5

Investigate:

```text
S3
Snowflake
dbt
Data Quality
```

### Step 6

Resolve the underlying issue.

### Step 7

Rerun only the required stage.

### Step 8

Verify:

```text
Airflow success
dbt success
quality checks PASS
reconciliation PASS
health check PASS
```

## 44. Production Readiness Checklist

### Pipeline

```text
[x] S3 ingestion implemented
[x] Snowflake raw ingestion implemented
[x] dbt transformations implemented
[x] Incremental fact model implemented
[x] Idempotent ingestion verified
```

### Data Quality

```text
[x] Physical-quality rejection handling
[x] Relationship rejection handling
[x] Reconciliation test
[x] Duplicate detection
[x] Rejection threshold
[x] Controlled failure test
```

### Orchestration

```text
[x] Airflow production schedule
[x] Retries
[x] Task timeouts
[x] DAG timeout
[x] max_active_runs
[x] Failure logging
[x] Production health check
```

### CI/CD

```text
[x] dbt parse validation
[x] Airflow syntax validation
[x] Health-check syntax validation
[x] Snowflake integration tests
[x] GitHub Actions
[x] Green CI
```

### Operations

```text
[x] Production health-check utility
[x] Incident investigation procedure
[x] Safe rerun procedure
[x] Recovery verification
[x] Production runbook
```

## 45. Production Success Criteria

A production run is healthy only when:

```text
Airflow DAG
    ↓
SUCCESS
    ↓
S3 ingestion
    ↓
SUCCESS
    ↓
dbt build
    ↓
SUCCESS
    ↓
Quality checks
    ↓
PASS
    ↓
Reconciliation
    ↓
PASS
    ↓
Health check
    ↓
PASS
```

## 46. Quick Reference

### Start Airflow

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   up -d
```

### Check Airflow

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   ps
```

### Check DAG

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list
```

### Check runs

```bash
docker compose   --env-file .env   -f docker/docker-compose.airflow.yml   exec -T airflow-scheduler   airflow dags list-runs   -d retail_dbt_pipeline   -o table
```

### Health check

```bash
python3 python/ops/retail_pipeline_health.py
```

### Check S3

```bash
aws s3 ls s3://retail-data-engineering-1790670224/sales/
```

### Check Snowflake stage

```sql
LIST @RETAIL_DW.RAW.RETAIL_SALES_S3_STAGE;
```

### Check RAW

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT ORDER_ITEM_ID) AS distinct_order_items,
    COUNT(DISTINCT SOURCE_FILE) AS source_files
FROM RETAIL_DW.RAW.RAW_S3_SALES_INGEST;
```

### Validate dbt

```bash
cd dbt/retail_dbt
dbt parse --no-partial-parse
```

### Build dbt

```bash
dbt build --no-partial-parse
```

### Run production quality checks

```bash
dbt test   --select   s3_sales_fact_reconciliation   fact_sales_duplicate_order_items   s3_sales_rejection_threshold   --no-partial-parse
```

### Validate code

```bash
python3 -m py_compile airflow/dags/retail_dbt_pipeline.py
python3 -m py_compile python/ops/retail_pipeline_health.py
git diff --check
```

## 47. Ownership and Change Control

This runbook is a production repository artifact.

When the DAG, dbt models, Snowflake objects, AWS configuration, operational scripts, or recovery procedures change, update this document in the same change or in a dedicated documentation change.

The runbook must remain aligned with the actual implementation.

## 48. Final Operational Principle

Never declare the pipeline healthy based on a single successful command.

Production health must be established across:

```text
Airflow
   ↓
S3
   ↓
Snowflake RAW
   ↓
dbt
   ↓
Validated data
   ↓
Fact table
   ↓
Data quality
   ↓
Reconciliation
   ↓
Operational health check
```

A production incident is resolved only when both the orchestration path and the data path have been validated.
