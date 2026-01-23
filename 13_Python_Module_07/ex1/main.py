from ex0 import Card
from ex0 import CreatureCard
from ex1 import ArtifactCard
from ex1 import SpellCard
from ex1 import Deck

print("=== DataDeck Deck Builder ===\n")

print("Building deck with different card types...")
deck = Deck()

spell_card = SpellCard("Lightning Bolt", 10, "Legendary", "damage")
artifact_card = ArtifactCard("Mana Crystal", 10, "Legendary", 10, "permanent")
creature_card = CreatureCard("Fire Dragon", 10, "Legendary", 7, 10)
deck.add_card(spell_card)
deck.add_card(artifact_card)
deck.add_card(creature_card)


print(f"Deck stats: {deck.get_deck_stats()}\n")

print("Drawing and playing cards:\n")

print(f"Drew: {spell_card.name} (Spell)")
play_spell = {'mana_used': 3}
print(f"Play result: {spell_card.play(play_spell)}\n")

print(f"Drew: {artifact_card.name} (Artifact)")
play_spell = {'mana_used': 2}
print(f"Play result: {artifact_card.play(play_spell)}\n")

print(f"Drew: {creature_card.name} (Creature)")
play_spell = {'mana_used': 5}
print(f"Play result: {creature_card.play(play_spell)}\n")

print("Polymorphism in action: Same interface, different card behaviors!")
