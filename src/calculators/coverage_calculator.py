"""
Coverage-specific premium calculation engine.
"""
from typing import Dict, Any
from ..models.coverage import Coverage, CoverageType
from ..models.vehicle import Vehicle
from ..models.driver import Driver
from ..models.coverage import PolicyInfo
from ..models.rate_table import RateTable
from ..models.factors import FactorEngine
from ..utils.rounding import apply_rounding_step, round_to_integer
from ..utils.term_calculation import calculate_term_factor, get_policy_years


class CoverageCalculator:
    """Calculator for individual coverage premiums"""
    
    def __init__(self, rate_table: RateTable, factor_engine: FactorEngine):
        self.rate_table = rate_table
        self.factor_engine = factor_engine
    
    def calculate_coverage_premium(self, coverage: Coverage, vehicle: Vehicle, 
                                 driver: Driver, policy_info: PolicyInfo) -> float:
        """
        Calculate premium for a single coverage.
        
        Args:
            coverage: Coverage configuration
            vehicle: Vehicle information
            driver: Driver information
            policy_info: Policy information
        
        Returns:
            Final premium amount (rounded to integer)
        """
        print(f"\nCalculating {coverage.type.value} premium:")
        
        # Step 1: Get base rate
        rate_date = policy_info.get_rate_date()
        driver_age = driver.get_age(rate_date)
        
        base_rate = self.rate_table.get_base_rate(
            coverage_type=coverage.type.value,
            vehicle_type=vehicle.vehicle_type.value,
            usage=vehicle.usage.value,
            driver_age=driver_age,
            rate_date=rate_date
        )
        
        print(f"  Base Rate: ${base_rate:.3f}")
        base_rate = apply_rounding_step(base_rate, "Base Rate Rounding")
        
        # Step 2: Apply factors
        context = self._build_context(coverage, vehicle, driver, policy_info)
        total_factor = self.factor_engine.calculate_total_factor(context)
        
        print(f"  Total Factor: {total_factor:.6f}")
        total_factor = apply_rounding_step(total_factor, "Total Factor Rounding")
        
        # Step 3: Calculate base premium with factors
        factored_premium = base_rate * total_factor
        print(f"  After Factors: ${base_rate:.3f} × {total_factor:.3f} = ${factored_premium:.6f}")
        factored_premium = apply_rounding_step(factored_premium, "After Factors Rounding")
        
        # Step 4: Apply term factor
        term_factor = calculate_term_factor(
            policy_info.policy_effective_date,
            policy_info.policy_expiry_date,
            rate_date
        )
        
        print(f"  Term Factor: {term_factor:.6f}")
        term_factor = apply_rounding_step(term_factor, "Term Factor Rounding")
        
        # Step 5: Final calculation
        final_premium = factored_premium * term_factor
        print(f"  Final Calculation: ${factored_premium:.3f} × {term_factor:.3f} = ${final_premium:.6f}")
        
        # Step 6: Round to integer
        final_premium_int = round_to_integer(final_premium)
        print(f"  Final Premium: ${final_premium:.6f} → ${final_premium_int}")
        
        return final_premium_int
    
    def calculate_multi_year_premium(self, coverage: Coverage, vehicle: Vehicle,
                                   driver: Driver, policy_info: PolicyInfo) -> float:
        """
        Calculate premium for multi-year policies.
        
        For multi-year policies, each year uses the rate table for that year.
        
        Args:
            coverage: Coverage configuration
            vehicle: Vehicle information
            driver: Driver information
            policy_info: Policy information
        
        Returns:
            Total premium for all years
        """
        print(f"\nCalculating multi-year {coverage.type.value} premium:")
        
        policy_years = get_policy_years(
            policy_info.policy_effective_date,
            policy_info.policy_expiry_date
        )
        
        total_premium = 0.0
        
        for year, year_start, year_end in policy_years:
            print(f"\n  Year {year} ({year_start} to {year_end}):")
            
            # Create year-specific policy info
            year_policy_info = PolicyInfo(
                policy_effective_date=year_start,
                policy_expiry_date=year_end,
                is_renewal=policy_info.is_renewal,
                renewal_date=year_start if policy_info.is_renewal else ""
            )
            
            # Calculate premium for this year
            year_premium = self.calculate_coverage_premium(
                coverage, vehicle, driver, year_policy_info
            )
            
            total_premium += year_premium
            print(f"  Year {year} Premium: ${year_premium}")
        
        print(f"\n  Multi-year Total Premium: ${total_premium}")
        return total_premium
    
    def _build_context(self, coverage: Coverage, vehicle: Vehicle, 
                      driver: Driver, policy_info: PolicyInfo) -> Dict[str, Any]:
        """Build context dictionary for factor application"""
        rate_date = policy_info.get_rate_date()
        
        # Count accidents and violations
        accident_count = len(driver.accidents) if driver.accidents else 0
        violation_count = len(driver.violations) if driver.violations else 0
        
        # Determine accident type (simplified)
        accident_type = "any" if accident_count > 0 else "none"
        if accident_count > 0:
            # Check if any accident is at-fault
            at_fault_accidents = [acc for acc in driver.accidents if acc.get('at_fault', False)]
            if at_fault_accidents:
                accident_type = "at_fault"
        
        # Determine violation type (simplified)
        violation_type = "any" if violation_count > 0 else "none"
        if violation_count > 0:
            # Check for major violations
            major_violations = [v for v in driver.violations if v.get('type') in ['dui', 'major']]
            if major_violations:
                violation_type = "major"
            else:
                violation_type = "minor"
        
        return {
            'coverage_type': coverage.type.value,
            'vehicle_type': vehicle.vehicle_type.value,
            'vehicle_usage': vehicle.usage.value,
            'driver_age': driver.get_age(rate_date),
            'safety_features': vehicle.safety_features,
            'accident_count': accident_count,
            'accident_type': accident_type,
            'violation_count': violation_count,
            'violation_type': violation_type,
            'car_count': 1,  # Default to 1 car, can be overridden
            'state': driver.license_state,
            'is_renewal': policy_info.is_renewal,
            'policy_effective_date': policy_info.policy_effective_date,
            'policy_expiry_date': policy_info.policy_expiry_date
        }
