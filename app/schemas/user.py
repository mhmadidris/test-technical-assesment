from typing import Optional, Union, Any
import uuid
from pydantic import BaseModel, EmailStr, constr, ConfigDict, field_validator
from app.enums.role import RoleName, RoleTitle
import re


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Union[uuid.UUID, None] = None
    username: Optional[str]
    email: Optional[EmailStr]
    full_name: Optional[str]
    phone_number: Optional[str]
    profile_img: Optional[str]


class CreateUserSchema(UserSchema):
    password: str
    role_id: uuid.UUID
    profile_img: Union[str, None] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "@$!%*?&" for c in v):
            raise ValueError("Password must contain at least one special character (@$!%*?&)")
        if not re.match(r"^[A-Za-z\d@$!%*?&]+$", v):
            raise ValueError("Password contains invalid characters")
        return v


class UpdateUserSchema(UserSchema):
    role_id: uuid.UUID
    profile_img: Union[str, None] = None


class RoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    title: RoleTitle
    name: RoleName


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    full_name: str
    phone_number: str
    is_active: bool
    username: str
    email: EmailStr
    role: RoleResponseSchema


class RoleListResponseSchame(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: RoleName
    title: RoleTitle


class UserListResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    full_name: str
    username: str
    email: str
    phone_number: str
    profile_img: Optional[str]
    created_at: Any
    updated_at: Union[Any, None]
    role: RoleListResponseSchame


class RequestCheckEmail(BaseModel):
    email: EmailStr


class ResponseCheckEmail(BaseModel):
    user_id: str
    email: EmailStr
    code: int
    status: str
