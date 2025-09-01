"""
Factor table loader for CSV-based factor lookup.
"""
import csv
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class FactorType(Enum):
    """Types of factors that can be applied"""
    DRIVER_AGE = "DRIVER_AGE"
    VEHICLE_TYPE = "VEHICLE_TYPE"
    VEHICLE_USAGE = "VEHICLE_USAGE"
    MULTI_CAR = "MULTI_CAR"
    SAFETY_FEATURES = "SAFETY_FEATURES"
    ACCIDENT_HISTORY = "ACCIDENT_HISTORY"
    VIOLATION_HISTORY = "VIOLATION_HISTORY"
    LOCATION = "LOCATION"
    CREDIT_SCORE = "CREDIT_SCORE"


@dataclass
class FactorRecord:
    """Individual factor record from CSV"""
    factor_type: str
    factor_name: str
    factor_value: float
    description: str
    conditions: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = {}


class FactorTableLoader:
    """Loader for CSV-based factor tables"""
    
    def __init__(self, factors_dir: str = "rating_factors"):
        self.factors_dir = factors_dir
        self.factor_tables: Dict[str, List[FactorRecord]] = {}
        self._load_all_tables()
    
    def _load_all_tables(self):
        """Load all CSV factor tables"""
        if not os.path.exists(self.factors_dir):
            print(f"Warning: Factors directory {self.factors_dir} not found")
            return
        
        csv_files = [f for f in os.listdir(self.factors_dir) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            table_name = csv_file.replace('.csv', '')
            self._load_table(table_name, os.path.join(self.factors_dir, csv_file))
    
    def _load_table(self, table_name: str, file_path: str):
        """Load a single CSV table"""
        try:
            factors = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    factor = self._parse_factor_row(row)
                    if factor:
                        factors.append(factor)
            
            self.factor_tables[table_name] = factors
            print(f"Loaded {len(factors)} factors from {table_name}")
            
        except Exception as e:
            print(f"Error loading table {table_name}: {e}")
    
    def _parse_factor_row(self, row: Dict[str, str]) -> Optional[FactorRecord]:
        """Parse a single CSV row into a FactorRecord"""
        try:
            # Extract basic fields
            factor_type = row.get('factor_type', '')
            factor_name = row.get('factor_name', '')
            factor_value = float(row.get('factor_value', '1.0'))
            description = row.get('description', '')
            
            # Extract conditions based on factor type
            conditions = {}
            
            if factor_type == 'DRIVER_AGE':
                if 'min_age' in row and row['min_age']:
                    conditions['min_age'] = int(row['min_age'])
                if 'max_age' in row and row['max_age']:
                    conditions['max_age'] = int(row['max_age'])
            
            elif factor_type == 'VEHICLE_TYPE':
                if 'vehicle_type' in row and row['vehicle_type']:
                    conditions['vehicle_type'] = row['vehicle_type']
            
            elif factor_type == 'VEHICLE_USAGE':
                if 'vehicle_usage' in row and row['vehicle_usage']:
                    conditions['vehicle_usage'] = row['vehicle_usage']
            
            elif factor_type == 'SAFETY_FEATURES':
                if 'safety_feature' in row and row['safety_feature']:
                    conditions['safety_feature'] = row['safety_feature']
            
            elif factor_type == 'ACCIDENT_HISTORY':
                if 'accident_count' in row and row['accident_count']:
                    conditions['accident_count'] = int(row['accident_count'])
                if 'accident_type' in row and row['accident_type']:
                    conditions['accident_type'] = row['accident_type']
            
            elif factor_type == 'VIOLATION_HISTORY':
                if 'violation_count' in row and row['violation_count']:
                    conditions['violation_count'] = int(row['violation_count'])
                if 'violation_type' in row and row['violation_type']:
                    conditions['violation_type'] = row['violation_type']
            
            elif factor_type == 'MULTI_CAR':
                if 'car_count' in row and row['car_count']:
                    conditions['car_count'] = int(row['car_count'])
            
            elif factor_type == 'LOCATION':
                if 'state' in row and row['state']:
                    conditions['state'] = row['state']
                if 'region' in row and row['region']:
                    conditions['region'] = row['region']
            
            return FactorRecord(
                factor_type=factor_type,
                factor_name=factor_name,
                factor_value=factor_value,
                description=description,
                conditions=conditions
            )
            
        except Exception as e:
            print(f"Error parsing factor row: {e}")
            return None
    
    def get_applicable_factors(self, context: Dict[str, Any]) -> List[FactorRecord]:
        """Get all factors that apply to the given context"""
        applicable_factors = []
        
        for table_name, factors in self.factor_tables.items():
            for factor in factors:
                if self._factor_applies(factor, context):
                    applicable_factors.append(factor)
        
        return applicable_factors
    
    def _factor_applies(self, factor: FactorRecord, context: Dict[str, Any]) -> bool:
        """Check if a factor applies to the given context"""
        if not factor.conditions:
            return True
        
        for condition_key, condition_value in factor.conditions.items():
            context_value = context.get(condition_key)
            
            if context_value is None:
                return False
            
            # Handle different condition types
            if isinstance(condition_value, (int, float)):
                if isinstance(context_value, (int, float)):
                    # Range conditions for age, counts, etc.
                    if condition_key in ['min_age', 'min_count']:
                        if context_value < condition_value:
                            return False
                    elif condition_key in ['max_age', 'max_count']:
                        if context_value > condition_value:
                            return False
                    elif condition_key in ['accident_count', 'violation_count', 'car_count']:
                        if context_value != condition_value:
                            return False
                else:
                    return False
            else:
                # String matching
                if context_value != condition_value:
                    return False
        
        return True
    
    def calculate_total_factor(self, context: Dict[str, Any]) -> float:
        """Calculate total factor by multiplying all applicable factors"""
        applicable_factors = self.get_applicable_factors(context)
        
        if not applicable_factors:
            return 1.0
        
        total_factor = 1.0
        for factor in applicable_factors:
            total_factor *= factor.factor_value
            print(f"  Applied {factor.factor_name}: {factor.factor_value} ({factor.description})")
        
        return total_factor
    
    def get_factor_summary(self) -> Dict[str, int]:
        """Get summary of loaded factors by type"""
        summary = {}
        for table_name, factors in self.factor_tables.items():
            summary[table_name] = len(factors)
        return summary
