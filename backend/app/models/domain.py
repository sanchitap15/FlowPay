import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    income_profile = Column(String, default="delivery_worker")  # delivery/driver/vendor/farmer
    created_at = Column(DateTime, default=datetime.utcnow)

    income_events = relationship("IncomeEvent", back_populates="user", cascade="all, delete-orphan")
    financial_state = relationship("FinancialState", back_populates="user", uselist=False, cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    allocations = relationship("Allocation", back_populates="user", cascade="all, delete-orphan")
    trust_history = relationship("TrustScoreHistory", back_populates="user", cascade="all, delete-orphan")


class IncomeEvent(Base):
    __tablename__ = "income_events"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    is_simulated = Column(Boolean, default=True)  # hackathon demo data vs "real" consented data

    user = relationship("User", back_populates="income_events")


class FinancialState(Base):
    """
    Rolling snapshot of a user's capacity. One row per user, overwritten as events arrive.
    """
    __tablename__ = "financial_states"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    baseline_income = Column(Float, default=0.0)
    forecast_low = Column(Float, default=0.0)
    forecast_high = Column(Float, default=0.0)
    weather_status = Column(String, default="STABLE")  # STRONG/STABLE/LEAN/SHOCK
    shock_streak = Column(Boolean, default=False)  # true while currently inside a shock period
    shocks_recovered = Column(Integer, default=0)
    savings_active = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="financial_state")


class SavingsPocket(Base):
    __tablename__ = "savings_pockets"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    label = Column(String, default="General")  # e.g. "School Fees", "Emergency Buffer"
    balance = Column(Float, default=0.0)
    goal_amount = Column(Float, nullable=True)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    principal = Column(Float, nullable=False)
    outstanding_balance = Column(Float, nullable=False)
    status = Column(String, default="active")  # active/closed/defaulted
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="loans")


class Allocation(Base):
    """
    One row per income event: how that income was split, for audit + explainability history.
    """
    __tablename__ = "allocations"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    income_event_id = Column(String, ForeignKey("income_events.id"), nullable=False)

    spendable = Column(Float, default=0.0)
    savings = Column(Float, default=0.0)
    repayment = Column(Float, default=0.0)
    protected = Column(Float, default=0.0)

    weather_status = Column(String, default="STABLE")
    repayment_due = Column(Boolean, default=False)
    explanation = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="allocations")


class TrustScoreHistory(Base):
    __tablename__ = "trust_score_history"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    factors_json = Column(Text, default="[]")  # serialized list of {label, impact}
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="trust_history")