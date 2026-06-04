import json

en_keys = {
    'esports_no_eligible_games': 'No eligible games found (Multiplayer/Action/Strategy required).',
    'esports_game_option': '{name} (Sales: {sales})',
    'esports_league_entry': '{name} - Hype: {hype} | Sponsor: {tier} | Events: {championships}',
    'esports_league_detail_title': 'League: {name}',
    'esports_detail_info': 'Game: {name} | Hype: {hype}/100 | Sponsor: {tier} | Events: {championships} | Sponsor Revenue: {sponsor_income} EUR',
    'esports_go_to_championship': 'Host World Championship',
    'esports_champ_done_this_year': 'Championship {year} already held.',
    'esports_manage_sponsor': 'Manage Sponsoring (Current: {tier})',
    'esports_sponsor_title': 'Sponsoring & Streaming',
    'esports_sponsor_tier_none': 'None',
    'esports_sponsor_tier_local': 'Local',
    'esports_sponsor_tier_regional': 'Regional',
    'esports_sponsor_tier_national': 'National',
    'esports_sponsor_tier_global': 'Global',
    'esports_sponsor_info': 'Current Sponsor: {tier} | Weekly approx. {weekly} EUR',
    'esports_sponsor_option': '{action} {tier} ({cost} EUR)',
    'esports_streaming_deal': 'Sign Streaming Deal ({cost} EUR, {current}/{max} active)',
    'esports_streaming_max': 'Maximum Streaming Deals active (5/5).',
    'esports_sponsor_changed': 'Sponsoring Tier changed to: {tier}!',
    'esports_streaming_deal_bought': 'Streaming Deal signed! Active: {deals}/5.',
    'esports_sender': 'E-Sports Team',
    'esports_champ_email_subject': 'World Championship {year}: {game}',
    'esports_champ_email_body': r"The World Championship for '{game}' is over!\nViewers: {viewers}\nRevenue: {revenue} EUR\nPrize pool: {prize} EUR\nNew Fans: +{fans}\nHype: +{hype}",
    'esports_locked': 'E-Sports leagues are available from {year} onward. Keep developing!',
    'esports_create_title': 'Found New E-Sports League',
    'esports_create_league': "Found new league for '{game}' (Cost: {cost} EUR)",
    'esports_league_created': "The '{game}' E-Sports League was successfully founded! Hype +{hype}, Fans +{fans}.",
    'esports_manage_title': 'Manage Active Leagues',
    'esports_manage_leagues': "League '{game}' | Hype: {hype} | Championships: {champ} | Founded: Week {week}",
    'esports_champ_title': "World Championship: '{game}'",
    'esports_champ_small': 'Small Championship Budget ({cost} EUR) - low sponsors',
    'esports_champ_med': 'Medium Championship Budget ({cost} EUR) - good sponsors',
    'esports_champ_huge': 'Mega Championship Budget ({cost} EUR) - maximum reach',
    'esports_champ_result': "Championship '{game}': Budget {cost} EUR. Revenue: {revenue} EUR (Sponsors: {sponsor}, Streaming: {stream}). Fans +{fans}, Hype +{hype}.",
    'esports_champ_done': 'Championship held! Next: next year.'
}

de_keys = {
    'esports_no_eligible_games': 'Keine geeigneten Spiele vorhanden (Multiplayer/Action/Strategie benötigt).',
    'esports_game_option': '{name} (Verkäufe: {sales})',
    'esports_league_entry': '{name} - Hype: {hype} | Sponsor: {tier} | Events: {championships}',
    'esports_league_detail_title': 'Liga: {name}',
    'esports_detail_info': 'Spiel: {name} | Hype: {hype}/100 | Sponsor: {tier} | Events: {championships} | Sponsor-Einnahmen: {sponsor_income} EUR',
    'esports_go_to_championship': 'World Championship veranstalten',
    'esports_champ_done_this_year': 'Championship {year} bereits abgehalten.',
    'esports_manage_sponsor': 'Sponsoring verwalten (Aktuell: {tier})',
    'esports_sponsor_title': 'Sponsoring & Streaming',
    'esports_sponsor_tier_none': 'Keiner',
    'esports_sponsor_tier_local': 'Lokal',
    'esports_sponsor_tier_regional': 'Regional',
    'esports_sponsor_tier_national': 'National',
    'esports_sponsor_tier_global': 'Global',
    'esports_sponsor_info': 'Aktueller Sponsor: {tier} | Wöchentlich ca. {weekly} EUR',
    'esports_sponsor_option': '{action} {tier} ({cost} EUR)',
    'esports_streaming_deal': 'Streaming-Deal abschließen ({cost} EUR, {current}/{max} aktiv)',
    'esports_streaming_max': 'Maximale Streaming-Deals aktiv (5/5).',
    'esports_sponsor_changed': 'Sponsoring-Tier geändert zu: {tier}!',
    'esports_streaming_deal_bought': 'Streaming-Deal abgeschlossen! Aktiv: {deals}/5.',
    'esports_sender': 'E-Sports Team',
    'esports_champ_email_subject': 'World Championship {year}: {game}',
    'esports_champ_email_body': r"Das World Championship für '{game}' ist Geschichte!\nZuschauer: {viewers}\nEinnahmen: {revenue} EUR\nPreisgeld: {prize} EUR\nNeue Fans: +{fans}\nHype: +{hype}",
    'esports_locked': 'E-Sports Ligen sind erst ab {year} verfuegbar. Weiterentwickeln!',
    'esports_create_title': 'Neue E-Sports Liga gruenden',
    'esports_create_league': "Neue Liga gruenden fuer '{game}' (Kosten: {cost} EUR)",
    'esports_league_created': "Die '{game}' E-Sports Liga wurde erfolgreich gegruendet! Hype +{hype}, Fans +{fans}.",
    'esports_manage_title': 'Aktive Ligen verwalten',
    'esports_manage_leagues': "Liga '{game}' | Hype: {hype} | Events: {champ} | Gegruendet: Woche {week}",
    'esports_champ_title': "World Championship: '{game}'",
    'esports_champ_small': 'Kleines Championship Budget ({cost} EUR) - lokale Sponsoren',
    'esports_champ_med': 'Mittleres Championship Budget ({cost} EUR) - gute Sponsoren',
    'esports_champ_huge': 'Mega Championship Budget ({cost} EUR) - maximale Reichweite',
    'esports_champ_result': "Championship '{game}': Budget {cost} EUR. Umsatz: {revenue} EUR (Sponsoren: {sponsor}, Streaming: {stream}). Fans +{fans}, Hype +{hype}.",
    'esports_champ_done': 'Championship veranstaltet! Naechstes: naechstes Jahr.'
}

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split('"esports_active_error":')
if len(parts) >= 3:
    en_str = ',\n        '.join([f'"{k}": "{v}"' for k,v in en_keys.items()]) + ',\n        "esports_active_error":'
    de_str = ',\n        '.join([f'"{k}": "{v}"' for k,v in de_keys.items()]) + ',\n        "esports_active_error":'
    
    new_content = parts[0] + en_str + parts[1] + de_str + parts[2]
    
    for i in range(3, len(parts)):
        new_content += '"esports_active_error":' + parts[i]
        
    with open("translations.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Translations added.")
else:
    print("Could not find translation markers.")
