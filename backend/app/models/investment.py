"""Investment model."""
import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Date, Boolean, Enum, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class InvestmentType(str, enum.Enum):
    """Investment type enumeration."""
    PPF = "PPF"
    ELSS = "ELSS"
    NPS = "NPS"
    FD = "FD"
    MUTUAL_FUND = "MUTUAL_FUND"
    STOCK = "STOCK"
    REAL_ESTATE = "REAL_ESTATE"
    GOLD = "GOLD"
    CRYPTO = "CRYPTO"
    LIC = "LIC"
    SUKANYA_SAMRIDDHI = "SUKANYA_SAMRIDDHI"
    NSC = "NSC"
    OTHER = "OTHER"


class TaxSection(str, enum.Enum):
    """Tax section enumeration."""
    SEC_80C = "80C"
    SEC_80CCC = "80CCC"
    SEC_80CCD = "80CCD"
    SEC_80D = "80D"
    SEC_80E = "80E"
    SEC_80G = "80G"
    NONE = "NONE"


class AssetLiabilityCategory(str, enum.Enum):
    """Asset/Liability category enumeration."""
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"


class Investment(Base):
    """Investment model for tracking investments and assets."""
    
    __tablename__ = "investments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    investment_type = Column(Enum(InvestmentType), nullable=False)
    amount_invested = Column(Numeric(15, 2), nullable=False)
    current_value = Column(Numeric(15, 2), nullable=True)
    annual_return_pct = Column(Numeric(5, 2), nullable=True)
    start_date = Column(Date, nullable=False)
    maturity_date = Column(Date, nullable=True)
    is_tax_saving = Column(Boolean, default=False, nullable=False)
    tax_section = Column(Enum(TaxSection), default=TaxSection.NONE, nullable=False)
    folio_number = Column(String, nullable=True)
    ticker_symbol = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    rich_dad_category = Column(Enum(AssetLiabilityCategory), default=AssetLiabilityCategory.ASSET, nullable=False)
    passive_income_amount = Column(Numeric(15, 2), default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="investments")
    tax_deductions = relationship("TaxDeduction", back_populates="investment")
