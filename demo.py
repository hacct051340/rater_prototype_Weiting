#!/usr/bin/env python3
"""
Demo script for Kemper Rater Prototype - Rule 2 Premium Calculation
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models.coverage import Coverage, CoverageType, PolicyInfo
from src.models.vehicle import Vehicle, VehicleType, VehicleUsage
from src.models.driver import Driver
from src.models.rate_table import RateTable, RateTableEntry
from src.models.factors import FactorEngine
from src.calculators.premium_calculator import PremiumCalculator


def create_sample_rate_table():
    """Create a sample rate table"""
    rate_table = RateTable()
    
    # Add sample rates
    rates = [
        # BI rates for Sedan, Commuting
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "65+", 180.0, "2024-01-01"),
        
        # PD rates for Sedan, Commuting
        RateTableEntry("Property Damage", "Sedan", "Commuting", "25-30", 80.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "31-65", 60.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "65+", 90.0, "2024-01-01"),
        
        # PIP rates for Sedan, Commuting
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "25-30", 120.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "31-65", 100.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "65+", 150.0, "2024-01-01"),
    ]
    
    for rate in rates:
        rate_table.add_entry(rate)
    
    return rate_table


def create_sample_factors():
    """Create factor engine using CSV-based factor tables"""
    # The FactorEngine now automatically loads factors from CSV files
    factor_engine = FactorEngine()
    return factor_engine


def main():
    """Main demo function"""
    print("Kemper Rater Prototype - Basic Premium Calculation (Rule 2)")
    print("=" * 60)
    
    # Setup
    rate_table = create_sample_rate_table()
    factor_engine = create_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Example 1: Young driver with safety features
    print("\nExample 1: Young Driver (24 years old) with Airbag")
    print("-" * 50)
    
    policy_info = PolicyInfo(
        policy_effective_date="2024-01-01",
        policy_expiry_date="2024-12-31",
        is_renewal=False
    )
    
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        vehicle_type=VehicleType.SEDAN,
        usage=VehicleUsage.COMMUTING,
        safety_features=["airbag"]
    )
    
    driver = Driver(
        name="John Smith",
        birth_date="2000-01-01",  # 24 years old
        license_number="A123456789",
        license_state="CA",
        is_primary=True
    )
    
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
    
    # Example 2: Senior driver
    print("\n\nExample 2: Senior Driver (70 years old)")
    print("-" * 50)
    
    driver2 = Driver(
        name="Jane Doe",
        birth_date="1954-01-01",  # 70 years old
        license_number="B987654321",
        license_state="CA",
        is_primary=True
    )
    
    results2 = calculator.calculate_total_premium(coverages, vehicle, [driver2], policy_info)
    
    # Example 3: Short-term policy (6 months)
    print("\n\nExample 3: Short-term Policy (6 months)")
    print("-" * 50)
    
    policy_info_short = PolicyInfo(
        policy_effective_date="2024-01-01",
        policy_expiry_date="2024-06-30",
        is_renewal=False
    )
    
    driver3 = Driver(
        name="Bob Johnson",
        birth_date="1985-01-01",  # 39 years old
        license_number="C456789123",
        license_state="CA",
        is_primary=True
    )
    
    results3 = calculator.calculate_total_premium(coverages, vehicle, [driver3], policy_info_short)
    
    print("\n\nCalculation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
