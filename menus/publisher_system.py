import pygame
from ui.router import register_menu
from translations import get_text

@register_menu('publisher_hub')
class PublisherHubMenu:
    """Hauptmenü für das neue Publisher-System (B1)."""
    def __init__(self, audio, state):
        self.audio = audio
        self.state = state
        self.title = get_text("publisher_title")
        self.options = [
            {"text": get_text("publisher_deals_title"), "action": "deals"},
            {"text": "Zurück", "action": "back"} # Hardcoded fallback if key missing
        ]
        self.current_index = 0

    def announce_entry(self):
        self.audio.say_interrupt(self.title)
        self._speak_current()

    def _speak_current(self):
        self.audio.say_interrupt(self.options[self.current_index]["text"])

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_index = (self.current_index - 1) % len(self.options)
                self.audio.play_sound("bump")
                self._speak_current()
            elif event.key == pygame.K_DOWN:
                self.current_index = (self.current_index + 1) % len(self.options)
                self.audio.play_sound("bump")
                self._speak_current()
            elif event.key == pygame.K_RETURN:
                action = self.options[self.current_index]["action"]
                if action == "back":
                    return "main_menu"
                elif action == "deals":
                    return "publisher_deals_list"
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None

@register_menu('publisher_deals_list')
class PublisherDealsListMenu:
    """Zeigt verfügbare Deals an und erlaubt deren Abschluss."""
    def __init__(self, audio, state):
        self.audio = audio
        self.state = state
        self.title = get_text("publisher_deals_title")
        
        # Neue Deals für Ansicht generieren
        self.state.publisher_manager.generate_deals()
        
        self.options = []
        for deal in self.state.publisher_manager.available_deals:
            text = get_text("publisher_deal_info").format(
                name=deal.publisher_name,
                funding=deal.upfront_funding,
                share=deal.rev_share_percent,
                deadline=deal.deadline_weeks,
                quality=deal.min_quality
            )
            self.options.append({"text": text, "deal_id": deal.id})
        
        if not self.options:
            self.options.append({"text": get_text("publisher_no_deals"), "deal_id": None})
            
        self.options.append({"text": "Zurück", "action": "back"})
        self.current_index = 0

    def announce_entry(self):
        self.audio.say_interrupt(self.title)
        self._speak_current()

    def _speak_current(self):
        self.audio.say_interrupt(self.options[self.current_index]["text"])

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_index = (self.current_index - 1) % len(self.options)
                self.audio.play_sound("bump")
                self._speak_current()
            elif event.key == pygame.K_DOWN:
                self.current_index = (self.current_index + 1) % len(self.options)
                self.audio.play_sound("bump")
                self._speak_current()
            elif event.key == pygame.K_RETURN:
                opt = self.options[self.current_index]
                if opt.get("action") == "back" or not opt.get("deal_id"):
                    return "publisher_hub"
                elif opt.get("deal_id"):
                    success = self.state.publisher_manager.sign_deal(opt["deal_id"])
                    if success:
                        self.audio.say_interrupt(get_text("publisher_contract").format(name=opt['deal_id'].split('_')[0]))
                        return "publisher_hub"
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                return "publisher_hub"
        return None
