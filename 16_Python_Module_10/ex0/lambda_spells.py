def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts,
        key=lambda x: x['power'],
        reverse=True
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(
        filter(
            lambda x: x['power'] >= min_power,
            mages
        )
    )


def spell_transformer(spells: list[str]) -> list[str]:
    return list(
        map(
            lambda x: f"* {x} *",
            spells
        )
    )


def mage_stats(mages: list[dict]) -> dict:
    max_power: int = max(mages, key=lambda x: x['power'])['power']
    min_power: int = min(mages, key=lambda x: x['power'])['power']
    avg_power: float = sum(map(lambda x: x['power'], mages)) / len(mages)

    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': float(f"{avg_power:.2f}")
    }


def main() -> None:
    artifacts = [
        {'name': 'Storm Crown', 'power': 117, 'type': 'relic'},
        {'name': 'Fire Staff', 'power': 83, 'type': 'accessory'},
        {'name': 'Crystal Orb', 'power': 60, 'type': 'relic'},
        {'name': 'Light Prism', 'power': 88, 'type': 'accessory'}
    ]
    mages = [
        {'name': 'Storm', 'power': 92, 'element': 'water'},
        {'name': 'Zara', 'power': 54, 'element': 'water'},
        {'name': 'Nova', 'power': 69, 'element': 'wind'},
        {'name': 'Ember', 'power': 63, 'element': 'shadow'},
        {'name': 'Nova', 'power': 78, 'element': 'fire'}
    ]
    spells = [
        'fireball',
        'heal',
        'shield',
        'flash',
        'earthquake',
        'blizzard'
    ]

    print("Testing artifact sorter...")
    print(
        f"{artifacts[1]['name']} ({artifacts[1]['power']} power) "
        f"comes before {artifacts[2]['name']} ({artifacts[2]['power']} power)"
    )

    print("\nTesting spell transformer...")

    for spell in spell_transformer(spells=spells[:3]):
        print(spell, end=" ")
    print()

    # My own testings
    print("\nMy own testings:")
    print("=" * 40)
    print("artifact_sorter()")
    print('.' * 20)
    for _ in artifact_sorter(artifacts=artifacts):
        print(f" - {_}")

    print("\npower_filter()")
    print('.' * 20)
    for _ in power_filter(mages=mages, min_power=70):
        print(f" - {_}")

    print("\nspell_transformer()")
    print('.' * 20)
    for _ in spell_transformer(spells=spells):
        print(f" - {_}")

    print("\nmage_stats()")
    print('.' * 20)
    for key, value in mage_stats(mages=mages).items():
        print(f" - {key}: {value}")


if __name__ == "__main__":
    main()
