import random
from models import Email


class EsportsManager:
    def __init__(self, state):
        self.state = state

    def tick(self):
        if self.state.get_calendar_year() < 2000:
            return
        self._process_tournaments()
        self._process_esports_leagues()

    def _process_tournaments(self):
        """Verarbeitet aktive E-Sport-Turniere: liefert Einnahmen, Hype und Fans."""
        if not getattr(self.state, "active_tournaments", []):
            return
        finished = []
        for tournament in self.state.active_tournaments:
            tournament["weeks_left"] = tournament.get("weeks_left", 4) - 1
            if tournament["weeks_left"] <= 0:
                finished.append(tournament)
        for t in finished:
            self.state.active_tournaments.remove(t)
            prize = t.get("prize_pool", 50000)
            hype_gain = t.get("hype_bonus", 20)
            fan_gain = t.get("fan_bonus", 10000)
            self.state.track_income("other", prize)
            self.state.hype = min(250, self.state.hype + hype_gain)
            self.state.fans += fan_gain
            self.state.emails.insert(
                0,
                Email(
                    sender=self.state.get_text("sender_industry_news"),
                    subject=self.state.get_text(
                        "esports_result_subject", name=t.get("name", "Turnier")
                    ),
                    body=self.state.get_text(
                        "esports_result_body",
                        name=t.get("name", "Turnier"),
                        prize=prize,
                        fans=fan_gain,
                        hype=hype_gain,
                    ),
                    date_week=self.state.week,
                ),
            )
            if hasattr(self.state, "audio"):
                self.state.audio.play_sound("cheer")
                self.state.audio.speak(
                    self.state.get_text(
                        "esports_result_subject", name=t.get("name", "Turnier")
                    ),
                    interrupt=False,
                )

    def _process_esports_leagues(self):
        """Verarbeitet aktive E-Sports-Ligen woechentlich:
        - Hype-Zerfall (0.3-0.5% pro Woche, geschuetzt durch Sponsor-Tier)
        - Passive Sponsoren-Einnahmen basierend auf Tier, Hype und Fans
        - Aktive Spieler-Retention (GaaS-Boost)
        - Streaming-Deal-Einnahmen woechentlich
        """
        leagues = getattr(self.state, "esports_leagues", [])
        if not leagues:
            return

        total_passive_income = 0

        for league in leagues:
            # 1. Hype-Zerfall: Tier schuetzt vor schnellem Verfall
            tier_data = league.get_sponsor_tier_data()
            hype_min = tier_data["hype_min"]
            decay_rate = (
                0.997
                if league.sponsor_tier == "global"
                else 0.995
                if league.sponsor_tier == "national"
                else 0.993
                if league.sponsor_tier == "regional"
                else 0.990
                if league.sponsor_tier == "local"
                else 0.988
            )
            league.hype = max(hype_min, league.hype * decay_rate)

            # 2. Sponsoren-Einnahmen basierend auf Tier
            sponsor_weekly = league.calculate_weekly_sponsor_income(
                self.state.fans, getattr(self.state, "hype", 50)
            )
            if sponsor_weekly > 0:
                variation = random.uniform(0.9, 1.1)
                sponsor_weekly = int(sponsor_weekly * variation)
                league.total_sponsor_income += sponsor_weekly
                total_passive_income += sponsor_weekly

            # 3. Streaming-Deal-Einnahmen
            if league.streaming_deals > 0:
                stream_income = int(
                    league.streaming_deals * 50000 * (league.hype / 100.0)
                )
                stream_income = int(stream_income * random.uniform(0.85, 1.15))
                league.total_sponsor_income += stream_income
                total_passive_income += stream_income

            # 4. Aktive Spieler-Retention: Spiel bleibt relevant
            game = next(
                (g for g in self.state.game_history if g.name == league.game_name), None
            )
            if game:
                retention_boost = max(
                    200, int(self.state.fans * 0.005 * (league.hype / 100.0))
                )
                game.active_players = max(
                    getattr(game, "active_players", 0), retention_boost
                )

            # 5. Hype global boostet leicht, wenn Liga aktiv
            hype_boost = 0.1 * (league.hype / 100.0)
            self.state.hype = min(100, getattr(self.state, "hype", 50) + hype_boost)

        if total_passive_income > 0:
            self.state.track_income("esports", total_passive_income)
