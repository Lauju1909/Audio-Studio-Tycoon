
with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            {'text': self.game_state.get_text('office_perks_menu'), 'action': lambda: "office_perks_menu"},"""

replacement = """            {'text': self.game_state.get_text('office_perks_menu'), 'action': lambda: "office_perks_menu"},
            {'text': "Mitarbeiter-Talentbäume (Skill Tree)", 'action': lambda: "talent_tree_menu"},"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/office.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched HRMenu for Talent-Bäume")
else:
    print("Could not find target in HRMenu")
