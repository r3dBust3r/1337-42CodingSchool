from ex4 import TournamentCard


class TournamentPlatform:
    register_cards = []
    leaderboard = []

    def register_card(self, card: TournamentCard) -> str:
        self.register_cards.append(card)
        return f"{card.name} has been registered"

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        print(f"{card1_id} vs {card2_id}")
        return {
            card1_id: self.register_cards[0].name,
            card2_id: self.register_cards[1].name
        }

    def get_leaderboard(self) -> list:
        return self.leaderboard

    def generate_tournament_report(self) -> dict:
        return {
            'report': self.register_cards
        }
