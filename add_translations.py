"""
Skript zum Einfuegen neuer Uebersetzungskeys in translations.py.
Fuer beide Sprachen DE und EN.
"""

new_de_keys = {
    # Monat-Ankuendigung
    "sender_calendar": "Kalender",
    "subject_new_month": "Neuer Monat: {date}",
    "body_new_month": "Ein neuer Monat hat begonnen: {date}.\n\nAktuelles Kapital: {money:,.0f} EUR\nFans: {fans:,.0f}",
    "announce_new_month": "Neuer Monat: {date}",
    # Monatlicher Kontoauszug
    "sender_bank": "Erste Spielerbank AG",
    "subject_monthly_statement": "Ihr Kontoauszug – {date}",
    "monthly_statement_period": "Abrechnungszeitraum",
    # Forschungs-Blockierung
    "research_blocked_already_researching": "Forschung nicht moeglich: Ihr erforscht bereits '{name}'.",
    "research_blocked_developing": "Forschung nicht moeglich: Entwicklung von '{name}' laeuft noch.",
    # Entwicklungszeit-Schaetzung
    "dev_time_estimate": "Geschaetzte Entwicklungszeit: ca. {weeks} Wochen.",
    # Allgemeine Dev-Events Titel
    "dev_event_dev_key_employee_sick_title": "Krank!",
    "dev_event_dev_key_employee_sick_desc": "Euer Schluessel-Entwickler ist krank! Das Projekt droht in Verzug zu geraten.",
    "dev_event_dev_tech_breakthrough_title": "Technischer Durchbruch!",
    "dev_event_dev_tech_breakthrough_desc": "Euer Team hat eine innovative Idee! Wollt ihr sie jetzt einbauen?",
    "dev_event_dev_scope_creep_title": "Feature-Wunsch",
    "dev_event_dev_scope_creep_desc": "Fans fordern ein neues Feature. Einbauen oder fokussiert bleiben?",
    "dev_event_dev_crunch_offer_title": "Ueberstunden-Angebot",
    "dev_event_dev_crunch_offer_desc": "Das Team bietet an, Ueberstunden zu machen. Akzeptieren?",
    "dev_event_dev_positive_review_title": "Positiver Hype!",
    "dev_event_dev_positive_review_desc": "Ein Journalist hat euer Projekt entdeckt. Wollt ihr eine Demo veroeffentlichen?",
    "dev_event_dev_data_loss_title": "Datenverlust!",
    "dev_event_dev_data_loss_desc": "Ein Server-Crash hat Teile des Codes zerstoert! Backup einspielen oder neu schreiben?",
    "dev_event_dev_viral_moment_title": "Viral gegangen!",
    "dev_event_dev_viral_moment_desc": "Ein Video von eurem Spiel ist viral gegangen! Den Hype nutzen oder ruhig bleiben?",
    "dev_event_dev_rival_copy_title": "Konkurrenz kopiert!",
    "dev_event_dev_rival_copy_desc": "Ein Konkurrent hat euer Konzept geklaut! Entwicklung beschleunigen oder ignorieren?",
    # Dev-Event Optionen
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
    # Allgemein
    "weeks": "Wochen",
    "morale": "Moral",
    "dev_event_opt_finish": "CGI-Trailer fertigstellen",
    "dev_event_opt_ignore": "Leak ignorieren",
    "dev_event_opt_implement": "Feature hinzufuegen",
    "dev_event_opt_focus": "Fokussiert bleiben",
    "dev_event_opt_hire": "Promi-Stimme engagieren",
    "dev_event_opt_pass": "Verzichten",
}

