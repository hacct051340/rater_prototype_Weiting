#!/usr/bin/env python3
"""
Batch demo script for Kemper Rater Prototype - Multiple scenarios
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
    
    # Add comprehensive sample rates
    rates = [
        # BI rates for Sedan, Commuting
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "20-24", 180.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "Sedan", "Commuting", "65+", 180.0, "2024-01-01"),
        
        # BI rates for SUV, Commuting
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "20-24", 220.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "25-30", 180.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "31-65", 150.0, "2024-01-01"),
        RateTableEntry("Bodily Injury", "SUV", "Commuting", "65+", 220.0, "2024-01-01"),
        
        # PD rates for Sedan, Commuting
        RateTableEntry("Property Damage", "Sedan", "Commuting", "20-24", 100.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "25-30", 80.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "31-65", 60.0, "2024-01-01"),
        RateTableEntry("Property Damage", "Sedan", "Commuting", "65+", 90.0, "2024-01-01"),
        
        # PD rates for SUV, Commuting
        RateTableEntry("Property Damage", "SUV", "Commuting", "20-24", 120.0, "2024-01-01"),
        RateTableEntry("Property Damage", "SUV", "Commuting", "25-30", 100.0, "2024-01-01"),
        RateTableEntry("Property Damage", "SUV", "Commuting", "31-65", 80.0, "2024-01-01"),
        RateTableEntry("Property Damage", "SUV", "Commuting", "65+", 110.0, "2024-01-01"),
        
        # PIP rates for Sedan, Commuting
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "20-24", 150.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "25-30", 120.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "31-65", 100.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "Sedan", "Commuting", "65+", 150.0, "2024-01-01"),
        
        # PIP rates for SUV, Commuting
        RateTableEntry("Personal Injury Protection", "SUV", "Commuting", "20-24", 180.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "SUV", "Commuting", "25-30", 150.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "SUV", "Commuting", "31-65", 120.0, "2024-01-01"),
        RateTableEntry("Personal Injury Protection", "SUV", "Commuting", "65+", 180.0, "2024-01-01"),
        
        # Collision rates for Sedan, Commuting
        RateTableEntry("Collision", "Sedan", "Commuting", "20-24", 400.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "25-30", 350.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "31-65", 300.0, "2024-01-01"),
        RateTableEntry("Collision", "Sedan", "Commuting", "65+", 400.0, "2024-01-01"),
        
        # Collision rates for SUV, Commuting
        RateTableEntry("Collision", "SUV", "Commuting", "20-24", 500.0, "2024-01-01"),
        RateTableEntry("Collision", "SUV", "Commuting", "25-30", 450.0, "2024-01-01"),
        RateTableEntry("Collision", "SUV", "Commuting", "31-65", 400.0, "2024-01-01"),
        RateTableEntry("Collision", "SUV", "Commuting", "65+", 500.0, "2024-01-01"),
        
        # Comprehensive rates for Sedan, Commuting
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "20-24", 200.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "25-30", 180.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "31-65", 150.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "Sedan", "Commuting", "65+", 200.0, "2024-01-01"),
        
        # Comprehensive rates for SUV, Commuting
        RateTableEntry("Comprehensive", "SUV", "Commuting", "20-24", 250.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "SUV", "Commuting", "25-30", 220.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "SUV", "Commuting", "31-65", 180.0, "2024-01-01"),
        RateTableEntry("Comprehensive", "SUV", "Commuting", "65+", 250.0, "2024-01-01"),
    ]
    
    for rate in rates:
        rate_table.add_entry(rate)
    
    return rate_table


def create_sample_factors():
    """Create factor engine using CSV-based factor tables"""
    factor_engine = FactorEngine(verbose=False)
    return factor_engine


def run_scenario(scenario_name, policy_info, vehicle, driver, coverages, calculator):
    """Run a single scenario and return results"""
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"{'='*60}")
    
    results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
    
    return {
        'scenario': scenario_name,
        'total_premium': results['total_premium'],
        'coverage_breakdown': results['coverage_breakdown'],
        'driver_age': results['primary_driver']['age'],
        'vehicle_type': results['vehicle_info']['type'],
        'policy_period': f"{policy_info.policy_effective_date} to {policy_info.policy_expiry_date}"
    }


def main():
    """Main batch demo function"""
    print("Kemper Rater Prototype - Batch Premium Calculation")
    print("=" * 60)
    
    # Setup
    rate_table = create_sample_rate_table()
    factor_engine = create_sample_factors()
    calculator = PremiumCalculator(rate_table, factor_engine)
    
    # Define common coverages
    basic_coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True)
    ]
    
    full_coverages = [
        Coverage(CoverageType.BI, 100000, is_required=True),
        Coverage(CoverageType.PD, 50000, is_required=True),
        Coverage(CoverageType.PIP, 10000, is_required=True),
        Coverage(CoverageType.COLL, 0, 500, is_required=False),
        Coverage(CoverageType.COMP, 0, 500, is_required=False)
    ]
    
    # Define scenarios
    scenarios = []
    
    # Scenario 1: Young driver with sedan
    scenarios.append({
        'name': 'Young Driver (24) - Sedan - Basic Coverage',
        'policy': PolicyInfo("2024-01-01", "2025-01-01", False),
        'vehicle': Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag"]),
        'driver': Driver("John Smith", "2000-01-01", "A123456789", "CA", True),
        'coverages': basic_coverages
    })
    
    # Scenario 2: Young driver with SUV
    scenarios.append({
        'name': 'Young Driver (24) - SUV - Basic Coverage',
        'policy': PolicyInfo("2024-01-01", "2025-01-01", False),
        'vehicle': Vehicle(2020, "Honda", "CR-V", VehicleType.SUV, VehicleUsage.COMMUTING, ["airbag", "abs"]),
        'driver': Driver("John Smith", "2000-01-01", "A123456789", "CA", True),
        'coverages': basic_coverages
    })
    
    # Scenario 3: Experienced driver with sedan
    scenarios.append({
        'name': 'Experienced Driver (35) - Sedan - Basic Coverage',
        'policy': PolicyInfo("2024-01-01", "2025-01-01", False),
        'vehicle': Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag", "abs"]),
        'driver': Driver("Jane Doe", "1989-01-01", "B987654321", "CA", True),
        'coverages': basic_coverages
    })
    
    # Scenario 4: Senior driver with sedan
    scenarios.append({
        'name': 'Senior Driver (70) - Sedan - Basic Coverage',
        'policy': PolicyInfo("2024-01-01", "2025-01-01", False),
        'vehicle': Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag"]),
        'driver': Driver("Bob Johnson", "1954-01-01", "C456789123", "CA", True),
        'coverages': basic_coverages
    })
    
    # Scenario 5: Young driver with full coverage
    scenarios.append({
        'name': 'Young Driver (24) - Sedan - Full Coverage',
        'policy': PolicyInfo("2024-01-01", "2025-01-01", False),
        'vehicle': Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag", "abs"]),
        'driver': Driver("John Smith", "2000-01-01", "A123456789", "CA", True),
        'coverages': full_coverages
    })
    
    # Scenario 6: Short-term policy
    scenarios.append({
        'name': 'Experienced Driver (35) - Sedan - 6 Month Policy',
        'policy': PolicyInfo("2024-01-01", "2024-06-30", False),
        'vehicle': Vehicle(2020, "Toyota", "Camry", VehicleType.SEDAN, VehicleUsage.COMMUTING, ["airbag"]),
        'driver': Driver("Jane Doe", "1989-01-01", "B987654321", "CA", True),
        'coverages': basic_coverages
    })
    
    # Run all scenarios
    results = []
    for scenario in scenarios:
        result = run_scenario(
            scenario['name'],
            scenario['policy'],
            scenario['vehicle'],
            scenario['driver'],
            scenario['coverages'],
            calculator
        )
        results.append(result)
    
    # Print summary
    print(f"\n{'='*80}")
    print("BATCH CALCULATION SUMMARY")
    print(f"{'='*80}")
    print(f"{'Scenario':<50} {'Total Premium':<15} {'Driver Age':<10}")
    print(f"{'-'*80}")
    
    for result in results:
        print(f"{result['scenario']:<50} ${result['total_premium']:<14.0f} {result['driver_age']:<10}")
    
    print(f"\n{'='*80}")
    print("DETAILED BREAKDOWN")
    print(f"{'='*80}")
    
    for result in results:
        print(f"\n{result['scenario']}:")
        print(f"  Policy Period: {result['policy_period']}")
        print(f"  Vehicle: {result['vehicle_type']}")
        print(f"  Driver Age: {result['driver_age']}")
        print(f"  Total Premium: ${result['total_premium']:.2f}")
        print("  Coverage Breakdown:")
        for coverage_type, details in result['coverage_breakdown'].items():
            print(f"    {coverage_type}: ${details['premium']:.2f}")
    
    print(f"\n{'='*80}")
    print("BATCH CALCULATION COMPLETE!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
