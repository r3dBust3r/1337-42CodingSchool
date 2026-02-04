def validate_ingredients(ingredients: str) -> str:
    valide_ingredients = ["fire", "water", "earth", "air"]

    for _ in ingredients.split(" "):
        if _ not in valide_ingredients:
            return f"{ingredients} - INVALID"

    return f"{ingredients} - VALID"
