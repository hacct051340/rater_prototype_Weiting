"""
Factor/multiplier system for premium calculation using CSV lookup.
"""
from typing import Dict, List, Any
from .factor_table_loader import FactorTableLoader


class FactorEngine:
    """Engine for applying factors to premium calculations using CSV lookup"""
    
    def __init__(self, factors_dir: str = "rating_factors"):
        """
        Initialize factor engine with CSV-based factor tables.
        
        Args:
            factors_dir: Directory containing CSV factor files
        """
        self.factor_loader = FactorTableLoader(factors_dir)
        self._print_loaded_factors()
    
    def _print_loaded_factors(self):
        """Print summary of loaded factors"""
        summary = self.factor_loader.get_factor_summary()
        print("Loaded Factor Tables:")
        for table_name, count in summary.items():
            print(f"  {table_name}: {count} factors")
    
    def get_applicable_factors(self, context: Dict[str, Any]) -> List[Any]:
        """
        Get all factors that apply to the given context.
        
        Args:
            context: Dictionary containing driver, vehicle, policy info
        
        Returns:
            List of applicable factor records
        """
        return self.factor_loader.get_applicable_factors(context)
    
    def calculate_total_factor(self, context: Dict[str, Any]) -> float:
        """
        Calculate total factor by multiplying all applicable factors.
        
        Args:
            context: Dictionary containing driver, vehicle, policy info
        
        Returns:
            Total factor value
        """
        return self.factor_loader.calculate_total_factor(context)
    
    def add_factor(self, factor: Any):
        """
        Legacy method for backward compatibility.
        Note: This method is deprecated. Use CSV files to manage factors.
        """
        print("Warning: add_factor() is deprecated. Use CSV files to manage factors.")
    
    def reload_factors(self):
        """Reload all factor tables from CSV files"""
        self.factor_loader = FactorTableLoader(self.factor_loader.factors_dir)
        self._print_loaded_factors()
