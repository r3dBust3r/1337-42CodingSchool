from typing import Callable
from operator import add, mul, gt, lt
from functools import reduce, partial
from functools import lru_cache, singledispatch


def spell_reducer(spells: list[int], operation: str) -> int:
    if operation == "add":
        return reduce(add, spells)

    if operation == "multiply":
        return reduce(mul, spells)

    if operation == "max":
        return reduce(
            lambda a, b: a if gt(a, b) else b, spells
        )

    if operation == "min":
        return reduce(
            lambda a, b: a if lt(a, b) else b, spells
        )

    raise ValueError("Unsupported operation!")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire_enchant = partial(base_enchantment, 50, "fire")
    ice_enchant = partial(base_enchantment, 50, "ice")
    lightning_enchant = partial(base_enchantment, 50, "lightning")

    return {
        'fire_enchant': fire_enchant,
        'ice_enchant': ice_enchant,
        'lightning_enchant': lightning_enchant
    }


@lru_cache
def memorized_fibonacci(n: int) -> int:
    return (
        n if n <= 1
        else memorized_fibonacci(n - 1) + memorized_fibonacci(n - 2)
    )


def spell_dispatcher() -> Callable:
    @singledispatch
    def dispatcher(param):
        raise ValueError("Unsupported data type!")

    @dispatcher.register
    def _dispatcher(damage: int):
        return f"Spell damage: {damage}"

    @dispatcher.register
    def _(enchantment: str):
        return f"Enchantment casted: {enchantment}"

    @dispatcher.register
    def _(multi_cast: list):
        return f"Multi-cast: {multi_cast}"

    return dispatcher


def main():
    spell_powers = [28, 11, 17, 43, 19, 10]

    try:
        print("Testing spell reducer...")
        print(f"Sum: {spell_reducer(spell_powers, 'add')}")
        print(f"Product: {spell_reducer(spell_powers, 'multiply')}")
        print(f"Max: {spell_reducer(spell_powers, 'max')}")
    except ValueError as e:
        print(e)

    print("\nTesting memoized fibonacci...")
    for n in [10, 15]:
        print(f"Fib({n}): {memorized_fibonacci(n)}")

    # My own testings
    print("\nMy own testings:")
    print("=" * 40)
    print("spell_reducer()")
    print('.' * 20)
    for op in ['add', 'multiply', 'min', 'max', None]:
        try:
            print(f" - {op}(): {spell_reducer(spell_powers, op)}")
        except ValueError as e:
            print(e)

    print("\npartial_enchanter()")
    print('.' * 20)

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element} enchantment with {power} power on {target}"

    enchants = partial_enchanter(base_enchantment)
    print(f' - {enchants["fire_enchant"]("orc")}')
    print(f' - {enchants["ice_enchant"]("dragon")}')
    print(f' - {enchants["lightning_enchant"]("goblin")}')

    print("\nmemorized_fibonacci()")
    print('.' * 20)
    for n in range(50, 56):
        print(f" - fibonacci({n}): {memorized_fibonacci(n)}")

    print("\nspell_dispatcher()")
    print('.' * 20)
    dispatcher = spell_dispatcher()
    for arg in [25, "fire", ["fire", "water"], 10.2]:
        try:
            print(f" - {dispatcher(arg)}")
        except ValueError as e:
            print("\nCaught expected error:", e)


if __name__ == "__main__":
    main()
