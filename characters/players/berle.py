import os
import pygame
from characters.creature import Character

class Berle(Character):
    def __init__(self, name="Берле", position=(0, 0)):
        super().__init__(
            name=name,
            strength=13,
            constitution=14,
            dexterity=16,
            intelligence=14,
            wisdom=15,
            charisma=16,
            max_hp=26
        )
        self.position = position
        self.is_player = True
        self._load_sprite()

    def _load_sprite(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            sprite_path = os.path.join(base_dir, "pictures", "berle.png")

            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (150, 150))
        except Exception as e:
            self.sprite = None
