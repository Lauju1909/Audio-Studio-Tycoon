import re

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

missing_de = [
  ('body_burnout', '{name} hat einen Burnout erlitten und faellt fuer {weeks} Wochen aus!'),
  ('content_started', 'Content-Update-Entwicklung gestartet.'),
  ('dlc_started', 'DLC-Entwicklung gestartet.'),
  ('patch_started', 'Patch-Entwicklung gestartet.'),
  ('start_content_update', 'Content-Update entwickeln (Kostenlos)'),
  ('start_dlc', 'DLC entwickeln (Kostenpflichtig)'),
  ('start_patch', 'Patch entwickeln (Bugs beheben)'),
  ('subject_burnout', 'Mitarbeiter-Burnout!'),
  ('vacation_employee_option', '{name} (Erschoepfung: {fatigue}%)'),
  ('vacation_menu_title', 'Mitarbeiter in den Urlaub schicken'),
  ('vacation_none_available', 'Keine verfuegbaren Mitarbeiter.'),
  ('vacation_success', '{name} ist nun fuer 4 Wochen im Urlaub.')
]

idx = content.find('"de": {')
if idx != -1:
    insert_str = ''
    for key, val in missing_de:
        insert_str += f'        "{key}": "{val}",\n'
    new_content = content[:idx+7] + '\n' + insert_str + content[idx+7:]
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Success')
else:
    print('Not found')
