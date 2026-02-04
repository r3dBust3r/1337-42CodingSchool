def garden_operations():
    """Catching multiple errors"""
    print("\nTesting ValueError...")
    try:
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()")

    print("\nTesting ZeroDivisionError...")
    try:
        50 / 0
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero")

    print("\nTesting FileNotFoundError...")
    try:
        open("missing.txt")
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file 'missing.txt'")

    print("\nTesting KeyError...")
    try:
        {"plant": "tomato"}['missing_plant']
    except KeyError:
        print("Caught KeyError: 'missing\\_plant'")

    print("\nTesting multiple errors together...")
    try:
        open("file.txt")
    except ValueError:
        print("Caught ValueError: invalid literal for int()")
    except FileNotFoundError:
        print("Caught an error, but program continues!")


def test_error_types():
    """Testing garden_operations()"""
    print("=== Garden Error Types Demo ===")
    garden_operations()
    print("\nAll error types tested successfully!")


test_error_types()
