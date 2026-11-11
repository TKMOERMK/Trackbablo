import json
from datetime import date
from pathlib import Path
import pendulum
from airflow.sdk import dag, task, Param, get_current_context
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="generate_expenses",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["trackbablo"],
    params={
        "batch_id": Param(
            "batch_test_001",
            type="string",
            pattern="^[A-Za-z0-9_-]{1,64}$",
        ),
        "target_date": Param(
            "2026-11-04",
            type="string",
            format="date",
        ),
        "files": Param(2, type="integer", minimum=1),
        "rows": Param(5, type="integer", minimum=1),
    },
)
def generate_expenses_dag():

    @task
    def prepare_generation():

        params = get_current_context()["params"]
        date.fromisoformat(params["target_date"])
        print(f"Создаём партию: {params['batch_id']}")
        return {
            "batch_id": params["batch_id"],
            "target_date": params["target_date"],
            "files": params["files"],
            "rows": params["rows"],
        } 
    run_generator = BashOperator(
        task_id="run_generator",
        bash_command=(
            "python /opt/airflow/scripts/generate_expenses.py "
            '--batch-id "$BATCH_ID" '
            '--target-date "$TARGET_DATE" '
            '--files "$FILES" '
            '--rows "$ROWS"'
        ),
        env={
            "BATCH_ID": "{{ params.batch_id }}",
            "TARGET_DATE": "{{ params.target_date }}",
            "FILES": "{{ params.files }}",
            "ROWS": "{{ params.rows }}",
        },
        append_env=True,
        do_xcom_push=False,
    )

    @task
    def check_generated_files(info: dict):
        batch_dir = (
            Path("/opt/airflow/data/batches") / info["batch_id"]
        )
        manifest_path = batch_dir / "manifest.json"
        if not manifest_path.is_file():
            raise RuntimeError("Нет anifest.json")
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if manifest["total_rows"] != info["files"] * info["rows"]:
            raise RuntimeError("Колво строк не совпадает")
        if manifest["target_date"] != info["target_date"]:
            raise RuntimeError("Дата не совпадает")

        for file_name in manifest["files"]:
            if not (batch_dir / file_name).is_file():
                raise RuntimeError(f"CSV: {file_name}")

        print(f"Итого: {manifest['total_rows']} расходов")

        return manifest

    prepared = prepare_generation()
    checked = check_generated_files(prepared)

    prepared >> run_generator >> checked

generate_expenses_dag()

