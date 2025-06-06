from abc import ABC, abstractmethod
from characters.creature import Character


class CharacterCreator(ABC):
    @abstractmethod
    def create(self, name: str, position: tuple) -> Character:
        pass


class CharacterFactory:
    @staticmethod
    def create_character(creator: CharacterCreator, name: str, position: tuple) -> Character:
        return creator.create(name, position)
