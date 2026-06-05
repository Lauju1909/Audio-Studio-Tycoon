import sys

with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to OfficeMenu options
# Look for self.options.append(("Urlaub", lambda: self.state.open_menu(VacationMenu(self.state))))
target = 'self.options.append(("Urlaub", lambda: self.state.open_menu(VacationMenu(self.state))))'
replacement = target + '\n        self.options.append((self.state.get_text("menu_merchandising"), lambda: self.state.open_menu(MerchandisingMenu(self.state))))'

if 'MerchandisingMenu(self.state)' not in content:
    content = content.replace(target, replacement)
    with open('menus/office.py', 'w', encoding='utf-8') as f:
        f.write(content)

