from operator import *
from functools import reduce, partial
from functools import lru_cache, singledispatch

def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return None

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

    return None


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
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


def spell_dispatcher() -> callable:
    @singledispatch
    def dispatcher(param):
        raise ValueError("Unsupported data type!")


    @dispatcher.register
    def _dispatcher(damage: int):
        return f"Spell damage: {damage}"


    @dispatcher.register
    def _dispatcher(enchantment: str):
        return f"Enchantment casted: {enchantment}"


    @dispatcher.register
    def _dispatcher(multi_cast: list):
        return f"Multi-cast: {multi_cast}"

    return dispatcher


def main():

    spell_powers = [28, 11, 17, 43, 19, 10]
    operations = ['add', 'multiply', 'max', 'min']
    fibonacci_tests = [9, 18, 19]

    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(spell_powers, 'add')}")
    print(f"Product: {spell_reducer(spell_powers, 'multiply')}")
    print(f"Max: {spell_reducer(spell_powers, 'max')}")
    
    print("\nTesting memoized fibonacci...")
    for n in [10, 15]:
        print(f"Fib({n}): {memorized_fibonacci(n)}")

    # My own testings
    print("\nMy own testings:")
    print("=" * 40)
    print("spell_reducer()")
    print('.' * 20)
    for op in ['add', 'multiply', 'min', 'max', None]:
        print(f" - {op}(): {spell_reducer(spell_powers, op)}")

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
