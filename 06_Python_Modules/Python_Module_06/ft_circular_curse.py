from alchemy.grimoire import validate_ingredients
from alchemy.grimoire import record_spell

print("=== Circular Curse Breaking ===\n")

print("Testing ingredient validation:")
print(
    f"validate_ingredients(\"fire air\"): {validate_ingredients('fire air')}"
)
print(
    f"validate_ingredients(\"dragon scales\"): "
    f"{validate_ingredients('dragon scales')}\n"
)

print("Testing spell recording with validation:")
print(
    f"record_spell(\"Fireball\", \"fire air\"): "
    f"{record_spell('Fireball', 'fire air')}"
)
print(
    f"record_spell(\"Dark Magic\", \"shadow\"): "
    f"{record_spell('Dark Magic', 'shadow')}\n"
)

print("Testing late import technique:")
print(
    f"record_spell(\"Lightning\", \"air\"): "
    f"{record_spell('Lightning', 'air')}\n"
)

print("Circular dependency curse avoided using late imports!")
print("All spells processed safely!")
