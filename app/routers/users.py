
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.auth import decode_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Sessão inválida."
        )

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado."
        )

    return user


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status,
        "credits": current_user.credits,
        "theme": current_user.theme,
        "radar_ai_avatar": current_user.radar_ai_avatar,
        "cpf": current_user.cpf,
        "cnpj": current_user.cnpj,
        "account_type": current_user.account_type,
        "professional_type": current_user.professional_type,
        "company_name": current_user.company_name,
    }


@router.get("/")
def list_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return {
        "total": len(users),
        "users": users
    }


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return user
