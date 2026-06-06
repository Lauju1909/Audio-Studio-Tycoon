import random
from game_data import TREND_TOPICS, TREND_GENRES, START_YEAR, WEEKS_PER_YEAR
from models import RivalGame

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
            rival.planned_project = None  # Reset

            # Basis-Score (schlechter als Advanced)
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

            # Sabotage-Logik: Rivale plant im gleichen Genre wie Spieler
            if game_state.is_developing:
                targets = [ap["project"].genre for ap in game_state.active_projects]
                target_genre = random.choice(targets)
                sabotage_chance = 0.2
                if personality == "Aggressive":
                    sabotage_chance = 0.5
                if personality == "Trendchaser":
                    sabotage_chance = 0.4
                if random.random() < sabotage_chance:
                    genre = target_genre

            # Trendchaser verfolgt aktuellen Trend
            if personality == "Trendchaser" and hasattr(game_state, "current_trend") and game_state.current_trend:
                if random.random() < 0.7:
                    if game_state.current_trend.get("genre"):
                        genre = game_state.current_trend["genre"]
                    if game_state.current_trend.get("topic"):
                        topic = game_state.current_trend.get("topic")

            # Gedächtnis: bestes Genre bevorzugen
            if best_genre and random.random() < 0.3:
                genre = best_genre

            # NEU: Marktreaktion – wenn Spieler viele Fans hat, Gegendruck aufbauen
            if game_state.fans > 500000 and personality == "Aggressive":
                # Wähle das Genre des zuletzt erschienenen Spieler-Spiels
                if game_state.game_history:
                    last_player_game = game_state.game_history[-1]
                    genre = last_player_game.genre
                    topic = last_player_game.topic

            rival.planned_project = {"topic": topic, "genre": genre}

        if game_state.week >= rival.next_release_week:
            plan = getattr(rival, "planned_project", None)
            topic = plan["topic"] if plan else random.choice(TREND_TOPICS)["topic"]
            genre = plan["genre"] if plan else random.choice(TREND_GENRES)["genre"]
            rival.planned_project = None

            # Score-Berechnung (besser als Basic)
            base_score = random.uniform(6.0, 9.0)
            personality = getattr(rival, "ai_personality", "Balanced")
            if personality == "Perfectionist":
                base_score = random.uniform(7.5, 9.5)

            year = get_calendar_year(game_state.week)
            score_boost = min(3.0, (year - START_YEAR) * 0.15)

            # NEU: Rivale lernt aus Spieler-Erfolg
            player_avg = 0.0
            if game_state.game_history:
                recent = game_state.game_history[-3:]
                scores = [g.review.average for g in recent if g.review]
                if scores:
                    player_avg = sum(scores) / len(scores)

            # Je besser der Spieler, desto stärker wird die Konkurrenz
            if player_avg > 8.0:
                base_score = min(10.0, base_score + 0.5)
            elif player_avg > 6.0:
                base_score = min(10.0, base_score + 0.2)

            score = round(min(10.0, base_score + score_boost), 1)

            # Q-Learning Gedächtnis updaten
            if not hasattr(rival, "ai_memory"):
                rival.ai_memory = {}
            if genre in rival.ai_memory:
                rival.ai_memory[genre] = (rival.ai_memory[genre] + score) / 2
            else:
                rival.ai_memory[genre] = score

            r_game = RivalGame(f"{rival.name} {genre}", topic, genre, score, week_developed=game_state.week)
            rival.games.append(r_game)

            # Cooldown (persönlichkeitsabhängig)
            cooldown = random.randint(30, 60)
            if personality == "Aggressive":
                cooldown = random.randint(20, 40)
            elif personality == "Perfectionist":
                cooldown = random.randint(50, 100)

            rival.next_release_week = game_state.week + cooldown

            # NEU: Mitarbeiter-Abwerbungs-Intensivierung wenn Rivale aggressiv ist
            if personality == "Aggressive" and random.random() < 0.15:
                if not hasattr(rival, "pending_headhunt"):
                    rival.pending_headhunt = True

            return r_game
        return None


def evaluate_turn(rival, game_state):
    """
    Haupt-Schnittstelle, die jede Woche in game_state._process_rivals() aufgerufen wird.
    Nutzt AdvancedCompetitorAI bei Schwierigkeit >= 2, sonst BasicCompetitorAI.
    """
    difficulty = getattr(game_state, "difficulty", 1)

    if difficulty >= 2:
        return AdvancedCompetitorAI.process(rival, game_state)
    else:
        return BasicCompetitorAI.process(rival, game_state)
