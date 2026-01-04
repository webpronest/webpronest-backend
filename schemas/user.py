from pydantic import BaseModel, computed_field

class UserPublic(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avtar_url: str | None = None
    phone_number: str | None = None
    google_id: str | None = None
    email_verified: bool | None = False
    is_active: bool = True

    @computed_field
    @property
    def name(self) -> str | None:
        return self.first_name + " " + self.last_name

    class Config:
        from_attributes = True  # for SQLModel / ORM
