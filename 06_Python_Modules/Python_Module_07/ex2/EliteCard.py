from ex0 import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):
    def __init__(
        self,
        name,
        cost,
        rarity,
        attack,
        defnd,
        health,
        mana=5
    ) -> None:
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.defnd = defnd
        self.health = health
        self.mana = mana

    def play(self, game_state: dict) -> dict:
        return {
            'attacker': self.name,
            'target': game_state['target'],
            'damage': self.attack,
            'combat_type': game_state['combat_type']
        }

    def attack(self, target) -> dict:
        return {'attack': self.attack}

    def defend(self, incoming_damage: int) -> dict:
        self.health -= incoming_damage
        return {
            'defender': self.name,
            'damage_taken': self.health,
            'damage_blocked': incoming_damage,
            'still_alive': True if self.health >= 1 else False
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack,
            "defnd": self.defnd,
            "health": self.health,
            "mana": self.mana
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        return {
            'caster': self.name,
            'spell': spell_name,
            'targets': targets,
            'mana_used': self.mana
        }

    def channel_mana(self, amount: int) -> dict:
        return {
            'channeled': amount,
            'total_mana': int(self.mana * 1.4)
        }

    def get_magic_stats(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "attack": self.attack,
            "defnd": self.defnd,
            "health": self.health,
            "mana": self.mana
        }
