"""
Coverage types and definitions for insurance premium calculation.
"""
from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass


class CoverageType(Enum):
    """Insurance coverage types"""
    BI = "Bodily Injury"  # Liability - Bodily Injury
    PD = "Property Damage"  # Liability - Property Damage
    PIP = "Personal Injury Protection"  # Personal Injury Protection
    UM = "Uninsured Motorist"  # Uninsured Motorist
    UIM = "Underinsured Motorist"  # Underinsured Motorist
    COLL = "Collision"  # Collision Coverage
    COMP = "Comprehensive"  # Comprehensive Coverage


@dataclass
class Coverage:
    """Individual coverage configuration"""
    type: CoverageType
    limit: float  # Coverage limit amount
    deductible: float = 0.0  # Deductible amount
    is_required: bool = False  # Whether this coverage is mandatory


@dataclass
class PolicyInfo:
    """Policy information for premium calculation"""
    policy_effective_date: str  # YYYY-MM-DD format
    policy_expiry_date: str  # YYYY-MM-DD format
    is_renewal: bool = False
    renewal_date: str = ""  # YYYY-MM-DD format, used for renewals
    
    def get_rate_date(self) -> str:
        """Get the date to use for rate table lookup"""
        if self.is_renewal and self.renewal_date:
            return self.renewal_date
        return self.policy_effective_date
