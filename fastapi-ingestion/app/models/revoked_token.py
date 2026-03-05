from . import BaseModel
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  
from app.enums.revoked_token import RevokedType

class RevokedToken(BaseModel):
    __tablename__ = "revoked_token"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', name='fk_user_revoked_token_id'), nullable=False)
    type = Column(Enum(RevokedType), nullable=False)
    token = Column(String, nullable=False)
    revoked_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="revoked_tokens")