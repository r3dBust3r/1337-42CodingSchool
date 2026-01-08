# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_water_reminder.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 14:13:14 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/08 15:22:03 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_water_reminder():
    days = int(input("Days since last watering: "))
    if (days > 2):
        print("Water the plants!")
    else:
        print("Plants are fine")
