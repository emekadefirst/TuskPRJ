"""
Auth routes: register / login / logout / me.

All routes use httponly cookies as the token transport.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status

from src.auth import (
    CurrentUser,
    JWTService,
    hash_password,
    verify_password,
)
from src.auth_schemas import (
    AuthResponse,
    LoginSchema,
    RegisterSchema,
    UserPublic,
)
from src.models import User


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
async def register(payload: RegisterSchema, response: Response) -> AuthResponse:
    if await User.get_or_none(email=payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = await User.create(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=hash_password(payload.password),
    )
    JWTService.issue(response, user)
    return AuthResponse(user=UserPublic.from_user(user), message="registered")


@auth_router.post("/login", response_model=AuthResponse)
async def login(payload: LoginSchema, response: Response) -> AuthResponse:
    user = await User.get_or_none(email=payload.email)
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    JWTService.issue(response, user)
    return AuthResponse(user=UserPublic.from_user(user), message="logged in")


@auth_router.post("/logout")
async def logout(response: Response) -> dict:
    JWTService.clear_cookie(response)
    return {"message": "logged out"}


@auth_router.get("/me", response_model=UserPublic)
async def me(user: CurrentUser) -> UserPublic:
    return UserPublic.from_user(user)



# ---------------------------------------------------------------------------
# User browsing endpoints (admin-style; any logged-in user can view for now)
# ---------------------------------------------------------------------------
from typing import Optional

from fastapi import Depends, Query
from tortoise.expressions import Q

from src.auth import get_current_user


users_router = APIRouter(prefix="/users", tags=["Users"])


def _user_to_dict(u: User) -> dict:
    return {
        "id":         str(u.id),
        "first_name": u.first_name,
        "last_name":  u.last_name,
        "email":      u.email,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "updated_at": u.updated_at.isoformat() if u.updated_at else None,
    }


@users_router.get("/")
async def list_users(
    _: User = Depends(get_current_user),
    search: Optional[str] = Query(default=None),
):
    """Return all users; optional case-insensitive search across name + email."""
    qs = User.all()
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )
    users = await qs
    return [_user_to_dict(u) for u in users]


@users_router.get("/{id}")
async def get_user(id: str, _: User = Depends(get_current_user)):
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_dict(user)


@users_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current: User = Depends(get_current_user),
):
    if str(current.id) == id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return None
