def ft_count_harvest_recursive(days=-1, day=1):
    if (days == -1):
        days = int(input("Days until harvest: "))
    if (day == days + 1):
        return
    print(f"Day {day}")
    ft_count_harvest_recursive(days, day + 1)
    if (day == days):
        print("Harvest time!")
