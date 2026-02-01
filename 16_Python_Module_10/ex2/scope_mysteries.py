def mage_counter() -> callable:
    c = 0

    def calls_counter():
        nonlocal c
        c += 1
        return c
    return calls_counter


def spell_accumulator(initial_power: int) -> callable:
    current_total = initial_power

    def add_power(amount):
        nonlocal current_total
        current_total += amount
        return current_total
    return add_power


def enchantment_factory(enchantment_type: str) -> callable:
    return lambda name: f"{enchantment_type} {name}"


def memory_vault() -> dict[str, callable]:
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


if __name__ == "__main__":
    main()
