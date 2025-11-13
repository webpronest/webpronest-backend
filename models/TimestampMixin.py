from sqlalchemy import Column, TIMESTAMP, func
from sqlmodel import Field
from datetime import datetime, timezone

class TimestampMixin:
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), 
            server_default=func.now(), 
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), 
            server_default=func.now(), 
            onupdate=func.now(), 
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )
