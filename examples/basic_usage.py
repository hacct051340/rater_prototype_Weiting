"""
Basic usage example for Kemper Rater Prototype - Rule 2 Premium Calculation.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.coverage import Coverage, CoverageType
from models.vehicle import Vehicle, VehicleType, VehicleUsage
from models.driver import Driver
from models.policy_info import PolicyInfo
from models.rate_table import RateTable, RateTableEntry
from models.factors import FactorEngine
from calculators.premium_calculator import PremiumCalculator


def setup_sample_rate_table():
    """Setup sample rate table with basic rates"""
    rate_table = RateTable()
    
    # Add sample rates for different combinations
    sample_rates = [
        # BI rates
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "65+", 180.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "25-30", 180.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "31-65", 150.0, "2024-01-01"),
        
        # PD rates
        RateTableEntry("Property Damage", "Sedan", "Commuting", "25-30", 80.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "31-65", 60.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "65+", 90.0, "2024-01-01"),
        RateTableEntry("Property Damage", "SUV", "Commuting", "25-30", 100.0, "2024-01-01"),
        RateTableEntry("Property Damage", "SUV", "Commuting", "31-65", 80.0, "2024-01-01"),
        
        # PIP rates
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "25-30", 120.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "31-65", 100.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "65+", 150.0, "2024-01-01"),
        
        # Collision rates
        RateTableEntry("Collision", "Sedan", "Commuting", "25-30", 300.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "31-65", 250.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "65+", 350.0, "2024-01-01"),
    ]
    
    for rate in sample_rates:
        rate_table.add_entry(rate)
    
    return rate_table


def setup_sample_factors():
    """Setup factor engine using CSV-based factor tables"""
    # The FactorEngine now automatically loads factors from CSV files
    factor_engine = FactorEngine()
    return factor_engine


def example_annual_policy():
    """Example: Annual policy calculation"""
    print("Example 1: Annual Policy Calculation")
    print("-" * 40)
    
    # Setup
    rate_table = setup_sample_rate_table()
    factor_engine = setup_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Policy details
    policy_info = PolicyInfo(
        policy_effective_date="2024-01-01",
        policy_expiry_date="2024-12-31",
        is_renewal=False
    )
    
    # Vehicle
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        vehicle_type=VehicleType.SEDAN,
        usage=VehicleUsage.COMMUTING,
        safety_features=["airbag", "abs"]
    )
    
    # Driver
    driver = Driver(
        name="John Smith",
        birth_date="1990-05-15",
        license_number="A123456789",
        license_state="CA",
        is_primary=True
    )
    
    # Coverages
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True),
        Coverage(CoverageType.COLL, 0, 500, is_required=False)
    ]
    
    # Calculate
    results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
    
    return results


def example_short_term_policy():
    """Example: Short-term policy calculation"""
    print("\n\nExample 2: Short-term Policy Calculation (6 months)")
    print("-" * 40)
    
    # Setup
    rate_table = setup_sample_rate_table()
    factor_engine = setup_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Policy details (6 months)
    policy_info = PolicyInfo(
        policy_effective_date="2024-01-01",
        policy_expiry_date="2024-06-30",
        is_renewal=False
    )
    
    # Vehicle
    vehicle = Vehicle(
        year=2018,
        make="Honda",
        model="CR-V",
        vehicle_type=VehicleType.SUV,
        usage=VehicleUsage.COMMUTING,
        safety_features=["airbag"]
    )
    
    # Driver
    driver = Driver(
        name="Jane Doe",
        birth_date="1985-03-20",
        license_number="B987654321",
        license_state="CA",
        is_primary=True
    )
    
    # Coverages
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    # Calculate
    results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
    
    return results


def example_multi_year_policy():
    """Example: Multi-year policy calculation"""
    print("\n\nExample 3: Multi-year Policy Calculation (2 years)")
    print("-" * 40)
    
    # Setup
    rate_table = setup_sample_rate_table()
    factor_engine = setup_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Add 2025 rates
    rate_table.add_entry(RateTableEntry("Bodily Injury", "Sedan", "Commuting", "25-30", 160.0, "2025-01-01"))
    rate_table.add_entry(RateTableEntry("Bodily Injury", "Sedan", "Commuting", "31-65", 130.0, "2025-01-01"))
    rate_table.add_entry(RateTableEntry("Property Damage", "Sedan", "Commuting", "25-30", 85.0, "2025-01-01"))
    rate_table.add_entry(RateTableEntry("Property Damage", "Sedan", "Commuting", "31-65", 65.0, "2025-01-01"))
    
    # Policy details (2 years)
    policy_info = PolicyInfo(
        policy_effective_date="2024-01-01",
        policy_expiry_date="2025-12-31",
        is_renewal=False
    )
    
    # Vehicle
    vehicle = Vehicle(
        year=2022,
        make="Nissan",
        model="Altima",
        vehicle_type=VehicleType.SEDAN,
        usage=VehicleUsage.COMMUTING,
        safety_features=["airbag", "abs"]
    )
    
    # Driver
    driver = Driver(
        name="Bob Johnson",
        birth_date="1988-08-10",
        license_number="C456789123",
        license_state="CA",
        is_primary=True
    )
    
    # Coverages
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True)
    ]
    
    # Calculate
    results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
    
    return results


if __name__ == "__main__":
    print("Kemper Rater Prototype - Basic Premium Calculation (Rule 2)")
    print("=" * 60)
    
    # Run examples
    example_annual_policy()
    example_short_term_policy()
    example_multi_year_policy()
    
    print("\n\nCalculation Complete!")
