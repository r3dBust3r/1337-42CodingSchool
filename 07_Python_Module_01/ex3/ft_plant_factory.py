# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_factory.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 17:18:20 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/10 09:40:09 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant:
    """
    The `Plant` class keeps track of the number of plants created and initializes each plant with a
    name, height, and age.
    """
    plants = 0

    def __init__(self, name, height, age):
        """
        The function initializes a Plant object with a name, height, and age, incrementing the total number
        of plants and printing a creation message.
        """
        Plant.plants += 1
        self.name = name
        self.height = height
        self.age = age
        print(f"Created: {self.name} ({self.height}cm, {self.age} days)")


print("=== Plant Factory Output ===")
Plant("Rose", 25, 30)
Plant("Oak", 200, 365)
Plant("Cactus", 5, 90)
Plant("Sunflower", 80, 45)
Plant("Fern", 15, 120)
print("")
print(f"Total plants created: {Plant.plants}")
