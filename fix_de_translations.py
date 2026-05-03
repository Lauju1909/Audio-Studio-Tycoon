"""Verschiebt die DE-Keys vom EN-Block in den DE-Block."""

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

# Die neuen Keys befinden sich NACH dem zweiten "yes_update" (im EN-Block).
# Wir muessen sie NACH dem ersten "yes_update" (im DE-Block) einfuegen.

de_keys_to_inject = {
    "sender_calendar": "Kalender",
    "subject_new_month": "Neuer Monat: {date}",
    "body_new_month": "Ein neuer Monat hat begonnen: {date}. Kapital: {money:,.0f} EUR. Fans: {fans:,.0f}",
    "announce_new_month": "Neuer Monat: {date}",
    "sender_bank": "Erste Spielerbank AG",
    "subject_monthly_statement": "Ihr Kontoauszug - {date}",
    "monthly_statement_period": "Abrechnungszeitraum",
    "research_blocked_already_researching": "Forschung nicht moeglich: Ihr erforscht bereits '{name}'.",
    "research_blocked_developing": "Forschung nicht moeglich: Entwicklung von '{name}' laeuft noch.",
    "dev_time_estimate": "Geschaetzte Entwicklungszeit: ca. {weeks} Wochen.",
    "dev_event_dev_key_employee_sick_title": "Krank!",
    "dev_event_dev_key_employee_sick_desc": "Euer Schluessel-Entwickler ist krank! Das Projekt droht in Verzug zu geraten.",
    "dev_event_dev_tech_breakthrough_title": "Technischer Durchbruch!",
    "dev_event_dev_tech_breakthrough_desc": "Euer Team hat eine innovative Idee! Wollt ihr sie jetzt einbauen?",
    "dev_event_dev_scope_creep_title": "Feature-Wunsch",
    "dev_event_dev_scope_creep_desc": "Fans fordern ein neues Feature. Einbauen oder fokussiert bleiben?",
    "dev_event_dev_crunch_offer_title": "Ueberstunden-Angebot",
    "dev_event_dev_crunch_offer_desc": "Das Team bietet Ueberstunden an. Akzeptieren?",
    "dev_event_dev_positive_review_title": "Positiver Hype!",
    "dev_event_dev_positive_review_desc": "Ein Journalist hat euer Projekt entdeckt. Demo veroeffentlichen?",
    "dev_event_dev_data_loss_title": "Datenverlust!",
    "dev_event_dev_data_loss_desc": "Ein Server-Crash hat Teile des Codes zerstoert! Backup einspielen oder neu schreiben?",
    "dev_event_dev_viral_moment_title": "Viral gegangen!",
    "dev_event_dev_viral_moment_desc": "Ein Video von eurem Spiel ist viral gegangen! Hype nutzen oder ruhig bleiben?",
    "dev_event_dev_rival_copy_title": "Konkurrenz kopiert!",
    "dev_event_dev_rival_copy_desc": "Ein Konkurrent hat euer Konzept geklaut! Schneller entwickeln oder ignorieren?",
    "dev_event_opt_dev_key_employee_sick_hire_freelancer": "Freelancer einstellen",
    "dev_event_opt_dev_key_employee_sick_continue_without": "Ohne ihn weitermachen",
    "dev_event_opt_dev_tech_breakthrough_implement_now": "Jetzt einbauen",
    "dev_event_opt_dev_tech_breakthrough_save_for_sequel": "Fuer Sequel aufsparen",
    "dev_event_opt_dev_scope_creep_add_feature": "Feature hinzufuegen",
    "dev_event_opt_dev_scope_creep_stay_focused": "Fokussiert bleiben",
    "dev_event_opt_dev_crunch_offer_accept_crunch": "Ueberstunden akzeptieren",
    "dev_event_opt_dev_crunch_offer_decline_crunch": "Ablehnen",
    "dev_event_opt_dev_positive_review_release_demo": "Demo veroeffentlichen",
    "dev_event_opt_dev_positive_review_keep_secret": "Geheimnis bewahren",
    "dev_event_opt_dev_data_loss_restore_backup": "Backup einspielen",
    "dev_event_opt_dev_data_loss_rewrite": "Neu schreiben",
    "dev_event_opt_dev_viral_moment_embrace_hype": "Hype nutzen",
    "dev_event_opt_dev_viral_moment_focus_quality": "Qualitaet priorisieren",
    "dev_event_opt_dev_rival_copy_speed_up": "Entwicklung beschleunigen",
    "dev_event_opt_dev_rival_copy_ignore_rival": "Konkurrenz ignorieren",
    "weeks": "Wochen",
    "morale": "Moral",
    "dev_event_opt_finish": "CGI-Trailer fertigstellen",
    "dev_event_opt_ignore": "Leak ignorieren",
    "dev_event_opt_implement": "Feature hinzufuegen",
    "dev_event_opt_focus": "Fokussiert bleiben",
    "dev_event_opt_hire": "Promi-Stimme engagieren",
    "dev_event_opt_pass": "Verzichten",
}

# Finde das erste "yes_update" (im DE-Block) und fuege danach ein
first_yes_update = content.find('"yes_update"')
if first_yes_update == -1:
    print("ERROR: yes_update nicht gefunden!")
    exit(1)

# Finde das Ende dieser Zeile
line_end = content.find("\n", first_yes_update)

# Welche Keys sind schon im DE-Block?
de_block_end = content.find('"en"')
de_block = content[:de_block_end]

new_lines = []
for k, v in de_keys_to_inject.items():
    if '"' + k + '"' in de_block:
        print(f"  DE schon vorhanden: {k}")
        continue
    v_escaped = v.replace('"', '\\"')
    new_lines.append(f'        "{k}": "{v_escaped}"')

if new_lines:
    insert_text = ",\n" + ",\n".join(new_lines)
    content = content[:line_end] + insert_text + content[line_end:]
    print(f"  {len(new_lines)} neue DE-Keys eingefuegt.")
else:
    print("  Keine neuen DE-Keys noetig.")

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done!")
