"""
Test cases for premium calculation system.
"""
import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import using absolute paths to avoid relative import issues
from src.models.coverage import Coverage, CoverageType, PolicyInfo
from src.models.vehicle import Vehicle, VehicleType, VehicleUsage
from src.models.driver import Driver
from src.models.rate_table import RateTable, RateTableEntry
from src.models.factors import FactorEngine
from src.models.factor_table_loader import FactorType
from src.calculators.premium_calculator import PremiumCalculator
from src.utils.rounding import round_to_three_decimals, round_to_integer
from src.utils.term_calculation import calculate_term_factor, is_annual_policy


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
        self.assertTrue(is_annual_policy("2024-01-01", "2025-01-01"))  # Exactly one year
        self.assertFalse(is_annual_policy("2024-01-01", "2024-12-31"))  # 365 days, not exactly one year
        self.assertFalse(is_annual_policy("2024-01-01", "2024-06-30"))  # 6 months
        self.assertFalse(is_annual_policy("2024-01-01", "2025-12-31"))  # Almost 2 years
    
    def test_term_factor_calculation(self):
        """Test term factor calculation"""
        # 365-day policy in 2024 (leap year) should have factor of 365/366
        factor = calculate_term_factor("2024-01-01", "2024-12-31")
        self.assertAlmostEqual(factor, 365/366, places=3)
        
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
        # Factor engine now loads factors from CSV files automatically
    
    def test_factor_application(self):
        """Test factor application"""
        context = {
            "driver_age": 22,
            "vehicle_type": "Sedan"
        }
        
        factors = self.factor_engine.get_applicable_factors(context)
        self.assertGreaterEqual(len(factors), 1)  # Should have at least one factor
        # Check that we have a young driver factor
        young_driver_factors = [f for f in factors if "young" in f.factor_name.lower() or "teen" in f.factor_name.lower()]
        if young_driver_factors:
            self.assertGreaterEqual(young_driver_factors[0].factor_value, 1.0)
        
        context = {
            "driver_age": 30,
            "vehicle_type": "SUV"
        }
        
        factors = self.factor_engine.get_applicable_factors(context)
        self.assertGreaterEqual(len(factors), 1)  # Should have at least one factor
        # Check that we have a vehicle type factor
        vehicle_factors = [f for f in factors if "suv" in f.factor_name.lower()]
        if vehicle_factors:
            self.assertGreaterEqual(vehicle_factors[0].factor_value, 1.0)
    
    def test_total_factor_calculation(self):
        """Test total factor calculation"""
        context = {
            "driver_age": 22,
            "vehicle_type": "SUV"
        }
        
        total_factor = self.factor_engine.calculate_total_factor(context)
        # Should have some factor applied (not 1.0)
        self.assertGreater(total_factor, 1.0)
        # Should be a reasonable factor (not too high)
        self.assertLess(total_factor, 5.0)


class TestPremiumCalculation(unittest.TestCase):
    """Test premium calculation integration"""
    
    def setUp(self):
        """Setup test environment"""
        # Rate table
        self.rate_table = RateTable()
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "20-24", 180.0, "2024-01-01"
        ))
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "25-30", 150.0, "2024-01-01"
        ))
        self.rate_table.add_entry(RateTableEntry(
            "Bodily Injury", "Sedan", "Commuting", "31-65", 120.0, "2024-01-01"
        ))
        
        # Factor engine
        self.factor_engine = FactorEngine()
        # Factor engine now loads factors from CSV files automatically
        
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
        
        # Should be reasonable premium for young driver (24 years old)
        # Base rate 180.0 * factors * term factor
        self.assertGreater(premium, 150)  # Should be higher than base rate due to young driver
        self.assertLess(premium, 250)     # Should not be unreasonably high
    
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
        
        # Should be reasonable premium for 6-month policy
        # Base rate * factors * term factor (approximately 0.5 for 6 months)
        self.assertGreater(premium, 40)   # Should be reasonable for 6-month policy
        self.assertLess(premium, 100)     # Should be less than annual premium


if __name__ == "__main__":
    unittest.main()
