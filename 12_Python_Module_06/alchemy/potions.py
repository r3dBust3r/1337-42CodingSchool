from .elements import create_fire, create_water, create_earth, create_air


def healing_potion():
    return f"Healing potion brewed with {create_fire()} and {create_water()}"


def strength_potion():
    return f"Strength potion brewed with {create_earth()} and {create_fire()}"


def invisibility_potion():
    return (
        f"Invisibility potion brewed with {create_air()} and {create_water()}"
    )


def wisdom_potion():
    return (
        f"Wisdom potion brewed with all elements: "
        f"{create_fire()} {create_water()} {create_earth()} {create_air()}"
    )
