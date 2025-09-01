"""
Vehicle information for premium calculation.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class VehicleType(Enum):
    """Vehicle type classifications"""
    SEDAN = "Sedan"
    SUV = "SUV"
    TRUCK = "Truck"
    MOTORCYCLE = "Motorcycle"
    COMMERCIAL = "Commercial"
    AGRICULTURAL = "Agricultural"


class VehicleUsage(Enum):
    """Vehicle usage types"""
    COMMUTING = "Commuting"  # Commuting
    BUSINESS = "Business"  # Business
    AGRICULTURAL = "Agricultural"  # Agricultural
    PLEASURE = "Pleasure"  # Pleasure


@dataclass
class Vehicle:
    """Vehicle information"""
    year: int
    make: str
    model: str
    vehicle_type: VehicleType
    usage: VehicleUsage
    vin: Optional[str] = None
    safety_features: list = None  # List of safety features
    
    def __post_init__(self):
        if self.safety_features is None:
            self.safety_features = []
