
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    TokenResponse,
    UserResponse,
)
from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    email = user_data.email.strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )

    if user_data.cpf:
        existing_cpf = (
            db.query(User)
            .filter(User.cpf == user_data.cpf)
            .first()
        )

        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="Este CPF já está cadastrado."
            )

    if user_data.cnpj:
        existing_cnpj = (
            db.query(User)
            .filter(User.cnpj == user_data.cnpj)
            .first()
        )

        if existing_cnpj:
            raise HTTPException(
                status_code=400,
                detail="Este CNPJ já está cadastrado."
            )

    password = user_data.password

    if (
        len(password) < 8
        or not any(c.isupper() for c in password)
        or not any(c.islower() for c in password)
        or not any(c.isdigit() for c in password)
        or not any(not c.isalnum() for c in password)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "A senha deve ter pelo menos 8 caracteres, "
                "incluindo maiúscula, minúscula, número "
                "e caractere especial."
            )
        )

    if not user_data.terms_accepted:
        raise HTTPException(
            status_code=400,
            detail="É necessário aceitar os termos de uso."
        )

    if not user_data.privacy_accepted:
        raise HTTPException(
            status_code=400,
            detail="É necessário aceitar a política de privacidade."
        )

    user = User(
        name=user_data.name,
        email=email,
        password_hash=hash_password(password),
        role="operador",
        status="ativo",
        credits=0,
        theme="dark",
        radar_ai_avatar="neutro",
        cpf=user_data.cpf,
        cnpj=user_data.cnpj,
        phone=user_data.phone,
        account_type=user_data.account_type,
        professional_type=user_data.professional_type,
        company_name=user_data.company_name,
        birth_date=user_data.birth_date,
        terms_accepted=True,
        privacy_accepted=True,
        terms_version="1.0",
        privacy_version="1.0",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    email = user_data.email.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos."
        )

    if user.status not in ("ativo", "active"):
        raise HTTPException(
            status_code=403,
            detail="Usuário não está ativo."
        )

    user.last_login_at = datetime.utcnow()
    db.commit()

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
