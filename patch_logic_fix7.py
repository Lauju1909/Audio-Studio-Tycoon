import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_finish = '''    def _finish_update_project(self, update):
        """Wendet die Effekte eines fertigen Updates/DLCs an."""
        game = next((g for g in self.game_history if g.name == update.base_game_name), None)
        if not game: return
        
        print(f"Finishing update: {update.update_type} for {game.name}"); game.updates.append(update)
        
        if update.update_type == "Patch":
            bugs_to_fix = int(game.bugs * 0.5) + 1
            game.bugs = max(0, game.bugs - bugs_to_fix)
            game.total_bugs_fixed += bugs_to_fix
        elif update.update_type == "Content":
            self.fans += 500
            self.hype = min(100, self.hype + 20)
        elif update.update_type == "Language":
            for l in update.languages:
                if l not in game.languages:
                    game.languages.append(l)'''

new_finish = '''    def _finish_update_project(self, update):
        """Wendet die Effekte eines fertigen Updates/DLCs an."""
        game = next((g for g in self.game_history if g.name == update.base_game_name), None)
        if not game: return
        
        game.updates.append(update)
        
        if update.update_type == "Patch":
            bugs_to_fix = int(game.bugs * 0.5) + 1
            game.bugs = max(0, game.bugs - bugs_to_fix)
            game.total_bugs_fixed += bugs_to_fix
        elif update.update_type == "Content":
            self.fans += 500
            self.hype = min(100, self.hype + 20)
        elif update.update_type == "Language":
            for l in update.languages:
                if l not in game.languages:
                    game.languages.append(l)
        elif update.update_type == "DLC":
            game.dlc_count += 1
            game.is_active = True
            game.sales += int(game.sales * 0.1)'''

content = content.replace(old_finish, new_finish)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
