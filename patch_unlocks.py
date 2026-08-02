
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add is_feature_unlocked method to GameState
method_str = """
    def is_feature_unlocked(self, feature_id):
        \"\"\"Prüft ob ein Feature laut FEATURE_UNLOCKS verfügbar ist.\"\"\"
        from game_data import FEATURE_UNLOCKS
        
        feature = FEATURE_UNLOCKS.get(feature_id)
        if not feature:
            return True # If not specified, it's unlocked by default
            
        current_year = self.get_calendar_year()
        if "year" in feature and current_year < feature["year"]:
            return False
            
        if "office_level" in feature and self.office_level < feature["office_level"]:
            return False
            
        return True
"""

# Insert it inside GameState, right after get_calendar_year
search_str = 'def get_calendar_year(self):\n        """Gibt das aktuelle Kalenderjahr zurück (Start: START_YEAR)."""\n        return START_YEAR + (self.week - 1) // WEEKS_PER_YEAR'

if search_str in content:
    content = content.replace(search_str, search_str + '\n' + method_str)
    with open('logic.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched logic.py!")
else:
    print("Could not find get_calendar_year method in logic.py")
