# Kemper Rater Prototype - Basic Premium Calculation (Rule 2)

This is a prototype insurance rating system that implements the basic premium calculation method (Rule 2).

## Calculation Formula

```
Premium = BaseRate × ∏Factors × TermFactor
```

## Calculation Steps

1. **Find Base Rate (Base Premium / Rate Table)**
   - Use the rate table for the policy effective date (new policy) or renewal date (renewal policy)
   - For policies longer than one year, use the rate for the start date in the first year, then use the rate table for each corresponding year

2. **Calculate Each Coverage Item Separately**
   - Insurance is typically divided into liability (BI, PD), PIP, UM/UIM, physical damage (Coll, Comp), etc.
   - Each coverage must be calculated separately

3. **Apply Various Factors (Factors/Multipliers)**
   - Examples: driver age, vehicle type, usage (commuting/business/agricultural), multi-car discount, safety device discount
   - Factors are multiplied, not added
   - ✅ Correct: Base × Factor1 × Factor2 × Factor3 …
   - ❌ Wrong: Base × (Factor1 + Factor2)

4. **Step-by-step Rounding (Three Decimal Places)**
   - Each intermediate calculation result should be rounded to three decimal places
   - Example: 0.1245 → 0.125

5. **Pro-rata Term Factor Adjustment**
   - If not a full year (e.g., six-month policy), adjust proportionally

6. **Final Amount Rounded to Integer**
   - The result of each coverage calculation should be rounded to the nearest dollar
   - Example: 100.499 → $100; 100.500 → $101

## Project Structure

```
kemper-rater-prototype/
├── src/
│   ├── models/           # Data models
│   │   ├── coverage.py   # Coverage definitions
│   │   ├── vehicle.py    # Vehicle information
│   │   ├── driver.py     # Driver information
│   │   ├── policy_info.py # Policy information
│   │   ├── rate_table.py # Rate table system
│   │   └── factors.py    # Factor system
│   ├── calculators/      # Calculation engines
│   │   ├── coverage_calculator.py # Individual coverage calculation
│   │   └── premium_calculator.py  # Main calculation orchestrator
│   └── utils/           # Utility functions
│       ├── rounding.py  # Rounding utilities
│       └── term_calculation.py # Term calculation utilities
├── examples/            # Usage examples
│   └── basic_usage.py   # Basic usage example
├── tests/              # Test cases
│   └── test_premium_calculation.py
└── data/               # Sample data
    └── sample_rates.json
```

## Usage

### Basic Usage

```python
from src.calculators.premium_calculator import PremiumCalculator
from src.models.coverage import Coverage, CoverageType
from src.models.vehicle import Vehicle, VehicleType, VehicleUsage
from src.models.driver import Driver
from src.models.policy_info import PolicyInfo

# Create calculator
calculator = PremiumCalculator(rate_table, factor_engine)

# Set policy information
policy_info = PolicyInfo(
    policy_effective_date="2024-01-01",
    policy_expiry_date="2024-12-31",
    is_renewal=False
)

# Set vehicle
vehicle = Vehicle(
    year=2020,
    make="Toyota",
    model="Camry",
    vehicle_type=VehicleType.SEDAN,
    usage=VehicleUsage.COMMUTING
)

# Set driver
driver = Driver(
    name="John Smith",
    birth_date="1990-05-15",
    license_number="A123456789",
    license_state="CA",
    is_primary=True
)

# Set coverages
coverages = [
    Coverage(CoverageType.BI, 100000, is_required=True),
    Coverage(CoverageType.PD, 50000, is_required=True),
    Coverage(CoverageType.PIP, 10000, is_required=True)
]

# Calculate premium
results = calculator.calculate_total_premium(coverages, vehicle, [driver], policy_info)
```

### Run Examples

```bash
python examples/basic_usage.py
```

### Run Tests

```bash
python -m pytest tests/
```

## Supported Coverage Types

- **BI (Bodily Injury)**: Bodily Injury Liability
- **PD (Property Damage)**: Property Damage Liability
- **PIP (Personal Injury Protection)**: Personal Injury Protection
- **UM (Uninsured Motorist)**: Uninsured Motorist
- **UIM (Underinsured Motorist)**: Underinsured Motorist
- **COLL (Collision)**: Collision Coverage
- **COMP (Comprehensive)**: Comprehensive Coverage

## Supported Factor Types (CSV-based)

The system now uses CSV files to manage all rating factors, making it easy to modify and maintain:

- **Driver Age Factors**: Young driver surcharge, senior driver surcharge, teen driver surcharge
- **Vehicle Type Factors**: Rate adjustments for different vehicle types (Sedan, SUV, Truck, etc.)
- **Usage Factors**: Different usage types such as commuting, business, agricultural
- **Safety Device Discounts**: Airbag, ABS, ESC, backup camera, LDW, AEB discounts
- **Multi-car Discounts**: Discounts for multiple vehicles (2-5+ cars)
- **Accident History Factors**: Rate adjustments based on accident history and type
- **Violation History Factors**: Rate adjustments based on traffic violations
- **Location Factors**: State and regional rate adjustments

### Factor Configuration
All factors are stored in CSV files in the `rating_factors/` directory:
- `driver_age_factors.csv`
- `vehicle_type_factors.csv`
- `vehicle_usage_factors.csv`
- `safety_features_factors.csv`
- `accident_history_factors.csv`
- `violation_history_factors.csv`
- `multi_car_factors.csv`
- `location_factors.csv`

## Key Features

1. **Date-based Rate Tables**: Support for different date rate tables, suitable for multi-year policies
2. **CSV-based Factor Management**: Easy-to-modify factor tables stored in CSV files
3. **Precise Rounding**: Intermediate calculations rounded to three decimal places, final results rounded to integers
4. **Pro-rata Term Adjustment**: Support for non-annual policy term proportion calculations
5. **Factor Multiplication**: Correctly implements factor multiplication, not addition
6. **Detailed Calculation Process**: Provides complete calculation process output for easy verification and debugging
7. **Flexible Factor Configuration**: Add, modify, or remove factors by editing CSV files

## Notes

- All date formats use YYYY-MM-DD
- Age calculation is based on policy effective date or renewal date
- Factor conditions support range matching and list matching
- Supports multi-year policies, using rate table for each corresponding year
