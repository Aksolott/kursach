from abc import ABC, abstractmethod


class CombatStrategy(ABC):
    @abstractmethod
    def execute(self, actor, target=None, battle_system=None):
        pass


class AttackStrategy(CombatStrategy):
    def execute(self, actor, target=None, battle_system=None):
        if target and battle_system:
            battle_system.attack(actor, target)


class HealStrategy(CombatStrategy):
    def execute(self, actor, target=None, battle_system=None):
        if battle_system:
            battle_system.heal(actor)