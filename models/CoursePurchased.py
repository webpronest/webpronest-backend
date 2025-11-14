from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .TimestampMixin import TimestampMixin

class CoursePurchased(SQLModel, TimestampMixin, table=True):
    __tablename__ = "course_purchased"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    payment_id: int = Field(foreign_key="payment.id")

    user: Optional["User"] = Relationship(back_populates="courses_purchased")
    course: Optional["Course"] = Relationship(back_populates="purchases")
    payment: Optional["Payment"] = Relationship(back_populates="course_purchases")