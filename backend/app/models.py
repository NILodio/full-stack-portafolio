from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")
    educations: list["Education"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int


class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class EducationBase(SQLModel):
    """Base model for educational background."""

    title: str
    description: str | None = None
    location: str
    school: str
    month_start: int
    year_start: int
    month_end: int
    year_end: int
    percentage: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Posgraduate",
                    "description": "Lambton",
                    "location": "Canada, Toronto",
                    "school": "Lambton College",
                    "month_start": 9,
                    "year_start": 2023,
                    "month_end": 6,
                    "year_end": 2025,
                    "percentage": 0.95,
                }
            ]
        }
    }


class EducationCreate(EducationBase):
    """Model for creating new educational entries."""

    title: str


class EducationUpdate(EducationBase):
    """Model for updating existing educational entries."""

    title: str | None = None  # type: ignore


class Education(EducationBase, table=True):
    """Database model for educational entries."""

    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="educations")


class EducationOut(EducationBase):
    id: int
    owner_id: int


class EducationOpen(SQLModel):
    title: str
    description: str | None = None
    location: str
    school: str
    month_start: int
    year_start: int
    month_end: int
    year_end: int
    percentage: float
