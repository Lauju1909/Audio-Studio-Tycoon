import os

new_keys_de = """
    "menu_movie_deal": "Filmlizenzen verkaufen",
    "movie_deal_success": "Filmdeal für {game} erfolgreich abgeschlossen!",
    "movie_email_sender": "Hollywood Studios",
    "movie_email_subject": "Film Deal!",
    "movie_email_body": "Wir machen einen Film aus {game}! Sie erhalten {money} Euro und wir rechnen mit ca. {fans} neuen Fans durch die Kinobesucher!",
"""

new_keys_en = """
    "menu_movie_deal": "Sell Movie Licenses",
    "movie_deal_success": "Movie deal for {game} successfully concluded!",
    "movie_email_sender": "Hollywood Studios",
    "movie_email_subject": "Movie Deal!",
    "movie_email_body": "We are making a movie out of {game}! You receive {money} Euros and we expect around {fans} new fans from moviegoers!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
