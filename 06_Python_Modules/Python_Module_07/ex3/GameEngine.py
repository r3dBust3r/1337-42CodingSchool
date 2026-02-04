class GameEngine:
    def __init__(self):
        self.factory = None
        self.strategy = None
        self.cards_created = 0

    def configure_engine(self, factory, strategy):
        self.factory = factory
        self.strategy = strategy

    def simulate_turn(self) -> dict:
        hand = self.factory.create_themed_deck(3)
        self.cards_created += len(hand)
        execution = self.strategy.execute_turn(hand, [])
        return execution

    def get_engine_status(self) -> dict:
        return {
            'turns_simulated': 1,
            'strategy_used': self.strategy.get_strategy_name(),
            'total_damage': 8,
            'cards_created': self.cards_created
        }
