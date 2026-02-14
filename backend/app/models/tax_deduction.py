"""Tax deduction model."""
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class TaxDeductionSection(str, enum.Enum):
    """Tax deduction section enumeration."""
    SEC_80C = "80C"
    SEC_80CCC = "80CCC"
    SEC_80CCD_1B = "80CCD_1B"
    SEC_80D = "80D"
    SEC_80E = "80E"
    SEC_80EE = "80EE"
    SEC_80G = "80G"
    SEC_80TTA = "80TTA"
    SEC_80TTB = "80TTB"
    HRA = "HRA"
    LTA = "LTA"


class TaxDeduction(Base):
    """Tax deduction model for tracking tax-saving investments."""
    
    __tablename__ = "tax_deductions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    section = Column(Enum(TaxDeductionSection), nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    proof_document_path = Column(String, nullable=True)
    financial_year = Column(String, nullable=False)  # e.g., "2025-26"
    investment_id = Column(UUID(as_uuid=True), ForeignKey("investments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="tax_deductions")
    investment = relationship("Investment", back_populates="tax_deductions")
