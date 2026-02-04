def record_spell(spell_name: str, ingredients: str) -> str:
    from .validator import validate_ingredients

    validatation_result = validate_ingredients(ingredients)

    if "- VALID" in validatation_result:
        return f"Spell recorded: {spell_name} ({validatation_result})"

    elif "- INVALID" in validatation_result:
        return f"Spell rejected: {spell_name} ({validatation_result})"
