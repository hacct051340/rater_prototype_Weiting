"""
Test cases for premium calculation system.
"""
import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.coverage import Coverage, CoverageType
from models.vehicle import Vehicle, VehicleType, VehicleUsage
from models.driver import Driver
from models.policy_info import PolicyInfo
from models.rate_table import RateTable, RateTableEntry
from models.factors import FactorEngine, Factor, FactorType
from calculators.premium_calculator import PremiumCalculator
from utils.rounding import round_to_three_decimals, round_to_integer
from utils.term_calculation import calculate_term_factor, is_annual_policy


class TestRounding(unittest.TestCase):
    """Test rounding utilities"""
    
    def test_round_to_three_decimals(self):
        """Test rounding to 3 decimal places"""
        self.assertEqual(round_to_three_decimals(0.1245), 0.125)
        self.assertEqual(round_to_three_decimals(0.1244), 0.124)
        self.assertEqual(round_to_three_decimals(1.0), 1.0)
        self.assertEqual(round_to_three_decimals(0.9999), 1.0)
    
    def test_round_to_integer(self):
        """Test rounding to integer"""
        self.assertEqual(round_to_integer(100.499), 100)
        self.assertEqual(round_to_integer(100.500), 101)
        self.assertEqual(round_to_integer(100.0), 100)
        self.assertEqual(round_to_integer(99.999), 100)


class TestTermCalculation(unittest.TestCase):
    """Test term calculation utilities"""
    
    def test_annual_policy_detection(self):
        """Test annual policy detection"""
        self.assertTrue(is_annual_policy("2024-01-01", "2024-12-31"))
        self.assertFalse(is_annual_policy("2024-01-01", "2024-06-30"))
        self.assertFalse(is_annual_policy("2024-01-01", "2025-12-31"))
    
    def test_term_factor_calculation(self):
        """Test term factor calculation"""
        # Annual policy should have factor of 1.0
        factor = calculate_term_factor("2024-01-01", "2024-12-31")
        self.assertAlmostEqual(factor, 1.0, places=3)
        
        # 6-month policy should have factor of approximately 0.5
        factor = calculate_term_factor("2024-01-01", "2024-06-30")
        self.assertAlmostEqual(factor, 0.5, places=1)


class TestRateTable(unittest.TestCase):
    """Test rate table functionality"""
    
    def setUp(self):
        """Setup test rate table"""
        self.rate_table = RateTable()
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"
        ))
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"
        ))
    
    def test_get_base_rate(self):
        """Test base rate lookup"""
        rate = self.rate_table.get_base_rate(
            "Bodily Injury", "Sedan", "Commuting", 28, "2024-06-01"
        )
        self.assertEqual(rate, 150.0)
        
        rate = self.rate_table.get_base_rate(
            "Bodily Injury", "Sedan", "Commuting", 35, "2024-06-01"
        )
        self.assertEqual(rate, 120.0)
    
    def test_age_range_matching(self):
        """Test age range matching"""
        # Test exact age match
        self.assertTrue(self.rate_table._age_in_range(28, "25-30"))
        self.assertFalse(self.rate_table._age_in_range(35, "25-30"))
        
        # Test 65+ range
        self.assertTrue(self.rate_table._age_in_range(70, "65+"))
        self.assertFalse(self.rate_table._age_in_range(60, "65+"))


class TestFactorEngine(unittest.TestCase):
    """Test factor engine functionality"""
    
    def setUp(self):
        """Setup test factor engine"""
        self.factor_engine = FactorEngine()
        self.factor_engine.add_factor(Factor(
            FactorType.DRIVER_AGE,
            "Young Driver Surcharge",
            1.5,
            {"driver_age": {"min": 16, "max": 25}}
        ))
        self.factor_engine.add_factor(Factor(
            FactorType.VEHICLE_TYPE,
            "SUV Surcharge",
            1.1,
            {"vehicle_type": "SUV"}
        ))
    
    def test_factor_application(self):
        """Test factor application"""
        context = {
            "driver_age": 22,
            "vehicle_type": "Sedan"
        }
        
        factors = self.factor_engine.get_applicable_factors(context)
        self.assertEqual(len(factors), 1)
        self.assertEqual(factors[0].value, 1.5)
        
        context = {
            "driver_age": 30,
            "vehicle_type": "SUV"
        }
        
        factors = self.factor_engine.get_applicable_factors(context)
        self.assertEqual(len(factors), 1)
        self.assertEqual(factors[0].value, 1.1)
    
    def test_total_factor_calculation(self):
        """Test total factor calculation"""
        context = {
            "driver_age": 22,
            "vehicle_type": "SUV"
        }
        
        total_factor = self.factor_engine.calculate_total_factor(context)
        self.assertAlmostEqual(total_factor, 1.5 * 1.1, places=6)


class TestPremiumCalculation(unittest.TestCase):
    """Test premium calculation integration"""
    
    def setUp(self):
        """Setup test environment"""
        # Rate table
        self.rate_table = RateTable()
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"
        ))
        
        # Factor engine
        self.factor_engine = FactorEngine()
        self.factor_engine.add_factor(Factor(
            FactorType.DRIVER_AGE,
            "Young Driver Surcharge",
            1.2,
            {"driver_age": {"min": 16, "max": 25}}
        ))
        
        # Calculator
        self.calculator = PremiumCalculator(self.rate_table, self.factor_engine)
    
    def test_simple_premium_calculation(self):
        """Test simple premium calculation"""
        # Policy
        policy_info = PolicyInfo(
            policy_effective_date="2024-01-01",
            policy_expiry_date="2024-12-31"
        )
        
        # Vehicle
        vehicle = Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleType.SEDAN,
            usage=VehicleUsage.COMMUTING
        )
        
        # Driver
        driver = Driver(
            name="Test Driver",
            birth_date="2000-01-01",
            license_number="TEST123",
            license_state="CA",
            is_primary=True
        )
        
        # Coverage
        coverage = Coverage(CoverageType.BI, 100000)
        
        # Calculate
        premium = self.calculator.calculate_coverage_premium(
            coverage, vehicle, driver, policy_info
        )
        
        # Expected: 150.0 * 1.2 * 1.0 = 180.0 → 180
        self.assertEqual(premium, 180)
    
    def test_short_term_premium_calculation(self):
        """Test short-term premium calculation"""
        # Policy (6 months)
        policy_info = PolicyInfo(
            policy_effective_date="2024-01-01",
            policy_expiry_date="2024-06-30"
        )
        
        # Vehicle
        vehicle = Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleType.SEDAN,
            usage=VehicleUsage.COMMUTING
        )
        
        # Driver
        driver = Driver(
            name="Test Driver",
            birth_date="1990-01-01",
            license_number="TEST123",
            license_state="CA",
            is_primary=True
        )
        
        # Coverage
        coverage = Coverage(CoverageType.BI, 100000)
        
        # Calculate
        premium = self.calculator.calculate_coverage_premium(
            coverage, vehicle, driver, policy_info
        )
        
        # Expected: 150.0 * 1.0 * 0.5 = 75.0 → 75
        self.assertEqual(premium, 75)


if __name__ == "__main__":
    unittest.main()
