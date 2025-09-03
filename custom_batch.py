#!/usr/bin/env python3
"""
Custom batch runner for Kemper Rater Prototype
Allows you to define and run multiple scenarios easily
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
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "20-24", 180.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "65+", 180.0, "2024-01-01"),
        
        # PD rates for Sedan, Commuting
        RateTableEntry("Property Damage", "Sedan", "Commuting", "20-24", 100.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "25-30", 80.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "31-65", 60.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "65+", 90.0, "2024-01-01"),
        
        # PIP rates for Sedan, Commuting
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "20-24", 150.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "25-30", 120.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "31-65", 100.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "65+", 150.0, "2024-01-01"),
        
        # Collision rates for Sedan, Commuting
        RateTableEntry("Collision", "Sedan", "Commuting", "20-24", 400.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "25-30", 350.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "31-65", 300.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "65+", 400.0, "2024-01-01"),
        
        # Comprehensive rates for Sedan, Commuting
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "20-24", 200.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "25-30", 180.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "31-65", 150.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "65+", 200.0, "2024-01-01"),
    ]
    
    for rate in rates:
        rate_table.add_entry(rate)
    
    return rate_table


def create_sample_factors():
    """Create factor engine using CSV-based factor tables"""
    factor_engine = FactorEngine(verbose=False)
    return factor_engine


def run_quick_comparison():
    """Run a quick comparison of different driver ages"""
    print("Quick Age Comparison - Same Vehicle, Different Drivers")
    print("=" * 60)
    
    # Setup
    rate_table = create_sample_rate_table()
    factor_engine = create_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Common setup
    vehicle = Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag"])
    policy_info = PolicyInfo("2024-01-01", "2025-01-01", False)
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    # Different driver ages
    drivers = [
        ("Young Driver", "2000-01-01", 24),
        ("Experienced Driver", "1989-01-01", 35),
        ("Senior Driver", "1954-01-01", 70)
    ]
    
    results = []
    for name, birth_date, age in drivers:
        driver = Driver(name, birth_date, f"LIC{age:03d}", "CA", True)
        result = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
        results.append((name, age, result['total_premium']))
    
    # Print comparison
    print(f"{'Driver Type':<20} {'Age':<5} {'Total Premium':<15}")
    print("-" * 45)
    for name, age, premium in results:
        print(f"{name:<20} {age:<5} ${premium:<14.2f}")


def run_vehicle_comparison():
    """Run a comparison of different vehicle types"""
    print("\nVehicle Type Comparison - Same Driver, Different Vehicles")
    print("=" * 60)
    
    # Setup
    rate_table = create_sample_rate_table()
    factor_engine = create_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Common setup
    driver = Driver("John Smith", "1989-01-01", "LIC001", "CA", True)  # 35 years old
    policy_info = PolicyInfo("2024-01-01", "2025-01-01", False)
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    # Different vehicles (using same rates for comparison)
    vehicles = [
        ("Sedan", VehicleType.SEDAN),
        ("SUV", VehicleType.SUV),
    ]
    
    results = []
    for vehicle_name, vehicle_type in vehicles:
        vehicle = Vehicle(2020, "Toyota", "Model", vehicle_type, VehicleUsage.COMMUTING, ["airbag"])
        result = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
        results.append((vehicle_name, result['total_premium']))
    
    # Print comparison
    print(f"{'Vehicle Type':<15} {'Total Premium':<15}")
    print("-" * 35)
    for vehicle_name, premium in results:
        print(f"{vehicle_name:<15} ${premium:<14.2f}")


def run_policy_term_comparison():
    """Run a comparison of different policy terms"""
    print("\nPolicy Term Comparison - Same Driver/Vehicle, Different Terms")
    print("=" * 60)
    
    # Setup
    rate_table = create_sample_rate_table()
    factor_engine = create_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Common setup
    driver = Driver("John Smith", "1989-01-01", "LIC001", "CA", True)  # 35 years old
    vehicle = Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag"])
    coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    # Different policy terms
    policy_terms = [
        ("6 Months", "2024-01-01", "2024-06-30"),
        ("1 Year", "2024-01-01", "2025-01-01"),
    ]
    
    results = []
    for term_name, start_date, end_date in policy_terms:
        policy_info = PolicyInfo(start_date, end_date, False)
        result = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
        results.append((term_name, result['total_premium']))
    
    # Print comparison
    print(f"{'Policy Term':<15} {'Total Premium':<15}")
    print("-" * 35)
    for term_name, premium in results:
        print(f"{term_name:<15} ${premium:<14.2f}")


def main():
    """Main function with menu"""
    print("Kemper Rater Prototype - Custom Batch Runner")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Quick Age Comparison")
        print("2. Vehicle Type Comparison") 
        print("3. Policy Term Comparison")
        print("4. Run All Comparisons")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            run_quick_comparison()
        elif choice == "2":
            run_vehicle_comparison()
        elif choice == "3":
            run_policy_term_comparison()
        elif choice == "4":
            run_quick_comparison()
            run_vehicle_comparison()
            run_policy_term_comparison()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
