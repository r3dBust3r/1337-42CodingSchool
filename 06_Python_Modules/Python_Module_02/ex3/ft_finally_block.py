def water_plants(plant_list):
    """Watering plants system with error handling"""
    print("Opening watering system")
    try:
        for p in plant_list:
            print(f"Watering {p.lower()}")

    except Exception:
        print(f"Error: Cannot water {p} - invalid plant!")

    finally:
        print("Closing watering system (cleanup)")


def test_watering_system():
    """Testing the watering plants system"""
    print("=== Garden Watering System ===\n")
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("Watering completed successfully!")

    print("\nTesting with error...")
    water_plants(["tomato", None])

    print("\nCleanup always happens, even with errors!")


test_watering_system()
