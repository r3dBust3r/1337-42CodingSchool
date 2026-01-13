class GardenError(Exception):
    """Base class for garden related errors."""
    pass


class PlantError(GardenError):
    """Error for plant problems."""
    pass


class WaterError(GardenError):
    """Error for watering problems."""
    pass


def check_plant():
    """Triggering PlantError"""
    raise PlantError("The tomato plant is wilting!")


def check_water():
    """Triggering WaterError"""
    raise WaterError("Not enough water in the tank!")


print("=== Custom Garden Errors Demo ===")

print("\nTesting PlantError...")
try:
    check_plant()
except PlantError as e:
    print(f"Caught PlantError: {e}")

print("\nTesting WaterError...")
try:
    check_water()
except WaterError as e:
    print(f"Caught WaterError: {e}")

print("\nTesting catching all garden errors...")
try:
    check_plant()
except GardenError as e:
    print(f"Caught a garden error: {e}")

try:
    check_water()
except GardenError as e:
    print(f"Caught a garden error: {e}")

print("\nAll custom error types work correctly!")
