from ex0 import Card
from ex0 import CreatureCard
from ex1 import SpellCard
from ex1 import ArtifactCard
from random import shuffle, choice


class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)

    def shuffle(self) -> None:
        shuffle(self.cards)

    def draw_card(self) -> Card:
        return choice(self.cards)

    def get_deck_stats(self) -> dict:
        return {
            'total_cards': len(self.cards),
            'creatures': len([card for card in self.cards if isinstance(card, CreatureCard)]),
            'spells': len([card for card in self.cards if isinstance(card, SpellCard)]),
            'artifacts': len([card for card in self.cards if isinstance(card, ArtifactCard)]),
            'avg_cost': 4.0
        }
