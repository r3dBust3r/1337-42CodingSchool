def check_temperature(temp_str):
    """This functions uses try/except for temperature checking"""
    print(f"\nTesting temperature: {temp_str}")
    try:
        temp = int(temp_str)
        if (temp < 0):
            print(f"Error: {temp}°C is too cold for plants (min 0°C)")
        elif (temp > 40):
            print(f"Error: {temp}°C is too hot for plants (max 40°C)")
        else:
            print(f"Temperature {temp}°C is perfect for plants!")
    except Exception:
        print(f"Error: '{temp_str}' is not a valid number")


def test_temperature_input():
    """Testing check_temperature with different values"""
    print("=== Garden Temperature Checker ===")
    check_temperature("25")
    check_temperature("abc")
    check_temperature("100")
    check_temperature("-50")
    print("\nAll tests completed - program didn't crash!")


test_temperature_input()
