from characters.abstract.creator import CharacterCreator
from characters.players.semirada import Semirada


class SemiradaCreator(CharacterCreator):
    def create(self, name: str, position: tuple) -> Semirada:
        return Semirada(name=name, position=position)
