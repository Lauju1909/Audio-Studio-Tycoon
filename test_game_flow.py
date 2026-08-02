import time
import translations

translations.set_language('en')

# Simulate what the menu does
class MockMenu:
    def __init__(self):
        self.options = []
        self._update_options()

    def _update_options(self):
        # Let's say we have 3 keys to translate
        keys = ['main_welcome', 'music', 'language', 'settings_menu']
        self.options = [translations.get_text(k) for k in keys]
        print(f"Options updated: {self.options}")

    def update(self):
        if getattr(translations, 'TRANSLATIONS_UPDATED', False):
            translations.TRANSLATIONS_UPDATED = False
            self._update_options()

menu = MockMenu()

# Simulate game loop
for i in range(20):
    menu.update()
    time.sleep(0.5)

print("Final cache keys:", list(translations._TRANSLATION_CACHE.keys()))
