"""
Rate table system for base premium lookup.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, date
import json


@dataclass
class RateTableEntry:
    """Individual rate table entry"""
    coverage_type: str
    vehicle_type: str
    usage: str
    age_range: str  # e.g., "25-30", "31-65", "65+"
    base_rate: float
    effective_date: str  # YYYY-MM-DD
    expiry_date: str = ""  # YYYY-MM-DD, empty means no expiry


class RateTable:
    """Rate table management system"""
    
    def __init__(self):
        self.entries: List[RateTableEntry] = []
    
    def add_entry(self, entry: RateTableEntry):
        """Add a rate table entry"""
        self.entries.append(entry)
    
    def get_base_rate(self, coverage_type: str, vehicle_type: str, 
                     usage: str, driver_age: int, rate_date: str) -> float:
        """
        Get base rate for given parameters and date.
        
        Args:
            coverage_type: Type of coverage (BI, PD, PIP, etc.)
            vehicle_type: Vehicle type (Sedan, SUV, etc.)
            usage: Vehicle usage (Commuting, Business, etc.)
            driver_age: Driver's age
            rate_date: Date to use for rate lookup (YYYY-MM-DD)
        
        Returns:
            Base rate amount
        """
        rate_dt = datetime.fromisoformat(rate_date)
        
        # Find matching entries
        matching_entries = []
        for entry in self.entries:
            entry_effective = datetime.fromisoformat(entry.effective_date)
            entry_expiry = datetime.fromisoformat(entry.expiry_date) if entry.expiry_date else None
            
            # Check date range
            if rate_dt < entry_effective:
                continue
            if entry_expiry and rate_dt > entry_expiry:
                continue
            
            # Check coverage type
            if entry.coverage_type != coverage_type:
                continue
            
            # Check vehicle type
            if entry.vehicle_type != vehicle_type:
                continue
            
            # Check usage
            if entry.usage != usage:
                continue
            
            # Check age range
            if not self._age_in_range(driver_age, entry.age_range):
                continue
            
            matching_entries.append(entry)
        
        if not matching_entries:
            raise ValueError(f"No rate found for {coverage_type}, {vehicle_type}, {usage}, age {driver_age} on {rate_date}")
        
        # Return the most recent rate (highest effective date)
        latest_entry = max(matching_entries, key=lambda x: x.effective_date)
        return latest_entry.base_rate
    
    def _age_in_range(self, age: int, age_range: str) -> bool:
        """Check if age falls within the specified range"""
        if age_range == "65+":
            return age >= 65
        
        if "-" in age_range:
            min_age, max_age = map(int, age_range.split("-"))
            return min_age <= age <= max_age
        
        # Single age
        return age == int(age_range)
    
    def load_from_file(self, file_path: str):
        """Load rate table from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for entry_data in data.get('entries', []):
            entry = RateTableEntry(**entry_data)
            self.add_entry(entry)
    
    def save_to_file(self, file_path: str):
        """Save rate table to JSON file"""
        data = {
            'entries': [
                {
                    'coverage_type': entry.coverage_type,
                    'vehicle_type': entry.vehicle_type,
                    'usage': entry.usage,
                    'age_range': entry.age_range,
                    'base_rate': entry.base_rate,
                    'effective_date': entry.effective_date,
                    'expiry_date': entry.expiry_date
                }
                for entry in self.entries
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
