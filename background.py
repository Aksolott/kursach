import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


def load_background(image_path):
    """Загружает и возвращает фоновое изображение"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, image_path)

        if not os.path.exists(full_path):
            print(f"Фон не найден: {full_path}")
            return None

        image = pygame.image.load(full_path).convert()
        return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Ошибка загрузки фона: {e}")
        return None
