import os
import re

with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

if "SubscriptionVaultMenu" not in main_code:
    main_code = main_code.replace("MerchAmountMenu,", "MerchAmountMenu, SubscriptionVaultMenu, CreatorSponsorshipMenu,")
    main_code = main_code.replace('"merch_menu": lambda: MerchMenu(audio, state),', '"merch_menu": lambda: MerchMenu(audio, state),\n        "subscription_add_game_menu": lambda: SubscriptionVaultMenu(audio, state),\n        "creator_menu": lambda: CreatorSponsorshipMenu(audio, state),')

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

print("Main patched.")

with open("translations.py", "r", encoding="utf-8") as f:
    trans_code = f.read()

if "subscription_add_game" not in trans_code:
    en = """
        "subscription_add_game": "Add released game to Subscription Vault",
        "subscription_vault_title": "Subscription Vault",
        "subscription_put_in_vault": "Put '{name}' into Vault",
        "subscription_added_to_vault": "'{name}' is now in the Subscription Vault!",
        "creator_small": "Small Streamer",
        "creator_medium": "Medium Streamer",
        "creator_large": "Mega Streamer",
        "creator_menu_title": "Content Creator Sponsoring",
        "creator_sponsor_option": "Sponsor {name} (Cost: {cost:,} EUR)",
        "creator_fail_money": "Not enough money for this sponsorship! Required: {cost:,} EUR.",
        "creator_success": "Successfully sponsored {name}! Your games will see a sales boost for the next 4 weeks.",
        "upgrade_campus": "Company Campus",
"""
    de = """
        "subscription_add_game": "Veröffentlichtes Spiel in den Abo-Tresor hinzufügen",
        "subscription_vault_title": "Abo-Tresor",
        "subscription_put_in_vault": "'{name}' in den Tresor aufnehmen",
        "subscription_added_to_vault": "'{name}' befindet sich nun im Abo-Tresor!",
        "creator_small": "Kleiner Streamer",
        "creator_medium": "Mittlerer Streamer",
        "creator_large": "Mega Streamer",
        "creator_menu_title": "Content Creator Sponsoring",
        "creator_sponsor_option": "{name} sponsern (Kosten: {cost:,} EUR)",
        "creator_fail_money": "Nicht genug Geld für dieses Sponsoring! Benötigt: {cost:,} EUR.",
        "creator_success": "{name} erfolgreich gesponsert! Deine Spiele erhalten in den nächsten 4 Wochen einen Verkaufsboost.",
        "upgrade_campus": "Firmen-Campus",
"""
    # Find dictionaries EN and DE
    trans_code = trans_code.replace('"esports_menu_title": "E-Sports & Tournaments",', '"esports_menu_title": "E-Sports & Tournaments",' + en)
    trans_code = trans_code.replace('"esports_menu_title": "E-Sports & Turniere",', '"esports_menu_title": "E-Sports & Turniere",' + de)

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(trans_code)

print("Translations patched.")
