from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime, timezone
from ..utils import security


# User Register Body Schema
class UserRegisterBody(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    email: EmailStr

    # Password complexity validation
    @field_validator("password")
    def validate_password(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        if not any(char in "!@#$%^&*()_+" for char in value):
            raise ValueError("Password must contain at least one special character")
        return value


# User Create Schema
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

    @field_validator("password")
    def hash_password(cls, value):
        if security.is_hash(value):
            return value
        return security.hash_password(value)

    class Config:
        from_attributes = True


# User Login Schema
class UserLogin(BaseModel):
    username: str
    password: str


# User Response Schema
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models


# Role Schema
class Role(BaseModel):
    role_id: int
    role_name: str

    class Config:
        from_attributes = True


# Permission Schema
class Permission(BaseModel):
    permission_id: int
    permission_name: str

    class Config:
        from_attributes = True


# Role Creation Schema
class RoleCreate(BaseModel):
    role_name: str


# Permission Creation Schema
class PermissionCreate(BaseModel):
    permission_name: str


# User with Roles and Permissions Response Schema
class UserWithRolesResponse(BaseModel):
    user_id: int
    username: str
    roles: List[Role] = []

    class Config:
        from_attributes = True
