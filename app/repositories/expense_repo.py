from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
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
