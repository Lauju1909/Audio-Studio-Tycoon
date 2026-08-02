import random
from models import CustomConsole

class HardwareManager:
    def __init__(self, state):
        self.state = state

    def tick(self):
        # Progress hardware development
        if getattr(self.state, 'is_developing_console', False) and self.state.current_console_draft:
            # We assume a fixed or team-based speed. Let's just use employees.
            speed = 1.0
            if hasattr(self.state, 'get_team_speed_modifier'):
                speed = self.state.get_team_speed_modifier()
            
            # Fortschritt pro Woche (Skaliert mit Teamgröße, max 100)
            progress_step = max(1, len(self.state.employees)) * speed
            self.state.console_progress += progress_step
            
            if self.state.console_progress >= self.state.console_total_weeks * 10:
                self._finish_console_development()
                
        # Generate revenue from active consoles
        self._process_sales()

    def start_development(self, name, architecture, performance, marketing_budget):
        # Extrem teuer
        dev_cost = 50000000 + (performance * 10000000) + marketing_budget
        if self.state.money < dev_cost:
            return False
            
        self.state.track_expense("other", dev_cost)
        
        self.state.current_console_draft = CustomConsole(
            name=name,
            architecture=architecture,
            performance=performance,
            marketing_budget=marketing_budget,
            dev_cost=dev_cost,
            release_week=0 # Will be set on release
        )
        self.state.is_developing_console = True
        self.state.console_progress = 0
        self.state.console_total_weeks = 50 + performance * 5 # Wochen
        return True

    def _finish_console_development(self):
        self.state.is_developing_console = False
        draft = self.state.current_console_draft
        draft.release_week = self.state.week
        
        if not hasattr(self.state, 'custom_consoles'):
            self.state.custom_consoles = []
        self.state.custom_consoles.append(draft)
        self.state.current_console_draft = None
        
        # Hype Bonus
        self.state.hype = min(250, getattr(self.state, 'hype', 0) + 50 + draft.performance * 5)
        
        if hasattr(self.state, 'audio'):
            self.state.audio.play_sound('success')
            try:
                self.state.audio.speak(self.state.get_text('console_finished', name=draft.name))
            except:
                self.state.audio.speak(f"Konsole {draft.name} fertiggestellt!")
        
        # Optionale Event Benachrichtigung
        try:
            from notifications import dispatcher, Event
            dispatcher.dispatch(Event("console_finished", {"console": draft}))
        except:
            pass

    def _process_sales(self):
        # Massive Einnahmen
        for console in getattr(self.state, 'custom_consoles', []):
            weeks_on_market = self.state.week - getattr(console, 'release_week', self.state.week)
            if weeks_on_market <= 0:
                continue
                
            # Lifecycle von ca. 150-200 Wochen
            market_factor = max(0.05, 1.0 - (weeks_on_market / 150.0))
            
            # Massive Verkäufe
            weekly_units = int((getattr(console, 'performance', 5) * 10000) * market_factor * getattr(console, 'market_share', 0.1) * random.uniform(0.8, 1.2))
            
            if weekly_units > 0:
                console.units_sold = getattr(console, 'units_sold', 0) + weekly_units
                # Konsole wird für z.B. 299 verkauft, Marge ca 50 Euro pro Konsole
                profit_per_unit = 50 + (getattr(console, 'performance', 5) * 5)
                revenue = weekly_units * profit_per_unit
                
                self.state.money += revenue
                if hasattr(self.state, 'track_income'):
                    self.state.track_income("other", revenue)
