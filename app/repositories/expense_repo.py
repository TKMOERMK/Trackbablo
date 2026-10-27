from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate
from sqlalchemy import select

def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:

    expense = Expense(**expense_data.model_dump())

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

def get_expenses(db: Session) -> list[Expense]:

    statement = select(Expense).order_by(Expense.id)

    expenses = db.scalars(statement).all()

    return expenses

def get_expense_by_id(db: Session, expense_id: int) -> Expense | None:
    return db.get(Expense, expense_id)
