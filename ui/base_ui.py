import pygame
import os
from config import PICTURES_DIR


class BaseUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 72)
        self.character_images = {}

    def load_image(self, filename, default_color, size=(250, 250)):
        path = os.path.join(PICTURES_DIR, filename)
        try:
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(image, size)
        except Exception as e:
            print(f"Error loading {filename}: {e}")

        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(default_color)
        return surf

    def draw_button(self, surface, rect, text, color):
        pygame.draw.rect(surface, color, rect)
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        return rect
