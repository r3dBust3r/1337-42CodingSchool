from ex3.CardFactory import CardFactory
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard


class FantasyCardFactory(CardFactory):
    def create_creature(self, name_or_power) -> CreatureCard:
        if name_or_power == "dragon":
            return CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
        return CreatureCard("Goblin Warrior", 2, "Common", 2, 1)

    def create_spell(self, name_or_power) -> SpellCard:
        return SpellCard("Lightning Bolt", 3, "Rare", "damage")

    def create_artifact(self, name_or_power) -> ArtifactCard:
        return ArtifactCard("Mana Ring", 2, "Rare", 3, "Add 1 mana")

    def get_supported_types(self) -> dict:
        return {
            'creatures': ['dragon', 'goblin'],
            'spells': ['fireball'],
            'artifacts': ['mana_ring']
        }

    def create_themed_deck(self, size: int) -> list:
        return [
            self.create_creature("dragon"),
            self.create_creature("goblin"),
            self.create_spell("fireball")
        ]
