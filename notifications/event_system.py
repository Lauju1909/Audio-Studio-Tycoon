from typing import Callable, Dict, List

class Event:
    def __init__(self, name: str, data: dict = None):
        self.name = name
        self.data = data or {}

class EventDispatcher:
    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Event], None]]] = {}

    def add_listener(self, event_name: str, listener: Callable[[Event], None]):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def remove_listener(self, event_name: str, listener: Callable[[Event], None]):
        if event_name in self._listeners and listener in self._listeners[event_name]:
            self._listeners[event_name].remove(listener)

    def dispatch(self, event: Event):
        if event.name in self._listeners:
            for listener in self._listeners[event.name]:
                listener(event)

# Global dispatcher instance for easy access across the project
dispatcher = EventDispatcher()
