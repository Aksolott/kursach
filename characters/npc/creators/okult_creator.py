from characters.abstract.creator import CharacterCreator
from characters.npc.okult import Okult


class OkultCreator(CharacterCreator):
    def create(self, name: str, position: tuple) -> Okult:
        return Okult(name=name, position=position)