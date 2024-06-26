
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
class UserRegister(SQLModel):
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
    experiences: list["Experience"] = Relationship(back_populates="owner")
    skills: list["Skill"] = Relationship(back_populates="owner")
    tags: list["Tag"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
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
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
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


class TagBase(SQLModel):
    """Base model for tags."""

    name: str
    model_config = {"json_schema_extra": {"examples": [{"name": "Backend"}]}}


class Tag(TagBase, table=True):
    """Database model for tags."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="tags")


class TagsCreate(TagBase):
    pass


class TagsUpdate(TagBase):
    pass


class TagsOut(TagBase):
    id: int
    owner_id: int


class SkillBase(SQLModel):
    """Base model for skills."""

    name: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Python",
                }
            ]
        }
    }


class SkillCreate(SkillBase):
    """Model for creating new skill entries."""

    name: str


class SkillUpdate(SkillBase):
    """Model for updating existing skill entries."""

    name: str | None = None  # type: ignore


class Skill(SkillBase, table=True):
    """Database model for skill entries."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="skills")


class SkillOut(SkillBase):
    id: int
    owner_id: int


class SkillOpen(SQLModel):
    name: str
    tags: list | None = None


class ExperienceBase(SQLModel):
    """Base model for work experience."""

    title: str
    description: str | None = None
    location: str
    company: str
    month_start: int
    year_start: int
    month_end: int
    year_end: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Software Developer",
                    "description": "Developing software",
                    "location": "Canada, Toronto",
                    "company": "Google",
                    "month_start": 9,
                    "year_start": 2023,
                    "month_end": 6,
                    "year_end": 2025,
                }
            ]
        }
    }


class ExperienceCreate(ExperienceBase):
    """Model for creating new work experience entries."""

    title: str


class ExperienceUpdate(ExperienceBase):
    """Model for updating existing work experience entries."""

    title: str | None = None  # type: ignore


class Experience(ExperienceBase, table=True):
    """Database model for work experience entries."""

    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="experiences")


class ExperienceOut(ExperienceBase):
    id: int
    owner_id: int


class ExperienceOpen(SQLModel):
    title: str
    description: str | None = None
    location: str
    company: str
    month_start: int
    year_start: int
    month_end: int
    year_end: int
