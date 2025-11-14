from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .TimestampMixin import TimestampMixin
from sqlalchemy import String, Boolean
import sqlalchemy as sa

class Course(SQLModel, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(String, nullable=False))
    description: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    price: float = Field(sa_column=sa.Column(sa.Float, nullable=False))
    is_active: bool = Field(default=True, sa_column=sa.Column(Boolean, nullable=False))
    