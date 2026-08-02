import random
from game_data import WEEKS_PER_YEAR

class MarketingManager:
    def __init__(self, state):
        self.state = state

    def tick(self, is_new_month):
        self._process_merchandising()
        self._process_crowdfunding()
        
        if is_new_month:
            self._process_intel()
            
        self._process_trends()
        self._process_soundcon()
        self._process_soundtrack_label()

    def _process_merchandising(self):
        for m in list(getattr(self.state, "active_merch_campaigns", [])):
            base_game = next((g for g in self.state.game_history if g.name == m.game_name), None)
            if base_game:
                multiplier = 1.0
                if m.merch_type == "T-Shirts": multiplier = 1.2
                elif m.merch_type == "Action-Figuren": multiplier = 2.0
                elif m.merch_type == "Soundtrack CD/Vinyl": multiplier = 1.5
                
                ip_strength = base_game.ip_rating / 100.0
                weekly_income = int((m.investment / m.duration_weeks) * 1.5 * multiplier * (0.5 + ip_strength))
                
                m.total_revenue += weekly_income
                self.state.track_income("merch", weekly_income)
                
                self.state.fans += int(10 * multiplier)
                self.state.hype = min(100, getattr(self.state, "hype", 0) + 1)
                
            m.weeks_active += 1
            if m.weeks_active >= m.duration_weeks:
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("merch_ended", {"game_name": m.game_name, "merch_type": m.merch_type, "total_revenue": m.total_revenue}))
                self.state.active_merch_campaigns.remove(m)

    def _process_crowdfunding(self):
        failed_campaigns = []
        for cf in getattr(self.state, "active_crowdfundings", []):
            if self.state.week > cf["deadline_week"]:
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("cf_fail", {"project_name": cf["project_name"]}))
                self.state.fans = max(0, self.state.fans - int(cf["target"] / 50))
                self.state.hype = max(0, self.state.hype - 100)
                failed_campaigns.append(cf)
        
        for cf in failed_campaigns:
            self.state.active_crowdfundings.remove(cf)

    def _process_intel(self):
        has_intel = False
        for obj in getattr(self.state, 'office_objects', []):
            if obj.get('bonus') == 'competitor_intel':
                has_intel = True
                break
        
        if has_intel:
            potential_targets = [r for r in getattr(self.state, 'rivals', []) if getattr(r, 'planned_project', None)]
            if potential_targets:
                target = random.choice(potential_targets)
                plan = target.planned_project
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("intel_report", {"target_name": target.name, "genre": plan['genre']}))

    def _process_trends(self):
        trend_interval = random.randint(int(WEEKS_PER_YEAR * 0.4), int(WEEKS_PER_YEAR * 0.8))
        if self.state.week - getattr(self.state, 'last_trend_week', 0) >= trend_interval:
            if self.state.week % 8 == 0:
                self.state.generate_trend()

    def _process_soundcon(self):
        week_in_year = (self.state.week - 1) % WEEKS_PER_YEAR + 1
        current_year = self.state.get_calendar_year()
        if week_in_year == 2 and current_year > getattr(self.state, 'soundcon_last_year', 0):
            from notifications import dispatcher, Event
            dispatcher.dispatch(Event("soundcon_announcement", {"year": current_year}))
            if hasattr(self.state, 'audio'):
                self.state.audio.play_sound('confirm')
                self.state.audio.speak(self.state.get_text('soundcon_announcement', year=current_year), interrupt=False)

    def _process_soundtrack_label(self):
        if getattr(self.state, 'soundtrack_label', None):
            label_income = self.state.soundtrack_label.tick_week()
            label_hype   = self.state.soundtrack_label.tick_hype()
            if label_income > 0:
                self.state.track_income('other', label_income)
            if label_hype > 0:
                self.state.hype = min(250, self.state.hype + label_hype)
