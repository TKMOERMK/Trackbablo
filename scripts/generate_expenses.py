import argparse
import csv
import json
import random
import re
import shutil
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

CATEGORIES = {
    "Еда": ["Бургер", "Кола", "Питца4сира", "х", "пусто"],
    "Транспортс": ["Автобус", "такси", "метро"],
    "разное": ["кино", "донат", "сиги"],
    "подписки": ["яндекс", "иви"],
}

FIELDS = ["source_id", "title", "amount", "category", "spent_on"]

BATCHES_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "batches"
)

def generate_expense(target_date: date) -> dict[str, str]:
    category = random.choice(list(CATEGORIES))
    title = random.choice(CATEGORIES[category])
    amount = (
        Decimal(random.randint(100, 50000)) / Decimal("100")
    )
    return {
        "source_id": str(uuid4()),
        "title": title,
        "amount": f"{amount:.2f}",
        "category": category,
        "spent_on": target_date.isoformat(),
    }

def generate_csv_files( files: int, rows: int, target_date: date, batch_id: str, ) -> None:

    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", batch_id):
        raise ValueError("Недопустимый batch_id")
    if files <= 0 or rows <= 0:
        raise ValueError("Отрицательное значение")
    
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    batch_dir = BATCHES_DIR / batch_id
    manifest_path = batch_dir / "manifest.json"

    if batch_dir.exists():
        if not manifest_path.is_file():
            raise RuntimeError("manifest.json отсутствует")
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if (
            manifest.get("batch_id") != batch_id
            or manifest.get("target_date") != target_date.isoformat()
            or manifest.get("rows_per_file") != rows
            or len(manifest.get("files", [])) != files
        ):
            raise RuntimeError("Партия уже существует")
        for file_name in manifest["files"]:
            if not (batch_dir / file_name).is_file():
                raise RuntimeError(f"Отсутствует файл {file_name}")
        print(f"Партия уже существует: {batch_dir}")
        return
    
    temp_dir = (
        BATCHES_DIR / f".{batch_id}_{uuid4().hex[:8]}.tmp"
    )

    temp_dir.mkdir()
    
    try:
        file_names = []
        for file_number in range(1, files + 1):
            file_name = f"expenses_{file_number:03d}.csv"
            file_path = temp_dir / file_name
            with file_path.open(
                "w", newline="", encoding="utf-8"
            ) as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=FIELDS,
                )
                writer.writeheader()
                for _ in range(rows):
                    writer.writerow(generate_expense(target_date))
            file_names.append(file_name)
        manifest = {
            "batch_id": batch_id,
            "target_date": target_date.isoformat(),
            "rows_per_file": rows,
            "total_rows": files * rows,
            "files": file_names,
        }
        (temp_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_dir.rename(batch_dir)
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    print(
        f"Партия {batch_id} готова в ней : "
        f"{files} файлов, {files * rows} расходов"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Генератор CSV для Trackbablo"
    )
    parser.add_argument("--files", type=int, default=5)
    parser.add_argument("--rows", type=int, default=100)
    parser.add_argument(
        "--target-date",
        default=date.today().isoformat(),
    )

    parser.add_argument("--batch-id", default=None)

    args = parser.parse_args()
    try:
        target_date = date.fromisoformat(args.target_date)
    except ValueError:
        parser.error("Формат даты не ГГГГ-ММ-ДД")
    batch_id = args.batch_id or f"manual_{uuid4().hex[:8]}"

    generate_csv_files(
        files=args.files,
        rows=args.rows,
        target_date=target_date,
        batch_id=batch_id,
    )
