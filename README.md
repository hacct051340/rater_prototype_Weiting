# Kemper Rater Prototype - Basic Premium Calculation

This is a prototype insurance rating system that implements the basic premium calculation method.

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
├── src/                        # Main source code
│   ├── models/                 # Data models and business logic
│   │   ├── coverage.py         # Coverage types and definitions
│   │   ├── vehicle.py          # Vehicle models and types
│   │   ├── driver.py           # Driver information models
│   │   ├── rate_table.py       # Rate table system
│   │   ├── factors.py          # Factor engine (CSV-based)
│   │   └── factor_table_loader.py  # CSV factor loader
│   ├── calculators/            # Calculation engines
│   │   ├── coverage_calculator.py  # Individual coverage calculation
│   │   └── premium_calculator.py   # Main premium orchestrator
│   └── utils/                  # Utility functions
│       ├── rounding.py         # Rounding utilities
│       └── term_calculation.py # Term factor calculations
├── rating_factors/             # CSV-based rating factors
│   ├── driver_age_factors.csv      # Driver age adjustments
│   ├── vehicle_type_factors.csv   # Vehicle type adjustments
│   ├── vehicle_usage_factors.csv  # Usage type adjustments
│   ├── safety_features_factors.csv # Safety feature discounts
│   ├── accident_history_factors.csv # Accident history adjustments
│   ├── violation_history_factors.csv # Violation history adjustments
│   ├── multi_car_factors.csv       # Multi-car discounts
│   ├── location_factors.csv        # Geographic adjustments
│   └── README.md                   # Factor documentation
├── data/                       # Data files
│   └── sample_rates.json       # Sample rate data
├── examples/                   # Usage examples
│   └── basic_usage.py          # Comprehensive usage examples
├── tests/                      # Test suite
│   └── test_premium_calculation.py  # Unit and integration tests
├── demo.py                     # Quick demo script
├── README.md                   # This file
└── IMPLEMENTATION_SUMMARY.md   # Implementation details
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

## Rating Factors (CSV-based)

The system uses CSV files to manage all rating factors, making it easy to modify and maintain. All factors are multiplicative (multiplied together) to calculate the final premium adjustment.

### Factor Types and Descriptions

#### 1. Driver Age Factors (`driver_age_factors.csv`)
Age-based rate adjustments that reflect the risk profile of different driver age groups:

- **Young Driver Surcharge (16-25 years)**: 1.5x multiplier
  - Higher risk due to inexperience and higher accident rates
- **Teen Driver Surcharge (16-18 years)**: 2.0x multiplier
  - Highest risk group with significantly higher accident rates
- **New Driver Surcharge (19-24 years)**: 1.3x multiplier
  - Additional surcharge for drivers with limited experience
- **Experienced Driver Discount (30-50 years)**: 0.9x multiplier
  - Discount for drivers in their prime with lower risk
- **Senior Driver Surcharge (65+ years)**: 1.2x multiplier
  - Slight increase due to potential health and reaction time factors

#### 2. Vehicle Type Factors (`vehicle_type_factors.csv`)
Rate adjustments based on vehicle type and associated risk:

- **Sedan Base Rate**: 1.0x multiplier (baseline)
- **SUV Surcharge**: 1.1x multiplier
  - Higher repair costs and rollover risk
- **Truck Surcharge**: 1.2x multiplier
  - Higher damage potential and repair costs
- **Motorcycle Surcharge**: 1.5x multiplier
  - Significantly higher injury risk
- **Commercial Vehicle Surcharge**: 1.3x multiplier
  - Higher usage and exposure
- **Agricultural Vehicle Discount**: 0.8x multiplier
  - Lower usage and rural environment

#### 3. Vehicle Usage Factors (`vehicle_usage_factors.csv`)
Rate adjustments based on how the vehicle is primarily used:

- **Commuting Base Rate**: 1.0x multiplier (baseline)
- **Business Usage Surcharge**: 1.2x multiplier
  - Higher mileage and exposure
