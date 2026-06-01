import os

new_keys_de = """
    "influencer_event_title": "INFLUENCER-SKANDAL!",
    "influencer_event_desc": "Boss! Unser gesponserter Streamer hat in {game} live vor Millionen Zuschauern Cheats verwendet und das Spiel massiv beleidigt! Die PR ist ein Desaster. Was tun wir?",
    "influencer_opt_1": "Öffentlich entschuldigen (-Fans, rettet Image)",
    "influencer_opt_2": "Fristlos feuern & klagen (-Viel Geld, bewahrt Ehre)",
    "influencer_opt_3": "Ignorieren (Riskant, kann Langzeit-Verkäufe ruinieren)",
    "influencer_res_1": "Wir haben uns entschuldigt. Die Presse beruhigt sich, aber einige Hardcore-Fans sind weg.",
    "influencer_res_2": "Streamer gefeuert! Vertragsstrafen kosten uns {cost} Euro, aber die Gamer respektieren uns dafür!",
    "influencer_res_3_bad": "Das Ignorieren war ein Fehler! Ein gigantischer Shitstorm zerstört das Spiel und wir verlieren massig Fans!",
    "influencer_res_3_good": "Glück gehabt. Das Internet hat den Skandal in wenigen Tagen vergessen. Keine Konsequenzen!",
"""

new_keys_en = """
    "influencer_event_title": "INFLUENCER SCANDAL!",
    "influencer_event_desc": "Boss! Our sponsored streamer used cheats in {game} live in front of millions of viewers and insulted the game massively! The PR is a disaster. What do we do?",
    "influencer_opt_1": "Apologize publicly (-Fans, saves image)",
    "influencer_opt_2": "Fire immediately & sue (-Lots of money, preserves honor)",
    "influencer_opt_3": "Ignore (Risky, can ruin long-term sales)",
    "influencer_res_1": "We apologized. The press calmed down, but some hardcore fans are gone.",
    "influencer_res_2": "Streamer fired! Contract penalties cost us {cost} Euros, but gamers respect us for it!",
    "influencer_res_3_bad": "Ignoring it was a mistake! A massive shitstorm destroys the game and we lose a ton of fans!",
    "influencer_res_3_good": "Got lucky. The internet forgot about the scandal in a few days. No consequences!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
