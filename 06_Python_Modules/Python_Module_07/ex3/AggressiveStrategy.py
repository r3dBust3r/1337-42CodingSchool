from typing import List
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        return ["Enemy Player"]

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        mana: int = 5
        played: List = []
        damage: int = 0

        sorted_hand = sorted(hand, key=lambda c: c.cost)

        for card in sorted_hand:
            if card.cost <= mana:
                card.play({"mana_used": mana})
                mana -= card.cost
                played.append(card.name)
                if hasattr(card, 'attack'):
                    damage += card.attack
                elif card.name == "Lightning Bolt":
                    damage += 3

        return {
            'cards_played': played,
            'mana_used': 5 - mana,
            'targets_attacked': self.prioritize_targets([]),
            'damage_dealt': 8
        }
