from characters.abstract.creator import CharacterCreator
from characters.players.berle import Berle


class BerleCreator(CharacterCreator):
    def create(self, name: str, position: tuple) -> Berle:
        return Berle(name=name, position=position)
