//! Symmetric German (`de`) and English (`en`) localization dictionary.
//! Enforces 100% key parity and UTF-8 cleanliness.

use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Lang {
    De,
    En,
}

impl Lang {
    pub fn from_code(code: &str) -> Self {
        if code.trim().eq_ignore_ascii_case("en") {
            Lang::En
        } else {
            Lang::De
        }
    }

    pub fn code(&self) -> &'static str {
        match self {
            Lang::De => "de",
            Lang::En => "en",
        }
    }

    pub fn toggle(&self) -> Self {
        match self {
            Lang::De => Lang::En,
            Lang::En => Lang::De,
        }
    }
}

pub fn build_dictionary(lang: Lang) -> BTreeMap<&'static str, &'static str> {
    let mut m = BTreeMap::new();
    let pairs: &[(&'static str, &'static str, &'static str)] = &[
        // General & Main Menu
        (
            "main_welcome",
            "Willkommen bei Audio Studio Tycoon in der schnellen Rust-Edition! Steuerung mit Pfeiltasten, Eingabetaste und Rücktaste.",
            "Welcome to Audio Studio Tycoon in the fast Rust Edition! Navigate with Arrow keys, Enter, and Backspace.",
        ),
        ("main_menu_title", "Hauptmenü", "Main Menu"),
        ("menu_new_game", "Neues Studio gründen", "Found New Studio"),
        ("menu_continue_game", "Spiel fortsetzen", "Continue Game"),
        ("menu_load_game", "Spielstand laden", "Load Savegame"),
        ("menu_save_game", "Spielstand speichern", "Save Game"),
        ("menu_tutorials", "Interaktive Tutorials (8 Kapitel)", "Interactive Tutorials (8 Chapters)"),
        ("menu_settings", "Einstellungen & Barrierefreiheit", "Settings & Accessibility"),
        ("menu_credits", "Mitwirkende & Architektur-Info", "Credits & Architecture Info"),
        ("menu_quit", "Spiel beenden", "Quit Game"),
        ("menu_back", "Zurück", "Back"),
        (
            "language_switched_de",
            "Sprache auf Deutsch umgestellt.",
            "Sprache auf Deutsch umgestellt.",
        ),
        (
            "language_switched_en",
            "Language switched to English.",
            "Language switched to English.",
        ),
        ("paused", "Spiel pausiert.", "Game paused."),
        ("speed_slow", "Geschwindigkeit: Langsam (0,5x).", "Speed: Slow (0.5x)."),
        ("speed_normal", "Geschwindigkeit: Normal (1x).", "Speed: Normal (1x)."),
        ("speed_fast", "Geschwindigkeit: Schnell (2x).", "Speed: Fast (2x)."),
        ("speed_ultra", "Geschwindigkeit: Ultra (4x).", "Speed: Ultra (4x)."),
        ("money_label", "Kontostand", "Balance"),
        ("calendar_week", "Woche", "Week"),
        // Months
        ("month_jan", "Januar", "January"),
        ("month_feb", "Februar", "February"),
        ("month_mar", "März", "March"),
        ("month_apr", "April", "April"),
        ("month_may", "Mai", "May"),
        ("month_jun", "Juni", "June"),
        ("month_jul", "Juli", "July"),
        ("month_aug", "August", "August"),
        ("month_sep", "September", "September"),
        ("month_oct", "Oktober", "October"),
        ("month_nov", "November", "November"),
        ("month_dec", "Dezember", "December"),
        // Difficulty
        ("difficulty_title", "Schwierigkeitsgrad & Startjahr wählen", "Select Difficulty & Start Year"),
        (
            "difficulty_easy",
            "Einfach (150.000 EUR Startkapital, entspannter Markt)",
            "Easy (150,000 EUR starting capital, forgiving market)",
        ),
        (
            "difficulty_normal",
            "Normal (100.000 EUR Startkapital, realistische Balance)",
            "Normal (100,000 EUR starting capital, realistic balance)",
        ),
        (
            "difficulty_hard",
            "Schwer (50.000 EUR Startkapital, anspruchsvolle Kritiker)",
            "Hard (50,000 EUR starting capital, demanding critics)",
        ),
        (
            "difficulty_legendary",
            "Legendär (25.000 EUR Startkapital, knallharter Wettbewerb)",
            "Legendary (25,000 EUR starting capital, ruthless competition)",
        ),
        (
            "company_name_title",
            "Firmenname eingeben (Tippen oder Enter für Vorschlag)",
            "Enter Studio Name (Type or press Enter for default)",
        ),
        // Studio Hub (GameMenu)
        ("game_menu_title", "Tonstudio-Zentrale", "Audio Studio Hub"),
        ("hub_develop_game", "Neue Produktion / Spiel entwickeln", "Develop New Production / Game"),
        ("hub_active_projects", "Aktive Projekte & Veröffentlichungen", "Active Projects & Releases"),
        ("hub_contracts", "Auftragsarbeiten (Sofort-Einnahmen)", "Contract Work (Immediate Income)"),
        ("hub_research", "Forschung & Eigene Audio-Engine", "Research & Custom Audio Engine"),
        ("hub_hr", "Personalabteilung (Team, Training, Urlaub)", "Human Resources (Team, Training, Vacation)"),
        ("hub_office", "Tonstudio & Büro-Ausbau", "Studio & Office Upgrades"),
        ("hub_marketing", "Marketing, Jingle-Studio & Fanpost", "Marketing, Jingle Studio & Fan Mail"),
        ("hub_soundcon", "SoundCon Messe & Live-Auftritt", "SoundCon Expo & Live Showcase"),
        ("hub_label_sub", "Soundtrack-Label & AudioPass Abo-Dienst", "Soundtrack Label & AudioPass Subscription"),
        ("hub_hardware", "Hardware-Labor (Soundkarten & Konsolen)", "Hardware Lab (Soundcards & Consoles)"),
        ("hub_bank_rivals", "Finanzen, Bankkredite & Konkurrenz", "Finances, Bank Loans & Rivals"),
        ("hub_inbox", "E-Mail Posteingang", "Email Inbox"),
        ("hub_charts_goty", "Verkaufscharts & Jahrespreise (GOTY)", "Sales Charts & Annual Awards (GOTY)"),
        ("hub_next_week", "Nächste Woche simulieren (Taste W)", "Simulate Next Week (Key W)"),
        // Compatibility ratings
        ("compat_0", "Unpassende Kombination (0/3)", "Poor Combination (0/3)"),
        ("compat_1", "Solide Kombination (1/3)", "Okay Combination (1/3)"),
        ("compat_2", "Gute Kombination (2/3)", "Good Combination (2/3)"),
        ("compat_3", "Perfekte Synergie! (3/3)", "Perfect Synergy! (3/3)"),
        // Review & Notifications
        ("sender_calendar", "Finanzbuchhaltung", "Accounting Department"),
        ("sender_industry", "Branchen-Nachrichten", "Industry News"),
        ("sender_hr", "Personalabteilung", "Human Resources"),
        ("sender_press", "Fachpresse & Kritik", "Industry Press & Critics"),
        ("sender_awards", "Preis-Komitee", "Awards Committee"),
        ("sender_community", "Fan-Community", "Fan Community"),
    ];

    for &(k, de_val, en_val) in pairs {
        m.insert(
            k,
            match lang {
                Lang::De => de_val,
                Lang::En => en_val,
            },
        );
    }
    m
}

pub fn tr(lang: Lang, key: &str) -> String {
    let dict = build_dictionary(lang);
    dict.get(key).copied().unwrap_or(key).to_string()
}

pub fn month_name(lang: Lang, month_idx_0_to_11: usize) -> &'static str {
    let de = [
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ];
    let en = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];
    let idx = month_idx_0_to_11.min(11);
    match lang {
        Lang::De => de[idx],
        Lang::En => en[idx],
    }
}
