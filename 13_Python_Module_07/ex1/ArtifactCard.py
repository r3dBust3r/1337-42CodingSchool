from ex0 import Card


class ArtifactCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, durability: int, effect: str):
        super().__init__(name, cost, rarity)
        self.durability = durability
        self.effect = effect

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': game_state['mana_used'],
            'effect': f'{self.effect}: +1 mana per turn'
        }

    def activate_ability(self) -> dict:
        print(f"{self.name}'s ability has been activated")
        return {}
