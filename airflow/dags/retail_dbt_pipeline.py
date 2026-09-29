from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_dbt_pipeline",
    start_date=datetime(2026, 9, 29),
    schedule=None,
    catchup=False,
    tags=["retail", "dbt", "snowflake"],
) as dag:

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/dbt/retail_dbt && "
            "dbt build"
        ),
    )
