from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_DIR = "/opt/airflow/dbt/retail_dbt"


with DAG(
    dag_id="retail_dbt_pipeline",
    start_date=datetime(2026, 9, 29),
    schedule=None,
    catchup=False,
    tags=["retail", "s3", "snowflake", "dbt", "quality"],
) as dag:

    ingest_s3_sales = BashOperator(
        task_id="ingest_s3_sales",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt run-operation ingest_s3_sales"
        ),
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt build"
        ),
    )

    quality_checks = BashOperator(
        task_id="quality_checks",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt test --select "
            "s3_sales_fact_reconciliation "
            "fact_sales_duplicate_order_items "
            "s3_sales_rejection_threshold "
            "--no-partial-parse"
        ),
    )

    ingest_s3_sales >> dbt_build >> quality_checks
