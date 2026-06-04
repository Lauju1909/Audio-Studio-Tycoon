import json

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

# Find the end of 'en' dict
en_str = ""
for k, v in EN_KEYS.items():
    en_str += f'        "{k}": "{v}",\n'

# Find the end of 'de' dict
de_str = ""
for k, v in DE_KEYS.items():
    de_str += f'        "{k}": "{v}",\n'

# Just insert before the end of the dictionaries.
# The dictionaries are nested inside TRANSLATIONS = { "en": { ... }, "de": { ... } }
# They end with "    }," for en and "    }" for de.

# Actually, let's use regex
import re
content = re.sub(r'("z_last_en": ".*",)', r'\1\n' + en_str.rstrip(','), content)
content = re.sub(r'("z_last_de": ".*")', r'\1,\n' + de_str.rstrip(','), content)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Translations added.")
