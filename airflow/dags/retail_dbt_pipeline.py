from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_DIR = "/opt/airflow/dbt/retail_dbt"


def log_task_failure(context):
    task_instance = context.get("task_instance")
    exception = context.get("exception")

    print("========== RETAIL PIPELINE TASK FAILURE ==========")
    print(f"DAG_ID: {task_instance.dag_id}")
    print(f"TASK_ID: {task_instance.task_id}")
    print(f"RUN_ID: {context.get('run_id')}")
    print(f"EXECUTION_DATE: {context.get('execution_date')}")
    print(f"EXCEPTION: {exception}")
    print("==================================================")


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": log_task_failure,
}


with DAG(
    dag_id="retail_dbt_pipeline",
    start_date=datetime(2026, 9, 29),
    schedule="0 2 * * *",
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=30),
    default_args=default_args,
    tags=["retail", "s3", "snowflake", "dbt", "quality"],
) as dag:

    ingest_s3_sales = BashOperator(
        task_id="ingest_s3_sales",
        execution_timeout=timedelta(minutes=15),
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt run-operation ingest_s3_sales"
        ),
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        execution_timeout=timedelta(minutes=15),
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt build "
            "--vars '{\"airflow_run_id\": \"{{ dag_run.run_id }}\"}'"
        ),
    )

    quality_checks = BashOperator(
        task_id="quality_checks",
        execution_timeout=timedelta(minutes=15),
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
