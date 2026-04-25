import random
from game_data import TREND_TOPICS, TREND_GENRES, START_YEAR, WEEKS_PER_YEAR
from models import RivalGame, Email

def get_calendar_year(week):
    return START_YEAR + (week - 1) // WEEKS_PER_YEAR

class BasicCompetitorAI:
    @staticmethod
    def process(rival, game_state):
        # Phase II: Planungsphase 10 Wochen vor Release
        if game_state.week >= (rival.next_release_week - 10) and not getattr(rival, "planned_project", None):
            rival.planned_project = {
                "topic": random.choice(TREND_TOPICS)["topic"],
                "genre": random.choice(TREND_GENRES)["genre"]
            }

        if game_state.week >= rival.next_release_week:
            plan = getattr(rival, "planned_project", None)
            topic = plan["topic"] if plan else random.choice(TREND_TOPICS)["topic"]
            genre = plan["genre"] if plan else random.choice(TREND_GENRES)["genre"]
            rival.planned_project = None # Reset
            
            # Basis-Score (schlechter)
            base_score = random.uniform(4.0, 7.5)
            year = get_calendar_year(game_state.week)
            score_boost = min(2.0, (year - START_YEAR) * 0.05)
            score = round(min(10.0, base_score + score_boost), 1)
            
            r_game = RivalGame(f"{rival.name} {genre}", topic, genre, score, week_developed=game_state.week)
            rival.games.append(r_game)
            
            # Langer Cooldown
            rival.next_release_week = game_state.week + random.randint(40, 80)
            
            return r_game
        return None

class AdvancedCompetitorAI:
    @staticmethod
    def process(rival, game_state):
        # Phase II: Planungsphase 10 Wochen vor Release
        if game_state.week >= (rival.next_release_week - 10) and not getattr(rival, "planned_project", None):
            best_genre = None
            if hasattr(rival, "ai_memory") and rival.ai_memory:
                best_genre = max(rival.ai_memory, key=rival.ai_memory.get)
            
            personality = getattr(rival, "ai_personality", "Balanced")
            topic = random.choice(TREND_TOPICS)["topic"]
            genre = random.choice(TREND_GENRES)["genre"]

            # Sabotage Logik in Planung
            if game_state.is_developing and game_state.active_project:
                target_genre = game_state.active_project.genre
                sabotage_chance = 0.2
                if personality == "Aggressive": sabotage_chance = 0.5
                if personality == "Trendchaser": sabotage_chance = 0.4
                if random.random() < sabotage_chance:
                    genre = target_genre
            
            # Trendchaser beachtet aktuellen Trend
            if personality == "Trendchaser" and hasattr(game_state, "current_trend") and game_state.current_trend:
                if random.random() < 0.7:
                     if game_state.current_trend.get("genre"): genre = game_state.current_trend["genre"]
                     if game_state.current_trend.get("topic"): topic = game_state.current_trend.get("topic")

            if best_genre and random.random() < 0.3:
                genre = best_genre
                
            rival.planned_project = {"topic": topic, "genre": genre}

        if game_state.week >= rival.next_release_week:
            plan = getattr(rival, "planned_project", None)
            topic = plan["topic"] if plan else random.choice(TREND_TOPICS)["topic"]
            genre = plan["genre"] if plan else random.choice(TREND_GENRES)["genre"]
            rival.planned_project = None

            # Score-Berechnung (Besser)
            base_score = random.uniform(6.0, 9.0)
            personality = getattr(rival, "ai_personality", "Balanced")
            if personality == "Perfectionist":
                base_score = random.uniform(7.5, 9.5)
            
            year = get_calendar_year(game_state.week)
            score_boost = min(3.0, (year - START_YEAR) * 0.15)
            
            score = round(min(10.0, base_score + score_boost), 1)
            
            # Q-Learning Gedächtnis
            if not hasattr(rival, "ai_memory"):
                rival.ai_memory = {}
            if genre in rival.ai_memory:
                rival.ai_memory[genre] = (rival.ai_memory[genre] + score) / 2
            else:
                rival.ai_memory[genre] = score
            
            r_game = RivalGame(f"{rival.name} {genre}", topic, genre, score, week_developed=game_state.week)
            rival.games.append(r_game)
            
            # Cooldown
            cooldown = random.randint(30, 60)
            if personality == "Aggressive":
                cooldown = random.randint(20, 40)
            elif personality == "Perfectionist":
                cooldown = random.randint(50, 100)
                
            rival.next_release_week = game_state.week + cooldown
            
            # Sabotage-Effekt in logic.py wird durch Genre-Überschneidung getriggert
            return r_game
        return None

def evaluate_turn(rival, game_state):
    """
    Haupt-Schnittstelle, die jede Woche in game_state._process_rivals() aufgerufen wird.
    """
    difficulty = getattr(game_state, "difficulty", 1)
    
    if difficulty >= 2:
        return AdvancedCompetitorAI.process(rival, game_state)
    else:
        return BasicCompetitorAI.process(rival, game_state)
