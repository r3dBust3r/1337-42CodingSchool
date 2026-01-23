from ex0 import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical

class EliteCard(Card, Combatable, Magical):
    def play(self, game_state: dict) -> dict:
        ...

    def attack(self, target) -> dict:
        ...

    def defend(self, incoming_damage: int) -> dict:
        ...

    def get_combat_stats(self) -> dict:
        ...

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        ...

    def channel_mana(self, amount: int) -> dict:
        ...

    def get_magic_stats(self) -> dict:
        ...



# • Represents powerful cards with multiple abilities
# • Combines combat prowess with magical capabilities