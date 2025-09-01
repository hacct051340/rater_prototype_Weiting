"""
Main premium calculation orchestrator implementing Rule 2.
"""
from typing import List, Dict, Any
from ..models.coverage import Coverage, CoverageType
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..models.coverage import PolicyInfo
from ..models.rate_table import RateTable
from ..models.factors import FactorEngine
from .coverage_calculator import CoverageCalculator
from ..utils.term_calculation import is_annual_policy


class PremiumCalculator:
    """
    Main premium calculator implementing Rule 2 calculation method.
    
    Formula: Premium = BaseRate × ∏Factors × TermFactor
    """
    
    def __init__(self, rate_table: RateTable, factor_engine: FactorEngine):
        self.rate_table = rate_table
        self.factor_engine = factor_engine
        self.coverage_calculator = CoverageCalculator(rate_table, factor_engine)
    
    def calculate_total_premium(self, coverages: List[Coverage], vehicle: Vehicle,
                              drivers: List[Driver], policy_info: PolicyInfo) -> Dict[str, Any]:
        """
        Calculate total premium for all coverages.
        
        Args:
            coverages: List of coverage configurations
            vehicle: Vehicle information
            drivers: List of drivers (primary driver is used for calculation)
            policy_info: Policy information
        
        Returns:
            Dictionary containing detailed calculation results
        """
        print("=" * 60)
        print("Basic Premium Calculation (Rule 2)")
        print("=" * 60)
        
        # Find primary driver
        primary_driver = next((d for d in drivers if d.is_primary), drivers[0])
        print(f"Primary Driver: {primary_driver.name} (Age: {primary_driver.get_age(policy_info.get_rate_date())})")
        print(f"Vehicle: {vehicle.year} {vehicle.make} {vehicle.model} ({vehicle.vehicle_type.value})")
        print(f"Usage: {vehicle.usage.value}")
        print(f"Policy Period: {policy_info.policy_effective_date} to {policy_info.policy_expiry_date}")
        
        # Check if multi-year policy
        is_multi_year = not is_annual_policy(
            policy_info.policy_effective_date,
            policy_info.policy_expiry_date
        )
        
        if is_multi_year:
            print("Note: Multi-year policy, using rate table for each corresponding year")
        
        # Calculate each coverage
        coverage_results = {}
        total_premium = 0.0
        
        for coverage in coverages:
            if is_multi_year:
                premium = self.coverage_calculator.calculate_multi_year_premium(
                    coverage, vehicle, primary_driver, policy_info
                )
            else:
                premium = self.coverage_calculator.calculate_coverage_premium(
                    coverage, vehicle, primary_driver, policy_info
                )
            
            coverage_results[coverage.type.value] = {
                'premium': premium,
                'limit': coverage.limit,
                'deductible': coverage.deductible,
                'is_required': coverage.is_required
            }
            
            total_premium += premium
        
        # Prepare results
        results = {
            'total_premium': total_premium,
            'coverage_breakdown': coverage_results,
            'calculation_method': 'Rule 2 - Basic Premium Calculation',
            'policy_info': {
                'effective_date': policy_info.policy_effective_date,
                'expiry_date': policy_info.policy_expiry_date,
                'is_renewal': policy_info.is_renewal,
                'is_multi_year': is_multi_year
            },
            'vehicle_info': {
                'year': vehicle.year,
                'make': vehicle.make,
                'model': vehicle.model,
                'type': vehicle.vehicle_type.value,
                'usage': vehicle.usage.value
            },
            'primary_driver': {
                'name': primary_driver.name,
                'age': primary_driver.get_age(policy_info.get_rate_date())
            }
        }
        
        print("\n" + "=" * 60)
        print("Calculation Results Summary")
        print("=" * 60)
        
        for coverage_type, details in coverage_results.items():
            print(f"{coverage_type}: ${details['premium']}")
        
        print(f"\nTotal Premium: ${total_premium}")
        print("=" * 60)
        
        return results
    
    def calculate_coverage_premium(self, coverage: Coverage, vehicle: Vehicle,
                                 driver: Driver, policy_info: PolicyInfo) -> float:
        """
        Calculate premium for a single coverage (convenience method).
        
        Args:
            coverage: Coverage configuration
            vehicle: Vehicle information
            driver: Driver information
            policy_info: Policy information
        
        Returns:
            Premium amount
        """
        return self.coverage_calculator.calculate_coverage_premium(
            coverage, vehicle, driver, policy_info
        )
