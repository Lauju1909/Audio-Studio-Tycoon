import random

class WarfareMission:
    def __init__(self, name, cost, duration_weeks, risk_level):
        self.name = name
        self.cost = cost
        self.duration_weeks = duration_weeks
        self.risk_level = risk_level  # 0.0 to 1.0 chance of getting caught
        self.progress = 0
        self.is_finished = False
        self.success = False

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "cost": self.cost,
            "duration_weeks": self.duration_weeks,
            "risk_level": self.risk_level,
            "progress": self.progress,
            "is_finished": self.is_finished,
            "success": self.success,
            "target_rival_name": getattr(self, "target_rival_name", None)
        }

    @classmethod
    def from_dict(cls, data):
        mission_type = data.get("type")
        if mission_type == "EspionageMission":
            m = EspionageMission(data.get("target_rival_name", ""))
        elif mission_type == "SabotageMission":
            m = SabotageMission(data.get("target_rival_name", ""))
        else:
            return None
        
        m.name = data.get("name", m.name)
        m.cost = data.get("cost", m.cost)
        m.duration_weeks = data.get("duration_weeks", m.duration_weeks)
        m.risk_level = data.get("risk_level", m.risk_level)
        m.progress = data.get("progress", 0)
        m.is_finished = data.get("is_finished", False)
        m.success = data.get("success", False)
        return m

class EspionageMission(WarfareMission):
    def __init__(self, target_rival_name):
        super().__init__("Industriespionage", 50000, 4, 0.2)
        self.target_rival_name = target_rival_name

    def apply_result(self, game_state):
        rival = next((r for r in game_state.rivals if r.name == self.target_rival_name), None)
        if not rival:
            return game_state.get_text("warfare_rival_not_found", name=self.target_rival_name)
        
        if random.random() > self.risk_level:
            self.success = True
            # Reveal planned project
            proj = getattr(rival, 'planned_project', None)
            if proj:
                details = f"{proj.get('topic', '???')} / {proj.get('genre', '???')}"
            else:
                details = game_state.get_text("warfare_no_project")
            
            return game_state.get_text("warfare_espionage_success", name=rival.name, details=details)
        else:
            self.success = False
            # Penalty
            game_state.fans = max(0, game_state.fans - 5000)
            return game_state.get_text("warfare_espionage_fail")

class SabotageMission(WarfareMission):
    def __init__(self, target_rival_name):
        super().__init__("Sabotage (Server-Hack)", 150000, 8, 0.4)
        self.target_rival_name = target_rival_name

    def apply_result(self, game_state):
        rival = next((r for r in game_state.rivals if r.name == self.target_rival_name), None)
        if not rival:
            return game_state.get_text("warfare_rival_not_found", name=self.target_rival_name)

        if random.random() > self.risk_level:
            self.success = True
            delay = random.randint(10, 25)
            rival.next_release_week += delay
            return game_state.get_text("warfare_sabotage_success", name=rival.name, delay=delay)
        else:
            self.success = False
            game_state.money -= 250000 # Legal fees
            return game_state.get_text("warfare_sabotage_fail")

class CorporateWarfareManager:
    def __init__(self):
        self.active_missions = []
    
    def start_mission(self, mission, game_state):
        if game_state.money >= mission.cost:
            game_state.money -= mission.cost
            self.active_missions.append(mission)
            return True
        return False

    def tick(self, game_state):
        results = []
        for mission in self.active_missions:
            mission.progress += 1
            if mission.progress >= mission.duration_weeks:
                mission.is_finished = True
                res_msg = mission.apply_result(game_state)
                results.append(res_msg)
                
                # Send email with result
                from models import Email
                game_state.emails.insert(0, Email(
                    sender=game_state.get_text("sender_darknet"),
                    subject=game_state.get_text("subject_warfare_result"),
                    body=res_msg,
                    date_week=game_state.week
                ))
                if hasattr(game_state, "audio"):
                    game_state.audio.play_sound("email")
                
        self.active_missions = [m for m in self.active_missions if not m.is_finished]
        return results

    def to_dict(self):
        return {
            "active_missions": [m.to_dict() for m in self.active_missions]
        }

    def from_dict(self, data):
        self.active_missions = []
        for m_data in data.get("active_missions", []):
            m = WarfareMission.from_dict(m_data)
            if m:
                self.active_missions.append(m)

def execute_hostile_takeover(target_rival, bid_amount, game_state):
    # Base value of rival
    base_value = 500000 + (len(target_rival.games) * 100000)
    
    recent_avg = 5.0
    if target_rival.games:
        recent_avg = target_rival.games[-1].score
        
    if recent_avg < 6.0:
        base_value *= 0.7  # 30% discount
    elif recent_avg > 8.0:
        base_value *= 1.5  # 50% premium
        
    if bid_amount >= base_value:
        game_state.money -= bid_amount
        if not hasattr(game_state, "subsidiaries"):
            game_state.subsidiaries = []
        game_state.subsidiaries.append(target_rival)
        game_state.rivals.remove(target_rival)
        
        # Subsidiary grants weekly passive income based on their size
        
        return True, game_state.get_text("warfare_takeover_success", name=target_rival.name)
    else:
        return False, game_state.get_text("warfare_takeover_fail", bid=bid_amount, expected=int(base_value))
