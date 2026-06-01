import os

new_keys_de = """
    "union_form_title": "GEWERKSCHAFTS-GRÜNDUNG!",
    "union_form_desc": "Boss, die miese Moral und der Stress haben das Fass zum Überlaufen gebracht. Die Mitarbeiter haben eine Gewerkschaft gegründet! Sie fordern sofortige Verhandlungen.",
    "union_strike_title": "STREIKDROHUNG!",
    "union_strike_desc": "Die Gewerkschaft ist unzufrieden! Wenn wir nicht zahlen, legen sie ab morgen die Arbeit nieder. Was sollen wir tun?",
    "union_opt_1": "Gehälter anpassen (+30% für alle, Moral steigt)",
    "union_opt_2": "Einmaliger Bonus (10k pro Mitarbeiter, keine Dauerlösung)",
    "union_opt_3": "Union-Busting betreiben (Feuert Rädelsführer, illegal & riskant)",
    "union_opt_4": "Ignorieren (STREIK!)",
    "union_res_1": "Die Gehälter wurden erhöht. Die Mitarbeiter sind glücklich und die Arbeit geht weiter!",
    "union_res_2": "Ein Bonus von {cost} Euro wurde gezahlt. Sie sind vorerst ruhig.",
    "union_res_3_success": "Rädelsführer gefeuert! Die Gewerkschaft ist zerschlagen, aber die Fans sind angewidert!",
    "union_res_3_fail": "Union-Busting aufgeflogen! Strafzahlung von 500.000 Euro! Fans hassen uns und die Gewerkschaft bleibt!",
    "union_res_4": "STREIK! Die gesamte Spieleentwicklung ruht und es kostet uns jede Woche ein Vermögen!",
"""

new_keys_en = """
    "union_form_title": "UNION FORMATION!",
    "union_form_desc": "Boss, the terrible morale and stress were the last straw. The employees have formed a union! They demand immediate negotiations.",
    "union_strike_title": "STRIKE THREAT!",
    "union_strike_desc": "The union is unhappy! If we don't pay up, they will strike tomorrow. What should we do?",
    "union_opt_1": "Adjust salaries (+30% for all, morale rises)",
    "union_opt_2": "One-time bonus (10k per employee, no permanent fix)",
    "union_opt_3": "Union-Busting (Fires leaders, illegal & risky)",
    "union_opt_4": "Ignore (STRIKE!)",
    "union_res_1": "Salaries were raised. The employees are happy and work continues!",
    "union_res_2": "A bonus of {cost} Euros was paid. They are quiet for now.",
    "union_res_3_success": "Ring leaders fired! The union is crushed, but the fans are disgusted!",
    "union_res_3_fail": "Union busting exposed! Fine of 500,000 Euros! Fans hate us and the union stays!",
    "union_res_4": "STRIKE! All game development halts and it costs us a fortune every week!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
