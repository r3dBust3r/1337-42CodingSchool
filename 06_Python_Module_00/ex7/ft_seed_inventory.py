# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_seed_inventory.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 14:49:37 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/08 16:52:50 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if (unit == "packets"):
        print(f"{seed_type.capitalize()} seeds: {quantity} packets available")
    elif (unit == "grams"):
        print(f"{seed_type.capitalize()} seeds: {quantity} grams total")
    elif (unit == "area"):
        print(f"{seed_type.capitalize()} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")
