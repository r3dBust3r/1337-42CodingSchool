# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_iterative.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ottalhao <ottalhao@student.1337.ma>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/08 14:16:44 by ottalhao          #+#    #+#              #
#    Updated: 2026/01/08 15:22:07 by ottalhao         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count_harvest_iterative():
    days = int(input("Days until harvest: "))
    for i in range(1, days + 1):
        print(f"Day {i}")
    print("Harvest time!")
