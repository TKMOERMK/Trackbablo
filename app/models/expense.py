from datetime import date
from decimal import Decimal
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

class Expense(Base):
    
    __tablename__ = "Расходы"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    amount: Mapped[Decimal] = mapped_column(Numeric(7, 2))
    category: Mapped[str] = mapped_column(String(20))
    spent_on: Mapped[date] = mapped_column()
