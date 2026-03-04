from . import BaseModel
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID  
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = "user"
    
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    profile_img = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id', name='fk_role_user_id'), nullable=True)
    
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")
    revoked_tokens = relationship("RevokedToken", back_populates="user", cascade="all, delete")