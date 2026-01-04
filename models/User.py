from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .TimestampMixin import TimestampMixin
from sqlalchemy import String, Boolean
import sqlalchemy as sa
from typing import List

class User(SQLModel, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=sa.Column(String, nullable=False))
    last_name: str = Field(sa_column=sa.Column(String, nullable=False))
    email: str = Field(sa_column=sa.Column(String, nullable=False, unique=True, index=True))
    password: str = Field(default=None, sa_column=sa.Column(String, nullable=True))
    avtar_url: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    phone_number: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True))
    google_id: Optional[str] = Field(default=None, sa_column=sa.Column(String, nullable=True, unique=True, index=True))
    email_verified: bool = Field(default=False, sa_column=sa.Column(Boolean, nullable=True))
    is_active: bool = Field(default=True, sa_column=sa.Column(Boolean, nullable=False))
    
    payments: List["Payment"] = Relationship(back_populates="user")
    courses_purchased: List["CoursePurchased"] = Relationship(back_populates="user")
    
