# Rating Factors - CSV Configuration

This directory contains CSV files that define various insurance rating factors. The system automatically loads these files and applies the appropriate factors based on driver, vehicle, and policy characteristics.

## File Structure

### Driver Age Factors (`driver_age_factors.csv`)
- **Young Driver Surcharge**: 16-25 years old (1.5x)
- **Senior Driver Surcharge**: 65+ years old (1.2x)
- **Teen Driver Surcharge**: 16-18 years old (2.0x)
- **Experienced Driver Discount**: 30-50 years old (0.9x)
- **New Driver Surcharge**: 19-24 years old (1.3x)

### Vehicle Type Factors (`vehicle_type_factors.csv`)
- **Sedan Base Rate**: 1.0x
- **SUV Surcharge**: 1.1x
- **Truck Surcharge**: 1.2x
- **Motorcycle Surcharge**: 1.5x
- **Commercial Vehicle Surcharge**: 1.3x
- **Agricultural Vehicle Discount**: 0.8x

### Vehicle Usage Factors (`vehicle_usage_factors.csv`)
- **Commuting Base Rate**: 1.0x
- **Business Usage Surcharge**: 1.2x
- **Agricultural Usage Discount**: 0.9x
- **Pleasure Usage Discount**: 0.95x
- **Commercial Usage Surcharge**: 1.4x

### Safety Features Factors (`safety_features_factors.csv`)
- **Airbag Discount**: 0.95x (5% discount)
- **Anti-lock Brakes Discount**: 0.98x (2% discount)
- **Electronic Stability Control Discount**: 0.97x (3% discount)
- **Backup Camera Discount**: 0.99x (1% discount)
- **Lane Departure Warning Discount**: 0.96x (4% discount)
- **Automatic Emergency Braking Discount**: 0.94x (6% discount)
- **Multiple Safety Features Discount**: 0.92x (8% discount for 3+ features)

### Accident History Factors (`accident_history_factors.csv`)
- **No Accidents Discount**: 0.9x (10% discount)
- **Single At-fault Accident Surcharge**: 1.2x (20% surcharge)
- **Single Not-at-fault Accident**: 1.0x (no surcharge)
- **Multiple Accidents Surcharge**: 1.5x (50% surcharge)
- **Severe Accident Surcharge**: 1.8x (80% surcharge)
- **DUI Accident Surcharge**: 2.0x (100% surcharge)

### Violation History Factors (`violation_history_factors.csv`)
- **No Violations Discount**: 0.95x (5% discount)
- **Single Minor Violation**: 1.1x (10% surcharge)
- **Single Major Violation**: 1.3x (30% surcharge)
- **Multiple Violations**: 1.4x (40% surcharge)
- **DUI Violation**: 1.8x (80% surcharge)
- **Speeding Violation**: 1.15x (15% surcharge)

### Multi-car Factors (`multi_car_factors.csv`)
- **Single Car Base Rate**: 1.0x
- **Two Car Discount**: 0.95x (5% discount)
- **Three Car Discount**: 0.9x (10% discount)
- **Four Car Discount**: 0.85x (15% discount)
- **Five Plus Car Discount**: 0.8x (20% discount)

### Location Factors (`location_factors.csv`)
- **California Base Rate**: 1.0x
- **Texas Rate**: 0.9x (lower rate)
- **Florida Rate**: 1.1x (higher rate)
- **New York Rate**: 1.2x (higher rate)
- **Illinois Rate**: 1.05x (slightly higher)
- **Urban Area Surcharge**: 1.15x (15% surcharge)
- **Rural Area Discount**: 0.9x (10% discount)

## CSV Format

Each CSV file follows this general format:

```csv
factor_type,factor_name,condition_field,condition_value,factor_value,description
```

### Example:
```csv
DRIVER_AGE,Young Driver Surcharge,min_age,16,max_age,25,1.5,Additional charge for young drivers
```

## Usage

The system automatically loads all CSV files in this directory when the `FactorEngine` is initialized. Factors are applied based on the context provided during premium calculation.

### Context Fields:
- `driver_age`: Driver's age
- `vehicle_type`: Vehicle type (Sedan, SUV, Truck, etc.)
- `vehicle_usage`: Usage type (Commuting, Business, etc.)
- `safety_features`: List of safety features
- `accident_count`: Number of accidents
- `accident_type`: Type of accidents (at_fault, not_at_fault, etc.)
- `violation_count`: Number of violations
- `violation_type`: Type of violations (minor, major, dui, etc.)
- `car_count`: Number of cars on policy
- `state`: Driver's license state

## Modifying Factors

To modify factors, simply edit the appropriate CSV file. The system will automatically reload the factors when the `FactorEngine` is reinitialized.

### Adding New Factors:
1. Add a new row to the appropriate CSV file
2. Follow the existing format
3. Restart the application or call `reload_factors()`

### Adding New Factor Types:
1. Create a new CSV file following the naming convention: `{factor_type}_factors.csv`
2. Update the `FactorTableLoader` to handle the new factor type
3. Add the new factor type to the context building logic
