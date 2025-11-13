from sqlmodel import SQLModel, Field
from typing import Optional
from .TimestampMixin import TimestampMixin
from sqlalchemy import String, Boolean
import sqlalchemy as sa

class User(SQLModel, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=sa.Column(String, nullable=False))
    middle_name: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    last_name: str = Field(sa_column=sa.Column(String, nullable=False))
    email: str = Field(sa_column=sa.Column(String, nullable=False, unique=True, index=True))
    password: str = Field(sa_column=sa.Column(String, nullable=False))
    is_active: bool = Field(default=True, sa_column=sa.Column(Boolean, nullable=False))
    avtar_url: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    phone_number: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    