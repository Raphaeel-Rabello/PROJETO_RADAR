
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
)
from jose import JWTError, jwt


# =========================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =========================================================

SECRET_KEY = os.getenv("RADAR_SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

if len(SECRET_KEY) < 32:
    raise RuntimeError(
        "Configure RADAR_SECRET_KEY no ambiente de produção "
        "com pelo menos 32 caracteres."
    )


# =========================================================
# ARGON2
# =========================================================

password_hasher = PasswordHasher()


# =========================================================
# SENHAS
# =========================================================

def hash_password(password: str) -> str:
    """Gera um hash seguro usando Argon2."""
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Valida senhas armazenadas em Argon2 ou bcrypt."""

    if not plain_password or not hashed_password:
        return False

    if hashed_password.startswith("$argon2"):
        try:
            return password_hasher.verify(
                hashed_password,
                plain_password,
            )
        except (
            VerifyMismatchError,
            VerificationError,
            ValueError,
        ):
            return False

    if hashed_password.startswith("$2"):
        try:
            from passlib.context import CryptContext

            bcrypt_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto",
            )
            return bcrypt_context.verify(
                plain_password,
                hashed_password,
            )
        except Exception:
            return False

    return False


def needs_password_rehash(
    hashed_password: str,
) -> bool:
    """Indica se um hash antigo precisa ser migrado."""
    if not hashed_password:
        return True

    return hashed_password.startswith("$2")


# =========================================================
# TOKEN JWT
# =========================================================

def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Cria um token JWT para o usuário autenticado."""

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> Optional[int]:
    """Retorna o ID do usuário ou None se o token for inválido."""

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (
        JWTError,
        ValueError,
        TypeError,
    ):
        return None
