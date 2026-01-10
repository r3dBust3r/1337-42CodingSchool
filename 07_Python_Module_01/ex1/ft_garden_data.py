# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_data.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 17:10:48 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/10 09:30:20 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant:
    """
    The class `Plant` has attributes for name, height, and age, initialized through its constructor.
    """
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


p1 = Plant("Rose", 25, 30)
p2 = Plant("Sunflower", 80, 45)
p3 = Plant("Cactus", 15, 120)

print("=== Garden Plant Registry ===")
print(f"{p1.name}: {p1.height}cm, {p1.age} days old")
print(f"{p2.name}: {p2.height}cm, {p2.age} days old")
print(f"{p3.name}: {p3.height}cm, {p3.age} days old")
