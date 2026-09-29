from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_dbt_pipeline",
    start_date=datetime(2026, 9, 29),
    schedule=None,
    catchup=False,
    tags=["retail", "s3", "snowflake", "dbt"],
) as dag:

    ingest_s3_sales = BashOperator(
        task_id="ingest_s3_sales",
        bash_command=(
            "cd /opt/airflow/dbt/retail_dbt && "
            "dbt run-operation ingest_s3_sales"
        ),
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/dbt/retail_dbt && "
            "dbt build"
        ),
    )

    ingest_s3_sales >> dbt_build