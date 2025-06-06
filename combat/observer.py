from abc import ABC, abstractmethod


class IGameObserver(ABC):

    @abstractmethod
    def on_combat_event(self, event_type: str, data: dict):
        """Обработка события боя"""
        pass


class IObservable(ABC):

    @abstractmethod
    def add_observer(self, observer: 'IGameObserver'):
        """Добавить наблюдателя"""
        pass

    @abstractmethod
    def remove_observer(self, observer: 'IGameObserver'):
        """Удалить наблюдателя"""
        pass

    @abstractmethod
    def notify_observers(self, event_type: str, data: dict):
        """Уведомить наблюдателей"""
        pass
