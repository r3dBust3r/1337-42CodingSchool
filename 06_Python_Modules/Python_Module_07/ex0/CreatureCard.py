from ex0 import Card


class CreatureCard(Card):
    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        health: int
    ):
        if (attack < 0 or health < 0):
            print("Negative value detected!")
            return

        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health
        self.mana = 8

    def get_card_info(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "attack": self.attack,
            "health": self.health,
            "mana": self.mana
        }

    def play(self, game_state: dict) -> dict:
        if game_state['mana_used'] > self.mana:
            return {"error": "Not enough mana!"}
        self.mana -= game_state['mana_used']

        return {
            'card_played': self.name,
            'mana_used': game_state['mana_used'],
            'effect': 'Creature summoned to battlefield'
        }

    def attack_target(self, target) -> dict:
        target.health -= self.attack
        result = {
            'attacker': self.name,
            'target': target.name,
            'damage_dealt': self.attack,
            'combat_resolved': True if target.health <= 0 else False
        }
        return result
