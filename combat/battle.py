import random
from singleton import singleton
from typing import List
from characters.creature import Character
from combat.observer import IObservable


@singleton
class BattleSystem(IObservable):
    def __init__(self):
        self.combat_log = []
        self.max_messages = 5
        self.message_colors = {
            'attack': (255, 255, 255),
            'crit': (255, 50, 50),
            'death': (200, 0, 0),
            'heal': (50, 255, 50)
        }
        self.participants: List[Character] = []
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event_type, data):
        for observer in self._observers:
            observer.on_combat_event(event_type, data)

    def _add_message(self, message, color):
        self.combat_log.append((message, color))
        if len(self.combat_log) > self.max_messages:
            self.combat_log.pop(0)

    def attack(self, attacker: Character, defender: Character) -> int:
        if attacker.hp <= 0 or defender.hp <= 0:
            return 0

        attack_roll = random.randint(1, 20)
        is_crit = attack_roll == 20
        damage_bonus = (attacker.strength - 10) // 2
        damage = max(1, random.randint(1, 6) + damage_bonus)

        if is_crit:
            damage *= 2
            message = f"{attacker.name} КРИТИЧЕСКИ атакует {defender.name} ({damage} урона)!"
            color = self.message_colors['crit']
            self.notify_observers('critical_attack', {
                'attacker': attacker,
                'defender': defender,
                'damage': damage
            })
        else:
            message = f"{attacker.name} атакует {defender.name} ({damage} урона)"
            color = self.message_colors['attack']
            self.notify_observers('attack', {
                'attacker': attacker,
                'defender': defender,
                'damage': damage
            })

        defender.hp -= damage
        defender.hp = max(0, defender.hp)

        self._add_message(message, color)

        if defender.hp <= 0:
            death_msg = f"{defender.name} повержен!"
            self._add_message(death_msg, self.message_colors['death'])
            self.notify_observers('death', {
                'character': defender,
                'killer': attacker
            })

        return damage

    def heal(self, healer: Character) -> int:
        if healer.hp <= 0:
            return 0

        heal_amount = random.randint(1, 8)
        healer.hp = min(healer.hp + heal_amount, healer.max_hp)

        message = f"{healer.name} восстанавливает {heal_amount} здоровья!"
        self._add_message(message, self.message_colors['heal'])
        self.notify_observers('heal', {
            'healer': healer,
            'amount': heal_amount
        })

        return heal_amount

    def is_combat_over(self) -> bool:
        """Проверяет, закончился ли бой"""
        players_alive = [p for p in self.participants if p.is_player and p.hp > 0]
        enemies_alive = [e for e in self.participants if not e.is_player and e.hp > 0]

        return len(players_alive) < len([p for p in self.participants if p.is_player]) or not enemies_alive

    def get_combat_result(self) -> str:
        """Возвращает результат боя: '1' - победа, '0' - поражение"""
        players_alive = [p for p in self.participants if p.is_player and p.hp > 0]
        enemies_alive = [e for e in self.participants if not e.is_player and e.hp > 0]

        if len(players_alive) < len([p for p in self.participants if p.is_player]):
            return "0"
        elif not enemies_alive:
            return "1"
        return "ONGOING"

    def get_recent_messages(self):
        return self.combat_log[-self.max_messages:]

