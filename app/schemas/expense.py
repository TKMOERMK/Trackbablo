from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ExpenseBase(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    amount: Decimal = Field(gt=0, max_digits=7, decimal_places=2)
    category: str = Field(min_length=1, max_length=20)
    spent_on: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseRead(ExpenseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=30)
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=7,
        decimal_places=2,
    )
    category: str | None = Field(default=None, min_length=1, max_length=20)
    spent_on: date | None = None