from datetime import datetime, timedelta, timezone
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

from fastapi import HTTPException
from jose import JWTError, jwt


# =========================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =========================================================

SECRET_KEY = "RADAR_CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# =========================================================
# ARGON2
# =========================================================

password_hasher = PasswordHasher()


# =========================================================
# SENHAS
# =========================================================

def hash_password(password: str) -> str:
    """
    Gera um novo hash de senha usando Argon2.
    """

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verifica uma senha contra um hash Argon2.

    Também mantém compatibilidade com hashes bcrypt
    que eventualmente existam no banco.
    """

    if not plain_password or not hashed_password:
        return False

    # -----------------------------------------------------
    # HASH ARGON2
    # -----------------------------------------------------

    if hashed_password.startswith("$argon2"):
        try:
            return password_hasher.verify(
                hashed_password,
                plain_password
            )

        except (
            VerifyMismatchError,
            VerificationError,
            ValueError
        ):
            return False

    # -----------------------------------------------------
    # HASH BCRYPT
    # -----------------------------------------------------

    if hashed_password.startswith("$2"):
        try:
            from passlib.context import CryptContext

            bcrypt_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto"
            )

            return bcrypt_context.verify(
                plain_password,
                hashed_password
            )

        except Exception:
            return False

    # -----------------------------------------------------
    # FORMATO DESCONHECIDO
    # -----------------------------------------------------

    return False


def needs_password_rehash(
    hashed_password: str
) -> bool:
    """
    Informa se a senha precisa ser atualizada.

    Hashes bcrypt antigos podem ser migrados para Argon2
    depois de um login bem-sucedido.
    """

    if not hashed_password:
        return True

    return hashed_password.startswith("$2")


# =========================================================
# TOKEN JWT
# =========================================================

def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT para o usuário autenticado.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
) -> Optional[int]:
    """
    Decodifica o JWT e retorna o ID do usuário.

    Retorna None quando o token é inválido,
    expirado ou possui formato incorreto.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (
        JWTError,
        ValueError,
        TypeError
    ):
        return None