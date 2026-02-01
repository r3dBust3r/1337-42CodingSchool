from typing import Callable, Any, Tuple


def spell_combiner(spell1: callable, spell2: callable) -> callable:
    # spell_combiner(spell1, spell2) - Combine two spells:
    # • Return a new function that calls both spells with the same arguments
    # • The combined spell should return a tuple of both results
    # • Example: combined = spell_combiner(fireball, heal)
    def combined(*args, **kwargs) -> Tuple[Any, Any]:
        return (
            spell1(*args, **kwargs),
            spell2(*args, **kwargs)
        )
    return combined


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    # power_amplifier(base_spell, multiplier) - Amplify spell power:
    # • Return a new function that multiplies the base spell’s result by multiplier
    # • Assume base spell returns a number (damage, healing, etc.)
    # • Example: mega_fireball = power_amplifier(fireball, 3)
    def amplified(*args, **kwargs):
        return base_spell(*args, **kwargs) * multiplier

    return amplified


def conditional_caster(condition: callable, spell: callable) -> callable:
    # conditional_caster(condition, spell) - Cast spell conditionally:
    # • Return a function that only casts the spell if condition returns True
    # • If condition fails, return "Spell fizzled"
    # • Both condition and spell receive the same arguments
    def caster(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        else:
            return "Spell fizzled"
    return caster


def spell_sequence(spells: list[callable]) -> callable:
    # spell_sequence(spells) - Create spell sequence:
    # • Return a function that casts all spells in order
    # • Each spell receives the same arguments
    # • Return a list of all spell results
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

    # $> python3 higher_magic.py
    # Testing spell combiner...
    # Combined spell result: Fireball hits Dragon, Heals Dragon
    # Testing power amplifier...
    # Original: 10, Amplified: 30

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
