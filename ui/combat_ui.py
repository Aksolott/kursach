import pygame
from ui.button import Button, ButtonManager
from combat.observer import IGameObserver
from typing import List
from characters.creature import Character


class CombatUI(IGameObserver):
    def __init__(self, game_controller, background=None):
        self.game_controller = game_controller
        self.background = background
        self.font = pygame.font.SysFont("Arial", 36)
        self.message_font = pygame.font.SysFont("Arial", 24)
        self.button_manager = ButtonManager()
        self.current_target = None
        self.colors = {
            'player': (0, 0, 255),
            'enemy': (255, 0, 0),
            'target': (255, 255, 0),
            'highlight': (255, 200, 0),
            'message': (255, 255, 255),
            'heal_effect': (0, 255, 0, 100)
        }
        self._setup_ui()

        if hasattr(game_controller, 'battle_system'):
            game_controller.battle_system.add_observer(self)

    def _setup_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.attack_btn = Button(
            x=50, y=600, width=200, height=50,
            text="Атаковать",
            color=(200, 0, 0),
            hover_color=(250, 50, 50),
            on_click=self._handle_attack
        )
        self.heal_btn = Button(
            x=300, y=600, width=200, height=50,
            text="Лечиться",
            color=(0, 200, 0),
            hover_color=(50, 250, 50),
            on_click=self._handle_heal
        )
        self.button_manager.add_button(self.attack_btn)
        self.button_manager.add_button(self.heal_btn)
        self.attack_btn.set_active(False)
        self.heal_btn.set_active(False)

    def on_combat_event(self, event_type: str, data: dict):
        """Обработка событий от BattleSystem"""
        if event_type == 'critical_attack':
            self.show_attack_indicator(data['attacker'], data['defender'])
            self.show_message(f"КРИТИЧЕСКИЙ УДАР! {data['damage']} урона!")
        elif event_type == 'attack':
            self.show_attack_indicator(data['attacker'], data['defender'])
        elif event_type == 'heal':
            self.show_heal_effect(data['healer'])
            self.show_message(f"Лечение: +{data['amount']} HP")
        elif event_type == 'death':
            self.show_message(f"{data['character'].name} повержен!")

    def set_game_controller(self, controller):
        """Установка ссылки на игровой контроллер"""
        self.game_controller = controller

    def set_turn_status(self, is_player_turn: bool):
        """Активация кнопок в зависимости от хода"""
        self.attack_btn.set_active(is_player_turn)
        self.heal_btn.set_active(is_player_turn)
        self.current_target = None

    def show_message(self, message: str):
        """Отображение сообщения на экране"""
        surface = pygame.display.get_surface()
        msg_panel = pygame.Surface((600, 100), pygame.SRCALPHA)
        msg_panel.fill((0, 0, 0, 200))

        text = self.font.render(message, True, self.colors['message'])

        surface.blit(msg_panel, (150, 300))
        surface.blit(text, (450 - text.get_width() // 2, 350 - text.get_height() // 2))

        pygame.display.flip()

    def _handle_attack(self):
        """Обработка нажатия кнопки атаки"""
        if self.current_target and self.game_controller:
            self.game_controller.set_attack_target(self.current_target)

    def _handle_heal(self):
        """Обработка нажатия кнопки лечения"""
        if self.game_controller:
            self.game_controller.set_heal_action()

    def show_attack_indicator(self, attacker: Character, target: Character):
        """Визуализация атаки"""
        surface = pygame.display.get_surface()
        pygame.draw.line(surface, self.colors['highlight'],
                         attacker.position, target.position, 3)
        for radius in range(25, 35, 2):
            pygame.draw.circle(surface, (255, 100, 100),
                               target.position, radius, 1)
        pygame.display.flip()

    def show_heal_effect(self, healer: Character):
        """Визуализация лечения"""
        surface = pygame.display.get_surface()
        heal_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
        pygame.draw.circle(heal_surface, self.colors['heal_effect'], (75, 75), 70)
        heal_rect = heal_surface.get_rect(center=healer.position)
        surface.blit(heal_surface, heal_rect)
        pygame.display.flip()
        pygame.time.delay(300)

    def draw(self, participants: List[Character], current_actor: Character):
        """Отрисовка игрового интерфейса"""
        surface = pygame.display.get_surface()

        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((30, 30, 70))

        for char in participants:
            if hasattr(char, 'sprite') and char.sprite:
                sprite_rect = char.sprite.get_rect(center=char.position)
                surface.blit(char.sprite, sprite_rect)
                if char == self.current_target:
                    pygame.draw.circle(surface, self.colors['target'],
                                       char.position, 50, 3)
            else:
                color = self.colors['player'] if char.is_player else self.colors['enemy']
                if char == self.current_target:
                    color = self.colors['target']
                pygame.draw.circle(surface, color, char.position, 40)

            # HP бар
            hp_width = 80
            pygame.draw.rect(surface, (255, 0, 0),
                             (char.position[0] - hp_width // 2, char.position[1] - 60,
                              hp_width, 5))
            pygame.draw.rect(surface, (0, 255, 0),
                             (char.position[0] - hp_width // 2, char.position[1] - 60,
                              hp_width * (char.hp / char.max_hp), 5))

            name_text = self.font.render(char.name, True, (255, 255, 255))
            surface.blit(name_text,
                         (char.position[0] - name_text.get_width() // 2,
                          char.position[1] - 80))

            if char == current_actor:
                pygame.draw.circle(surface, (255, 255, 0), char.position, 50, 3)

        screen_height = surface.get_height()
        self.attack_btn.rect.y = screen_height - 180
        self.heal_btn.rect.y = screen_height - 180

        if hasattr(self.game_controller, 'battle_system'):
            messages = self.game_controller.battle_system.get_recent_messages()
            self.draw_messages(surface, messages)

        self.button_manager.draw_all(surface)

        mouse_pos = pygame.mouse.get_pos()
        for char in participants:
            if not char.is_player and char.hp > 0:
                distance = ((mouse_pos[0] - char.position[0]) ** 2 +
                            (mouse_pos[1] - char.position[1]) ** 2) ** 0.5
                if distance < 50:
                    pygame.draw.circle(surface, self.colors['highlight'],
                                       char.position, 50, 3)
                    if pygame.mouse.get_pressed()[0]:
                        self.current_target = char

    def draw_messages(self, surface: pygame.Surface, messages: list):
        """Отрисовка лога сообщений внизу экрана"""
        if not messages:
            return

        screen_width, screen_height = surface.get_size()
        msg_panel_height = 120
        msg_panel_y = screen_height - msg_panel_height

        msg_panel = pygame.Surface((screen_width, msg_panel_height), pygame.SRCALPHA)
        msg_panel.fill((0, 0, 0, 180))

        visible_messages = messages[-4:]
        for i, (msg, color) in enumerate(visible_messages):
            text = self.message_font.render(msg, True, color)
            msg_panel.blit(text, (10, 10 + i * 28))

        surface.blit(msg_panel, (0, msg_panel_y))

    def handle_events(self, events):
        """Обработка событий ввода"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        self.button_manager.update_all(mouse_pos, mouse_clicked)
