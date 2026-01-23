from abc import ABC, abstractmethod

class Magical(ABC):
    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        ...

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        ...

    @abstractmethod
    def get_magic_stats(self) -> dict:
        ...