- **Agricultural Usage Discount**: 0.9x multiplier
  - Lower risk rural environment
- **Pleasure Usage Discount**: 0.95x multiplier
  - Lower usage and risk
- **Commercial Usage Surcharge**: 1.4x multiplier
  - Highest usage and exposure

#### 4. Safety Features Factors (`safety_features_factors.csv`)
Discounts for vehicles equipped with safety features that reduce risk:

- **Airbag Discount**: 0.95x multiplier (5% discount)
- **Anti-lock Brakes (ABS) Discount**: 0.98x multiplier (2% discount)
- **Electronic Stability Control (ESC) Discount**: 0.97x multiplier (3% discount)
- **Backup Camera Discount**: 0.99x multiplier (1% discount)
- **Lane Departure Warning (LDW) Discount**: 0.96x multiplier (4% discount)
- **Automatic Emergency Braking (AEB) Discount**: 0.94x multiplier (6% discount)
- **Multiple Safety Features Discount**: 0.92x multiplier (8% discount for 3+ features)

#### 5. Accident History Factors (`accident_history_factors.csv`)
Rate adjustments based on driver's accident history:

- **No Accidents Discount**: 0.9x multiplier (10% discount)
- **Single At-fault Accident Surcharge**: 1.2x multiplier (20% surcharge)
- **Single Not-at-fault Accident**: 1.0x multiplier (no surcharge)
- **Multiple Accidents Surcharge**: 1.5x multiplier (50% surcharge)
- **Severe Accident Surcharge**: 1.8x multiplier (80% surcharge)
- **DUI Accident Surcharge**: 2.0x multiplier (100% surcharge)

#### 6. Violation History Factors (`violation_history_factors.csv`)
Rate adjustments based on traffic violations:

- **No Violations Discount**: 0.95x multiplier (5% discount)
- **Single Minor Violation**: 1.1x multiplier (10% surcharge)
- **Single Major Violation**: 1.3x multiplier (30% surcharge)
- **Multiple Violations**: 1.4x multiplier (40% surcharge)
- **DUI Violation**: 1.8x multiplier (80% surcharge)
- **Speeding Violation**: 1.15x multiplier (15% surcharge)

#### 7. Multi-car Factors (`multi_car_factors.csv`)
Volume discounts for insuring multiple vehicles:

- **Single Car Base Rate**: 1.0x multiplier (baseline)
- **Two Car Discount**: 0.95x multiplier (5% discount)
- **Three Car Discount**: 0.9x multiplier (10% discount)
- **Four Car Discount**: 0.85x multiplier (15% discount)
- **Five Plus Car Discount**: 0.8x multiplier (20% discount)

#### 8. Location Factors (`location_factors.csv`)
Geographic rate adjustments based on state and region:

- **California Base Rate**: 1.0x multiplier (baseline)
- **Texas Rate**: 0.9x multiplier (lower cost of living)
- **Florida Rate**: 1.1x multiplier (higher risk factors)
- **New York Rate**: 1.2x multiplier (high density, high costs)
- **Illinois Rate**: 1.05x multiplier (slightly higher)
- **Urban Area Surcharge**: 1.15x multiplier (15% surcharge)
- **Rural Area Discount**: 0.9x multiplier (10% discount)

### Factor Application Logic

1. **Multiplicative Application**: All applicable factors are multiplied together
   - Example: Young driver (1.5) × SUV (1.1) × Airbag (0.95) = 1.5675x total factor

2. **Conditional Matching**: Factors only apply when their conditions are met
   - Age factors check driver age ranges
   - Vehicle factors check vehicle type/usage
   - Safety factors check for specific features

3. **Priority Handling**: When multiple factors of the same type could apply, the system uses the most specific match

4. **Default Behavior**: If no factors apply, the system uses a 1.0x multiplier (no adjustment)

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
