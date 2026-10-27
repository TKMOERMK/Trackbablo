from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.repositories import expense_repo
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

DbSession = Annotated[Session, Depends(get_db)]

@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED, )

def create_expense( expense_data: ExpenseCreate, db: DbSession, ):
    return expense_repo.create_expense(db, expense_data)

@router.get( "", response_model=list[ExpenseRead], )
def get_expenses(db: DbSession):
    return expense_repo.get_expenses(db)

@router.get( "/{expense_id}", response_model=ExpenseRead, )

def get_expense( expense_id: int, db: DbSession, ):
    
    expense = expense_repo.get_expense_by_id(db, expense_id)

    if expense is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found", )

    return expense

@router.patch( "/{expense_id}", response_model=ExpenseRead, )

def update_expense( expense_id: int, expense_data: ExpenseUpdate, db: DbSession, ):
    expense = expense_repo.update_expense( db, expense_id, expense_data, )

    if expense is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found", )

    return expense

@router.delete( "/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, )
def delete_expense( expense_id: int, db: DbSession, ):
    
    deleted = expense_repo.delete_expense(db, expense_id)

    if not deleted:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found", )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
