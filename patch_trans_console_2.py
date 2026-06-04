import re

DE_KEYS = {
    "console_opt_develop": "Eigene Konsole entwickeln",
    "console_active_stats": "{name}: {users} Nutzer | Gewinn: {revenue}€",
    "console_in_dev": "Konsole {name} in Entwicklung ({progress}%)",
    "console_name_prompt": "Gib einen Namen für deine Konsole ein:",
    "console_comp_title": "Konsolen-Komponenten wählen",
    "console_tier_opt": "{tier} (Kosten: {cost}€, Preis: {price}€, Tech: +{tech})",
    "console_started": "Entwicklung der Konsole {name} gestartet!",
    "console_finished": "Die Konsole {name} ist fertiggestellt und nun auf dem Markt!"
}

EN_KEYS = {
    "console_opt_develop": "Develop custom console",
    "console_active_stats": "{name}: {users} Users | Profit: ",
    "console_in_dev": "Console {name} in development ({progress}%)",
    "console_name_prompt": "Enter a name for your console:",
    "console_comp_title": "Select Console Components",
    "console_tier_opt": "{tier} (Cost: , Price: , Tech: +{tech})",
    "console_started": "Started development of console {name}!",
    "console_finished": "The console {name} is finished and now on the market!"
}

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of "de" dict
de_match = re.search(r'"de"\s*:\s*\{', content)
if de_match:
    de_idx = de_match.end()
    insert_str = ""
    for k, v in DE_KEYS.items():
        insert_str += f'        "{k}": "{v}",\n'
    content = content[:de_idx] + "\n" + insert_str + content[de_idx:]

en_match = re.search(r'"en"\s*:\s*\{', content)
if en_match:
    en_idx = en_match.end()
    insert_str = ""
    for k, v in EN_KEYS.items():
        insert_str += f'        "{k}": "{v}",\n'
    content = content[:en_idx] + "\n" + insert_str + content[en_idx:]

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Translations correctly added.")
