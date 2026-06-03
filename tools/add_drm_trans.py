import codecs

lines = []
with codecs.open('translations.py', 'r', 'utf-8') as f:
    lines = f.readlines()

de_lines = []
en_lines = []

de_dict = {
    'drm_choice_title': 'Kopierschutz (DRM) wählen',
    'drm_none': 'Kein DRM (Massive Piraterie, +Review Bonus)',
    'drm_standard': 'Standard DRM (50.000 EUR, Moderate Piraterie)',
    'drm_aggressive': 'Aggressives DRM (200.000 EUR, Wenig Piraterie, -Review Strafe)'
}

en_dict = {
    'drm_choice_title': 'Select Copy Protection (DRM)',
    'drm_none': 'No DRM (Massive Piracy, +Review Bonus)',
    'drm_standard': 'Standard DRM (50,000 EUR, Moderate Piracy)',
    'drm_aggressive': 'Aggressive DRM (200,000 EUR, Low Piracy, -Review Penalty)'
}

for k, v in de_dict.items():
    de_lines.append(f'        "{k}": "{v}",\n')
for k, v in en_dict.items():
    en_lines.append(f'        "{k}": "{v}",\n')

# find en start
en_idx = -1
for i, line in enumerate(lines):
    if '"en": {' in line:
        en_idx = i
        break
lines = lines[:en_idx+1] + en_lines + lines[en_idx+1:]

# find de start
de_idx = -1
for i, line in enumerate(lines):
    if '"de": {' in line:
        de_idx = i
        break
lines = lines[:de_idx+1] + de_lines + lines[de_idx+1:]

with codecs.open('translations.py', 'w', 'utf-8') as f:
    f.writelines(lines)
