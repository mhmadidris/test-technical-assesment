from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.role import Role

def get_role_by_id(id: str, db: Session):
    query = select(Role).where(Role.id == id)
    data = db.scalars(query).first()
    return data
