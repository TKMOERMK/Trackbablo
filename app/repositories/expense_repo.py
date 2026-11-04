from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from sqlalchemy import select
from datetime import date
from sqlalchemy.dialects.postgresql import insert
from app.schemas.expense import ExpenseBulkItem

def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:

    expense = Expense(**expense_data.model_dump())

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

def get_expenses( db: Session, category: str | None = None, date_from: date | None = None, date_to: date | None = None, ) -> list[Expense]:
    
    statement = select(Expense)

    if category is not None:
        statement = statement.where(Expense.category == category)

    if date_from is not None:
        statement = statement.where(Expense.spent_on >= date_from)

    if date_to is not None:
        statement = statement.where(Expense.spent_on <= date_to)

    statement = statement.order_by(Expense.id)

    return db.scalars(statement).all()

def get_expense_by_id(db: Session, expense_id: int) -> Expense | None:
    return db.get(Expense, expense_id)

def update_expense( db: Session, expense_id: int, expense_data: ExpenseUpdate, ) -> Expense | None:

    expense = db.get(Expense, expense_id)

    if expense is None:
        return None

    update_data = expense_data.model_dump( exclude_unset=True, exclude_none=True, )

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense

def delete_expense(db: Session, expense_id: int) -> bool:
    
    expense = db.get(Expense, expense_id)

    if expense is None:
        return False

    db.delete(expense)
    db.commit()

    return True


def create_expenses_bulk( db: Session, expenses: list[ExpenseBulkItem], ) -> dict[str, int]:
    records = []
    for expense in expenses:
        record = expense.model_dump(exclude={"source_id"})
        record["source_id"] = str(expense.source_id)
        records.append(record)

    statement = ( insert(Expense).values(records).on_conflict_do_nothing(index_elements=[Expense.source_id]).returning(Expense.id))

    try:
        inserted_ids = db.scalars(statement).all()
        db.commit()
    except Exception:
        db.rollback()
        raise
    inserted = len(inserted_ids)
    received = len(expenses)
    return {
        "received": received,
        "inserted": inserted,
        "skipped": received - inserted,
    }

