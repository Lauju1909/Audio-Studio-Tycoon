import codecs

lines = []
with codecs.open('translations.py', 'r', 'utf-8') as f:
    lines = f.readlines()

de_lines = []
en_lines = []

de_dict = {
    'hardware_dev': 'Hardware-Labor',
    'create_console': 'Neue Konsole entwickeln',
    'console_reqs_not_met': 'Gesperrt (Benötigt Jahr 2001 & 100 Mio EUR)',
    'my_consoles': 'Meine Konsolen ansehen',
    'create_console_title': 'Gebe den Namen der neuen Konsole ein',
    'console_name_prompt': 'Konsolen-Name:',
    'console_specs': 'Konsolen-Spezifikationen festlegen',
    'console_arch': 'Architektur',
    'console_perf': 'Leistung (1-10)',
    'console_marketing': 'Marketing-Budget',
    'console_dev_started': 'Konsolenentwicklung gestartet! Die R&D-Phase wird mehrere Jahre dauern.',
    'subject_console_done': 'Konsole {name} ist fertig!',
    'body_console_done': 'Die Entwicklung der {name} ist abgeschlossen! Sie ist nun auf dem Markt und generiert Hardware-Umsätze. Veröffentliche exklusive Spiele für deine Plattform, um die Konsolen-Verkäufe massiv zu pushen!',
    'sender_hardware': 'Hardware-Team'
}

en_dict = {
    'hardware_dev': 'Hardware Lab',
    'create_console': 'Develop New Console',
    'console_reqs_not_met': 'Locked (Requires Year 2001 & 100m EUR)',
    'my_consoles': 'View My Consoles',
    'create_console_title': 'Enter the name of your new console',
    'console_name_prompt': 'Console Name:',
    'console_specs': 'Set Console Specifications',
    'console_arch': 'Architecture',
    'console_perf': 'Performance (1-10)',
    'console_marketing': 'Marketing Budget',
    'console_dev_started': 'Console development started! The R&D phase will take several years.',
    'subject_console_done': 'Console {name} is complete!',
    'body_console_done': 'Development of {name} has finished! It is now on the market and generating hardware revenue. Release exclusive games for your platform to massively boost console sales!',
    'sender_hardware': 'Hardware Team'
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
