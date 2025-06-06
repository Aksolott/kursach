import os
import pygame
from characters.creature import Character


class Semirada(Character):
    def __init__(self, name="Семирада", position=(0, 0)):
        super().__init__(
            name=name,
            strength=14,
            constitution=12,
            dexterity=16,
            intelligence=10,
            wisdom=13,
            charisma=15,
            max_hp=11
        )
        self.position = position
        self.is_player = True
        self._load_sprite()

    def _load_sprite(self):
        """Загрузка спрайта Семирады"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            sprite_path = os.path.join(base_dir, "pictures", "semirada.png")
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (150, 150))
        except:
            self.sprite = None
