from ex0 import Card


class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)
        effects = ["damage", "heal", "buff", "debuf"]
        if effect_type not in effects:
            print("Not a valid spell!")
            return
        self.effect_type = effect_type

    def play(self, game_state: dict) -> dict:
        return {
            'card_played': self.name,
            'mana_used': game_state['mana_used'],
            'effect': f'Deal {game_state["mana_used"]} {self.effect_type} to target'
        }

    def resolve_effect(self, targets: list) -> dict:
        for t in targets:
            print(f"{t.name} affected with {self.name}'s spell")
        return {}
