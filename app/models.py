from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="operador")
    status = Column(String(30), nullable=False, default="ativo")
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    credits = Column(Integer, nullable=False, default=0)
    theme = Column(String(20), nullable=False, default="dark")
    radar_ai_avatar = Column(String(20), nullable=False, default="neutro")
    cpf = Column(String(14), nullable=True)
    cnpj = Column(String(18), nullable=True)
    account_type = Column(String(30), nullable=False, default="pessoa_fisica")
    professional_type = Column(String(50), nullable=True)
    company_name = Column(String(180), nullable=True)
    birth_date = Column(Date, nullable=True)
    terms_accepted = Column(Boolean, nullable=False, default=False)
    privacy_accepted = Column(Boolean, nullable=False, default=False)
    terms_version = Column(String(30), nullable=True)
    privacy_version = Column(String(30), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    daily_opportunities = Column(Integer, nullable=True, default=0)
    monthly_ai_analyses = Column(Integer, nullable=True, default=0)
    advanced_filters = Column(Boolean, nullable=True, default=False)
    advanced_reports = Column(Boolean, nullable=True, default=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    base_terms = Column(Text, nullable=True)
    status = Column(String(30), nullable=True)


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    type = Column(String(50), nullable=False)
    url = Column(Text, nullable=True)
    status = Column(String(30), nullable=True)
    last_checked_at = Column(DateTime, nullable=True)
    permission_note = Column(Text, nullable=False)


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    published_at = Column(DateTime, nullable=True)
    url = Column(Text, nullable=True)
    text = Column(Text, nullable=False)
    subcategory = Column(String(100), nullable=True)
    need = Column(Text, nullable=False)
    intent = Column(Text, nullable=False)
    urgency = Column(String(30), nullable=False)
    location = Column(String(255), nullable=True)
    score = Column(Float, nullable=False, default=0)
    status = Column(String(30), nullable=True)
    classification_reason = Column(Text, nullable=True)
    deduplication_key = Column(String(255), nullable=True)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    score = Column(Float, nullable=False)
    priority = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False)
    suggested_response = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    purchased_at = Column(DateTime, nullable=True)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    opportunity_id = Column(
        Integer,
        ForeignKey("opportunities.id"),
        nullable=False
    )
    channel = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    legal_basis = Column(String(100), nullable=False)
    consent_recorded = Column(Boolean, nullable=True, default=False)
    contacted_at = Column(DateTime, nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
