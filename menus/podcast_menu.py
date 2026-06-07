class PodcastMenu:
    def __init__(self, engine, previous_menu):
        self.engine = engine
        self.previous_menu = previous_menu
        self.logic = engine.logic
        if not hasattr(self.logic, "podcast_network"):
            from models import PodcastNetwork
            self.logic.podcast_network = PodcastNetwork()

    def show(self):
        self.engine.audio.speak(self.logic.get_text("podcast_menu_title", default="Podcast & Hörbuch Produktion"))
        while True:
            options = []
            
            if not self.logic.podcast_network.is_active:
                options.append(self.logic.get_text("podcast_setup", default="Podcast-Netzwerk gründen (100.000 €)"))
            else:
                info = f"Abonnenten: {self.logic.podcast_network.subscribers} | Ruf: {self.logic.podcast_network.reputation}"
                options.append(f"Info: {info}")
                options.append(self.logic.get_text("podcast_new", default="Neues Audio-Format produzieren"))
                options.append(self.logic.get_text("podcast_list", default="Aktive Produktionen verwalten"))
                
            options.append(self.logic.get_text("back", default="Zurück"))

            sel = self.engine.run_menu("Podcast & Hörbuch", options)
            if sel == len(options) - 1:
                return
            
            opt_text = options[sel]
            if "gründen" in opt_text:
                if self.logic.money >= 100000:
                    self.logic.money -= 100000
                    self.logic.podcast_network.is_active = True
                    self.logic.podcast_network.subscribers = 500
                    self.logic.podcast_network.reputation = 50
                    self.engine.audio.speak(self.logic.get_text("podcast_setup_success", default="Netzwerk gegründet!"))
                else:
                    self.engine.audio.speak(self.logic.get_text("not_enough_money", default="Nicht genug Geld."))
            elif "Neues" in opt_text:
                self.create_podcast()
            elif "Aktive" in opt_text:
                self.list_podcasts()
            elif "Info" in opt_text:
                self.engine.audio.speak(info)

    def create_podcast(self):
        formats = ["Täglich", "Wöchentlich", "Hörbuch"]
        sel = self.engine.run_menu("Format wählen", formats + ["Zurück"])
        if sel == len(formats): return
        fmt = formats[sel]
        
        name = self.engine.get_text_input("Name der Produktion eingeben:")
        if not name: return
        
        topic = self.engine.get_text_input("Thema eingeben:")
        if not topic: return
        
        # Simple quality generation based on staff
        qual = min(100, 40 + len(self.logic.employees) * 5)
        
        cost = 10000 if fmt == "Hörbuch" else 2000
        if self.logic.money >= cost:
            self.logic.money -= cost
            from models import PodcastProduction
            p = PodcastProduction(name, topic, fmt, qual)
            self.logic.podcast_network.active_podcasts.append(p)
            self.engine.audio.speak(f"{fmt} {name} wird nun produziert! Kosten: {cost} Euro.")
        else:
            self.engine.audio.speak(self.logic.get_text("not_enough_money", default="Nicht genug Geld."))

    def list_podcasts(self):
        while True:
            pods = self.logic.podcast_network.active_podcasts
            if not pods:
                self.engine.audio.speak("Keine aktiven Produktionen.")
                return
                
            opts = [f"{p.name} ({p.format_type}) - Qualität: {p.quality} - Einnahmen: {p.total_revenue} €" for p in pods]
            opts.append("Zurück")
            sel = self.engine.run_menu("Produktionen", opts)
            if sel == len(opts) - 1: return
            
            p = pods[sel]
            action = self.engine.run_menu(p.name, ["Einstellen", "Zurück"])
            if action == 0:
                self.logic.podcast_network.active_podcasts.remove(p)
                self.engine.audio.speak(f"{p.name} wurde eingestellt.")
