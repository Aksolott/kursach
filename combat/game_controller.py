import pygame
import random
from combat.battle import BattleSystem
from combat.initiative_system import InitiativeSystem
from combat.strategies import AttackStrategy, HealStrategy
from typing import List
from characters.creature import Character


class CombatGame:
    def __init__(self, players: List[Character], enemies: List[Character], background=None):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        self.players = players
        self.enemies = enemies
        self.participants = players + enemies
        self.background = background
        self.current_target = None
        self.heal_performed = False

        self.initiative_system = InitiativeSystem()
        self.battle_system = BattleSystem()
        self.battle_system.participants = self.participants

        from ui.combat_ui import CombatUI
        self.ui = CombatUI(self, background)

        self._setup_participants()
        self._show_initiative()

    def _setup_participants(self):
        for char in self.participants:
            if not hasattr(char, 'initiative'):
                char.initiative = 0
            if not hasattr(char, 'initiative_bonus'):
                char.initiative_bonus = (char.dexterity - 10) // 2
            self.initiative_system.add_participant(char)

    def _show_initiative(self):
        self.initiative_system.roll_initiatives()
        waiting = True

        while waiting:
            if not self.initiative_system.show_initiative_screen(self.screen):
                pygame.quit()
                exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            pygame.display.flip()

    def _handle_turn(self, actor: Character):
        if actor.hp <= 0:
            self.initiative_system.next_turn()
            return

        if actor.is_player:
            self._handle_player_turn(actor)
        else:
            self._handle_enemy_turn(actor)

    def _handle_player_turn(self, player: Character):
        self.current_target = None
        self.heal_performed = False
        self.ui.set_turn_status(True)

        waiting = True
        clock = pygame.time.Clock()

        while waiting:
            events = pygame.event.get()
            self.ui.handle_events(events)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"

            if self.current_target or self.heal_performed:
                waiting = False
                pygame.time.delay(500)

            if self.battle_system.is_combat_over():
                return

            self.ui.draw(self.participants, player)
            pygame.display.flip()
            clock.tick(60)

        self.ui.set_turn_status(False)
        self.initiative_system.next_turn()

    def _handle_enemy_turn(self, enemy: Character):
        alive_players = [p for p in self.players if p.hp > 0]
        if not alive_players:
            self.ui.show_message("Все игроки погибли!")
            pygame.time.delay(2000)
            pygame.quit()
            exit()

        target = random.choice(alive_players)
        self.battle_system.attack(enemy, target)

        self.ui.draw(self.participants, enemy)
        pygame.display.flip()
        pygame.time.delay(700)

        self.initiative_system.next_turn()

    def set_attack_target(self, target: Character):
        if target:
            current_actor = self.initiative_system.get_current_actor()
            current_actor.set_strategy(AttackStrategy())
            current_actor.perform_action(target, self.battle_system)
            self.current_target = target

    def set_heal_action(self):
        current_actor = self.initiative_system.get_current_actor()
        current_actor.set_strategy(HealStrategy())
        current_actor.perform_action(None, self.battle_system)
        self.heal_performed = True

    def run(self):
        clock = pygame.time.Clock()
        running = True
        result = None

        while running:
            events = pygame.event.get()
            self.ui.handle_events(events)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    result = "0"

            current_actor = self.initiative_system.get_current_actor()
            self._handle_turn(current_actor)

            if self.battle_system.is_combat_over():
                result = self.battle_system.get_combat_result()
                running = False

            self.ui.draw(self.participants, current_actor)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return result if result else "0"
