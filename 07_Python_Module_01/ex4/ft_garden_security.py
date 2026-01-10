# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_security.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 18:36:22 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/10 09:44:16 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class SecurePlant:
    """
    The `SecurePlant` class ensures that negative values are not accepted for height and age attributes.
    """
    def __init__(self, name, height, age):
        """
        The function initializes a plant object with a name, height, and age, checking for negative values
        and printing a message if found.
        """
        if (height < 0):
            print("Height cannot be negative")
            return
        if (age < 0):
            print("Age cannot be negative")
            return
        self.__name = name
        self.__height = height
        self.__age = age
        print(f"Plant created: {self.__name}")

    def set_height(self, height):
        """
        The `set_height` function sets the height attribute of an object, rejecting negative values
        and providing feedback messages.
        """
        if (height < 0):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.__height = height
        print(f"Height updated: {self.__height}cm [OK]")

    def set_age(self, age):
        """
        The `set_age` function sets the age attribute of an object, rejecting negative values
        and providing feedback messages.
        """
        if (age < 0):
            print("Invalid operation attempted: age {height} days [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.__age = age
        print(f"Age updated: {self.__age} days [OK]")

    def get_height(self):
        """
        This function returns the height attribute of an object.
        """
        return self.__height

    def get_age(self):
        """
        This function returns the age attribute of an object.
        """
        return self.__age

    def get_info(self):
        """
        This function prints the current plant's name, height, and age.
        """
        print(f"Current plant: {self.__name} ({self.__height}cm, {self.__age} days)")


print("=== Garden Security System ===")
plant = SecurePlant("Rose", 0, 0)
plant.set_height(25)
plant.set_age(30)
print("")
plant.set_height(-5)
print("")
plant.get_info()
