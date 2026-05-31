"""
JWT + password + cookie helpers for the prototype.

Hard-coded constants on purpose — no .env, this is a prototype.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, Depends, HTTPException, Response, status

from src.models import User


# ---------------------------------------------------------------------------
# Hard-coded prototype config
# ---------------------------------------------------------------------------
JWT_SECRET            = "prototype-super-secret-change-me-later"
JWT_ALGORITHM         = "HS256"
ACCESS_TOKEN_TTL_MIN  = 60 * 24      # 24 hours
COOKIE_NAME           = "access_token"
COOKIE_PATH           = "/"
COOKIE_SAMESITE       = "lax"        # use "none" + secure=True if cross-site over HTTPS
COOKIE_SECURE         = False        # flip to True behind HTTPS
COOKIE_HTTPONLY       = True


# ---------------------------------------------------------------------------
# Password hashing (argon2)
# ---------------------------------------------------------------------------
_hasher = PasswordHasher()


def hash_password(plain: str) -> str:
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _hasher.verify(hashed, plain)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


# ---------------------------------------------------------------------------
# JWT service
# ---------------------------------------------------------------------------
class JWTService:
    """All token + cookie operations live here."""

    secret    = JWT_SECRET
    algorithm = JWT_ALGORITHM
    ttl_min   = ACCESS_TOKEN_TTL_MIN

    # ---------- token creation / decoding -----------------------------------
    @classmethod
    def generate_token(cls, subject: str, extra_claims: Optional[dict[str, Any]] = None) -> str:
        """
        Create a signed JWT.
        `subject` is what `sub` becomes (we use the user id).
        `extra_claims` is merged in (e.g. email, name, role).
        """
        now = datetime.now(timezone.utc)
        payload: dict[str, Any] = {
            "sub": str(subject),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=cls.ttl_min)).timestamp()),
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(payload, cls.secret, algorithm=cls.algorithm)

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        """
        Decode and validate a JWT. Raises 401 on any failure.
        Use this when you need the raw claims.
        """
        try:
            return jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
            )

    @classmethod
    def verify_token(cls, token: str) -> bool:
        """Return True if the token is valid, False otherwise (no raise)."""
        try:
            jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            return True
        except jwt.PyJWTError:
            return False

    # ---------- cookie helpers ---------------------------------------------
    @classmethod
    def set_cookie(cls, response: Response, token: str) -> None:
        """Attach the JWT to the response as an httponly cookie."""
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            max_age=cls.ttl_min * 60,
            path=COOKIE_PATH,
            httponly=COOKIE_HTTPONLY,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
        )

    @classmethod
    def clear_cookie(cls, response: Response) -> None:
        """Remove the auth cookie from the client."""
        response.delete_cookie(
            key=COOKIE_NAME,
            path=COOKIE_PATH,
            samesite=COOKIE_SAMESITE,
            secure=COOKIE_SECURE,
            httponly=COOKIE_HTTPONLY,
        )

    @classmethod
    def issue(cls, response: Response, user: User) -> str:
        """
        Convenience: build a token for `user`, set the cookie, and return the token.
        """
        token = cls.generate_token(
            subject=str(user.id),
            extra_claims={
                "email":      user.email,
                "first_name": user.first_name,
                "last_name":  user.last_name,
            },
        )
        cls.set_cookie(response, token)
        return token


# ---------------------------------------------------------------------------
# FastAPI dependencies
# ---------------------------------------------------------------------------
def _unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


async def get_current_user(
    access_token: Annotated[Optional[str], Cookie(alias=COOKIE_NAME)] = None,
) -> User:
    """
    Resolve the currently logged-in user from the auth cookie.

    Usage:
        @router.get("/me")
        async def me(user: User = Depends(get_current_user)):
            ...
    """
    if not access_token:
        raise _unauthorized("Missing auth cookie")

    payload = JWTService.decode_token(access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise _unauthorized("Token missing subject")

    user = await User.get_or_none(id=user_id)
    if not user:
        raise _unauthorized("User no longer exists")

    return user


async def get_current_user_optional(
    access_token: Annotated[Optional[str], Cookie(alias=COOKIE_NAME)] = None,
) -> Optional[User]:
    """Same as get_current_user but returns None instead of raising."""
    if not access_token or not JWTService.verify_token(access_token):
        return None
    payload = JWTService.decode_token(access_token)
    return await User.get_or_none(id=payload.get("sub"))


# Re-export types FastAPI dependents commonly use.
CurrentUser = Annotated[User, Depends(get_current_user)]
