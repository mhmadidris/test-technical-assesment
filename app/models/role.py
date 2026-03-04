from . import BaseModel
from app.enums.role import RoleName, RoleTitle
from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

class Role(BaseModel):
    __tablename__ = "role"
    
    title = Column(Enum(RoleTitle), nullable=False)
    name = Column(Enum(RoleName), nullable=False)
    
    users = relationship("User", back_populates="role")