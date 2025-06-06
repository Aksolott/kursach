import random
import pygame
from singleton import singleton


@singleton
class InitiativeSystem:
    def __init__(self):
        self.participants = []
        self.current_turn = 0
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def add_participant(self, character):
        if not hasattr(character, 'initiative'):
            character.initiative = 0
        self.participants.append(character)

    def roll_initiatives(self):
        for char in self.participants:
            bonus = getattr(char, 'initiative_bonus', 0)
            char.initiative = random.randint(1, 20) + bonus
        self.participants.sort(key=lambda x: x.initiative, reverse=True)

    def get_current_actor(self):
        return self.participants[self.current_turn]

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.participants)
        return self.get_current_actor()

    def show_initiative_screen(self, screen):
        screen.fill((30, 30, 70))
        title_font = pygame.font.SysFont("Arial", 72)
        font = pygame.font.SysFont("Arial", 36)

        title = title_font.render("Порядок ходов", True, (255, 255, 255))
        screen.blit(title, (450 - title.get_width() // 2, 100))

        for i, char in enumerate(self.participants):
            text = f"{i + 1}. {char.name}: {char.initiative}"
            char_text = font.render(text, True, (255, 255, 255))
            screen.blit(char_text, (450 - char_text.get_width() // 2, 200 + i * 50))

        instruction = font.render("Кликните чтобы продолжить...", True, (200, 200, 200))
        screen.blit(instruction, (450 - instruction.get_width() // 2, 550))

        return True
