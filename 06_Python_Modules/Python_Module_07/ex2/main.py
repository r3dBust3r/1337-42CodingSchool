from typing import List, Dict
from ex0 import Card
from ex2 import Combatable, Magical, EliteCard


def main():
    print("=== DataDeck Ability System ===\n")

    print("EliteCard capabilities:")

    for clss in [Card, Combatable, Magical]:
        clss_methods: List = []
        for key, val in clss.__dict__.items():
            if callable(val) and key != '__init__':
                clss_methods.append(key)

        print(
            f"- {clss.__name__.split('.')[-1]}: "
            f"{clss_methods}"
        )

    print("\nPlaying Arcane Warrior (Elite Card):\n")
    arcane_warrior: EliteCard = EliteCard(
        "Arcane Warrior", 10,
        "Legendary", 5, 3, 7
    )

    print("Combat phase:")
    play_dict: Dict[str, str] = {'target': 'Enemy', 'combat_type': 'melee'}
    print(f"Attack result: {arcane_warrior.play(play_dict)}")
    print(f"Defense result: {arcane_warrior.defend(5)}\n")

    print("Magic phase:")
    print(
        f"Spell cast: "
        f"{arcane_warrior.cast_spell('Fireball', ['Enemy1', 'Enemy2'])}\n"
    )

    print(f"Mana channel: {arcane_warrior.channel_mana(3)}\n")

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()
