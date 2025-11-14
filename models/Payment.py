from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .TimestampMixin import TimestampMixin
from sqlalchemy import String
import sqlalchemy as sa

class Payment(SQLModel, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(sa_column=sa.Column(sa.Float, nullable=False))
    status: str = Field(sa_column=sa.Column(String, nullable=False))
    user_id: int = Field(foreign_key="user.id")
    
    user: Optional["User"] = Relationship(back_populates="payments")
    course_purchases: Optional["CoursePurchased"] = Relationship(back_populates="payment")
    