from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


# =========================================================
# CADASTRO DE USUÁRIO
# =========================================================

class UserCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )

    # =====================================================
    # DADOS PESSOAIS
    # =====================================================

    cpf: Optional[str] = Field(
        default=None,
        min_length=11,
        max_length=14
    )

    phone: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=20
    )

    birth_date: Optional[date] = None

    # =====================================================
    # TIPO DA CONTA
    # =====================================================

    account_type: str = Field(
        default="pessoa_fisica",
        pattern="^(pessoa_fisica|profissional|empresa)$"
    )

    # =====================================================
    # PERFIL PROFISSIONAL
    # =====================================================

    professional_type: Optional[str] = Field(
        default=None,
        max_length=50
    )

    # =====================================================
    # EMPRESA
    # =====================================================

    cnpj: Optional[str] = Field(
        default=None,
        min_length=14,
        max_length=18
    )

    company_name: Optional[str] = Field(
        default=None,
        max_length=180
    )

    # =====================================================
    # TERMOS E PRIVACIDADE
    # =====================================================

    terms_accepted: bool = False

    privacy_accepted: bool = False


# =========================================================
# LOGIN
# =========================================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =========================================================
# RESPOSTA DO USUÁRIO
# =========================================================

class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    status: str

    credits: int

    theme: str

    radar_ai_avatar: str

    plan_id: Optional[int] = None

    # =====================================================
    # NOVOS DADOS DO PERFIL
    # =====================================================

    cpf: Optional[str] = None

    cnpj: Optional[str] = None

    account_type: str

    professional_type: Optional[str] = None

    company_name: Optional[str] = None

    birth_date: Optional[date] = None

    terms_accepted: bool

    privacy_accepted: bool

    terms_version: Optional[str] = None

    privacy_version: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# =========================================================
# TOKEN
# =========================================================

class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

    user: UserResponse


# =========================================================
# PLANOS
# =========================================================

class PlanResponse(BaseModel):

    id: int

    name: str

    price: float

    description: Optional[str] = None

    is_active: bool

    daily_opportunities: int

    monthly_ai_analyses: int

    advanced_filters: bool

    advanced_reports: bool

    model_config = {
        "from_attributes": True
    }


# =========================================================
# TEMA
# =========================================================

class ThemeUpdate(BaseModel):

    theme: str = Field(
        pattern="^(dark|light)$"
    )


# =========================================================
# AVATAR DO RADAR IA
# =========================================================

class RadarAIAvatarUpdate(BaseModel):

    radar_ai_avatar: str = Field(
        pattern="^(masculino|feminino|neutro)$"
    )


# =========================================================
# CRÉDITOS
# =========================================================

class CreditResponse(BaseModel):

    credits: int