from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models import TransactionType


# ---------- User ----------
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Category ----------
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)


class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Transaction ----------
class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    amount: float = Field(gt=0)
    type: TransactionType
    date: Optional[datetime] = None
    notes: Optional[str] = None
    category_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1, max_length=255)
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[TransactionType] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None
    category_id: Optional[int] = None


class TransactionOut(BaseModel):
    id: int
    description: str
    amount: float
    type: TransactionType
    date: datetime
    notes: Optional[str] = None
    category: Optional[CategoryOut] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Reports ----------
class SummaryByCategory(BaseModel):
    category: str
    total: float


class MonthlySummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    by_category: list[SummaryByCategory]
