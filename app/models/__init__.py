import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID

from app.utils.database import Base

class BaseModel(Base):
    __abstract__ = True 
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(TIMESTAMP(
        timezone=True), 
        nullable=True, 
        onupdate=datetime.now
    )

# Import and re-export all models
from .user import User as User
from .role import Role as Role
from .refresh_token import RefreshToken as RefreshToken
from .revoked_token import RevokedToken as RevokedToken