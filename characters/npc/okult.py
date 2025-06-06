import os
import pygame
from characters.creature import Character

class Okult(Character):
    def __init__(self, name="Культист", position=(0, 0)):
        super().__init__(
            name=name,
            strength=11,
            constitution=12,
            dexterity=10,
            intelligence=10,
            wisdom=11,
            charisma=10,
            max_hp=19
        )
        self.position = position
        self._load_sprite()

    def _load_sprite(self):
        """Загрузка спрайта культиста"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            sprite_path = os.path.join(base_dir, "pictures", "okult.png")
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (150, 150))
        except:
            self.sprite = None