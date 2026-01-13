def check_plant_health(plant_name, water_level, sunlight_hours):
    """Checking plant health with error handling"""
    plant_name = plant_name.strip()

    try:
        if (plant_name == ""):
            raise ValueError("Error: Plant name cannot be empty!")
    except ValueError:
        return "Error: Plant name cannot be empty!"

    try:
        if (water_level < 0):
            raise ValueError(
                f"Error: Water level {water_level} is too low (min 0)")
    except ValueError as e:
        return e

    try:
        if (water_level > 10):
            raise ValueError(
                f"Error: Water level {water_level} is too high (max 10)")
    except ValueError as e:
        return e

    try:
        if (sunlight_hours < 2):
            raise ValueError(
                f"Error: Sunlight hours {sunlight_hours} is too low (min 2)")
    except ValueError as e:
        return e

    try:
        if (sunlight_hours > 12):
            raise ValueError(
                f"Error: Sunlight hours {sunlight_hours} is too high (max 12)")
    except ValueError as e:
        return e

    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks():
    """Testing check_plant_health()"""
    print("=== Garden Plant Health Checker ===")

    print("\nTesting good values...")
    print(check_plant_health("tomato", 5, 5))

    print("\nTesting empty plant name...")
    print(check_plant_health("", 5, 5))

    print("\nTesting bad water level...")
    print(check_plant_health("rose", 15, 5))

    print("\nTesting bad sunlight hours...")
    print(check_plant_health("rose", 5, 0))

    print("\nAll error raising tests completed!")


test_plant_checks()
