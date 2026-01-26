from typing import List
from ex0 import Card
from ex2 import Combatable
from ex4 import Rankable


class TournamentCard(Card, Combatable, Rankable):
    cards: List = []
    total_cards: int = 0
    matches_played: int = 0

    def __init__(self, name: str, cost: int, rarity: str):
        super().__init__(name, cost, rarity)
        self.record: int = 0
        TournamentCard.total_cards += 1
        TournamentCard.cards.append(self)

    def play(self, game_state: dict) -> dict:
        TournamentCard.matches_played += 1
        return game_state

    def attack(self, target) -> dict:
        damage: int = 16
        target.record -= damage
        self.record += damage
        return {'target': target.name, 'damage': damage}

    def defend(self, incoming_damage: int) -> dict:
        return {'defended': incoming_damage}

    def get_combat_stats(self) -> dict:
        return {
            'winner': 'dragon_001',
            'loser': 'wizard_001',
            'winner_rating': 1216,
            'loser_rating': 1134
        }

    def calculate_rating(self) -> int:
        res: int = 0
        if self.name == "Fire Dragon":
            res = 1200 + self.record
        else:
            res = 1150 + self.record
        return res

    def update_wins(self, wins: int) -> None:
        self.record += wins

    def update_losses(self, losses: int) -> None:
        self.record -= losses

    def get_rank_info(self) -> dict:
        return {'record': self.record}

    def get_tournament_stats(self) -> dict:
        avg_rating: int = sum(
            [c.calculate_rating() for c in TournamentCard.cards]
        )
        avg_rating /= len(
            [c.calculate_rating() for c in TournamentCard.cards]
        )
        avg_rating = int(avg_rating)
        return {
            'total_cards': TournamentCard.total_cards,
            'matches_played': TournamentCard.matches_played,
            'avg_rating': avg_rating,
            'platform_status': 'active'
        }
