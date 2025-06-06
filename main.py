from combat.game_controller import CombatGame
from characters.players.creators.berle_creator import BerleCreator
from characters.players.creators.semirada_creator import SemiradaCreator
from characters.npc.creators.okult_creator import OkultCreator
from characters.abstract.creator import CharacterFactory
import pygame
from background import load_background


def configure_battle():
    pygame.init()
    pygame.display.set_mode((900, 700))

    background = load_background("python\\pictures\\background.png")

    berle_factory = BerleCreator()
    semirada_factory = SemiradaCreator()
    okult_factory = OkultCreator()

    players = [
        CharacterFactory.create_character(berle_factory, "Берле", (100, 200)),
        CharacterFactory.create_character(semirada_factory, "Семирада", (100, 400))
    ]

    enemies = [
        CharacterFactory.create_character(okult_factory, "Культист 1", (600, 200)),
        CharacterFactory.create_character(okult_factory, "Культист 2", (600, 400))
    ]

    game = CombatGame(players=players, enemies=enemies, background=background)
    result = game.run()

    return result


if __name__ == "__main__":
    result = configure_battle()
    