"""
Driver information for premium calculation.
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import date


@dataclass
class Driver:
    """Driver information"""
    name: str
    birth_date: str  # YYYY-MM-DD format
    license_number: str
    license_state: str
    is_primary: bool = False
    accidents: List[dict] = None  # List of accident records
    violations: List[dict] = None  # List of traffic violations
    
    def __post_init__(self):
        if self.accidents is None:
            self.accidents = []
        if self.violations is None:
            self.violations = []
    
    def get_age(self, reference_date: str = None) -> int:
        """Calculate driver age at reference date"""
        if reference_date is None:
            reference_date = date.today().strftime("%Y-%m-%d")
        
        birth = date.fromisoformat(self.birth_date)
        ref = date.fromisoformat(reference_date)
        
        age = ref.year - birth.year
        if (ref.month, ref.day) < (birth.month, birth.day):
            age -= 1
        
        return age
