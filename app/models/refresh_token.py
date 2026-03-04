from . import BaseModel
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  

class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', name='fk_user_refresh_token_id'), nullable=False)
    token = Column(String, nullable=False)
    expired_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="refresh_tokens")