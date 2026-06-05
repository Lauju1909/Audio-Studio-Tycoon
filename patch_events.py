import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_events = """
    "RES_EMPLOYEE_EVENTS": "Mitarbeiter-Events",
    "RES_EMPLOYEE_EVENTS_DESC": "Erforsche regelmäßige Events, um die Motivation deiner Belegschaft zu boosten.",
"""

en_events = """
    "RES_EMPLOYEE_EVENTS": "Employee Events",
    "RES_EMPLOYEE_EVENTS_DESC": "Research regular events to boost the motivation of your workforce.",
"""

if '"RES_EMPLOYEE_EVENTS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_events)
    content = content.replace('"EN": {', '"EN": {\n' + en_events)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Employee Events Translations added.")
else:
    print("Employee Events Translations already exist.")
