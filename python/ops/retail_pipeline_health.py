import subprocess
import sys


DAG_ID = "retail_dbt_pipeline"


def main():
    command = [
        "docker",
        "compose",
        "--env-file",
        ".env",
        "-f",
        "docker/docker-compose.airflow.yml",
        "exec",
        "-T",
        "airflow-scheduler",
        "airflow",
        "dags",
        "list-runs",
        "-d",
        DAG_ID,
        "-o",
        "table",
    ]

    print(f"Checking Airflow DAG: {DAG_ID}")
    print("-" * 60)

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        print("HEALTH CHECK: ERROR")
        sys.exit(1)

    print(result.stdout)

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    run_lines = [
        line
        for line in lines
        if line.startswith(DAG_ID + " | ")
    ]

    if not run_lines:
        print("HEALTH CHECK: FAIL")
        print("Reason: No DAG runs found.")
        sys.exit(1)

    latest_run = run_lines[0]
    columns = [column.strip() for column in latest_run.split("|")]

    if len(columns) < 3:
        print("HEALTH CHECK: FAIL")
        print("Reason: Could not parse latest DAG run.")
        sys.exit(1)

    latest_state = columns[2]
    latest_run_id = columns[1]

    print("-" * 60)
    print(f"Latest run:   {latest_run_id}")
    print(f"Latest state: {latest_state}")

    if latest_state != "success":
        print("HEALTH CHECK: FAIL")
        sys.exit(1)

    print("HEALTH CHECK: PASS")


if __name__ == "__main__":
    main()
