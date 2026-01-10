class Plant:
    """
    The class `Plant` represents a plant with attributes
    for name, height, and age, along with methods
    to get information and simulate growth.
    """
    def __init__(self, name, height, age):
        """
        Define a class constructor that initializes instances
        with attributes for name, height, and age.
        """
        self.name = name
        self.height = height
        self.age = age

    def age(self):
        """
        The function `age()` is intended to return the age attribute
        of the object it is called on.
        """
        return self.age

    def grow(self, n):
        """
        The `grow` function increases both the height and age attributes
        of an object by 6.
        """
        self.height += n
        self.age += n

    def get_info(self):
        """
        The `get_info` function prints the name, height, and age in
        days of an object.
        """
        print(f"{self.name}: {self.height}cm, {self.age} days old")


plant = Plant("Rose", 25, 30)
print("=== Day 1 ===")
plant.get_info()
six_days = 6
plant.grow(six_days)
print("=== Day 7 ===")
plant.get_info()
print(f"Growth this week: +{six_days}cm")
