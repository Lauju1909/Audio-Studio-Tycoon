import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_finish = '''    def _finish_update_project(self, update):
        """Wendet die Effekte eines fertigen Updates/DLCs an."""
        game = next((g for g in self.game_history if g.name == update.base_game_name), None)
        if not game: return

        game.updates.append(update)

        if update.update_type == "Patch":
            bugs_to_fix = int(game.bugs * 0.5) + 1
            game.bugs = max(0, game.bugs - bugs_to_fix)
            game.total_bugs_fixed += bugs_to_fix
        elif update_type == "Content":
            game.hype += 10
            self.fans += 500
        elif update_type == "DLC":
            game.dlc_count += 1
            game.is_active = True
            game.sales += int(game.sales * 0.1) # 10% kaufen den DLC sofort'''

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
            game.hype += 10
            self.fans += 500
        elif update.update_type == "DLC":
            game.dlc_count += 1
            game.is_active = True
            game.sales += int(game.sales * 0.1) # 10% kaufen den DLC sofort'''

content = content.replace(old_finish, new_finish)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched update_type to update.update_type")
