# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_age.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 14:09:56 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/08 15:21:59 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_plant_age():
    days = int(input("Enter plant age in days: "))
    if (days > 60):
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")
