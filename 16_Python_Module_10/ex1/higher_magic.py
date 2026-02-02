from typing import Any, Tuple, Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(*args, **kwargs) -> Tuple[Any, Any]:
        return (
            spell1(*args, **kwargs),
            spell2(*args, **kwargs)
        )
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(*args, **kwargs):
        return base_spell(*args, **kwargs) * multiplier

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def caster(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        else:
            return "Spell fizzled"
    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    def sp_sq(*args, **kwargs):
        result = []
        for spell in spells:
            result.append(
                spell(*args, **kwargs)
            )
        return result
    return sp_sq


def fireball(target):
    return f"Fireball hits {target}"


def heal(target):
    return f"Heals {target}"


def damage(amount):
    return amount


def main():

    print("Testing spell combiner...")

    combined = spell_combiner(fireball, heal)
    result1, result2 = combined("Dragon")

    print(f"Combined spell result: {result1}, {result2}")

    print("Testing power amplifier...")

    amplified_damage = power_amplifier(damage, 3)

    original = damage(10)
    amplified = amplified_damage(10)

    print(f"Original: {original}, Amplified: {amplified}")


if __name__ == "__main__":
    main()
