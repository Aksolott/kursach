import pygame
from typing import Callable, Optional, Tuple


class Button:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            color: Tuple[int, int, int],
            hover_color: Optional[Tuple[int, int, int]] = None,
            text_color: Tuple[int, int, int] = (255, 255, 255),
            font_size: int = 32,
            on_click: Optional[Callable] = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or self._adjust_brightness(color, 1.2)
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.on_click = on_click
        self.is_hovered = False
        self.is_active = True

    @staticmethod
    def _adjust_brightness(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        return tuple(min(255, max(0, int(c * factor))) for c in color)

    def draw(self, surface: pygame.Surface) -> None:
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)  # Border

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> bool:
        if not self.is_active:
            self.is_hovered = False
            return False

        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered and mouse_clicked and self.on_click:
            self.on_click()
            return True
        return False

    def set_active(self, active: bool) -> None:
        self.is_active = active


class ButtonManager:
    def __init__(self):
        self.buttons = []

    def add_button(self, button: Button) -> None:
        self.buttons.append(button)

    def draw_all(self, surface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(surface)

    def update_all(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> bool:
        for button in self.buttons:
            if button.update(mouse_pos, mouse_clicked):
                return True
        return False

    def clear(self) -> None:
        self.buttons = []