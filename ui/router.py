"""
Menu Router System
Dynamically manages menu instances and transitions.
"""

_MENU_REGISTRY = {}

def register_menu(menu_id):
    """
    Decorator to register a menu class with a specific ID.
    Usage:
        @register_menu('main_menu')
        class MainMenu:
            ...
    """
    def decorator(cls):
        _MENU_REGISTRY[menu_id] = cls
        return cls
    return decorator

class MenuRouter:
    def __init__(self, audio, state):
        self.audio = audio
        self.state = state
        self.dynamic_routes = {}

    def register_dynamic(self, menu_id, factory):
        """Register a menu factory dynamically, useful for lambdas/imports."""
        self.dynamic_routes[menu_id] = factory

    def get_menu(self, menu_id):
        """Instantiate and return the menu with the given ID."""
        if menu_id in self.dynamic_routes:
            return self.dynamic_routes[menu_id]()
        
        if menu_id in _MENU_REGISTRY:
            return _MENU_REGISTRY[menu_id](self.audio, self.state)
            
        raise KeyError(f"Menu '{menu_id}' is not registered in the MenuRouter.")

    def has_menu(self, menu_id):
        return menu_id in self.dynamic_routes or menu_id in _MENU_REGISTRY
