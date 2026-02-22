"""
Central game strings for Audio Studio Tycoon.
Contains hardcoded German sentences extracted from main.py and menus.py.
"""

game_strings = {
    # == MAIN.PY ==
    "main_title": "Audio Studio Tycoon - Audio Edition",
    "main_welcome": (
        "Willkommen bei Audio Studio Tycoon, Audio Edition! "
        "Gründe deine eigene Spielefirma, stelle Mitarbeiter ein, "
        "erforsche Technologien und entwickle Bestseller! "
        "Nutze die Pfeiltasten zum Navigieren und Enter zum Auswählen."
    ),
    "main_screenreader_hint": (
        "Dieses Spiel ist für Screenreader (NVDA/JAWS) optimiert. "
        "Das Fenster dient nur der Tastatureingabe."
    ),
    "main_progress": "Fortschritt: {progress}/{total} Ww. | Bugs: {bugs}{crunch}",
    "main_office_status": "Büro: {office} | Mitarbeiter: {emp_count}/{emp_max} | Engines: {eng_count}",
    "main_current_menu": "Aktuelles Menü: {menu}",
    "main_trend": "TREND: {topic} / {genre}",
    "time_speed_speech": "Zeitgeschwindigkeit: {speed}",
    
    # == MENUS.PY (GENERAL) ==
    "menu_empty_history": "Leer.",
    "menu_history_count": "Spielhistorie: {count}.",
    "menu_goodbye": "Auf Wiedersehen!",
    
    # == SPIELENTWICKLUNG ==
    "dev_select_topic_speak": "Wähle ein Thema für dein Spiel.",
    "dev_topic_selected": "Thema: {topic}",
    "dev_select_genre_speak": "Wähle ein Genre für dein {topic}-Spiel.",
    "dev_genre_selected": "{topic} plus {genre}: {compat_text}.",
    "dev_platform_license_error": "Nicht genug Geld für die {platform} Lizenz. Du brauchst {cost:,} {currency}.",
    "dev_platform_selected": "Plattform: {platform}.",
    "dev_audience_selected": "Zielgruppe: {audience}.",
    "dev_size_employee_error": "Für ein {size} Spiel brauchst du mindestens {min_emp} Mitarbeiter. Du hast nur {current_emp}.",
    "dev_size_selected": "Größe: {size}.",
    "dev_remaster_selected": "Klassiker {game} ausgewählt. Direkt weiter zur Plattform-Wahl.",
    "dev_marketing_error": "Nicht genug Geld. Du brauchst {cost:,} Euro.",
    "dev_marketing_success": "Marketing gebucht. Hype steigt um {hype}. Aktueller Hype: {current_hype:.1f}.",
    "dev_engine_selected": "Engine: {engine}, Tech-Level {tech}.",
    "dev_name_prompt": "Spielname eingeben. Dein {topic} {genre}-Spiel auf {platform}. Tippe den Namen und drücke Enter.",
    "dev_name_success": "Spielname: {name}. Weiter zur Entwicklung!",
    "dev_slider_prompt": (
        "Entwicklung von '{name}', ein {topic} {genre}-Spiel auf {platform}. "
        "Geschätzte Kosten: {cost:,} Euro. Verteile {budget} Punkte auf 6 Bereiche."
    ),
    "dev_started": "Entwicklung läuft... Dein Team arbeitet hart!",
    "dev_progress_start": "Entwicklung von {game} gestartet. Dauer: {weeks} Wochen. Nutze 1, 2, 3 für Tempo und C für Crunch.",
    "dev_progress_update": "{percent} Prozent fertig. {bugs} Bugs. Hype: {hype:.1f}.",
    "dev_finish_prompt": "Entwicklung abgeschlossen! Veröffentlichen oder Polishing?",
    "dev_polish_start": "Polishing aktiv. Drücke Pfeiltaste oder Enter, um das Menü jederzeit wieder zu öffnen.",
    "dev_polish_update": "Polishing: {bugs} Bugs übrig.",
    "dev_review_intro": "Die Reviews für '{game}' sind da!",
    "dev_review_score": "Reviewer {num}: {score} von 10.",
    "dev_review_avg": "Durchschnittsbewertung: {avg:.1f} von 10.",
    "dev_review_sales": "Verkäufe: {sales:,} Einheiten. Einnahmen: {rev:,} Euro. Kosten: {cost:,} Euro. Gewinn: {profit:,} Euro.",
    "dev_review_wallet": "Neuer Kontostand: {money:,} Euro. Fans: {fans:,}.",
    "dev_review_saved": "Spielstand gespeichert. Auf Wiedersehen!",
    
    # == PERSONAL ==
    "hr_intro": "Personal-Abteilung. {current} von {max_emp} Mitarbeiter.",
    "hr_hire_office_full": "Dein {office} hat nur Platz für {max_emp} Mitarbeiter. Upgrade dein Büro für mehr Plätze.",
    "hr_show_none": "Du hast noch keine Mitarbeiter.",
    "hr_train_none": "Du hast keine Mitarbeiter zum Trainieren.",
    "hr_fire_none": "Du hast keine Mitarbeiter zum Entlassen.",
    "hr_hire_intro": "3 Bewerber verfügbar.",
    "hr_hire_success": "{name} eingestellt! Kosten: {cost:,} Euro. Restgeld: {money:,} Euro.",
    "hr_hire_fail": "Einstellung fehlgeschlagen.",
    "hr_fire_prompt": "Wen möchtest du entlassen?",
    "hr_fire_success": "{name} entlassen. Restgeld: {money:,} Euro.",
    
    # == FORSCHUNG & ENGINES ==
    "res_intro": "Forschung und Engines. {unlocked} Features freigeschaltet. {available} neue Features verfügbar. {engines} Engines erstellt.",
    "res_avail_intro": "{count} Features zum Erforschen.",
    "res_research_success": "{name} erforscht! Restgeld: {money:,} Euro.",
    "res_research_fail": "Nicht genug Geld oder bereits erforscht.",
    "res_engine_create_prompt": "Wähle Features für '{name}'. Enter zum An/Abwählen. Letzte Option zum Erstellen.",
    "res_engine_toggle": "{name} {status}. {count} Features gewählt.",
    "res_engine_create_fail": "Wähle mindestens ein Feature!",
    "res_engine_create_success": "Engine '{name}' erstellt mit Tech-Level {tech}.",
    
    # == BÜRO / SONSTIGES ==
    "office_intro": "Dein Büro: {name}. Miete: {rent} pro Woche.",
    "office_upgrade_fail": "Nicht genug Geld oder bereits maximal.",
    "office_upgrade_success": "Büro aufgewertet auf {name}! Neues Limit: {max_emp} Mitarbeiter.",
    "publish_contract": "Vertrag mit {pub} unterzeichnet.",
    "publish_self": "Spiel wird im Selbstverlag veröffentlicht.",
    "expo_intro": "Audio Expo! Möchtest du dein Studio präsentieren?",
    "expo_fail": "Nicht genug Geld für diesen Stand.",
    "expo_success": "Erfolgreicher Messeauftritt! Hype steigt massiv um {hype}.",
    "mail_deleted": "E-Mail gelöscht.",
    "mail_reply_patch_fail": "Nicht genug Geld oder keine Bugs für Patch.",
    "mail_reply_patch_success": "Patch veröffentlicht! {fans} Fans gewonnen.",
    "mail_reply_dlc_fail": "Nicht genug Geld für DLC.",
    "mail_reply_dlc_success": "DLC veröffentlicht! Verkaufszahlen steigen. {fans} Fans gewonnen.",
    "mail_reply_ok": "Nachricht gelesen.",
    "service_intro": "Welches Spiel möchten Sie verwalten?",
    "training_select_emp": "Welchen Mitarbeiter möchtest du trainieren?",
    "training_select_course": "Welches Training für {name}?",
    "training_success": "{name} hat {course} absolviert! Restgeld: {money:,} Euro.",
    "training_fail": "Nicht genug Geld für dieses Training.",
}