new_en_keys = {
    # Calendar announcement
    "sender_calendar": "Calendar",
    "subject_new_month": "New Month: {date}",
    "body_new_month": "A new month has begun: {date}.\n\nCurrent capital: {money:,.0f} EUR\nFans: {fans:,.0f}",
    "announce_new_month": "New month: {date}",
    # Monthly statement
    "sender_bank": "First Player Bank",
    "subject_monthly_statement": "Your Bank Statement – {date}",
    "monthly_statement_period": "Billing period",
    # Research blocking
    "research_blocked_already_researching": "Research not possible: already researching '{name}'.",
    "research_blocked_developing": "Research not possible: development of '{name}' is still running.",
    # Dev time estimate
    "dev_time_estimate": "Estimated development time: approx. {weeks} weeks.",
    # Dev event titles
    "dev_event_dev_key_employee_sick_title": "Sick Leave!",
    "dev_event_dev_key_employee_sick_desc": "Your key developer is sick! The project risks falling behind.",
    "dev_event_dev_tech_breakthrough_title": "Tech Breakthrough!",
    "dev_event_dev_tech_breakthrough_desc": "Your team has an innovative idea! Do you want to implement it now?",
    "dev_event_dev_scope_creep_title": "Feature Request",
    "dev_event_dev_scope_creep_desc": "Fans are demanding a new feature. Add it or stay focused?",
    "dev_event_dev_crunch_offer_title": "Overtime Offer",
    "dev_event_dev_crunch_offer_desc": "The team offers to work overtime. Accept?",
    "dev_event_dev_positive_review_title": "Positive Hype!",
    "dev_event_dev_positive_review_desc": "A journalist discovered your project. Release a demo?",
    "dev_event_dev_data_loss_title": "Data Loss!",
    "dev_event_dev_data_loss_desc": "A server crash destroyed parts of the code! Restore backup or rewrite?",
    "dev_event_dev_viral_moment_title": "Gone Viral!",
    "dev_event_dev_viral_moment_desc": "A video of your game went viral! Capitalize on the hype or stay quiet?",
    "dev_event_dev_rival_copy_title": "Rival Copied!",
    "dev_event_dev_rival_copy_desc": "A competitor has copied your concept! Speed up or ignore?",
    # Dev event options
    "dev_event_opt_dev_key_employee_sick_hire_freelancer": "Hire a freelancer",
    "dev_event_opt_dev_key_employee_sick_continue_without": "Continue without them",
    "dev_event_opt_dev_tech_breakthrough_implement_now": "Implement now",
    "dev_event_opt_dev_tech_breakthrough_save_for_sequel": "Save for sequel",
    "dev_event_opt_dev_scope_creep_add_feature": "Add the feature",
    "dev_event_opt_dev_scope_creep_stay_focused": "Stay focused",
    "dev_event_opt_dev_crunch_offer_accept_crunch": "Accept overtime",
    "dev_event_opt_dev_crunch_offer_decline_crunch": "Decline",
    "dev_event_opt_dev_positive_review_release_demo": "Release demo",
    "dev_event_opt_dev_positive_review_keep_secret": "Keep it secret",
    "dev_event_opt_dev_data_loss_restore_backup": "Restore backup",
    "dev_event_opt_dev_data_loss_rewrite": "Rewrite the code",
    "dev_event_opt_dev_viral_moment_embrace_hype": "Embrace the hype",
    "dev_event_opt_dev_viral_moment_focus_quality": "Focus on quality",
    "dev_event_opt_dev_rival_copy_speed_up": "Speed up development",
    "dev_event_opt_dev_rival_copy_ignore_rival": "Ignore the rival",
    # General
    "weeks": "weeks",
    "morale": "morale",
    "dev_event_opt_finish": "Finish CGI trailer",
    "dev_event_opt_ignore": "Ignore the leak",
    "dev_event_opt_implement": "Add the feature",
    "dev_event_opt_focus": "Stay focused",
    "dev_event_opt_hire": "Hire celebrity voice",
    "dev_event_opt_pass": "Pass",
}

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

# Finde den letzten Eintrag in 'de' - suche nach "yes_update"
# und fuege danach ein

def inject_keys(content, keys_dict, lang_marker):
    """Fuegt Keys vor der schliessenden } des language-Blocks ein."""
    # Suche nach dem letzten Schluesseleintrag im DE-Block
    # Wir suchen nach '"yes_update"' und fuegen danach ein
    import re
    marker_key = '"yes_update"' if lang_marker == 'de' else '"yes_update"'
    # Finde den Block
    idx = content.rfind(marker_key)
    if idx == -1:
        print(f"WARNUNG: marker_key nicht gefunden fuer {lang_marker}")
        return content
    # Finde das Zeilenende dieses Eintrags
    line_end = content.find("\n", idx)
    if line_end == -1:
        line_end = len(content)
    # Erstelle neuen Text
    new_lines = []
    for k, v in keys_dict.items():
        # Schon vorhanden?
        if f'"{k}"' in content:
            continue
        # Wert escapen
        v_escaped = v.replace("\\", "\\\\").replace('"', '\\"')
        new_lines.append(f'        "{k}": "{v_escaped}"')
    if new_lines:
        insert_text = ",\n" + ",\n".join(new_lines)
        content = content[:line_end] + insert_text + content[line_end:]
    return content

# Injiziere in 'de' Block
content = inject_keys(content, new_de_keys, 'de')
# Injiziere in 'en' Block (zweites Vorkommen von yes_update)
# Da beide die gleiche Struktur haben, finden wir den zweiten
# Wir muessen zuerst den de-Block fertig haben, dann den en-Block
# Der en-Block kommt nach dem de-Block
de_end = content.find('"en"')
if de_end == -1:
    print("WARNUNG: en-Block nicht gefunden")
else:
    content_de = content[:de_end]
    content_en = content[de_end:]
    content_en = inject_keys(content_en, new_en_keys, 'en')
    content = content_de + content_en

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done!")
