from threading import Thread


class LeaderboardManager:
    """
    Mock-Manager für globale Online-Leaderboards.
    Simuliert asynchrone Netzwerk-Anfragen (Dummy-Requests).
    """

    def __init__(self, state):
        self.state = state
        self.scores = [
            {"name": "Dev_Lauri", "score": 99999999, "prestige": 1000},
            {"name": "AudioTycoon_Pro", "score": 50000000, "prestige": 850},
            {"name": "NoobMaster", "score": 1000000, "prestige": 120},
            {"name": "SoundGuru", "score": 25000000, "prestige": 500},
        ]
        self.is_fetching = False

    def get_top_scores(self, callback):
        """Mockt einen Netzwerk-Request um Top-Scores zu laden."""
        if self.is_fetching:
            return

        self.is_fetching = True

        def fetch_task():
            # Dummy delay
            import time

            time.sleep(1)
            # Sort scores dynamically
            sorted_scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)
            self.is_fetching = False
            callback(sorted_scores)

        Thread(target=fetch_task, daemon=True).start()

    def submit_score(self, name, score, prestige, callback=None):
        """Mockt das Senden eines Scores."""

        def submit_task():
            import time

            time.sleep(1)
            # Update if exists, else append
            existing = next((x for x in self.scores if x["name"] == name), None)
            if existing:
                if score > existing["score"]:
                    existing["score"] = score
                    existing["prestige"] = prestige
            else:
                self.scores.append({"name": name, "score": score, "prestige": prestige})

            if callback:
                callback(True)

        Thread(target=submit_task, daemon=True).start()
