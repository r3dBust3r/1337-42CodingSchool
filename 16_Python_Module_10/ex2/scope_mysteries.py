from typing import Callable


def mage_counter() -> Callable:
    c = 0

    def calls_counter():
        nonlocal c
        c += 1
        return c
    return calls_counter


def spell_accumulator(initial_power: int) -> Callable:
    current_total = initial_power

    def add_power(amount):
        nonlocal current_total
        current_total += amount
        return current_total
    return add_power


def enchantment_factory(enchantment_type: str) -> Callable:
    return lambda name: f"{enchantment_type} {name}"


def memory_vault() -> dict[str, Callable]:
    data = {}

    def store(k, v):
        data[k] = v

    def recall(k):
        try:
            return data[k]
        except KeyError:
            return "Memory not found"

    return {
        'store': store,
        'recall': recall
    }


def main():
    ...
    print("Testing mage counter...")

    function1 = mage_counter()
    for _ in range(3):
        x = function1()
        print(f"Call {x}: {x}")

    print("\nTesting enchantment factory...")
    function2 = enchantment_factory("Flaming")
    print(function2("Sword"))

    function2 = enchantment_factory("Frozen")
    print(function2("Shield"))

    # My own testings
    print("\nMy own testings:")
    print("=" * 40)
    print("mage_counter()")
    print('.' * 20)
    mg = mage_counter()
    for i in range(1, 6):
        print(f" - Call No({i}): {mg()}")

    print("\nspell_accumulator()")
    print('.' * 20)
    init_power = 50
    print(f"Initial power: {init_power}")
    spac = spell_accumulator(init_power)
    for i in range(25, 76, 15):
        print(f" - Power added +{i}: {spac(i)}")

    print("\nenchantment_factory()")
    print('.' * 20)
    ench_fac = enchantment_factory("Enchantment")
    for enchantment in ['Fire', 'Ice', 'Lightning', 'Healing']:
        print(f" - {ench_fac(enchantment)}")

    print("\nmemory_vault()")
    print('.' * 20)
    mem_valut = memory_vault()
    i = 1
    for ench in ['Fire', 'Water', 'Ice']:
        mem_valut['store'](f"enchantment_{i}", ench)
        i += 1

    for i in range(1, 4):
        enchantment = mem_valut['recall'](f"enchantment_{i}")
        print(f" - enchantment_{i}: {enchantment}")


if __name__ == "__main__":
    main()
