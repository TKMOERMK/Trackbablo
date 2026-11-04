import csv
import random
import argparse
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

CATEGORIES = {
    "Еда": ["Бургер", "Кола", "Питца4сира", "х", "пусто"],
    "Транспортс": ["Автобус", "такси", "метро"],
    "разное": ["кино", "донат", "сиги"],
    "подписки": ["яндекс", "иви"],
}

OUTPUT_DIR = Path("data/incoming")
FIELDS = ["source_id", "title", "amount", "category", "spent_on"]

def generate_expense() -> dict[str, str]:
    category = random.choice(list(CATEGORIES))
    title = random.choice(CATEGORIES[category])
    amount = Decimal(random.randint(100, 50000)) / Decimal("100")
    spent_on = date.today() - timedelta(days=random.randint(0, 30))
    return {
        "source_id": str(uuid4()),
        "title": title,
        "amount": f"{amount:.2f}",
        "category": category,
        "spent_on": spent_on.isoformat(),
    }



def generate_csv_files(files: int, rows: int) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid4().hex[:8]
    for file_number in range(1, files + 1):
        file_path = OUTPUT_DIR / (
            f"expenses_{run_id}_{file_number:03d}.csv"
        )
        with file_path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=FIELDS,
            )
            writer.writeheader()
            for _ in range(rows):
                writer.writerow(generate_expense())
        print(f"Создан файл: {file_path} ({rows} записей)")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Генератор CSV"
    )
    parser.add_argument(
        "--files",
        type=int,
        default=5,
        help="Колво CSV файлов",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=100,
        help="Колво расходов в каждом файле",
    )
    args = parser.parse_args()
    if args.files <= 0 or args.rows <= 0:
        parser.error("Количество файлов и строк должно быть больше нуля")
    generate_csv_files(
        files=args.files,
        rows=args.rows,
    )

