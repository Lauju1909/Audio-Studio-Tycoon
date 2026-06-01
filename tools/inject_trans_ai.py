import os

new_keys_de = """
    "use_ai_assets": "KI-Assets generieren (Risikoreich!)",
    "ai_assets_used_msg": "KI-Assets generiert! Der Fortschritt ist massiv gestiegen.",
    "ai_email_sender": "Lead Developer",
    "ai_email_subject": "KI-Assets integriert",
    "ai_email_body": "Boss, wir haben die KI-Assets ins Spiel integriert. Das spart uns Wochen an Arbeit! Hoffen wir, dass niemand merkt, woher die Daten stammen...",
    "lawsuit_email_sender": "Anwaltskanzlei",
    "lawsuit_email_subject": "URHEBERRECHTSVERLETZUNG!",
    "lawsuit_email_body": "Sie werden wegen Urheberrechtsverletzung durch KI-generierte Assets in {game} verklagt! Strafe: {cost} Euro. Die Fans sind empört!",
"""

new_keys_en = """
    "use_ai_assets": "Generate AI Assets (High Risk!)",
    "ai_assets_used_msg": "AI assets generated! Progress has increased massively.",
    "ai_email_sender": "Lead Developer",
    "ai_email_subject": "AI Assets Integrated",
    "ai_email_body": "Boss, we integrated AI assets into the game. This saves us weeks of work! Let's hope no one notices where the data comes from...",
    "lawsuit_email_sender": "Law Firm",
    "lawsuit_email_subject": "COPYRIGHT INFRINGEMENT!",
    "lawsuit_email_body": "You are being sued for copyright infringement due to AI-generated assets in {game}! Fine: {cost} Euros. The fans are outraged!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
