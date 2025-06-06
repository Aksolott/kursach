import pygame
import os
from combat.strategies import AttackStrategy


class Character:
    def __init__(self, name, strength, constitution, dexterity,
                 intelligence, wisdom, charisma, max_hp):
        self.name = name
        self.strength = strength
        self.constitution = constitution
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.max_hp = max_hp
        self.hp = max_hp
        self.is_player = False
        self.initiative = 0
        self.initiative_bonus = (dexterity - 10) // 2
        self.position = (0, 0)
        self.current_strategy = AttackStrategy()

        self.sprite = None
        self.current_state = 'idle'

    def set_strategy(self, strategy):
        """Установка текущей стратегии"""
        self.current_strategy = strategy

    def perform_action(self, target=None, battle_system=None):
        """Выполнение текущей стратегии"""
        self.current_strategy.execute(self, target, battle_system)

    def load_sprite(self, sprite_path):
        """Загружает основной спрайт персонажа"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            full_path = os.path.join(base_dir, sprite_path)
            self.sprite = pygame.image.load(full_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        except Exception as e:
            print(f"Ошибка загрузки спрайта {self.name}: {e}")
            self._create_placeholder()

    def _create_placeholder(self):
        """Создает цветную заглушку"""
        color = (0, 0, 200) if self.is_player else (200, 0, 0)
        self.sprite = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.sprite.fill(color)

    def draw(self, surface, position=None):
        """Отрисовывает персонажа"""
        pos = position if position else self.position
        if self.sprite:
            sprite_rect = self.sprite.get_rect(center=pos)
            surface.blit(self.sprite, sprite_rect)
        else:
            pygame.draw.circle(surface,
                               (0, 0, 255) if self.is_player else (255, 0, 0),
                               pos, 40)
