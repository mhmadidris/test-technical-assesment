from pydantic import BaseModel, EmailStr, constr, ConfigDict, field_validator
from typing import Optional
from app.enums.role import RoleName, RoleTitle
import uuid
from typing import Union
import re


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshRequestSchema(BaseModel):
    refresh_token: str


class LogoutRequestSchema(BaseModel):
    refresh_token: Optional[str]


class ChangePasswordSchema(BaseModel):
    password: str

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


class RefreshResponseSchema(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    expires_in: str


class RoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    title: RoleTitle
    name: RoleName


class LoginResponseSchema(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    expires_in: str
    role: Union[RoleName, str]

    @classmethod
    def from_orm(cls, user):
        response = cls.model_validate(user)
        response.role = user.role.name
        return response


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    full_name: str
    phone_number: str
    profile_img: Optional[str]
    is_active: bool
    username: str
    email: EmailStr
    role: RoleResponseSchema
