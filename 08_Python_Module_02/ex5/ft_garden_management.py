class GardenError(Exception):
    """Base error class"""
    pass


class GardenManager:
    """GardenManager is a class that manages the entire garden system"""
    water_level = 25

    def __init__(self, name):
        """The constructor method that initializes the attributes"""
        self.plants = []
        self.name = name

    def add_plant(self, plant):
        """Add new plants to the garden"""
        try:
            if (plant.name.strip() == ""):
                raise ValueError(
                    "Error adding plant: Plant name cannot be empty!")
            else:
                self.plants.append(plant)
                print(f"Added {plant.name} successfully")
        except ValueError as e:
            print(e)

    def water_plant(self, name, water):
        """Water one plant"""
        for p in self.plants:
            if (p.name == name):
                p.water = water
                GardenManager.water_level -= water

    def water_plants(self, water):
        """Water all plants"""
        print("\nWatering plants...")
        print("Opening watering system")
        try:
            for p in self.plants:
                p.water = water
                GardenManager.water_level -= water
                print(f"Watering {p.name.lower()} - success")
        except Exception as e:
            print(e)
        finally:
            print("Closing watering system (cleanup)")

    def sun_exposion(self, name, sun):
        """Expose one plant to the sun"""
        for p in self.plants:
            if (p.name == name):
                p.sun = sun

    def check_plants_health(self):
        """Check all plants health and display messages about them"""
        print("\nChecking plant health...")
        for p in self.plants:
            try:
                if (p.water < 0):
                    raise Exception(
                        f"Error checking {p.name}: Water level {p.water} "
                        "is too low (min 0)")

                if (p.water > 10):
                    raise Exception(
                        f"Error checking {p.name}: Water level {p.water} "
                        "is too high (max 10)")

                if (p.sun < 2):
                    raise Exception(
                        f"Error checking {p.name}: Sunlight hours {p.sun} "
                        "is too low (min 2)")

                if (p.sun > 12):
                    raise Exception(
                        f"Error checking {p.name}: Sunlight hours {p.sun} "
                        "is too high (max 12)")

                print(f"{p.name}: healthy (water: {p.water}, sun: {p.sun})")

            except Exception as e:
                print(e)

    @classmethod
    def error_recovery_test(cls):
        """a class method that checks the garden tank level"""
        print("\nTesting error recovery...")
        try:
            if (cls.water_level <= 0):
                cls.water_level = 0
                raise GardenError(
                    "Caught GardenError: Not enough water in tank")
        except GardenError as e:
            print(e)


class Plant:
    """Plant class"""
    def __init__(self, name, water, sun):
        """The constructor method that initializes the attributes"""
        self.name = name
        self.water = water
        self.sun = sun


print("=== Garden Management System ===")
print("\nAdding plants to garden...")
otmane = GardenManager("otmane")
otmane.add_plant(Plant("tomato", 0, 0))
otmane.add_plant(Plant("lettuce", 0, 0))
otmane.add_plant(Plant("", 0, 0))

otmane.water_plants(5)
otmane.sun_exposion("tomato", 8)
otmane.sun_exposion("lettuce", 8)

otmane.water_plant("lettuce", 15)
otmane.check_plants_health()

GardenManager.error_recovery_test()
print("System recovered and continuing...")
print("\nGarden management system test complete!")
