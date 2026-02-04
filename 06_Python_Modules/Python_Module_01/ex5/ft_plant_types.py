class Plant:
    """
    The class `Plant` has attributes for name, height, and age,
    initialized through its constructor.
    """
    def __init__(self, name, height, age):
        """
        This function is a constructor that initializes instances with
        attributes for name, height, and age.
        """
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    """
    The class `Flower` is a child class of `Plant` with additional attribute
    `color` in its constructor.
    """
    def __init__(self, name, height, age, color):
        """
        This function initializes an object with attributes for
        name, height, age, and color.
        """
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        """
        This function prints a message indicating that a
        flower is blooming beautifully.
        """
        print(f"{self.name.capitalize()} is blooming beautifully!")


class Tree(Plant):
    """
    The `Tree` class represents a type of plant with additional
    attributes for trunk diameter and a method to produce shade.
    """
    def __init__(self, name, height, age, trunk_diameter):
        """
        This function initializes an object with attributes
        for name, height, age, and trunk diameter.
        """
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self, shade_space):
        """
        This function outputs the amount of shade provided by
        a specific object in square meters.
        """
        print(f"{self.name} provides {shade_space} square meters of shade")


class Vegetable(Plant):
    """
    This class defines a Vegetable that inherits from Plant and includes
    attributes such as name height, age, harvest season,
    and nutritional value.
    """
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        """
        This function initializes attributes for a plant object
        including name, height, age, harvest season,
        and nutritional value.
        """
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value


print("=== Garden Plant Types ===")
print("")
f1 = Flower("Rose", 25, 30, "red")
print(f"{f1.name} (Flower): {f1.height}cm, {f1.age} days, {f1.color} color")
f1.bloom()

f2 = Flower("Lotus", 15, 40, "pink")
print(f"{f2.name} (Flower): {f2.height}cm, {f2.age} days, {f2.color} color")
f2.bloom()

print("")
t1 = Tree("Oak", 500, 1825, 50)
t1_td = t1.trunk_diameter
print(f"{t1.name} (Tree): {t1.height}cm, {t1.age} days, {t1_td}cm diameter")
t1.produce_shade(78)

t2 = Tree("Pine", 620, 925, 29)
t2_td = t2.trunk_diameter
print(f"{t2.name} (Tree): {t2.height}cm, {t2.age} days, {t2_td}cm diameter")
t2.produce_shade(42)

print("")
v1 = Vegetable("Tomato", 80, 90, "summer", "Tomato is rich in vitamin C")
v1_hv = v1.harvest_season
print(f"{v1.name} (Vegetable): {v1.height}cm, {v1.age} days, {v1_hv} harvest")
print(f"{v1.nutritional_value}")

v2 = Vegetable("Carrot", 30, 67, "summer", "Carrot is rich in vitamin A")
v2_hv = v2.harvest_season
print(f"{v2.name} (Vegetable): {v2.height}cm, {v2.age} days, {v2_hv} harvest")
print(f"{v2.nutritional_value}")
