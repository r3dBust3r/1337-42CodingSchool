class GardenManager:
    """
    The `GardenManager` class manages gardens, tracks plant types
    and growth, and provides methods for adding plants, helping plants
    grow, generating reports, and performing height validation tests.
    """
    total_gardens = 0

    def __init__(self, manager):
        """
        This function initializes a Garden object with a manager,
        plant lists, and counters for different types of plants.
        """
        GardenManager.total_gardens += 1
        self.manager = manager.capitalize()
        self.plants = []
        self.all_plants_counter = 0
        self.regular_plants = 0
        self.flowering_plants = 0
        self.prize_flowers_plants = 0
        self.unknown_plants = 0
        self.plants_growth = 0

    def add_plant(self, plant):
        """
        This function adds a plant to a garden, updates plant counters based
        on plant kind, and prints a message indicating the plant addition.
        """
        self.plants.append(plant)
        self.all_plants_counter += 1
        if (plant.kind == "regular"):
            self.regular_plants += 1
        elif (plant.kind == "flowering"):
            self.flowering_plants += 1
        elif (plant.kind == "prize flowers"):
            self.prize_flowers_plants += 1
        else:
            self.unknown_plants += 1
        print(f"Added {plant.name} to {self.manager}'s garden")

    def help_growth(self):
        """
        This function helps all plants grow by a specified height and
        updates the growth progress for each plant.
        """
        print("")
        print(f"{self.manager} is helping all plants grow...")
        grew_height = 1
        for p in self.plants:
            p.grow(grew_height)
            self.plants_growth += 1
            print(f"{p.name} grew {grew_height}cm")

    def report(self):
        """
        This function prints a summary of the plants in the garden managed
        by a specific person.
        """
        print("")
        print(f"=== {self.manager}'s Garden Report ===")
        print("Plants in garden:")
        for p in self.plants:
            print(f"- {p.get_details()}")

        print("")
        all_plc = self.all_plants_counter
        all_plg = self.plants_growth
        r = self.regular_plants
        fp = self.flowering_plants
        pf = self.prize_flowers_plants
        print(f"Plants added: {all_plc}, Total growth: {all_plg}cm")
        print(f"Plant types: {r} regular, {fp} flowering, {pf} prize flowers")

    @classmethod
    def create_garden_network(cls):
        """
        This function is a class method that prints the total number of
        gardens managed by the class.
        """
        print(f"Total gardens managed: {cls.total_gardens}")

    @staticmethod
    def high_validation_test(height):
        """
        This function is a high validation test, if a given height is greater
        than 0 and returns True, otherwise returns False.
        """
        if (height > 0):
            return True
        return False

    class GardenStats():
        """
        The `GardenStats` class contains a static method `calc_score` that
        calculates a score based on the height and kind of plants in a garden.
        """
        @staticmethod
        def calc_score(plants):
            """
            This static method calculates a score based on the height and
            kind of plants in a given list.
            """
            score = 0
            for p in plants:
                score += p.height
                if (p.kind == "flowering"):
                    score += 15
                elif (p.kind == "prize flowers"):
                    score += 25
            return score


class Plant:
    """
    The `Plant` class defines plants with a name, height,
    and methods to grow and get details.
    """
    kind = "regular"

    def __init__(self, name, height):
        """
        This function is a constructor that initializes an object
        with a name and height attribute.
        """
        self.name = name
        self.height = height

    def grow(self, height):
        """
        This function increases the height of an object by
        a specified amount.
        """
        self.height += height

    def get_details(self):
        """
        This function returns a string containing the name
        and height of a plant.
        """
        return (f"{self.name}: {self.height}cm")


class FloweringPlant(Plant):
    """
    The `FloweringPlant` class represents a flowering plant with
    attributes such as name, height, color, and methods
    to check its status and get details.
    """
    kind = "flowering"

    def __init__(self, name, height, color):
        """
        The function initializes a flowering plant with attributes
        for name, height, and color.
        """
        super().__init__(name, height)
        self.color = color

    def status(self):
        """
        The `status` function returns the static string "blooming".
        """
        return ("blooming")

    def get_details(self):
        """
        This function returns a string containing the name, height, color
        of flowers, and status of an object.
        """
        name = self.name
        height = self.height
        color = self.color
        return (f"{name}: {height}cm, {color} flowers ({self.status()})")


class PrizeFlower(FloweringPlant):
    """
    The `PrizeFlower` class represents flowering plants with competition
    points and provides a method to get details including name, height,
    color, status, and competition points.
    """
    kind = "prize flowers"

    def __init__(self, name, height, color, competition_points):
        """
        This function is an initializer method that sets attributes for
        a price flower, including name, height, color, and competition points.
        """
        super().__init__(name, height, color)
        self.competition_points = competition_points

    def get_details(self):
        """
        This function returns a formatted string containing the name, height,
        color, status, and competition points of an object.
        """
        nm = self.name
        hig = self.height
        clr = self.color
        pts = self.competition_points
        sts = self.status()
        return (f"{nm}: {hig}cm, {clr} flowers ({sts}), Prize points: {pts}")


print("=== Garden Management System Demo ===")
print("")
alice = GardenManager('alice')
plant1 = Plant("Oak Tree", 100)
plant2 = FloweringPlant("Rose", 25, "red")
plant3 = PrizeFlower("Sunflower", 50, "yellow", 10)
alice.add_plant(plant1)
alice.add_plant(plant2)
alice.add_plant(plant3)
alice.help_growth()
alice.report()

print("")
bob = GardenManager('bob')
plant4 = FloweringPlant("Rose", 20, "red")
plant5 = PrizeFlower("Sunflower", 32, "yellow", 10)
bob.add_plant(plant4)
bob.add_plant(plant5)

print("")
if (GardenManager.high_validation_test(1)):
    print("Height validation test: True")

alice_score = GardenManager.GardenStats.calc_score(alice.plants)
bob_score = GardenManager.GardenStats.calc_score(bob.plants)
print(f"Garden scores - Alice: {alice_score}, Bob: {bob_score}")
GardenManager.create_garden_network()
