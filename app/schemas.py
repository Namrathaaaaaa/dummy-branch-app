from pydantic import BaseModel, Field, condecimal, field_validator, ConfigDict
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    borrower_id: str
    amount: Decimal
    currency: str
    status: str
    term_months: Optional[int] = None
    interest_rate_apr: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateLoanRequest(BaseModel):
    borrower_id: str = Field(min_length=1)
    amount: condecimal(gt=0, le=50000, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    term_months: Optional[int] = Field(default=None, ge=1)
    interest_rate_apr: Optional[condecimal(ge=0, le=100, max_digits=5, decimal_places=2)] = None

    @field_validator("currency")
    @classmethod
    def currency_upper(cls, v: str) -> str:
        return v.upper()
