from sqlalchemy import and_, not_, or_, select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.schemas.user import CreateUserSchema
from app.enums.role import RoleName
from typing import List, Tuple, Any


def get_user_by_id(id: str, db: Session):
    query = (
        select(User)
        .outerjoin(Role)
        .where(User.id == id)
    )
    data = db.execute(query).first()

    return data


def get_user_by_email(email: str, db: Session):
    query = select(User).where(User.email == email)
    data = db.scalars(query).first()

    return data


def get_all_users(
    page: int,
    limit: int,
    keyword: str,
    role: str,
    db: Session,
) -> Tuple[List[Any], int]:
    query = db.query(User).outerjoin(Role)

    if role:
        query = query.filter(Role.name == role)

    if keyword:
        query = query.filter(User.full_name.ilike(f"%{keyword}%"))

    total_items = query.count()

    if page > 1:
        query = query.offset((page - 1) * limit)

    query = query.limit(limit)
    items = query.all()

    return items, total_items


def insert_user(payload: CreateUserSchema, db: Session):
    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(user: User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def insert_user_with_role(payload: CreateUserSchema, role: Role, db: Session):
    user = User(**payload.model_dump())
    user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def insert_user_with_rollback(data: dict, db: Session):
    try:
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)

        is_succeeded = True
        username = data["username"]

        return username, is_succeeded

    except Exception as e:
        db.rollback()

        is_succeeded = False
        username = data["username"]

        return username, is_succeeded


def remove_user_by_id(id: str, db: Session):
    user = get_user_by_id(id, db)
    user_to_remove = user.User

    db.delete(user_to_remove)
    db.commit()
