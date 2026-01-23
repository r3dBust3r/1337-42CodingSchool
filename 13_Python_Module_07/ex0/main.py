from ex0 import CreatureCard

print("=== DataDeck Card Foundation ===\n")

print("Testing Abstract Base Class Design:\n")

print("CreatureCard Info:")
creature1 = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
print(creature1.get_card_info())
print()

print(f"Playing {creature1.name} with {creature1.mana} mana available:")
print(f"Playable: {creature1.is_playable(creature1.mana)}")

play_card = {
    'card_played': creature1.name,
    'mana_used': 5,
    'effect': 'Creature summoned to battlefield'
}

print(f"Play result: {creature1.play(play_card)}\n")


creature2 = CreatureCard("Goblin Warrior", 5, "Legendary", 3, 5)
print(f"{creature1.name} attacks {creature2.name}:")

print(f"Attack result: {creature1.attack_target(creature2)}\n")

print(f"Testing insufficient mana ({creature1.mana} available):")
print(f"Playable: {creature1.is_playable(creature1.mana)}\n")

print("Abstract pattern successfully demonstrated!")
