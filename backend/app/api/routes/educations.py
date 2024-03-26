from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Education,
    EducationCreate,
    EducationOpen,
    EducationOut,
    EducationUpdate,
    Message,
)

router = APIRouter()


@router.post("/", response_model=EducationOut)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, education: EducationCreate
) -> Any:
    """
    Create new Education.
    """
    item = Education.model_validate(education, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/list", response_model=list[EducationOpen])
def list_educations(
    session: SessionDep, user_id: int = 0, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    statment = (
        select(Education).where(Education.owner_id == user_id).offset(skip).limit(limit)
    )
    items = session.exec(statment).all()
    return items


@router.get("/{id}", response_model=EducationOut)
def read_education(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get item by ID.
    """
    education = session.get(Education, id)
    if not education:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (education.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return education


@router.put("/{id}", response_model=EducationOut)
def update_education(
    *, session: SessionDep, current_user: CurrentUser, id: int, item_in: EducationUpdate
) -> Any:
    """
    Update an Education.
    """
    education = session.get(Education, id)
    if not education:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (education.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    education.sqlmodel_update(update_dict)
    session.add(education)
    session.commit()
    session.refresh(education)
    return education


@router.delete("/{id}")
def delete_education(
    session: SessionDep, current_user: CurrentUser, id: int
) -> Message:
    """
    Delete an Education.
    """
    education = session.get(Education, id)
    if not education:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (education.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(education)
    session.commit()
    return Message(message="Education deleted successfully")
