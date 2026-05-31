"""Pydantic schemas for auth requests/responses."""

from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name:  str = Field(..., min_length=1, max_length=100)
    email:      EmailStr
    password:   str = Field(..., min_length=6, max_length=255)


class LoginSchema(BaseModel):
    email:    EmailStr
    password: str


class UserPublic(BaseModel):
    id:         str
    first_name: str
    last_name:  str
    email:      str

    @classmethod
    def from_user(cls, user) -> "UserPublic":
        return cls(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


class AuthResponse(BaseModel):
    user:    UserPublic
    message: str = "ok"
