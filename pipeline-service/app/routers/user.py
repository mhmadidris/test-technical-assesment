from fastapi import status, APIRouter, HTTPException, Depends, Query
from app.schemas.user import (
    CreateUserSchema,
    RequestCheckEmail,
    ResponseCheckEmail,
    UpdateUserSchema,
    UserSchema,
    UserResponseSchema,
    UserListResponseSchema,
)
from app.schemas.auth import ChangePasswordSchema
from app.schemas import Pagination, PaginationMeta
from app.daos.user import (
    get_user_by_email,
    insert_user_with_role,
    get_user_by_id,
    remove_user_by_id,
    get_all_users,
    update_user,
)
from app.daos.role import get_role_by_id
from app.utils.database import get_db
from app.middlewares.auth import JWTBearer
from passlib.hash import argon2
from sqlalchemy.orm import Session
from typing import Optional
from math import ceil
import uuid

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
    response_model=UserSchema,
    include_in_schema=False,
)
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
    response_model=UserSchema,
)
def create_user(request: CreateUserSchema, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(request.email, db)

    if existing_user is not None:
        raise HTTPException(status_code=409, detail="User already exists")

    role = get_role_by_id(request.role_id, db)

    if role is None:
        raise HTTPException(status_code=404, detail="Role is not found")

    request.password = argon2.hash(request.password)

    added_user = insert_user_with_role(request, role, db)
    return_data = get_user_by_id(added_user.id, db)

    return return_data.User


@router.post(
    "/check-email", status_code=status.HTTP_200_OK, response_model=ResponseCheckEmail
)
def check_email(request: RequestCheckEmail, db: Session = Depends(get_db)):
    user = get_user_by_email(request.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )

    return ResponseCheckEmail(
        user_id=str(user.id),
        email=str(user.email),
        code=status.HTTP_200_OK,
        status="success",
    )


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
    include_in_schema=False,
)
@router.delete("/", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_multiple_user(data: str, db: Session = Depends(get_db)):
    id_list = [uuid.UUID(user_id) for user_id in data.split(",") if user_id]

    for user_id in id_list:
        user = get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=422, detail="One of the user is missing, failed to remove"
            )

    for user_id in id_list:
        remove_user_by_id(user_id, db)

    return {"message": "Succesfully removed"}


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
    response_model=Pagination,
    include_in_schema=False,
)
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
    response_model=Pagination,
)
def read_users(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    limit: Optional[int] = Query(10, le=100, description="Number of items per page"),
    role: str | None = None,
    keyword: Optional[str] = Query(
        None, description="Keyword to search for in user by full_name"
    )
):
    items, total_items = get_all_users(
        page,
        limit,
        keyword,
        role,
        db,
    )
    total_pages = ceil(total_items / limit)

    items = [
        UserListResponseSchema(
            id=item.id,
            email=item.email,
            full_name=item.full_name,
            role=item.role,
            username=item.username,
            phone_number=item.phone_number,
            profile_img=item.profile_img,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in items
    ]

    meta = PaginationMeta(
        items_limit=limit,
        items_count=len(items),
        current_page=page,
        total_items=total_items,
        total_pages=total_pages,
    )
    data = Pagination(items=items, meta=meta)

    return data


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
    response_model=UserResponseSchema,
)
def read_specific_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User is not found")

    data = user.User

    return data


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
    response_model=UserResponseSchema,
)
def updated_specific_user(
    user_id: str, request: UpdateUserSchema, db: Session = Depends(get_db)
):
    user = get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    if request.role_id:
        role = get_role_by_id(request.role_id, db)

        if role is None:
            raise HTTPException(status_code=404, detail="Role is not found")

    payload = request.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(user.User, key, value)

    update_user(user.User, db)

    return user.User


@router.patch(
    "/{user_id}/change-password",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
)
def change_password(
    user_id: str, request: ChangePasswordSchema, db: Session = Depends(get_db)
):
    existing_user = get_user_by_id(user_id, db)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    user = existing_user.User

    user.password = argon2.hash(request.password)

    update_user(user, db)

    return {"message": "Succesfully updated"}