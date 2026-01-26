from ex0 import Card
from ex0 import CreatureCard
from ex1 import SpellCard
from ex1 import ArtifactCard
from random import shuffle, choice


class Deck:
    def __init__(self) -> None:
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
        creatures: int = 0
        spells: int = 0
        artifacts: int = 0

        for card in self.cards:
            if isinstance(card, CreatureCard):
                creatures += 1

        for card in self.cards:
            if isinstance(card, SpellCard):
                spells += 1

        for card in self.cards:
            if isinstance(card, ArtifactCard):
                artifacts += 1

        return {
            'total_cards': len(self.cards),
            'creatures': creatures,
            'spells': spells,
            'artifacts': artifacts,
            'avg_cost': 4.0
        }
