//! Core GameState and coherent simulation systems for Audio Studio Tycoon (Rust Edition).

use crate::data::*;
use crate::i18n::{month_name, tr, Lang};
use crate::json::{parse_json, JsonValue};
use crate::models::*;
use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, PartialEq)]
pub struct PendingResearch {
    pub kind: String, // "topic", "genre", "feature", "tech"
    pub name: String,
    pub weeks_left: u32,
    pub total_weeks: u32,
    pub tech_bonus: u32,
}

impl PendingResearch {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("kind".into(), JsonValue::Str(self.kind.clone()));
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert("weeks_left".into(), JsonValue::Number(self.weeks_left as f64));
        m.insert(
            "total_weeks".into(),
            JsonValue::Number(self.total_weeks as f64),
        );
        m.insert("tech_bonus".into(), JsonValue::Number(self.tech_bonus as f64));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            kind: v.get_str("kind", "tech"),
            name: v.get_str("name", "Radio-Werbung"),
            weeks_left: v.get_u32("weeks_left", 1),
            total_weeks: v.get_u32("total_weeks", 2),
            tech_bonus: v.get_u32("tech_bonus", 10),
        }
    }
}

#[derive(Debug, Clone)]
pub struct GameState {
    pub company_name: String,
    pub money: i64,
    pub fans: u64,
    pub hype: f64,
    pub week: u32,
    pub difficulty: usize, // 0=Easy, 1=Normal, 2=Hard, 3=Legendary
    pub time_speed: f64,
    pub last_speed: f64,
    pub week_progress: f64,
    pub developer_mode: bool,

    // Progression & Unlocks
    pub office_level: usize,
    pub office_upgrades: Vec<String>,
    pub bought_platforms: Vec<String>,
    pub unlocked_topics: Vec<String>,
    pub unlocked_genres: Vec<String>,
    pub unlocked_features: Vec<String>,
    pub unlocked_technologies: Vec<String>,
    pub engines: Vec<Engine>,
    pub pending_research: Option<PendingResearch>,

    // Trends & Multipliers
    pub trend_topic: String,
    pub trend_genre: String,
    pub sales_multiplier: f64,
    pub marketing_efficiency: f64,
    pub accessibility_reputation: u32,

    // Projects & History
    pub current_draft: GameDraft,
    pub active_projects: Vec<ActiveProject>,
    pub last_finished_game: Option<GameProject>,
    pub game_history: Vec<GameProject>,
    pub high_score: f64,
    pub total_revenue: i64,
    pub goty_awards: u32,
    pub audio_awards: u32,

    // Contracts
    pub available_contracts: Vec<ContractProject>,
    pub active_contract: Option<ContractProject>,
    pub next_contract_id: u32,

    // HR & Employees
    pub employees: Vec<Employee>,
    pub hire_candidates: Vec<Employee>,
    pub next_employee_id: u32,

    // Business, SoundCon, Label, Subscription, Hardware, Bank
    pub last_soundcon_year: u32,
    pub soundcon_history: Vec<String>,
    pub label_active: bool,
    pub label_name: String,
    pub subscription_active: bool,
    pub subscription_price: f64,
    pub subscription_subscribers: u64,
    pub custom_soundcards: Vec<CustomSoundCard>,
    pub custom_consoles: Vec<CustomConsole>,
    pub bank_loan: i64,
    pub merch_stock: u64,
    pub jingle_bonus: f64,
    pub unanswered_fan_mails: u32,

    // Rivals & Inbox
    pub rivals: Vec<RivalStudio>,
    pub emails: Vec<Email>,
    pub event_log: Vec<String>,
    pub tutorials_completed: Vec<String>,
    pub settings: Settings,

    // Deterministic PRNG state for reproducible simulation
    rng_state: u64,
}

impl Default for GameState {
    fn default() -> Self {
        Self::new(1, START_YEAR)
    }
}

impl GameState {
    pub fn new(difficulty: usize, start_year: u32) -> Self {
        let clamped_year = start_year.max(START_YEAR);
        let start_week = (clamped_year - START_YEAR) * WEEKS_PER_YEAR + 1;
        let start_money = match difficulty {
            0 => 150_000,
            1 => 100_000,
            2 => 50_000,
            _ => 25_000,
        };

        let avail_plats = get_available_platforms(clamped_year);
        let first_plat = avail_plats
            .first()
            .map(|p| p.name.to_string())
            .unwrap_or_else(|| "Radio-Sendernetz (AM)".to_string());
        let mut bought_platforms = vec![first_plat.clone()];
        if avail_plats.len() > 1 && avail_plats[1].license_fee == 0 {
            bought_platforms.push(avail_plats[1].name.to_string());
        }

        let unlocked_topics: Vec<String> = START_TOPICS.iter().map(|s| s.to_string()).collect();
        let unlocked_genres: Vec<String> = START_GENRES.iter().map(|s| s.to_string()).collect();

        let starter_engine = Engine {
            name: "Basis-Tonstudio V1".to_string(),
            features: vec![
                "Papier- & Relais-Logik".to_string(),
                "Foley-Geräuschkulisse".to_string(),
            ],
            tech_level: 1,
            quality_bonus: 0.08,
            license_fee: 5_000,
            licensed_out: false,
        };

        let ceo = Employee {
            id: 1,
            name: "Studio-Gründer (CEO)".to_string(),
            role: "Sound-Designer".to_string(),
            trait_name: "Perfektionist".to_string(),
            skill_sound: 65,
            skill_code: 55,
            skill_story: 60,
            skill_graphics: 50,
            salary: 0, // CEO draws no fixed salary
            morale: 100,
            fatigue: 0,
            is_ceo: true,
            vacation_weeks_left: 0,
            training_weeks_left: 0,
            level: 1,
        };

        let rivals = vec![
            RivalStudio {
                name: "Klangwerk Entertainment".to_string(),
                reputation: 6.8,
                valuation: 180_000,
                best_year_score: 6.8,
                best_year_game: "Äther-Detektiv".to_string(),
                acquired_by_player: false,
            },
            RivalStudio {
                name: "Polyphon Audio Labs".to_string(),
                reputation: 7.2,
                valuation: 260_000,
                best_year_score: 7.2,
                best_year_game: "Symphonie der Logik".to_string(),
                acquired_by_player: false,
            },
            RivalStudio {
                name: "Aether Broadcast Studios".to_string(),
                reputation: 6.4,
                valuation: 140_000,
                best_year_score: 6.4,
                best_year_game: "Mitternachts-Express".to_string(),
                acquired_by_player: false,
            },
            RivalStudio {
                name: "NovaSonic Interactive".to_string(),
                reputation: 7.6,
                valuation: 380_000,
                best_year_score: 7.6,
                best_year_game: "Sternenklang".to_string(),
                acquired_by_player: false,
            },
        ];

        let mut draft = GameDraft::default();
        draft.platform = first_plat;

        let mut state = Self {
            company_name: "Klangpionier Tonstudio".to_string(),
            money: start_money,
            fans: 100,
            hype: 10.0,
            week: start_week,
            difficulty: difficulty.min(3),
            time_speed: 1.0,
            last_speed: 1.0,
            week_progress: 0.0,
            developer_mode: false,
            office_level: 0,
            office_upgrades: Vec::new(),
            bought_platforms,
            unlocked_topics,
            unlocked_genres,
            unlocked_features: vec![
                "Papier- & Relais-Logik".to_string(),
                "Foley-Geräuschkulisse".to_string(),
            ],
            unlocked_technologies: Vec::new(),
            engines: vec![starter_engine],
            pending_research: None,
            trend_topic: "Radio-Drama".to_string(),
            trend_genre: "Abenteuer".to_string(),
            sales_multiplier: 1.0,
            marketing_efficiency: 1.0,
            accessibility_reputation: 25,
            current_draft: draft,
            active_projects: Vec::new(),
            last_finished_game: None,
            game_history: Vec::new(),
            high_score: 0.0,
            total_revenue: 0,
            goty_awards: 0,
            audio_awards: 0,
            available_contracts: Vec::new(),
            active_contract: None,
            next_contract_id: 1,
            employees: vec![ceo],
            hire_candidates: Vec::new(),
            next_employee_id: 2,
            last_soundcon_year: 0,
            soundcon_history: Vec::new(),
            label_active: false,
            label_name: String::new(),
            subscription_active: false,
            subscription_price: 9.99,
            subscription_subscribers: 0,
            custom_soundcards: Vec::new(),
            custom_consoles: Vec::new(),
            bank_loan: 0,
            merch_stock: 0,
            jingle_bonus: 0.0,
            unanswered_fan_mails: 1,
            rivals,
            emails: Vec::new(),
            event_log: Vec::new(),
            tutorials_completed: Vec::new(),
            settings: Settings::default(),
            rng_state: 0x9E37_79B9_7F4A_7C15 ^ (clamped_year as u64),
        };

        // Actively initialize the starting year event, contracts, and candidates right at Week 1
        // (as required by lessons_learned.md!)
        state.apply_year_event(clamped_year);
        state.refresh_contracts();
        state.refresh_hire_candidates();
        state.add_welcome_email();
        state
    }

    pub fn next_rand_u32(&mut self, bound: u32) -> u32 {
        if bound <= 1 {
            return 0;
        }
        // Xorshift64*
        let mut x = self.rng_state;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.rng_state = x;
        let r = x.wrapping_mul(0x2545_F491_4F6C_DD1D);
        ((r >> 32) as u32) % bound
    }

    pub fn lang(&self) -> Lang {
        Lang::from_code(&self.settings.language)
    }

    pub fn is_en(&self) -> bool {
        self.lang() == Lang::En
    }

    pub fn toggle_language(&mut self) -> Lang {
        let next = self.lang().toggle();
        self.settings.language = next.code().to_string();
        next
    }

    pub fn calendar_year(&self) -> u32 {
        START_YEAR + (self.week.saturating_sub(1)) / WEEKS_PER_YEAR
    }

    pub fn week_in_year(&self) -> u32 {
        ((self.week.saturating_sub(1)) % WEEKS_PER_YEAR) + 1
    }

    pub fn month_index(&self) -> usize {
        (((self.week_in_year() - 1) * 12) / WEEKS_PER_YEAR).min(11) as usize
    }

    pub fn week_in_month(&self) -> u32 {
        ((self.week_in_year() - 1) % WEEKS_PER_MONTH) + 1
    }

    pub fn current_era(&self) -> &'static EraInfo {
        get_current_era(self.calendar_year())
    }

    pub fn calendar_text(&self) -> String {
        let lang = self.lang();
        let m_name = month_name(lang, self.month_index());
        let year = self.calendar_year();
        let w = self.week_in_month();
        let w_label = tr(lang, "calendar_week");
        format!("{} {}, {} {}", m_name, year, w_label, w)
    }

    pub fn add_welcome_email(&mut self) {
        let year = self.calendar_year();
        let era = self.current_era();
        if self.is_en() {
            self.emails.insert(
                0,
                Email {
                    sender: "Board of Directors".to_string(),
                    subject: format!("Welcome to {} ({})", self.company_name, year),
                    body: format!(
                        "Your audio & game studio is open in the {}! Current trend: {} + {}. Tip: Start with a contract or a small production matching the current trend.",
                        era.name_en, self.trend_topic, self.trend_genre
                    ),
                    week: self.week,
                    year,
                    read: false,
                },
            );
        } else {
            self.emails.insert(
                0,
                Email {
                    sender: "Studio-Leitung".to_string(),
                    subject: format!("Willkommen bei {} ({})", self.company_name, year),
                    body: format!(
                        "Dein Ton- und Spielestudio startet in der {}! Aktueller Markttrend: Thema {} mit Genre {}. Tipp: Starte mit einer Auftragsarbeit oder einer kleinen Produktion passend zum Trend!",
                        era.name_de, self.trend_topic, self.trend_genre
                    ),
                    week: self.week,
                    year,
                    read: false,
                },
            );
        }
    }

    pub fn apply_year_event(&mut self, year: u32) {
        let _ = self.apply_year_event_internal(year);
    }

    fn apply_year_event_internal(&mut self, year: u32) -> Vec<String> {
        let mut notes = Vec::new();
        let is_en = self.is_en();
        let ev = get_year_event(year);
        if let Some(t) = ev.trend_topic {
            self.trend_topic = t.to_string();
            if !self.unlocked_topics.iter().any(|x| x == t) {
                self.unlocked_topics.push(t.to_string());
            }
        }
        if let Some(g) = ev.trend_genre {
            self.trend_genre = g.to_string();
            if !self.unlocked_genres.iter().any(|x| x == g) {
                self.unlocked_genres.push(g.to_string());
            }
        }
        self.sales_multiplier = (self.sales_multiplier + ev.sales_multi_delta).clamp(0.5, 4.0);
        if ev.cash_grant != 0 {
            self.money += ev.cash_grant;
        }
        self.hype = (self.hype + ev.hype_bonus).clamp(0.0, 250.0);

        // Automatically unlock free platforms of the new era
        let avail_plats = get_available_platforms(year);
        for p in &avail_plats {
            if p.license_fee == 0 && !self.bought_platforms.iter().any(|bp| bp == p.name) {
                self.bought_platforms.push(p.name.to_string());
            }
        }

        // Automatically switch draft platform if current standard platform has retired
        let is_custom_console = self
            .custom_consoles
            .iter()
            .any(|c| c.name == self.current_draft.platform);
        let mut retired_switch_note: Option<(String, String)> = None;
        if !is_custom_console && !is_platform_active(&self.current_draft.platform, year) {
            let old_plat = self.current_draft.platform.clone();
            let replacement = avail_plats
                .iter()
                .find(|p| self.bought_platforms.iter().any(|bp| bp == p.name))
                .or_else(|| avail_plats.iter().find(|p| p.license_fee == 0))
                .or_else(|| avail_plats.first())
                .map(|p| p.name.to_string());
            if let Some(new_plat) = replacement {
                self.current_draft.platform = new_plat.clone();
                if new_plat != old_plat {
                    retired_switch_note = Some((old_plat, new_plat));
                }
            }
        }

        let newly_unlocked = get_newly_unlocked_platforms(year);
        let newly_retired = get_newly_retired_platforms(year);

        let milestone_msg: Option<&'static str> = match (year, is_en) {
            (1975, true) => Some(
                "1975 Milestone: Hardware Lab unlocked! You can now develop custom soundcards and consoles.",
            ),
            (1975, false) => Some(
                "Meilenstein 1975: Das Hardware-Labor ist freigeschaltet! Du kannst nun eigene Soundkarten und Konsolen entwickeln.",
            ),
            (1985, true) => Some(
                "1985 Milestone: Soundtrack Label unlocked! Found your own record label and host live concerts.",
            ),
            (1985, false) => Some(
                "Meilenstein 1985: Das Soundtrack-Label ist freigeschaltet! Gründe dein eigenes Label und veranstalte Live-Konzerte.",
            ),
            (1995, true) => Some(
                "1995 Milestone: SoundCon Expo & AudioPass subscription service are now unlocked!",
            ),
            (1995, false) => Some(
                "Meilenstein 1995: Die SoundCon-Messe & der AudioPass Abo-Dienst sind jetzt freigeschaltet!",
            ),
            (2026, true) => Some(
                "2026 Milestone: 96-Year Milestone reached! Endless Mode is now active.",
            ),
            (2026, false) => Some(
                "Meilenstein 2026: 96-Jahre-Meilenstein erreicht! Der Endlosmodus ist nun aktiv.",
            ),
            _ => None,
        };

        let year_prefix = year.to_string();
        let event_title = if is_en { ev.title_en } else { ev.title_de };
        let trend_label = if is_en { "Trend" } else { "Markttrend" };
        if event_title.starts_with(&year_prefix) {
            notes.push(format!(
                "{} ({}: {} + {}).",
                event_title, trend_label, self.trend_topic, self.trend_genre
            ));
        } else {
            notes.push(format!(
                "{}: {} ({}: {} + {}).",
                year, event_title, trend_label, self.trend_topic, self.trend_genre
            ));
        }

        let mut body_parts = Vec::new();
        body_parts.push(if is_en {
            format!(
                "{} New trend: {} + {}.",
                ev.desc_en, self.trend_topic, self.trend_genre
            )
        } else {
            format!(
                "{} Neuer Markttrend: {} + {}.",
                ev.desc_de, self.trend_topic, self.trend_genre
            )
        });

        if !newly_unlocked.is_empty() {
            let names: Vec<&str> = newly_unlocked.iter().map(|p| p.name).collect();
            let msg = if is_en {
                format!("New platforms unlocked ({}): {}.", year, names.join(", "))
            } else {
                format!("Neue Plattformen ({}): {}.", year, names.join(", "))
            };
            body_parts.push(msg.clone());
            notes.push(msg);
        }

        if !newly_retired.is_empty() {
            let names: Vec<&str> = newly_retired.iter().map(|p| p.name).collect();
            let msg = if is_en {
                format!(
                    "Retired platforms ({}): {} (retro niche market).",
                    year,
                    names.join(", ")
                )
            } else {
                format!(
                    "Eingestellte Plattformen ({}): {} (jetzt Retro-Nische).",
                    year,
                    names.join(", ")
                )
            };
            body_parts.push(msg.clone());
            notes.push(msg);
        }

        if let Some((ref old_p, ref new_p)) = retired_switch_note {
            let msg = if is_en {
                format!(
                    "Draft platform '{}' retired; automatically switched to '{}'.",
                    old_p, new_p
                )
            } else {
                format!(
                    "Entwurfs-Plattform '{}' wurde eingestellt; automatisch auf '{}' gewechselt.",
                    old_p, new_p
                )
            };
            body_parts.push(msg.clone());
            notes.push(msg);
        }

        if let Some(m) = milestone_msg {
            body_parts.push(m.to_string());
            notes.push(m.to_string());
        }

        let log_entry = if is_en {
            if let Some(m) = milestone_msg {
                format!("{}: {} [{}]", ev.title_en, ev.desc_en, m)
            } else {
                format!("{}: {}", ev.title_en, ev.desc_en)
            }
        } else if let Some(m) = milestone_msg {
            format!("{}: {} [{}]", ev.title_de, ev.desc_de, m)
        } else {
            format!("{}: {}", ev.title_de, ev.desc_de)
        };
        self.event_log.push(log_entry);

        self.emails.insert(
            0,
            Email {
                sender: tr(self.lang(), "sender_industry"),
                subject: if is_en {
                    ev.title_en.to_string()
                } else {
                    ev.title_de.to_string()
                },
                body: body_parts.join(" "),
                week: self.week,
                year,
                read: false,
            },
        );

        notes
    }

    pub fn active_employees(&self) -> Vec<&Employee> {
        self.employees
            .iter()
            .filter(|e| e.is_available())
            .collect()
    }

    pub fn monthly_payroll(&self) -> i64 {
        self.employees.iter().map(|e| e.salary).sum()
    }

    pub fn monthly_rent(&self) -> i64 {
        OFFICE_LEVELS
            .get(self.office_level)
            .map(|o| o.monthly_rent)
            .unwrap_or(200)
    }

    pub fn max_employees(&self) -> usize {
        OFFICE_LEVELS
            .get(self.office_level)
            .map(|o| o.max_employees)
            .unwrap_or(2)
    }

    pub fn financial_summary(&self) -> String {
        let payroll = self.monthly_payroll();
        let rent = self.monthly_rent();
        if self.is_en() {
            format!(
                "Balance: {} EUR. Monthly fixed costs: {} EUR salaries, {} EUR studio rent. Bank loan: {} EUR. Total revenue: {} EUR.",
                self.money, payroll, rent, self.bank_loan, self.total_revenue
            )
        } else {
            format!(
                "Kontostand: {} Euro. Monatliche Fixkosten: {} Euro Gehälter, {} Euro Studiomiete. Bankkredit: {} Euro. Gesamtumsatz: {} Euro.",
                self.money, payroll, rent, self.bank_loan, self.total_revenue
            )
        }
    }

    pub fn status_summary(&self) -> String {
        let cal = self.calendar_text();
        let era = self.current_era();
        let avail_emps = self.active_employees().len();
        let total_emps = self.employees.len();
        let proj_info = if let Some(ap) = self.active_projects.first() {
            format!("{} ({}%)", ap.project.name, ap.percent())
        } else if self.is_en() {
            "None".to_string()
        } else {
            "Keins".to_string()
        };
        if self.is_en() {
            format!(
                "{}, {}. Studio: {}. Fans: {}, Hype: {:.0}. Team: {}/{} available. Active project: {}. Current trend: {} + {}.",
                cal, era.name_en, self.company_name, self.fans, self.hype, avail_emps, total_emps, proj_info, self.trend_topic, self.trend_genre
            )
        } else {
            format!(
                "{}, {}. Studio: {}. Fans: {}, Hype: {:.0}. Team: {} von {} einsatzbereit. Aktives Projekt: {}. Aktueller Trend: {} mit {}.",
                cal, era.name_de, self.company_name, self.fans, self.hype, avail_emps, total_emps, proj_info, self.trend_topic, self.trend_genre
            )
        }
    }

    pub fn refresh_contracts(&mut self) {
        self.available_contracts.clear();
        let era_scale = self.current_era().base_market_scale;
        let templates = [
            (
                "Radio-Jingle & Kennmelodie komponieren",
                "Compose Radio Jingle & Station ID",
                "Sound",
                4_500.0,
                16.0,
                4,
            ),
            (
                "Geräuschkulisse (Foley) für Hörspiel abmischen",
                "Mix Foley Soundscape for Audio Drama",
                "Sound",
                7_500.0,
                24.0,
                5,
            ),
            (
                "Drehbuch & Sprecher-Regie für Unterhaltungssendung",
                "Script & Voice Direction for Broadcast Show",
                "Story",
                9_000.0,
                28.0,
                5,
            ),
            (
                "Audio-Engine & Signalfilter optimieren",
                "Optimize Audio Engine & Signal Filters",
                "Code",
                12_000.0,
                34.0,
                6,
            ),
        ];
        for (de, en, cat, base_rew, pts, weeks) in templates {
            let reward = ((base_rew * era_scale.sqrt()) / 100.0).round() as i64 * 100;
            let penalty = (reward / 4).max(500);
            let id = self.next_contract_id;
            self.next_contract_id += 1;
            self.available_contracts.push(ContractProject {
                id,
                name_de: de.to_string(),
                name_en: en.to_string(),
                category: cat.to_string(),
                reward,
                penalty,
                required_points: pts,
                current_points: 0.0,
                weeks_left: weeks,
            });
        }
    }

    pub fn refresh_hire_candidates(&mut self) {
        self.hire_candidates.clear();
        let names = [
            ("Max Müller", "Sound-Designer", "Perfektionist", 68, 45, 50, 42, 1_800),
            ("Anna Weber", "Programmierer", "Sauberer Coder", 48, 72, 44, 50, 2_100),
            ("Felix Hartmann", "Autor & Regie", "Teamplayer", 55, 42, 74, 48, 1_900),
            ("Sarah König", "Grafik & Kulisse", "Schneller Lerner", 52, 48, 50, 72, 2_000),
            ("Leon Richter", "Sound-Designer", "Sound-Genie", 82, 55, 60, 50, 3_400),
        ];
        for (name, role, tr_name, s_snd, s_cod, s_sty, s_gfx, sal) in names {
            let id = self.next_employee_id;
            self.next_employee_id += 1;
            self.hire_candidates.push(Employee {
                id,
                name: name.to_string(),
                role: role.to_string(),
                trait_name: tr_name.to_string(),
                skill_sound: s_snd,
                skill_code: s_cod,
                skill_story: s_sty,
                skill_graphics: s_gfx,
                salary: sal,
                morale: 95,
                fatigue: 0,
                is_ceo: false,
                vacation_weeks_left: 0,
                training_weeks_left: 0,
                level: 1,
            });
        }
    }

    pub fn buy_platform_license(&mut self, platform_name: &str) -> Result<String, String> {
        if self.bought_platforms.iter().any(|p| p == platform_name) {
            return Ok(if self.is_en() {
                format!("Platform {} is already licensed.", platform_name)
            } else {
                format!("Plattform {} ist bereits lizenziert.", platform_name)
            });
        }
        let year = self.calendar_year();
        let spec = PLATFORMS
            .iter()
            .find(|p| p.name == platform_name)
            .ok_or_else(|| "Unbekannte Plattform.".to_string())?;
        if year < spec.unlock_year {
            return Err(if self.is_en() {
                format!(
                    "{} is not available until {}.",
                    spec.name, spec.unlock_year
                )
            } else {
                format!(
                    "{} ist erst ab dem Jahr {} verfügbar.",
                    spec.name, spec.unlock_year
                )
            });
        }
        if self.money < spec.license_fee {
            return Err(if self.is_en() {
                format!(
                    "Insufficient funds! License costs {} EUR.",
                    spec.license_fee
                )
            } else {
                format!(
                    "Nicht genug Geld! Die Lizenz kostet {} Euro.",
                    spec.license_fee
                )
            });
        }
        self.money -= spec.license_fee;
        self.bought_platforms.push(spec.name.to_string());
        Ok(if self.is_en() {
            format!(
                "Purchased license for {} for {} EUR.",
                spec.name, spec.license_fee
            )
        } else {
            format!(
                "Lizenz für {} für {} Euro erworben.",
                spec.name, spec.license_fee
            )
        })
    }

    pub fn start_game_project(&mut self) -> Result<String, String> {
        let cost = self.current_draft.base_dev_cost();
        let pub_idx = self
            .current_draft
            .publisher_idx
            .min(PUBLISHERS.len().saturating_sub(1));
        let pub_spec = &PUBLISHERS[pub_idx];

        let plat = self.current_draft.platform.clone();
        let mut pending_license_fee = 0;
        let is_licensed = self.bought_platforms.iter().any(|p| p == &plat)
            || self.custom_consoles.iter().any(|c| c.name == plat);
        if !is_licensed {
            let year = self.calendar_year();
            let spec = PLATFORMS
                .iter()
                .find(|p| p.name == plat)
                .ok_or_else(|| "Unbekannte Plattform.".to_string())?;
            if year < spec.unlock_year {
                return Err(if self.is_en() {
                    format!(
                        "{} is not available until {}.",
                        spec.name, spec.unlock_year
                    )
                } else {
                    format!(
                        "{} ist erst ab dem Jahr {} verfügbar.",
                        spec.name, spec.unlock_year
                    )
                });
            }
            pending_license_fee = spec.license_fee;
        }

        let total_upfront_cost = cost + pending_license_fee;
        let net_upfront_needed = (total_upfront_cost - pub_spec.advance).max(0);

        if self.money - total_upfront_cost + pub_spec.advance < 0 {
            return Err(if self.is_en() {
                format!(
                    "Not enough money! Starting this project requires {} EUR (after publisher advance of {} EUR).",
                    net_upfront_needed, pub_spec.advance
                )
            } else {
                format!(
                    "Nicht genug Geld! Der Projektstart erfordert {} Euro (nach Publisher-Vorschuss von {} Euro).",
                    net_upfront_needed, pub_spec.advance
                )
            });
        }

        let min_emps = match self.current_draft.size.as_str() {
            "Groß" => 3,
            "AAA" => 6,
            "MMO" => 8,
            _ => 1,
        };
        if self.employees.len() < min_emps {
            return Err(if self.is_en() {
                format!(
                    "Project size '{}' requires at least {} employees (you have {}).",
                    self.current_draft.size,
                    min_emps,
                    self.employees.len()
                )
            } else {
                format!(
                    "Projektgröße '{}' erfordert mindestens {} Mitarbeiter (aktuell {}).",
                    self.current_draft.size,
                    min_emps,
                    self.employees.len()
                )
            });
        }

        if self.current_draft.size == "MMO"
            && !self
                .unlocked_technologies
                .iter()
                .any(|t| t == "Live-Service Architektur")
        {
            return Err(if self.is_en() {
                "MMO projects require 'Live-Service Architektur' research first!".to_string()
            } else {
                "MMO-Projekte erfordern zuerst die Forschung 'Live-Service Architektur'!"
                    .to_string()
            });
        }

        // Auto-license platform if needed and affordable
        if !is_licensed {
            self.bought_platforms.push(plat.clone());
        }

        self.money = self.money - total_upfront_cost + pub_spec.advance;

        let mkt_hype = match self.current_draft.marketing.as_str() {
            "Kleine Kampagne" => 15.0,
            "Mittlere Kampagne" => 40.0,
            "Große Kampagne" => 95.0,
            _ => 0.0,
        };
        self.hype = (self.hype + mkt_hype * self.marketing_efficiency + self.jingle_bonus)
            .clamp(0.0, 250.0);

        let engine_obj = self
            .engines
            .get(self.current_draft.engine_idx)
            .or_else(|| self.engines.first())
            .cloned();
        let engine_name = engine_obj
            .as_ref()
            .map(|e| e.name.clone())
            .unwrap_or_else(|| "Basis-Tonstudio V1".to_string());
        let curr_engine_tech = engine_obj.as_ref().map(|e| e.tech_level).unwrap_or(1);

        let mut sequel_number = 0;
        let mut initial_quality_boost = 0.0;
        if let Some(ref orig_name) = self.current_draft.sequel_of {
            let matching_count = self
                .game_history
                .iter()
                .filter(|g| {
                    &g.name == orig_name
                        || (g.topic == self.current_draft.topic
                            && g.genre == self.current_draft.genre)
                })
                .count() as u32;
            sequel_number = matching_count.max(1) + 1;

            if let Some(orig_game) = self
                .game_history
                .iter()
                .rev()
                .find(|g| &g.name == orig_name)
            {
                let orig_tech = self
                    .engines
                    .iter()
                    .find(|e| e.name == orig_game.engine_name)
                    .map(|e| e.tech_level)
                    .unwrap_or(1);
                if curr_engine_tech > orig_tech {
                    initial_quality_boost += 0.06;
                    self.hype = (self.hype + 20.0).clamp(0.0, 250.0);
                } else {
                    // Franchise fatigue when re-using the same or older engine tech level
                    initial_quality_boost -= 0.04;
                }
            } else {
                initial_quality_boost += 0.04;
                self.hype = (self.hype + 12.0).clamp(0.0, 250.0);
            }
        }

        let game_name = if self.current_draft.name.trim().is_empty() {
            if let Some(ref orig_name) = self.current_draft.sequel_of {
                format!("{} {}", orig_name, sequel_number)
            } else {
                format!(
                    "{} {} #{}",
                    self.current_draft.topic,
                    self.current_draft.genre,
                    self.game_history.len() + self.active_projects.len() + 1
                )
            }
        } else {
            self.current_draft.name.trim().to_string()
        };

        let proj = GameProject {
            name: game_name.clone(),
            topic: self.current_draft.topic.clone(),
            genre: self.current_draft.genre.clone(),
            sub_genre: self.current_draft.sub_genre.clone(),
            platform: self.current_draft.platform.clone(),
            audience: self.current_draft.audience.clone(),
            size: self.current_draft.size.clone(),
            marketing: self.current_draft.marketing.clone(),
            engine_name,
            sliders: self.current_draft.sliders,
            review: None,
            sales: 0,
            revenue: 0,
            dev_cost: cost,
            release_week: 0,
            release_year: self.calendar_year(),
            weeks_on_market: 0,
            is_active: true,
            bugs: 0,
            patches_released: 0,
            dlc_count: 0,
            in_soundtrack_label: false,
            in_subscription_vault: false,
            sequel_number,
            publisher_idx: pub_idx,
            post_mortem_done: false,
            quality_boost: initial_quality_boost,
        };

        let total_weeks = self.current_draft.dev_weeks();
        self.active_projects.push(ActiveProject {
            project: proj,
            progress_weeks: 0.0,
            total_weeks,
            bugs: 0,
            crunch_active: false,
            ready_to_finish: false,
            decision_made: false,
            polish_passes: 0,
        });

        self.current_draft.name.clear();
        self.current_draft.sequel_of = None;
        self.current_draft.publisher_idx = 0;

        Ok(if self.is_en() {
            if pub_spec.advance > 0 {
                format!(
                    "Started production of '{}' ({} weeks, cost: {} EUR, publisher advance: +{} EUR).",
                    game_name, total_weeks, cost, pub_spec.advance
                )
            } else {
                format!(
                    "Started production of '{}' ({} weeks, cost: {} EUR).",
                    game_name, total_weeks, cost
                )
            }
        } else if pub_spec.advance > 0 {
            format!(
                "Produktion von '{}' gestartet (Dauer: {} Wochen, Kosten: {} Euro, Publisher-Vorschuss: +{} Euro).",
                game_name, total_weeks, cost, pub_spec.advance
            )
        } else {
            format!(
                "Produktion von '{}' gestartet (Dauer: {} Wochen, Kosten: {} Euro).",
                game_name, total_weeks, cost
            )
        })
    }

    pub fn calculate_review(&self, project: &GameProject, bugs: u32) -> ReviewScore {
        // 1. Topic-Genre Compatibility (0..=3 -> 0.25 .. 1.0)
        let compat = get_compatibility(&project.topic, &project.genre);
        let synergy_score = match compat {
            3 => 1.0,
            2 => 0.80,
            1 => 0.55,
            _ => 0.25,
        };

        // 2. Slider Match against Genre Ideal Profile (0.0 .. 1.0)
        let ideal = get_ideal_sliders(&project.genre);
        let mut diff_sum: i32 = 0;
        for i in 0..6 {
            diff_sum += (project.sliders[i] as i32 - ideal[i] as i32).abs();
        }
        // Max reasonable diff is ~30
        let slider_match = (1.0 - (diff_sum as f64 / 30.0)).clamp(0.2, 1.0);

        // 3. Team Skill & Sound Studio Quality Bonus (0.0 .. 1.0)
        let emps = self.active_employees();
        let avg_skill = if emps.is_empty() {
            50.0
        } else {
            let total: u32 = emps.iter().map(|e| e.total_skill()).sum();
            (total as f64) / ((emps.len() * 4) as f64)
        };
        let team_factor = (avg_skill / 85.0).clamp(0.4, 1.15);

        // 4. Engine & Studio Tech Bonus
        let engine_bonus = self
            .engines
            .iter()
            .find(|e| e.name == project.engine_name)
            .map(|e| e.quality_bonus)
            .unwrap_or(0.08);

        let mut tech_bonus = (self.office_level as f64) * 0.015;
        if self
            .unlocked_technologies
            .iter()
            .any(|t| t == "Studios & Schallkabinen")
        {
            tech_bonus += 0.05;
        }
        if self
            .unlocked_technologies
            .iter()
            .any(|t| t == "Audio-Meisterschaft")
        {
            tech_bonus += 0.08;
        }
        if self.office_upgrades.iter().any(|u| u == "mixing_desk") {
            tech_bonus += 0.04;
        }
        if self.office_upgrades.iter().any(|u| u == "foley_stage") {
            tech_bonus += 0.05;
        }
        for sc in &self.custom_soundcards {
            tech_bonus += sc.sound_bonus * 0.25;
        }
        let access_bonus = (self.accessibility_reputation as f64 / 1000.0).min(0.06);

        // 5. Target Audience Fit
        let aud_compat =
            get_audience_compatibility(&project.topic, &project.genre, &project.audience);
        let aud_mod = match aud_compat {
            3 => 0.04,
            2 => 0.0,
            _ => -0.07,
        };

        // 5b. Sub-Genre Compatibility
        let sub_compat = get_sub_genre_compatibility(&project.genre, &project.sub_genre);
        let sub_mod = match sub_compat {
            3 => 0.03,
            1 => -0.03,
            _ => 0.0,
        };

        // 6. Trend Bonus
        let mut trend_multi = 1.0;
        if project.topic == self.trend_topic {
            trend_multi += 0.10;
        }
        if project.genre == self.trend_genre {
            trend_multi += 0.08;
        }

        // 7. Difficulty modifier
        let diff_mod = match self.difficulty {
            0 => 0.06,
            1 => 0.0,
            2 => -0.05,
            _ => -0.10,
        };

        let raw_0_to_1 = (synergy_score * 0.38
            + slider_match * 0.37
            + team_factor * 0.15
            + engine_bonus
            + tech_bonus
            + access_bonus
            + aud_mod
            + sub_mod
            + project.quality_boost
            + diff_mod)
            * trend_multi;

        // Bug penalty: each bug costs 0.12 points on the 10-point scale
        let bug_penalty = (bugs as f64) * 0.12;
        let final_10 = (raw_0_to_1 * 9.5 - bug_penalty).clamp(1.5, 10.0);

        let s1 = final_10.round().clamp(1.0, 10.0) as u8;
        let s2 = (final_10 + 0.3).round().clamp(1.0, 10.0) as u8;
        let s3 = (final_10 - 0.3).round().clamp(1.0, 10.0) as u8;
        let s4 = ((s1 as u16 + s2 as u16 + s3 as u16 + final_10.round() as u16) / 4)
            .clamp(1, 10) as u8;

        let mut comments = Vec::new();
        if self.is_en() {
            comments.push(match compat {
                3 => format!(
                    "Audio Press: '{} + {}' is a brilliant thematic and acoustic match!",
                    project.topic, project.genre
                ),
                2 => format!(
                    "Audio Press: Good combination of {} and {}.",
                    project.topic, project.genre
                ),
                1 => format!(
                    "Audio Press: {} and {} feels somewhat unconventional.",
                    project.topic, project.genre
                ),
                _ => format!(
                    "Audio Press: {} and {} simply do not fit together well.",
                    project.topic, project.genre
                ),
            });
            if slider_match >= 0.80 {
                comments.push(
                    "Sound & Design: The production focus (sliders) hits the genre sweet spot!"
                        .to_string(),
                );
            } else if slider_match < 0.55 {
                comments.push(
                    "Sound & Design: The slider priorities missed what fans expect from this genre."
                        .to_string(),
                );
            }
            if aud_compat == 3 {
                comments.push(format!(
                    "Market Fit: Target audience '{}' is a perfect match for this production!",
                    project.audience
                ));
            } else if aud_compat == 1 {
                comments.push(format!(
                    "Market Fit: Target audience '{}' does not match '{}' + '{}' well.",
                    project.audience, project.topic, project.genre
                ));
            }
            if sub_compat == 3 {
                comments.push(format!(
                    "Sub-Genre: '{}' elevates '{}' brilliantly!",
                    project.sub_genre, project.genre
                ));
            } else if sub_compat == 1 {
                comments.push(format!(
                    "Sub-Genre: '{}' feels awkward with '{}'.",
                    project.sub_genre, project.genre
                ));
            }
            if project.sequel_number > 0 {
                comments.push(format!(
                    "Franchise: Sequel #{} builds on an established series!",
                    project.sequel_number
                ));
            }
            if bugs > 3 {
                comments.push(format!(
                    "Technical QA: {} noticeable audio/logic bugs hurt the score.",
                    bugs
                ));
            } else {
                comments.push("Technical QA: Clean, polished studio production!".to_string());
            }
        } else {
            comments.push(match compat {
                3 => format!(
                    "Fachpresse: '{} + {}' ist eine absolut geniale Synergie!",
                    project.topic, project.genre
                ),
                2 => format!(
                    "Fachpresse: Gute und stimmige Kombination aus {} und {}.",
                    project.topic, project.genre
                ),
                1 => format!(
                    "Fachpresse: {} und {} wirkt etwas ungewöhnlich.",
                    project.topic, project.genre
                ),
                _ => format!(
                    "Fachpresse: Thema {} und Genre {} passen leider kaum zusammen.",
                    project.topic, project.genre
                ),
            });
            if slider_match >= 0.80 {
                comments.push(
                    "Klang & Regie: Die Slider-Gewichtung trifft den Kern des Genres perfekt!"
                        .to_string(),
                );
            } else if slider_match < 0.55 {
                comments.push(
                    "Klang & Regie: Die Slider-Schwerpunkte gingen an den Erwartungen des Genres vorbei."
                        .to_string(),
                );
            }
            if aud_compat == 3 {
                comments.push(format!(
                    "Zielgruppe: '{}' passt perfekt zu dieser Produktion!",
                    project.audience
                ));
            } else if aud_compat == 1 {
                comments.push(format!(
                    "Zielgruppe: '{}' passt leider schlecht zu '{}' und '{}'.",
                    project.audience, project.topic, project.genre
                ));
            }
            if sub_compat == 3 {
                comments.push(format!(
                    "Sub-Genre: '{}' ergänzt '{}' hervorragend!",
                    project.sub_genre, project.genre
                ));
            } else if sub_compat == 1 {
                comments.push(format!(
                    "Sub-Genre: '{}' passt nur bedingt zu '{}'.",
                    project.sub_genre, project.genre
                ));
            }
            if project.sequel_number > 0 {
                comments.push(format!(
                    "Fortsetzung: Teil {} führt eine bekannte Reihe fort!",
                    project.sequel_number
                ));
            }
            if bugs > 3 {
                comments.push(format!(
                    "Technik-Check: {} hörbare Fehler (Bugs) haben Punkte gekostet.",
                    bugs
                ));
            } else {
                comments.push("Technik-Check: Saubere, fehlerfreie Studio-Abmischung!".to_string());
            }
        }

        ReviewScore::new([s1, s2, s3, s4], comments)
    }

    pub fn finish_ready_project(&mut self, index: usize) -> Option<GameProject> {
        if index >= self.active_projects.len() {
            return None;
        }
        let ap = self.active_projects.remove(index);
        let mut proj = ap.project;
        proj.bugs = ap.bugs;
        proj.release_week = self.week;
        proj.release_year = self.calendar_year();
        let review = self.calculate_review(&proj, ap.bugs);
        let avg = review.average();
        if avg > self.high_score {
            self.high_score = avg;
        }
        proj.review = Some(review);

        // Publisher contract target evaluation
        let pub_idx = proj.publisher_idx.min(PUBLISHERS.len().saturating_sub(1));
        if pub_idx > 0 {
            let pub_spec = &PUBLISHERS[pub_idx];
            if avg >= pub_spec.min_score as f64 {
                self.fans += 300;
                self.hype = (self.hype + 15.0).clamp(0.0, 250.0);
            } else {
                self.hype = (self.hype - 8.0).max(0.0);
            }
        }

        // Initial launch week sales
        let (launch_sales, launch_rev) = self.compute_weekly_game_sales(&proj, true);
        proj.sales += launch_sales;
        proj.revenue += launch_rev;
        self.money += launch_rev;
        self.total_revenue += launch_rev;

        // Fan gain based on review score
        if avg >= 7.0 {
            let new_fans = ((avg - 6.0) * 350.0 * (1.0 + self.hype / 100.0)).round() as u64;
            self.fans += new_fans;
        } else if avg < 4.5 {
            self.fans = self.fans.saturating_sub(50);
        }
        self.unanswered_fan_mails = (self.unanswered_fan_mails + 2).min(10);

        self.last_finished_game = Some(proj.clone());
        self.game_history.push(proj.clone());
        Some(proj)
    }

    pub fn compute_weekly_game_sales(&self, proj: &GameProject, is_launch_week: bool) -> (u64, i64) {
        let avg = proj.review.as_ref().map(|r| r.average()).unwrap_or(5.0);
        let curr_year = self.calendar_year();
        let plat_multi = PLATFORMS
            .iter()
            .find(|p| p.name == proj.platform)
            .map(|p| {
                if curr_year > p.end_year {
                    p.market_multi * 0.55
                } else {
                    p.market_multi
                }
            })
            .or_else(|| {
                self.custom_consoles
                    .iter()
                    .find(|c| c.name == proj.platform)
                    .map(|c| 8.0 + c.market_share * 10.0)
            })
            .unwrap_or(1.5);

        let size_multi = match proj.size.as_str() {
            "Klein" => 0.7,
            "Mittel" => 1.2,
            "Groß" => 2.4,
            "AAA" => 4.8,
            "MMO" => 3.5,
            _ => 1.0,
        };

        let price: i64 = match proj.audience.as_str() {
            "Jeder" => 22,
            "Jugendliche" => 30,
            "Hardcore-Gamer" => 45,
            _ => 25,
        };

        let aud_compat = get_audience_compatibility(&proj.topic, &proj.genre, &proj.audience);
        let aud_multi = match aud_compat {
            3 => 1.20,
            2 => 1.0,
            _ => 0.65,
        };
        let sequel_multi = if proj.sequel_number > 0 { 1.25 } else { 1.0 };
        let pub_spec = &PUBLISHERS[proj.publisher_idx.min(PUBLISHERS.len().saturating_sub(1))];

        // Exponential quality curve: 8+ hits sell dramatically better than 4/10
        let quality_factor = (avg / 5.5).powf(2.2);
        let hype_factor = 1.0 + (self.hype / 120.0);
        let fan_factor = 1.0 + (self.fans as f64 / 25_000.0).min(4.0);
        let decay = if is_launch_week {
            1.8
        } else {
            (0.82f64).powi(proj.weeks_on_market as i32)
        };

        let mut cd_bonus = 1.0;
        if self
            .unlocked_technologies
            .iter()
            .any(|t| t == "CD-Presswerk")
        {
            cd_bonus += 0.15;
        }
        if self
            .unlocked_technologies
            .iter()
            .any(|t| t == "Digitaler Eigenvertrieb")
        {
            cd_bonus += 0.20;
        }

        let raw_units = 220.0
            * quality_factor
            * plat_multi
            * size_multi
            * hype_factor
            * fan_factor
            * self.sales_multiplier
            * cd_bonus
            * aud_multi
            * sequel_multi
            * pub_spec.reach_mult
            * decay;

        let units = raw_units.max(10.0).round() as u64;
        let gross_rev = (units as i64) * price;
        let net_rev = (gross_rev * (100 - pub_spec.royalty_cut_pct as i64)) / 100;
        (units, net_rev)
    }

    /// Simulates one full game week (`tick_week`), handling active projects, contracts,
    /// research, employee vacation/training, sales, monthly salaries/rent, and annual events.
    pub fn tick_week(&mut self) -> Vec<String> {
        let mut notifications = Vec::new();
        let prev_year = self.calendar_year();
        let prev_month = self.month_index();

        self.week += 1;

        // 1. Hype natural decay
        if self.hype > 0.0 {
            self.hype = (self.hype - 1.5).max(0.0);
        }

        // 2. Employee Vacation & Training countdown
        let is_en = self.is_en();
        for emp in &mut self.employees {
            if emp.vacation_weeks_left > 0 {
                emp.vacation_weeks_left -= 1;
                emp.fatigue = emp.fatigue.saturating_sub(30);
                emp.morale = (emp.morale + 15).min(100);
                if emp.vacation_weeks_left == 0 {
                    notifications.push(if is_en {
                        format!("{} returned refreshed from vacation!", emp.name)
                    } else {
                        format!("{} ist erholt aus dem Urlaub zurückgekehrt!", emp.name)
                    });
                }
            } else if emp.training_weeks_left > 0 {
                emp.training_weeks_left -= 1;
                if emp.training_weeks_left == 0 {
                    emp.skill_sound = (emp.skill_sound + 6).min(100);
                    emp.skill_code = (emp.skill_code + 6).min(100);
                    emp.skill_story = (emp.skill_story + 6).min(100);
                    emp.skill_graphics = (emp.skill_graphics + 6).min(100);
                    emp.level += 1;
                    notifications.push(if is_en {
                        format!(
                            "{} completed training (now Level {})!",
                            emp.name, emp.level
                        )
                    } else {
                        format!(
                            "{} hat die Fortbildung abgeschlossen (jetzt Stufe {})!",
                            emp.name, emp.level
                        )
                    });
                }
            }
        }

        // 3. Active Game Projects progress
        let avail_count = self.active_employees().len();
        let speed_tech_multi = if self
            .unlocked_technologies
            .iter()
            .any(|t| t == "KI-Soundtrack & Mastering")
        {
            1.25
        } else {
            1.0
        };
        let qa_tech_active = self
            .unlocked_technologies
            .iter()
            .any(|t| t == "Automatische Qualitätsprüfung (QA)");
        let ergo_active = self
            .unlocked_technologies
            .iter()
            .any(|t| t == "Gesundes Arbeiten & Ergonomie");

        let has_active_projects = !self.active_projects.is_empty();
        for i in 0..self.active_projects.len() {
            if self.active_projects[i].ready_to_finish {
                continue;
            }
            let crunch_mult = if self.active_projects[i].crunch_active {
                1.35
            } else {
                1.0
            };
            let team_speed = if avail_count == 0 {
                0.5
            } else {
                1.0 + ((avail_count.saturating_sub(1)) as f64 * 0.12).min(0.6)
            };
            let step = 1.0 * crunch_mult * team_speed * speed_tech_multi;
            self.active_projects[i].progress_weeks += step;

            // Bug generation vs QA fixing
            let bug_roll = self.next_rand_u32(100);
            let bug_chance = if qa_tech_active { 18 } else { 28 };
            if bug_roll < bug_chance && self.active_projects[i].progress_weeks < self.active_projects[i].total_weeks as f64 {
                self.active_projects[i].bugs += 1;
            } else if self.active_projects[i].bugs > 0 && bug_roll > 65 {
                self.active_projects[i].bugs -= 1;
            }

            if self.active_projects[i].progress_weeks >= self.active_projects[i].total_weeks as f64 {
                self.active_projects[i].progress_weeks = self.active_projects[i].total_weeks as f64;
                self.active_projects[i].ready_to_finish = true;
                let p_name = self.active_projects[i].project.name.clone();
                notifications.push(if is_en {
                    format!("Production '{}' is ready for release!", p_name)
                } else {
                    format!("Produktion '{}' ist fertig zur Veröffentlichung!", p_name)
                });
            }
        }

        // Apply slight fatigue to working employees if developing
        if has_active_projects {
            let fatigue_gain = if ergo_active { 2 } else { 3 };
            for emp in &mut self.employees {
                if emp.is_available() {
                    emp.fatigue = (emp.fatigue + fatigue_gain).min(95);
                }
            }
        } else {
            // Natural recovery when idle
            for emp in &mut self.employees {
                if emp.vacation_weeks_left == 0 {
                    emp.fatigue = emp.fatigue.saturating_sub(5);
                    emp.morale = (emp.morale + 2).min(100);
                }
            }
        }

        // 4. Active Contract Work progress
        if let Some(mut contract) = self.active_contract.take() {
            let team_points: f64 = self
                .active_employees()
                .iter()
                .map(|e| (e.total_skill() as f64) / 28.0)
                .sum::<f64>()
                .max(6.0);
            contract.current_points += team_points;
            if contract.current_points >= contract.required_points {
                self.money += contract.reward;
                self.total_revenue += contract.reward;
                notifications.push(if is_en {
                    format!(
                        "Contract '{}' completed! Received {} EUR.",
                        contract.name_en, contract.reward
                    )
                } else {
                    format!(
                        "Auftragsarbeit '{}' abgeschlossen! {} Euro erhalten.",
                        contract.name_de, contract.reward
                    )
                });
            } else if contract.weeks_left <= 1 {
                self.money -= contract.penalty;
                notifications.push(if is_en {
                    format!(
                        "Contract '{}' missed deadline! Penalty: {} EUR.",
                        contract.name_en, contract.penalty
                    )
                } else {
                    format!(
                        "Auftrag '{}' Frist abgelaufen! Vertragsstrafe: {} Euro.",
                        contract.name_de, contract.penalty
                    )
                });
            } else {
                contract.weeks_left -= 1;
                self.active_contract = Some(contract);
            }
        }

        // 5. Pending Research progress
        if let Some(mut res) = self.pending_research.take() {
            if res.weeks_left <= 1 {
                match res.kind.as_str() {
                    "topic" => {
                        if !self.unlocked_topics.contains(&res.name) {
                            self.unlocked_topics.push(res.name.clone());
                        }
                    }
                    "genre" => {
                        if !self.unlocked_genres.contains(&res.name) {
                            self.unlocked_genres.push(res.name.clone());
                        }
                    }
                    "feature" => {
                        if !self.unlocked_features.contains(&res.name) {
                            self.unlocked_features.push(res.name.clone());
                        }
                    }
                    "tech" => {
                        if !self.unlocked_technologies.contains(&res.name) {
                            self.unlocked_technologies.push(res.name.clone());
                        }
                        if res.name == "Radio-Werbung" {
                            self.marketing_efficiency += 0.15;
                        }
                    }
                    _ => {}
                }
                notifications.push(if is_en {
                    format!("Research completed: {}!", res.name)
                } else {
                    format!("Forschung abgeschlossen: {}!", res.name)
                });
            } else {
                res.weeks_left -= 1;
                self.pending_research = Some(res);
            }
        }

        // 6. Active Market Sales & Passive Revenues (Label, Subscription, Hardware)
        let mut active_sales_income: i64 = 0;
        for i in 0..self.game_history.len() {
            if !self.game_history[i].is_active {
                continue;
            }
            self.game_history[i].weeks_on_market += 1;
            let (units, rev) = self.compute_weekly_game_sales(&self.game_history[i], false);
            self.game_history[i].sales += units;
            self.game_history[i].revenue += rev;
            active_sales_income += rev;
            if self.game_history[i].weeks_on_market >= 24 {
                self.game_history[i].is_active = false;
            }
        }
        if active_sales_income > 0 {
            self.money += active_sales_income;
            self.total_revenue += active_sales_income;
        }

        // Soundtrack Label passive royalty
        if self.label_active {
            let label_games = self
                .game_history
                .iter()
                .filter(|g| g.in_soundtrack_label)
                .count() as i64;
            let label_income = (label_games * 450) + (self.fans as i64 / 50).min(15_000);
            if label_income > 0 {
                self.money += label_income;
                self.total_revenue += label_income;
            }
        }

        // Subscription service (AudioPass)
        if self.subscription_active {
            let vault_games = self
                .game_history
                .iter()
                .filter(|g| g.in_subscription_vault)
                .count() as u64;
            let target_subs = (vault_games * 600 + self.fans / 4).max(100);
            if self.subscription_subscribers < target_subs {
                self.subscription_subscribers +=
                    ((target_subs - self.subscription_subscribers) / 5).max(10);
            }
            let weekly_sub_rev =
                ((self.subscription_subscribers as f64) * (self.subscription_price / 4.0)).round()
                    as i64;
            let server_cost = (self.subscription_subscribers as i64 / 20).max(100);
            let net_sub = weekly_sub_rev - server_cost;
            self.money += net_sub;
            if net_sub > 0 {
                self.total_revenue += net_sub;
            }
        }

        // Custom Hardware royalties
        for sc in &mut self.custom_soundcards {
            sc.units_sold += 120;
            self.money += sc.weekly_royalty;
            self.total_revenue += sc.weekly_royalty;
        }
        for cc in &mut self.custom_consoles {
            let weekly_units = ((1500.0 * cc.market_share) as u64).max(50);
            cc.units_sold += weekly_units;
            let hw_profit = (weekly_units as i64) * 15;
            self.money += hw_profit;
            self.total_revenue += hw_profit;
        }

        // Custom Audio Engine third-party licensing royalties
        for (idx, eng) in self.engines.iter().enumerate() {
            if idx >= 1 && eng.licensed_out {
                let license_rev = (eng.tech_level as i64) * 350;
                self.money += license_rev;
                self.total_revenue += license_rev;
            }
        }

        // Acquired rival studio subsidiary weekly dividends
        for r in &self.rivals {
            if r.acquired_by_player {
                let dividend = (r.valuation / 250).max(400);
                self.money += dividend;
                self.total_revenue += dividend;
            }
        }

        // Merchandising sales
        if self.merch_stock > 0 && self.fans > 0 {
            let sold = (self.fans / 50).max(5).min(self.merch_stock);
            self.merch_stock -= sold;
            let merch_rev = (sold as i64) * 20;
            self.money += merch_rev;
            self.total_revenue += merch_rev;
        }

        // 7. Monthly Accounting (Salaries, Studio Rent, Loan Interest)
        if self.month_index() != prev_month {
            let payroll = self.monthly_payroll();
            let rent = self.monthly_rent();
            let loan_interest = if self.bank_loan > 0 {
                (self.bank_loan as f64 * 0.01).round() as i64
            } else {
                0
            };
            let total_monthly_cost = payroll + rent + loan_interest;
            self.money -= total_monthly_cost;

            let cal = self.calendar_text();
            self.emails.insert(
                0,
                Email {
                    sender: tr(self.lang(), "sender_calendar"),
                    subject: if is_en {
                        format!("Monthly Statement: {}", cal)
                    } else {
                        format!("Monatsabrechnung: {}", cal)
                    },
                    body: if is_en {
                        format!(
                            "Balance: {} EUR | Salaries: -{} EUR | Studio Rent: -{} EUR | Loan Interest: -{} EUR",
                            self.money, payroll, rent, loan_interest
                        )
                    } else {
                        format!(
                            "Kontostand: {} Euro | Gehälter: -{} Euro | Studiomiete: -{} Euro | Kreditzinsen: -{} Euro",
                            self.money, payroll, rent, loan_interest
                        )
                    },
                    week: self.week,
                    year: self.calendar_year(),
                    read: false,
                },
            );
            // Keep inbox tidy
            if self.emails.len() > 40 {
                self.emails.truncate(40);
            }
            if self.available_contracts.len() < 2 {
                self.refresh_contracts();
            }
            if self.fans >= 100 {
                self.unanswered_fan_mails = (self.unanswered_fan_mails + 1).min(10);
            }
        }

        // 8. Annual Transition (Year Event, GOTY & Best Audio Design Awards)
        let curr_year = self.calendar_year();
        if curr_year > prev_year {
            let year_notes = self.apply_year_event_internal(curr_year);
            notifications.extend(year_notes);
            if let Some(award_msg) = self.evaluate_annual_goty(prev_year) {
                notifications.push(award_msg);
            }
            if let Some(audio_award_msg) = self.evaluate_annual_audio_award(prev_year) {
                notifications.push(audio_award_msg);
            }
            self.refresh_contracts();
            self.refresh_hire_candidates();
        }

        // 9. Studio Achievements
        let achievement_notes = self.check_and_unlock_achievements();
        notifications.extend(achievement_notes);

        notifications
    }

    pub fn evaluate_annual_goty(&mut self, year: u32) -> Option<String> {
        // Update rivals' annual scores
        for r in &mut self.rivals {
            if !r.acquired_by_player {
                r.best_year_score = (r.reputation + 0.3).clamp(5.0, 9.2);
            }
        }

        let player_best = self
            .game_history
            .iter()
            .filter(|g| g.release_year == year)
            .filter_map(|g| g.review.as_ref().map(|r| (g.name.clone(), r.average())))
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));

        if let Some((best_name, best_score)) = player_best {
            let top_rival_score = self
                .rivals
                .iter()
                .filter(|r| !r.acquired_by_player)
                .map(|r| r.best_year_score)
                .fold(6.5, f64::max);

            if best_score >= top_rival_score {
                self.goty_awards += 1;
                let prize = 25_000 * (self.office_level as i64 + 1);
                self.money += prize;
                self.fans += 2_500;
                let msg = if self.is_en() {
                    format!(
                        "GOTY Award {} Winner: '{}' ({:.1}/10)! Prize: {} EUR + 2,500 fans!",
                        year, best_name, best_score, prize
                    )
                } else {
                    format!(
                        "Spiel des Jahres (GOTY {}) gewonnen mit '{}' ({:.1}/10)! Preisgeld: {} Euro + 2.500 Fans!",
                        year, best_name, best_score, prize
                    )
                };
                self.emails.insert(
                    0,
                    Email {
                        sender: tr(self.lang(), "sender_awards"),
                        subject: format!("GOTY {}", year),
                        body: msg.clone(),
                        week: self.week,
                        year: self.calendar_year(),
                        read: false,
                    },
                );
                return Some(msg);
            }
        }
        None
    }

    pub fn evaluate_annual_audio_award(&mut self, year: u32) -> Option<String> {
        let best_audio_game = self
            .game_history
            .iter()
            .filter(|g| g.release_year == year && g.sliders[2] >= 7)
            .filter_map(|g| {
                g.review
                    .as_ref()
                    .map(|r| (g.name.clone(), r.average(), g.sliders[2]))
            })
            .max_by(|a, b| {
                a.1.partial_cmp(&b.1)
                    .unwrap_or(std::cmp::Ordering::Equal)
                    .then_with(|| a.2.cmp(&b.2))
            });

        if let Some((best_name, best_score, sound_focus)) = best_audio_game {
            if best_score >= 7.5 {
                self.audio_awards += 1;
                self.money += 15_000;
                self.fans += 400;
                self.hype = (self.hype + 15.0).clamp(0.0, 250.0);
                let msg = if self.is_en() {
                    format!(
                        "Golden Microphone (Best Audio Design {}) awarded to '{}' ({:.1}/10, Sound {}/10)! Prize: +15,000 EUR, +400 fans, +15 hype!",
                        year, best_name, best_score, sound_focus
                    )
                } else {
                    format!(
                        "Goldenes Mikrofon (Bester Sound des Jahres {}) gewonnen mit '{}' ({:.1}/10, Sound {}/10)! Preisgeld: +15.000 Euro, +400 Fans, +15 Hype!",
                        year, best_name, best_score, sound_focus
                    )
                };
                self.emails.insert(
                    0,
                    Email {
                        sender: tr(self.lang(), "sender_awards"),
                        subject: if self.is_en() {
                            format!("Golden Microphone (Best Audio Design) {}", year)
                        } else {
                            format!("Goldenes Mikrofon (Bester Sound des Jahres) {}", year)
                        },
                        body: msg.clone(),
                        week: self.week,
                        year: self.calendar_year(),
                        read: false,
                    },
                );
                return Some(msg);
            }
        }
        None
    }

    // --- Subsystem Actions (All Year-Validated per lessons_learned.md!) ---

    pub fn start_research(
        &mut self,
        kind: &str,
        name: &str,
        cost: i64,
        unlock_year: u32,
        weeks: u32,
        tech_bonus: u32,
    ) -> Result<String, String> {
        let year = self.calendar_year();
        if year < unlock_year {
            return Err(if self.is_en() {
                format!(
                    "'{}' cannot be researched until the year {}.",
                    name, unlock_year
                )
            } else {
                format!(
                    "'{}' kann erst ab dem Jahr {} erforscht werden.",
                    name, unlock_year
                )
            });
        }
        if self.pending_research.is_some() {
            return Err(if self.is_en() {
                "Another research project is already in progress!".to_string()
            } else {
                "Es läuft bereits ein Forschungsprojekt!".to_string()
            });
        }
        if self.money < cost {
            return Err(if self.is_en() {
                format!("Not enough money! Research costs {} EUR.", cost)
            } else {
                format!("Nicht genug Geld! Die Forschung kostet {} Euro.", cost)
            });
        }
        self.money -= cost;
        self.pending_research = Some(PendingResearch {
            kind: kind.to_string(),
            name: name.to_string(),
            weeks_left: weeks.max(1),
            total_weeks: weeks.max(1),
            tech_bonus,
        });
        Ok(if self.is_en() {
            format!(
                "Started researching '{}' ({} weeks, {} EUR).",
                name, weeks, cost
            )
        } else {
            format!(
                "Forschung an '{}' gestartet ({} Wochen, {} Euro).",
                name, weeks, cost
            )
        })
    }

    pub fn build_custom_engine(&mut self, custom_name: &str) -> Result<String, String> {
        let base_cost = 15_000 + (self.unlocked_features.len() as i64 * 5_000);
        if self.money < base_cost {
            return Err(if self.is_en() {
                format!("Building this custom engine costs {} EUR.", base_cost)
            } else {
                format!(
                    "Die Entwicklung dieser eigenen Engine kostet {} Euro.",
                    base_cost
                )
            });
        }
        self.money -= base_cost;
        let tech_level = (self.unlocked_features.len() as u32 / 2).max(1) + 1;
        let quality_bonus = (0.08 + (self.unlocked_features.len() as f64 * 0.035)).min(0.60);
        let name = if custom_name.trim().is_empty() {
            format!("AudioEngine V{}", self.engines.len() + 1)
        } else {
            custom_name.trim().to_string()
        };
        self.engines.push(Engine {
            name: name.clone(),
            features: self.unlocked_features.clone(),
            tech_level,
            quality_bonus,
            license_fee: (tech_level as i64) * 8_000,
            licensed_out: false,
        });
        self.current_draft.engine_idx = self.engines.len() - 1;
        Ok(if self.is_en() {
            format!(
                "Created custom engine '{}' (Tech Level {}, Quality Bonus +{:.0}%)!",
                name,
                tech_level,
                quality_bonus * 100.0
            )
        } else {
            format!(
                "Eigene Engine '{}' entwickelt (Tech-Stufe {}, Qualitätsbonus +{:.0}%)!",
                name,
                tech_level,
                quality_bonus * 100.0
            )
        })
    }

    pub fn toggle_engine_license(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx == 0 {
            return Err(if is_en {
                "The starter engine cannot be licensed out to third parties.".to_string()
            } else {
                "Die Basis-Engine kann nicht an Drittstudios lizenziert werden.".to_string()
            });
        }
        let eng = self.engines.get_mut(idx).ok_or_else(|| {
            if is_en {
                "Invalid audio engine index.".to_string()
            } else {
                "Ungültige Audio-Engine.".to_string()
            }
        })?;
        eng.licensed_out = !eng.licensed_out;
        let weekly_royalty = (eng.tech_level as i64) * 350;
        let name = eng.name.clone();
        let now_licensed = eng.licensed_out;
        Ok(if now_licensed {
            if is_en {
                format!(
                    "Audio engine '{}' is now licensed to third parties (+{} EUR/week).",
                    name, weekly_royalty
                )
            } else {
                format!(
                    "Audio-Engine '{}' ist jetzt an Drittstudios lizenziert (+{} Euro/Woche).",
                    name, weekly_royalty
                )
            }
        } else if is_en {
            format!(
                "Third-party licensing for '{}' paused (private studio use).",
                name
            )
        } else {
            format!(
                "Drittlizenzierung für '{}' beendet (wieder exklusiv privat).",
                name
            )
        })
    }

    pub fn hire_candidate(&mut self, idx: usize) -> Result<String, String> {
        if self.employees.len() >= self.max_employees() {
            return Err(if self.is_en() {
                format!(
                    "Studio capacity reached ({}/{})! Upgrade your studio first.",
                    self.employees.len(),
                    self.max_employees()
                )
            } else {
                format!(
                    "Maximale Mitarbeiterzahl erreicht ({}/{})! Baue zuerst dein Tonstudio aus.",
                    self.employees.len(),
                    self.max_employees()
                )
            });
        }
        if idx >= self.hire_candidates.len() {
            return Err("Ungültiger Kandidat.".to_string());
        }
        let signing_fee = self.hire_candidates[idx].salary * 2;
        if self.money < signing_fee {
            return Err(if self.is_en() {
                format!("Hiring requires a signing bonus of {} EUR.", signing_fee)
            } else {
                format!(
                    "Für die Einstellung wird ein Handgeld von {} Euro benötigt.",
                    signing_fee
                )
            });
        }
        self.money -= signing_fee;
        let emp = self.hire_candidates.remove(idx);
        let msg = if self.is_en() {
            format!("Hired {} as {}!", emp.name, emp.role)
        } else {
            format!("{} als {} eingestellt!", emp.name, emp.role)
        };
        self.employees.push(emp);
        Ok(msg)
    }

    pub fn send_employee_on_vacation(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        let emp = self
            .employees
            .get_mut(idx)
            .ok_or_else(|| "Mitarbeiter nicht gefunden.".to_string())?;
        if emp.vacation_weeks_left > 0 {
            return Err(if is_en {
                format!("{} is already on vacation!", emp.name)
            } else {
                format!("{} ist bereits im Urlaub!", emp.name)
            });
        }
        let bonus_cost = 1_000;
        if self.money < bonus_cost {
            return Err(if is_en {
                "Not enough money for vacation bonus (1,000 EUR).".to_string()
            } else {
                "Nicht genug Geld für das Urlaubsgeld (1.000 Euro).".to_string()
            });
        }
        self.money -= bonus_cost;
        emp.vacation_weeks_left = 3;
        emp.training_weeks_left = 0;
        let name = emp.name.clone();
        Ok(if is_en {
            format!("Sent {} on a 3-week paid vacation!", name)
        } else {
            format!("{} für 3 Wochen in den Erholungsurlaub geschickt!", name)
        })
    }

    pub fn train_employee(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        let cost = 5_000;
        if self.money < cost {
            return Err(if is_en {
                "Training workshop costs 5,000 EUR.".to_string()
            } else {
                "Die Fortbildung kostet 5.000 Euro.".to_string()
            });
        }
        let emp = self
            .employees
            .get_mut(idx)
            .ok_or_else(|| "Mitarbeiter nicht gefunden.".to_string())?;
        if !emp.is_available() {
            return Err(if is_en {
                format!("{} is currently unavailable (vacation or training).", emp.name)
            } else {
                format!(
                    "{} ist derzeit im Urlaub oder bereits in einer Schulung.",
                    emp.name
                )
            });
        }
        self.money -= cost;
        emp.training_weeks_left = 2;
        let name = emp.name.clone();
        Ok(if is_en {
            format!("{} started a 2-week masterclass training!", name)
        } else {
            format!("{} nimmt für 2 Wochen an einer Fortbildung teil!", name)
        })
    }

    pub fn fire_employee(&mut self, idx: usize) -> Result<String, String> {
        if idx >= self.employees.len() {
            return Err("Ungültiger Mitarbeiter.".to_string());
        }
        if self.employees[idx].is_ceo {
            return Err(if self.is_en() {
                "You cannot fire the Studio Founder (CEO)!".to_string()
            } else {
                "Du kannst den Studio-Gründer (CEO) nicht entlassen!".to_string()
            });
        }
        let emp = self.employees.remove(idx);
        Ok(if self.is_en() {
            format!("Dismissed {}.", emp.name)
        } else {
            format!("{} wurde entlassen.", emp.name)
        })
    }

    pub fn upgrade_office(&mut self) -> Result<String, String> {
        let next_lvl = self.office_level + 1;
        let spec = OFFICE_LEVELS.get(next_lvl).ok_or_else(|| {
            if self.is_en() {
                "Maximum studio level already reached!".to_string()
            } else {
                "Maximale Ausbaustufe des Tonstudios bereits erreicht!".to_string()
            }
        })?;
        if self.money < spec.upgrade_cost {
            return Err(if self.is_en() {
                format!(
                    "Upgrade to '{}' costs {} EUR.",
                    spec.name_en, spec.upgrade_cost
                )
            } else {
                format!(
                    "Der Ausbau zu '{}' kostet {} Euro.",
                    spec.name_de, spec.upgrade_cost
                )
            });
        }
        self.money -= spec.upgrade_cost;
        self.office_level = next_lvl;
        Ok(if self.is_en() {
            format!(
                "Upgraded studio to '{}'! Max employees: {}.",
                spec.name_en, spec.max_employees
            )
        } else {
            format!(
                "Tonstudio ausgebaut zu '{}'! Maximale Teamgröße: {} Mitarbeiter.",
                spec.name_de, spec.max_employees
            )
        })
    }

    pub fn attend_soundcon(&mut self, booth_tier: usize) -> Result<String, String> {
        let year = self.calendar_year();
        if year < 1995 {
            return Err(if self.is_en() {
                "The SoundCon Expo does not open until 1995! Earlier eras use radio & press campaigns.".to_string()
            } else {
                "Die SoundCon Messe findet erst ab dem Jahr 1995 statt! Nutze vorher Radio- und Pressekampagnen.".to_string()
            });
        }
        if self.last_soundcon_year == year {
            return Err(if self.is_en() {
                format!("You already attended SoundCon in {}!", year)
            } else {
                format!("Du hast im Jahr {} bereits an der SoundCon teilgenommen!", year)
            });
        }
        let (cost, hype_gain, fan_gain, tier_name) = match booth_tier {
            0 => (15_000, 30.0, 800, "Kleiner Hörstand"),
            1 => (50_000, 75.0, 3_000, "Große Klangbühne"),
            _ => (150_000, 150.0, 10_000, "Gigantischer Sound-Dome"),
        };
        if self.money < cost {
            return Err(if self.is_en() {
                format!("SoundCon booth costs {} EUR.", cost)
            } else {
                format!("Dieser Messestand kostet {} Euro.", cost)
            });
        }
        self.money -= cost;
        self.last_soundcon_year = year;
        self.hype = (self.hype + hype_gain).clamp(0.0, 250.0);
        self.fans += fan_gain;
        let summary = format!("SoundCon {} ({}): +{} Fans, +{:.0} Hype", year, tier_name, fan_gain, hype_gain);
        self.soundcon_history.push(summary.clone());
        Ok(summary)
    }

    pub fn develop_soundcard(&mut self, card_name: &str) -> Result<String, String> {
        let year = self.calendar_year();
        if year < 1975 && !self.unlocked_technologies.iter().any(|t| t == "Hardware-Labor") {
            return Err(if self.is_en() {
                "Custom soundcard development requires the year 1975 or 'Hardware-Labor' research!".to_string()
            } else {
                "Eigene Soundkarten erfordern das Jahr 1975 oder die Forschung 'Hardware-Labor'!".to_string()
            });
        }
        let cost = 60_000;
        if self.money < cost {
            return Err(if self.is_en() {
                format!("Developing a custom soundcard costs {} EUR.", cost)
            } else {
                format!("Die Entwicklung einer eigenen Soundkarte kostet {} Euro.", cost)
            });
        }
        self.money -= cost;
        let name = if card_name.trim().is_empty() {
            format!("KlangKarte Pro {}", self.custom_soundcards.len() + 1)
        } else {
            card_name.trim().to_string()
        };
        let bonus = 0.08 + (self.custom_soundcards.len() as f64 * 0.04).min(0.20);
        let royalty = 1_200 + (self.custom_soundcards.len() as i64 * 600);
        self.custom_soundcards.push(CustomSoundCard {
            name: name.clone(),
            generation_year: year,
            sound_bonus: bonus,
            units_sold: 500,
            weekly_royalty: royalty,
        });
        Ok(if self.is_en() {
            format!(
                "Launched soundcard '{}'! Passive royalty: +{} EUR/week.",
                name, royalty
            )
        } else {
            format!(
                "Eigene Soundkarte '{}' veröffentlicht! Lizenzeinnahmen: +{} Euro pro Woche.",
                name, royalty
            )
        })
    }

    pub fn develop_console(&mut self, console_name: &str) -> Result<String, String> {
        let year = self.calendar_year();
        if year < 1975 && !self.unlocked_technologies.iter().any(|t| t == "Hardware-Labor") {
            return Err(if self.is_en() {
                "Custom console development requires the year 1975 or 'Hardware-Labor' research!".to_string()
            } else {
                "Eigene Konsolen erfordern das Jahr 1975 oder die Forschung 'Hardware-Labor'!".to_string()
            });
        }
        let cost = 200_000;
        if self.money < cost {
            return Err(if self.is_en() {
                format!("Developing a custom console costs {} EUR.", cost)
            } else {
                format!("Die Entwicklung einer eigenen Konsole kostet {} Euro.", cost)
            });
        }
        self.money -= cost;
        let name = if console_name.trim().is_empty() {
            format!("SonicConsole {}", self.custom_consoles.len() + 1)
        } else {
            console_name.trim().to_string()
        };
        self.custom_consoles.push(CustomConsole {
            name: name.clone(),
            release_year: year,
            market_share: 0.18,
            units_sold: 5_000,
            hype: 50.0,
        });
        if !self.bought_platforms.contains(&name) {
            self.bought_platforms.push(name.clone());
        }
        Ok(if self.is_en() {
            format!(
                "Launched custom console '{}'! Now available as a target platform.",
                name
            )
        } else {
            format!(
                "Eigene Konsole '{}' auf den Markt gebracht! Ab sofort als Zielplattform wählbar.",
                name
            )
        })
    }

    pub fn take_loan(&mut self, amount: i64) -> Result<String, String> {
        if amount <= 0 {
            return Err("Loan amount must be positive.".to_string());
        }
        let max_credit = 150_000 + (self.office_level as i64 * 200_000);
        if self.bank_loan + amount > max_credit {
            return Err(if self.is_en() {
                format!("Credit limit reached (max {} EUR)!", max_credit)
            } else {
                format!("Kreditlimit erreicht (maximal {} Euro)!", max_credit)
            });
        }
        self.bank_loan += amount;
        self.money += amount;
        Ok(if self.is_en() {
            format!(
                "Took bank loan of {} EUR. Total debt: {} EUR.",
                amount, self.bank_loan
            )
        } else {
            format!(
                "Bankkredit über {} Euro aufgenommen. Gesamtschuld: {} Euro.",
                amount, self.bank_loan
            )
        })
    }

    pub fn repay_loan(&mut self, amount: i64) -> Result<String, String> {
        if self.bank_loan <= 0 {
            return Err(if self.is_en() {
                "You have no active bank loans!".to_string()
            } else {
                "Du hast aktuell keine offenen Bankkredite!".to_string()
            });
        }
        let pay = amount.min(self.bank_loan).min(self.money.max(0));
        if pay <= 0 {
            return Err(if self.is_en() {
                "Not enough cash to repay the loan.".to_string()
            } else {
                "Nicht genug Bargeld zur Tilgung vorhanden.".to_string()
            });
        }
        self.money -= pay;
        self.bank_loan -= pay;
        Ok(if self.is_en() {
            format!(
                "Repaid {} EUR. Remaining loan: {} EUR.",
                pay, self.bank_loan
            )
        } else {
            format!(
                "{} Euro Kredit getilgt. Restschuld: {} Euro.",
                pay, self.bank_loan
            )
        })
    }

    // --- Persistence (Save/Load JSON) ---

    pub fn answer_fan_mail(&mut self) -> Result<String, String> {
        if self.unanswered_fan_mails == 0 {
            return Err(if self.is_en() {
                "No unanswered fan mail right now. Release productions or wait a few weeks!"
                    .to_string()
            } else {
                "Aktuell liegt keine neue Fanpost vor. Veröffentliche Produktionen oder warte einige Wochen!"
                    .to_string()
            });
        }
        self.unanswered_fan_mails -= 1;
        self.fans += 200;
        self.hype = (self.hype + 5.0).min(250.0);
        self.accessibility_reputation += 5;
        Ok(if self.is_en() {
            format!(
                "Answered community fan mail! +200 fans, +5 hype ({} remaining).",
                self.unanswered_fan_mails
            )
        } else {
            format!(
                "Fanpost herzlich beantwortet! +200 Fans und +5 Hype (noch {} offen).",
                self.unanswered_fan_mails
            )
        })
    }

    pub fn release_patch(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx >= self.game_history.len() {
            return Err(if is_en {
                "Invalid game index.".to_string()
            } else {
                "Ungültiges Spiel.".to_string()
            });
        }
        if self.game_history[idx].bugs == 0 {
            return Err(if is_en {
                "This production already has 0 bugs!".to_string()
            } else {
                "Diese Produktion ist bereits komplett fehlerfrei (0 Bugs)!".to_string()
            });
        }
        if self.money < 2_000 {
            return Err(if is_en {
                "Not enough money for a patch (2,000 EUR).".to_string()
            } else {
                "Nicht genug Geld für einen Patch (2.000 Euro).".to_string()
            });
        }
        self.money -= 2_000;
        let g = &mut self.game_history[idx];
        g.bugs = 0;
        g.patches_released += 1;
        g.weeks_on_market = g.weeks_on_market.saturating_sub(3);
        g.is_active = true;
        let name = g.name.clone();
        Ok(if is_en {
            format!(
                "Released patch for '{}'! Fixed all bugs and refreshed market interest.",
                name
            )
        } else {
            format!(
                "Patch für '{}' veröffentlicht! Alle Bugs behoben und Verkäufe belebt.",
                name
            )
        })
    }

    pub fn release_dlc(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx >= self.game_history.len() {
            return Err(if is_en {
                "Invalid game index.".to_string()
            } else {
                "Ungültiges Spiel.".to_string()
            });
        }
        if self.game_history[idx].dlc_count >= 2 {
            return Err(if is_en {
                "Maximum of 2 Addons/DLCs already released for this production!".to_string()
            } else {
                "Für diese Produktion wurden bereits die maximal 2 Addons/DLCs veröffentlicht!"
                    .to_string()
            });
        }
        if self.money < 6_000 {
            return Err(if is_en {
                "Not enough money for an Addon/DLC (6,000 EUR).".to_string()
            } else {
                "Nicht genug Geld für ein Addon/DLC (6.000 Euro).".to_string()
            });
        }
        self.money -= 6_000;
        let g = &mut self.game_history[idx];
        g.dlc_count += 1;
        let bonus_sales = (g.sales / 5).clamp(300, 50_000);
        let bonus_rev = (bonus_sales as i64) * 15;
        g.sales += bonus_sales;
        g.revenue += bonus_rev;
        let name = g.name.clone();
        self.money += bonus_rev;
        self.total_revenue += bonus_rev;
        Ok(if is_en {
            format!(
                "Released Addon/DLC for '{}'! +{} sales, +{} EUR revenue!",
                name, bonus_sales, bonus_rev
            )
        } else {
            format!(
                "Addon für '{}' veröffentlicht! +{} Verkäufe, +{} Euro Umsatz!",
                name, bonus_sales, bonus_rev
            )
        })
    }

    pub fn polish_active_project(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx >= self.active_projects.len() {
            return Err(if is_en {
                "Invalid active project.".to_string()
            } else {
                "Ungültiges aktives Projekt.".to_string()
            });
        }
        if self.active_projects[idx].polish_passes >= 3 && self.active_projects[idx].bugs == 0 {
            return Err(if is_en {
                "Maximum QA & Mastering passes (3/3) reached and 0 bugs remaining!".to_string()
            } else {
                "Maximale QA- & Mastering-Durchläufe (3/3) erreicht und 0 Bugs übrig!".to_string()
            });
        }
        let cost = 1_500;
        if self.money < cost {
            return Err(if is_en {
                "Not enough money for QA & Mastering Polish (1,500 EUR).".to_string()
            } else {
                "Nicht genug Geld für QA-Feinschliff & Mastering (1.500 Euro).".to_string()
            });
        }
        self.money -= cost;
        let ap = &mut self.active_projects[idx];
        let fixed = ap.bugs.min(4);
        ap.bugs = ap.bugs.saturating_sub(4);
        if ap.polish_passes < 3 {
            ap.polish_passes += 1;
            ap.project.quality_boost += 0.03;
        }
        let name = ap.project.name.clone();
        let rem_bugs = ap.bugs;
        let passes = ap.polish_passes;
        Ok(if is_en {
            format!(
                "QA & Mastering session on '{}': fixed {} bugs ({} remaining), quality polish {}/3!",
                name, fixed, rem_bugs, passes
            )
        } else {
            format!(
                "QA-Feinschliff & Mastering für '{}': {} Bugs behoben (noch {} übrig), Qualitäts-Politur {}/3!",
                name, fixed, rem_bugs, passes
            )
        })
    }

    pub fn apply_studio_decision(&mut self, idx: usize, option: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx >= self.active_projects.len() {
            return Err(if is_en {
                "Invalid active project.".to_string()
            } else {
                "Ungültiges aktives Projekt.".to_string()
            });
        }
        if self.active_projects[idx].decision_made {
            return Err(if is_en {
                "A creative studio decision has already been made for this project!".to_string()
            } else {
                "Für dieses Projekt wurde bereits eine kreative Studio-Entscheidung getroffen!"
                    .to_string()
            });
        }
        match option {
            0 => {
                let cost = 3_000;
                if self.money < cost {
                    return Err(if is_en {
                        "Live Foley & Acoustic Session requires 3,000 EUR.".to_string()
                    } else {
                        "Die Live-Foley- & Akustik-Session kostet 3.000 Euro.".to_string()
                    });
                }
                self.money -= cost;
                let ap = &mut self.active_projects[idx];
                ap.decision_made = true;
                ap.project.quality_boost += 0.06;
                let name = ap.project.name.clone();
                self.hype = (self.hype + 12.0).clamp(0.0, 250.0);
                Ok(if is_en {
                    format!(
                        "Recorded Live Foley & Acoustic Session for '{}'! +6% quality bonus, +12 hype!",
                        name
                    )
                } else {
                    format!(
                        "Live-Foley- & Akustik-Session für '{}' aufgenommen! +6% Qualitätsbonus, +12 Hype!",
                        name
                    )
                })
            }
            1 => {
                let ap = &mut self.active_projects[idx];
                ap.decision_made = true;
                let fixed = ap.bugs;
                ap.bugs = 0;
                ap.total_weeks += 1;
                if ap.ready_to_finish && ap.progress_weeks < ap.total_weeks as f64 {
                    ap.ready_to_finish = false;
                }
                ap.project.quality_boost += 0.04;
                let name = ap.project.name.clone();
                Ok(if is_en {
                    format!(
                        "Signal & Code Refactoring on '{}': eliminated {} bugs, +4% quality (+1 week dev time)!",
                        name, fixed
                    )
                } else {
                    format!(
                        "Signal- & Code-Refactoring für '{}': {} Bugs behoben, +4% Qualität (+1 Woche Dauer)!",
                        name, fixed
                    )
                })
            }
            _ => {
                let cost = 2_000;
                if self.money < cost {
                    return Err(if is_en {
                        "Community Playtest Session requires 2,000 EUR.".to_string()
                    } else {
                        "Der Community-Fokus-Test kostet 2.000 Euro.".to_string()
                    });
                }
                self.money -= cost;
                let ap = &mut self.active_projects[idx];
                ap.decision_made = true;
                ap.project.quality_boost += 0.05;
                let name = ap.project.name.clone();
                self.fans += 250;
                self.hype = (self.hype + 15.0).clamp(0.0, 250.0);
                Ok(if is_en {
                    format!(
                        "Ran Community Playtest for '{}'! +5% quality, +250 fans, +15 hype!",
                        name
                    )
                } else {
                    format!(
                        "Community-Fokus-Test für '{}' durchgeführt! +5% Qualität, +250 Fans, +15 Hype!",
                        name
                    )
                })
            }
        }
    }

    pub fn analyze_post_mortem(&mut self, idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if idx >= self.game_history.len() {
            return Err(if is_en {
                "Invalid game index.".to_string()
            } else {
                "Ungültiges Spiel.".to_string()
            });
        }
        if self.game_history[idx].post_mortem_done {
            return Err(if is_en {
                "Post-Mortem analysis was already completed for this production!".to_string()
            } else {
                "Für diese Produktion wurde bereits ein Post-Mortem-Spielbericht erstellt!"
                    .to_string()
            });
        }
        self.game_history[idx].post_mortem_done = true;
        let g = self.game_history[idx].clone();
        if let Some(ref mut lfg) = self.last_finished_game {
            if lfg.name == g.name {
                lfg.post_mortem_done = true;
            }
        }
        let compat = get_compatibility(&g.topic, &g.genre);
        let aud_compat = get_audience_compatibility(&g.topic, &g.genre, &g.audience);
        let ideal = get_ideal_sliders(&g.genre);

        let mut biggest_gap = 0i32;
        let mut gap_idx = 2usize;
        for i in 0..6 {
            let diff = ideal[i] as i32 - g.sliders[i] as i32;
            if diff.abs() > biggest_gap.abs() {
                biggest_gap = diff;
                gap_idx = i;
            }
        }
        let slider_hint = if biggest_gap == 0 {
            if is_en {
                "Sliders matched the genre profile perfectly!".to_string()
            } else {
                "Alle Slider trafen das Genre-Profil perfekt!".to_string()
            }
        } else if biggest_gap > 0 {
            if is_en {
                format!(
                    "For '{}', increase '{}' (ideal: {}, used: {}).",
                    g.genre, SLIDER_NAMES[gap_idx], ideal[gap_idx], g.sliders[gap_idx]
                )
            } else {
                format!(
                    "Für '{}' sollte '{}' höher gewichtet sein (Ideal: {}, gewählt: {}).",
                    g.genre, SLIDER_NAMES[gap_idx], ideal[gap_idx], g.sliders[gap_idx]
                )
            }
        } else if is_en {
            format!(
                "For '{}', reduce '{}' (ideal: {}, used: {}).",
                g.genre, SLIDER_NAMES[gap_idx], ideal[gap_idx], g.sliders[gap_idx]
            )
        } else {
            format!(
                "Für '{}' war '{}' zu hoch angesetzt (Ideal: {}, gewählt: {}).",
                g.genre, SLIDER_NAMES[gap_idx], ideal[gap_idx], g.sliders[gap_idx]
            )
        };

        self.accessibility_reputation += 15;
        self.fans += 200;
        self.hype = (self.hype + 15.0).clamp(0.0, 250.0);

        let report_msg = if is_en {
            format!(
                "Post-Mortem '{}': Topic+Genre Synergy: {}/3 stars | Audience Fit ('{}'): {}/3 | Insight: {} | Reward: +200 Fans, +15 Hype, +15 Studio Know-How!",
                g.name, compat, g.audience, aud_compat, slider_hint
            )
        } else {
            format!(
                "Spielbericht (Post-Mortem) zu '{}': Thema+Genre-Synergie: {}/3 Sterne | Zielgruppe ('{}'): {}/3 | Erkenntnis: {} | Belohnung: +200 Fans, +15 Hype, +15 Studio-Know-How!",
                g.name, compat, g.audience, aud_compat, slider_hint
            )
        };

        self.emails.insert(
            0,
            Email {
                sender: if is_en {
                    "Studio Analytics".to_string()
                } else {
                    "Studio-Analyse".to_string()
                },
                subject: if is_en {
                    format!("Post-Mortem Report: {}", g.name)
                } else {
                    format!("Post-Mortem Spielbericht: {}", g.name)
                },
                body: report_msg.clone(),
                week: self.week,
                year: self.calendar_year(),
                read: false,
            },
        );

        Ok(report_msg)
    }

    /// Start a modernized remaster of an eligible classic from `game_history`.
    pub fn develop_remaster(&mut self, history_idx: usize) -> Result<String, String> {
        let is_en = self.is_en();
        if history_idx >= self.game_history.len() {
            return Err(if is_en {
                "Invalid game index.".to_string()
            } else {
                "Ungültiges Spiel.".to_string()
            });
        }
        let orig = self.game_history[history_idx].clone();
        if orig.name.contains("(Remaster)") {
            return Err(if is_en {
                format!("'{}' is already a remaster!", orig.name)
            } else {
                format!("'{}' ist bereits ein Remaster!", orig.name)
            });
        }
        let remaster_title = format!("{} (Remaster)", orig.name);
        if self
            .active_projects
            .iter()
            .any(|ap| ap.project.name == remaster_title)
            || self.game_history.iter().any(|g| g.name == remaster_title)
        {
            return Err(if is_en {
                format!("A remaster of '{}' already exists or is in production!", orig.name)
            } else {
                format!("Für '{}' existiert oder entsteht bereits ein Remaster!", orig.name)
            });
        }

        let year = self.calendar_year();
        if year < orig.release_year + 3 {
            return Err(if is_en {
                format!(
                    "'{}' is too recent for a remaster (available from {}).",
                    orig.name,
                    orig.release_year + 3
                )
            } else {
                format!(
                    "'{}' ist noch zu neu für ein Remaster (erst ab {} möglich).",
                    orig.name,
                    orig.release_year + 3
                )
            });
        }

        let base_size_cost = match orig.size.as_str() {
            "Klein" => 6_000,
            "Mittel" => 18_000,
            "Groß" => 55_000,
            "AAA" => 180_000,
            "MMO" => 350_000,
            _ => 12_000,
        };
        let cost = if orig.dev_cost > 0 {
            ((orig.dev_cost as f64) * 0.5).round() as i64
        } else {
            base_size_cost / 2
        };
        if self.money < cost {
            return Err(if is_en {
                format!(
                    "Not enough money! Remastering '{}' requires {} EUR.",
                    orig.name, cost
                )
            } else {
                format!(
                    "Nicht genug Geld! Das Remaster von '{}' kostet {} Euro.",
                    orig.name, cost
                )
            });
        }

        let base_weeks = match orig.size.as_str() {
            "Klein" => 4,
            "Mittel" => 6,
            "Groß" => 10,
            "AAA" => 14,
            "MMO" => 18,
            _ => 6,
        };
        let total_weeks = ((base_weeks as f64) * 0.6).round().max(1.0) as u32;

        let avail_plats = get_available_platforms(year);
        let best_standard = avail_plats
            .iter()
            .filter(|p| self.bought_platforms.iter().any(|bp| bp == p.name))
            .max_by(|a, b| {
                a.market_multi
                    .partial_cmp(&b.market_multi)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
        let best_custom = self.custom_consoles.iter().max_by(|a, b| {
            a.market_share
                .partial_cmp(&b.market_share)
                .unwrap_or(std::cmp::Ordering::Equal)
        });
        let platform = match (best_standard, best_custom) {
            (Some(std_p), Some(cust_p)) => {
                let cust_multi = 8.0 + cust_p.market_share * 10.0;
                if cust_multi > std_p.market_multi {
                    cust_p.name.clone()
                } else {
                    std_p.name.to_string()
                }
            }
            (Some(std_p), None) => std_p.name.to_string(),
            (None, Some(cust_p)) => cust_p.name.clone(),
            (None, None) => avail_plats
                .iter()
                .filter(|p| p.license_fee == 0)
                .max_by(|a, b| {
                    a.market_multi
                        .partial_cmp(&b.market_multi)
                        .unwrap_or(std::cmp::Ordering::Equal)
                })
                .or_else(|| avail_plats.first())
                .map(|p| p.name.to_string())
                .unwrap_or_else(|| orig.platform.clone()),
        };

        let engine_name = self
            .engines
            .iter()
            .max_by(|a, b| {
                a.tech_level.cmp(&b.tech_level).then_with(|| {
                    a.quality_bonus
                        .partial_cmp(&b.quality_bonus)
                        .unwrap_or(std::cmp::Ordering::Equal)
                })
            })
            .map(|e| e.name.clone())
            .unwrap_or_else(|| orig.engine_name.clone());

        self.money -= cost;
        self.hype = (self.hype + 15.0).clamp(0.0, 250.0);

        let proj = GameProject {
            name: remaster_title.clone(),
            topic: orig.topic,
            genre: orig.genre,
            sub_genre: orig.sub_genre,
            platform: platform.clone(),
            audience: orig.audience,
            size: orig.size,
            marketing: "Keine Kampagne".to_string(),
            engine_name,
            sliders: orig.sliders,
            review: None,
            sales: 0,
            revenue: 0,
            dev_cost: cost,
            release_week: 0,
            release_year: year,
            weeks_on_market: 0,
            is_active: true,
            bugs: 0,
            patches_released: 0,
            dlc_count: 0,
            in_soundtrack_label: false,
            in_subscription_vault: false,
            sequel_number: 0,
            publisher_idx: 0,
            post_mortem_done: false,
            quality_boost: 0.04,
        };

        self.active_projects.push(ActiveProject {
            project: proj,
            progress_weeks: 0.0,
            total_weeks,
            bugs: 0,
            crunch_active: false,
            ready_to_finish: false,
            decision_made: false,
            polish_passes: 0,
        });

        Ok(if is_en {
            format!(
                "Started remaster '{}' for {} ({} weeks, cost: {} EUR, +15 hype, +4% quality)!",
                remaster_title, platform, total_weeks, cost
            )
        } else {
            format!(
                "Remaster '{}' für {} gestartet ({} Wochen, Kosten: {} Euro, +15 Hype, +4% Qualität)!",
                remaster_title, platform, total_weeks, cost
            )
        })
    }

    /// Evaluate and unlock studio milestone achievements, persisting `"ach:<id>"` in `tutorials_completed`.
    pub fn check_and_unlock_achievements(&mut self) -> Vec<String> {
        let is_en = self.is_en();
        let curr_year = self.calendar_year();
        let has_score_at_least = |threshold: f64| -> bool {
            self.high_score >= threshold
                || self.game_history.iter().any(|g| {
                    g.review
                        .as_ref()
                        .map(|r| r.average() >= threshold)
                        .unwrap_or(false)
                })
        };

        let mut unlocked_msgs = Vec::new();
        for spec in ACHIEVEMENTS {
            let key = format!("ach:{}", spec.id);
            if self.tutorials_completed.iter().any(|t| t == &key) {
                continue;
            }
            let met = match spec.id {
                "first_release" => !self.game_history.is_empty(),
                "hit_8_plus" => has_score_at_least(8.0),
                "masterpiece_9_plus" => has_score_at_least(9.0),
                "millionaire" => self.money >= 1_000_000,
                "fans_10k" => self.fans >= 10_000,
                "custom_engine" => self.engines.len() >= 2,
                "hardware_pioneer" => {
                    !self.custom_soundcards.is_empty() || !self.custom_consoles.is_empty()
                }
                "label_mogul" => self.label_active,
                "soundcon_keynote" => {
                    self.last_soundcon_year >= 1995 || !self.soundcon_history.is_empty()
                }
                "rival_acquirer" => self.rivals.iter().any(|r| r.acquired_by_player),
                "golden_mic" => self.audio_awards >= 1,
                "timeline_veteran" => curr_year >= 2026,
                _ => false,
            };
            if met {
                self.tutorials_completed.push(key);
                self.money += spec.reward_money;
                self.fans += spec.reward_fans;
                self.hype = (self.hype + spec.reward_hype).clamp(0.0, 250.0);

                let (title, desc) = if is_en {
                    (spec.title_en, spec.desc_en)
                } else {
                    (spec.title_de, spec.desc_de)
                };
                let msg = if is_en {
                    format!(
                        "Achievement Unlocked: {}! (+{} EUR, +{} fans, +{:.0} hype)",
                        title, spec.reward_money, spec.reward_fans, spec.reward_hype
                    )
                } else {
                    format!(
                        "Erfolg freigeschaltet: {}! (+{} Euro, +{} Fans, +{:.0} Hype)",
                        title, spec.reward_money, spec.reward_fans, spec.reward_hype
                    )
                };
                self.emails.insert(
                    0,
                    Email {
                        sender: tr(self.lang(), "sender_awards"),
                        subject: if is_en {
                            format!("Studio Achievement: {}", title)
                        } else {
                            format!("Studio-Meilenstein: {}", title)
                        },
                        body: format!("{}\n{}", desc, msg),
                        week: self.week,
                        year: curr_year,
                        read: false,
                    },
                );
                if self.emails.len() > 40 {
                    self.emails.truncate(40);
                }
                unlocked_msgs.push(msg);
            }
        }
        unlocked_msgs
    }

    // --- Persistence (Save/Load JSON with full Rust roundtrip & Legacy Python migration) ---

    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert(
            "company_name".into(),
            JsonValue::Str(self.company_name.clone()),
        );
        m.insert("money".into(), JsonValue::Number(self.money as f64));
        m.insert("fans".into(), JsonValue::Number(self.fans as f64));
        m.insert("hype".into(), JsonValue::Number(self.hype));
        m.insert("week".into(), JsonValue::Number(self.week as f64));
        m.insert(
            "difficulty".into(),
            JsonValue::Number(self.difficulty as f64),
        );
        m.insert("time_speed".into(), JsonValue::Number(self.time_speed));
        m.insert(
            "developer_mode".into(),
            JsonValue::Bool(self.developer_mode),
        );
        m.insert(
            "office_level".into(),
            JsonValue::Number(self.office_level as f64),
        );
        m.insert(
            "office_upgrades".into(),
            JsonValue::Array(
                self.office_upgrades
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "bought_platforms".into(),
            JsonValue::Array(
                self.bought_platforms
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "unlocked_topics".into(),
            JsonValue::Array(
                self.unlocked_topics
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "unlocked_genres".into(),
            JsonValue::Array(
                self.unlocked_genres
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "unlocked_features".into(),
            JsonValue::Array(
                self.unlocked_features
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "unlocked_technologies".into(),
            JsonValue::Array(
                self.unlocked_technologies
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "engines".into(),
            JsonValue::Array(self.engines.iter().map(|e| e.to_json()).collect()),
        );
        if let Some(ref pr) = self.pending_research {
            m.insert("pending_research".into(), pr.to_json());
        }
        m.insert(
            "trend_topic".into(),
            JsonValue::Str(self.trend_topic.clone()),
        );
        m.insert(
            "trend_genre".into(),
            JsonValue::Str(self.trend_genre.clone()),
        );
        m.insert(
            "sales_multiplier".into(),
            JsonValue::Number(self.sales_multiplier),
        );
        m.insert(
            "marketing_efficiency".into(),
            JsonValue::Number(self.marketing_efficiency),
        );
        m.insert(
            "accessibility_reputation".into(),
            JsonValue::Number(self.accessibility_reputation as f64),
        );
        m.insert(
            "active_projects".into(),
            JsonValue::Array(self.active_projects.iter().map(|p| p.to_json()).collect()),
        );
        if let Some(ref lfg) = self.last_finished_game {
            m.insert("last_finished_game".into(), lfg.to_json());
        }
        m.insert(
            "game_history".into(),
            JsonValue::Array(self.game_history.iter().map(|g| g.to_json()).collect()),
        );
        m.insert("high_score".into(), JsonValue::Number(self.high_score));
        m.insert(
            "total_revenue".into(),
            JsonValue::Number(self.total_revenue as f64),
        );
        m.insert(
            "goty_awards".into(),
            JsonValue::Number(self.goty_awards as f64),
        );
        m.insert(
            "audio_awards".into(),
            JsonValue::Number(self.audio_awards as f64),
        );
        m.insert(
            "available_contracts".into(),
            JsonValue::Array(
                self.available_contracts
                    .iter()
                    .map(|c| c.to_json())
                    .collect(),
            ),
        );
        if let Some(ref ac) = self.active_contract {
            m.insert("active_contract".into(), ac.to_json());
        }
        m.insert(
            "next_contract_id".into(),
            JsonValue::Number(self.next_contract_id as f64),
        );
        m.insert(
            "employees".into(),
            JsonValue::Array(self.employees.iter().map(|e| e.to_json()).collect()),
        );
        m.insert(
            "hire_candidates".into(),
            JsonValue::Array(self.hire_candidates.iter().map(|e| e.to_json()).collect()),
        );
        m.insert(
            "next_employee_id".into(),
            JsonValue::Number(self.next_employee_id as f64),
        );
        m.insert(
            "last_soundcon_year".into(),
            JsonValue::Number(self.last_soundcon_year as f64),
        );
        m.insert(
            "soundcon_history".into(),
            JsonValue::Array(
                self.soundcon_history
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert("label_active".into(), JsonValue::Bool(self.label_active));
        m.insert("label_name".into(), JsonValue::Str(self.label_name.clone()));
        m.insert(
            "subscription_active".into(),
            JsonValue::Bool(self.subscription_active),
        );
        m.insert(
            "subscription_price".into(),
            JsonValue::Number(self.subscription_price),
        );
        m.insert(
            "subscription_subscribers".into(),
            JsonValue::Number(self.subscription_subscribers as f64),
        );
        m.insert(
            "custom_soundcards".into(),
            JsonValue::Array(self.custom_soundcards.iter().map(|c| c.to_json()).collect()),
        );
        m.insert(
            "custom_consoles".into(),
            JsonValue::Array(self.custom_consoles.iter().map(|c| c.to_json()).collect()),
        );
        m.insert("bank_loan".into(), JsonValue::Number(self.bank_loan as f64));
        m.insert(
            "merch_stock".into(),
            JsonValue::Number(self.merch_stock as f64),
        );
        m.insert("jingle_bonus".into(), JsonValue::Number(self.jingle_bonus));
        m.insert(
            "unanswered_fan_mails".into(),
            JsonValue::Number(self.unanswered_fan_mails as f64),
        );
        m.insert(
            "rivals".into(),
            JsonValue::Array(self.rivals.iter().map(|r| r.to_json()).collect()),
        );
        m.insert(
            "emails".into(),
            JsonValue::Array(self.emails.iter().map(|e| e.to_json()).collect()),
        );
        m.insert(
            "event_log".into(),
            JsonValue::Array(
                self.event_log
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "tutorials_completed".into(),
            JsonValue::Array(
                self.tutorials_completed
                    .iter()
                    .map(|s| JsonValue::Str(s.clone()))
                    .collect(),
            ),
        );
        m.insert("settings".into(), self.settings.to_json());
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let mut s = Self::new(v.get_usize("difficulty", 1), START_YEAR);
        s.company_name = v.get_str("company_name", "Klangpionier Tonstudio");
        s.money = v.get_i64("money", 100_000);
        s.fans = v.get_i64("fans", 100).max(0) as u64;
        s.hype = v.get_f64("hype", 10.0);
        s.week = v.get_u32("week", 1).max(1);
        s.time_speed = v.get_f64("time_speed", 1.0);
        s.developer_mode = v.get_bool("developer_mode", false);
        s.office_level = v.get_usize("office_level", 0).min(OFFICE_LEVELS.len() - 1);

        let str_list = |key: &str| -> Option<Vec<String>> {
            v.get(key).and_then(|a| a.as_array()).map(|arr| {
                arr.iter()
                    .filter_map(|x| {
                        if let Some(st) = x.as_str() {
                            Some(st.to_string())
                        } else {
                            x.get("name").and_then(|n| n.as_str()).map(|st| st.to_string())
                        }
                    })
                    .collect()
            })
        };

        if let Some(list) = str_list("office_upgrades") {
            s.office_upgrades = list;
        }
        if let Some(mut list) = str_list("bought_platforms") {
            let cal_year = START_YEAR + (s.week.saturating_sub(1)) / WEEKS_PER_YEAR;
            if cal_year < 1981 {
                for p in &mut list {
                    if p == "PC (MS-DOS)" {
                        *p = "Radio-Sendernetz (AM)".to_string();
                    }
                }
            }
            if !list.is_empty() {
                s.bought_platforms = list;
            }
        }
        if let Some(list) = str_list("unlocked_topics") {
            if !list.is_empty() {
                s.unlocked_topics = list;
            }
        }
        if let Some(list) = str_list("unlocked_genres") {
            if !list.is_empty() {
                s.unlocked_genres = list;
            }
        }
        if let Some(list) = str_list("unlocked_features") {
            s.unlocked_features = list;
        }
        if let Some(list) = str_list("unlocked_technologies") {
            s.unlocked_technologies = list;
        }
        if let Some(arr) = v.get("engines").and_then(|a| a.as_array()) {
            let parsed: Vec<Engine> = arr.iter().map(Engine::from_json).collect();
            if !parsed.is_empty() {
                s.engines = parsed;
            }
        }
        s.pending_research = v.get("pending_research").map(PendingResearch::from_json);

        if v.get("trend_topic").is_some() {
            s.trend_topic = v.get_str("trend_topic", "Radio-Drama");
            s.trend_genre = v.get_str("trend_genre", "Abenteuer");
        } else if let Some(ct) = v.get("current_trend") {
            s.trend_topic = ct.get_str("topic", "Radio-Drama");
            s.trend_genre = ct.get_str("genre", "Abenteuer");
        }

        s.sales_multiplier = v.get_f64("sales_multiplier", 1.0);
        s.marketing_efficiency = v.get_f64("marketing_efficiency", 1.0);
        s.accessibility_reputation = v.get_u32("accessibility_reputation", 25);

        if let Some(arr) = v.get("active_projects").and_then(|a| a.as_array()) {
            s.active_projects = arr.iter().map(ActiveProject::from_json).collect();
        }
        if let Some(lfg) = v.get("last_finished_game") {
            s.last_finished_game = Some(GameProject::from_json(lfg));
        }
        if let Some(arr) = v.get("game_history").and_then(|a| a.as_array()) {
            s.game_history = arr.iter().map(GameProject::from_json).collect();
        }
        s.high_score = v.get_f64("high_score", 0.0);
        s.total_revenue = v.get_i64("total_revenue", 0);
        s.goty_awards = v.get_u32("goty_awards", v.get_u32("my_goty_wins", 0));
        s.audio_awards = v.get_u32("audio_awards", 0);

        if let Some(arr) = v.get("available_contracts").and_then(|a| a.as_array()) {
            s.available_contracts = arr.iter().map(ContractProject::from_json).collect();
        }
        s.active_contract = v.get("active_contract").map(ContractProject::from_json);
        s.next_contract_id = v.get_u32("next_contract_id", s.next_contract_id);

        if let Some(arr) = v.get("employees").and_then(|a| a.as_array()) {
            let parsed: Vec<Employee> = arr.iter().map(Employee::from_json).collect();
            if !parsed.is_empty() {
                s.employees = parsed;
            }
        }
        if let Some(arr) = v.get("hire_candidates").and_then(|a| a.as_array()) {
            let parsed: Vec<Employee> = arr.iter().map(Employee::from_json).collect();
            if !parsed.is_empty() {
                s.hire_candidates = parsed;
            }
        }
        s.next_employee_id = v.get_u32("next_employee_id", s.next_employee_id);
        s.last_soundcon_year =
            v.get_u32("last_soundcon_year", v.get_u32("soundcon_last_year", 0));
        if let Some(arr) = v.get("soundcon_history").and_then(|a| a.as_array()) {
            s.soundcon_history = arr
                .iter()
                .filter_map(|item| {
                    if let Some(st) = item.as_str() {
                        Some(st.to_string())
                    } else if item.as_object().is_some() {
                        let yr = item.get_u32("year", 1995);
                        let tier = item.get_str("booth_tier", "Standard");
                        Some(format!("SoundCon {} ({})", yr, tier))
                    } else {
                        None
                    }
                })
                .collect();
        }

        if v.get("label_active").is_some() {
            s.label_active = v.get_bool("label_active", false);
            s.label_name = v.get_str("label_name", "");
        } else if let Some(lbl_obj) = v.get("soundtrack_label").and_then(|l| l.as_object()) {
            if !lbl_obj.is_empty() {
                s.label_active = true;
                s.label_name = v
                    .get("soundtrack_label")
                    .map(|l| {
                        let fallback = l.get_str("name", &format!("{} Records", s.company_name));
                        l.get_str("label_name", &fallback)
                    })
                    .unwrap_or_default();
            }
        }

        s.subscription_active = v.get_bool("subscription_active", false);
        s.subscription_price = v.get_f64("subscription_price", 9.99);
        s.subscription_subscribers = v.get_i64("subscription_subscribers", 0).max(0) as u64;

        if let Some(arr) = v
            .get("custom_soundcards")
            .or_else(|| v.get("sound_card_projects"))
            .and_then(|a| a.as_array())
        {
            s.custom_soundcards = arr.iter().map(CustomSoundCard::from_json).collect();
        }
        if let Some(arr) = v.get("custom_consoles").and_then(|a| a.as_array()) {
            s.custom_consoles = arr.iter().map(CustomConsole::from_json).collect();
        }

        if let Some(loan_val) = v.get("bank_loan") {
            if let Some(n) = loan_val.as_f64() {
                s.bank_loan = n.round() as i64;
            } else if loan_val.as_object().is_some() {
                s.bank_loan = loan_val.get_i64(
                    "amount_remaining",
                    loan_val.get_i64("amount_borrowed", loan_val.get_i64("borrowed", 0)),
                );
            }
        }
        s.merch_stock = v.get_i64("merch_stock", 0).max(0) as u64;
        s.jingle_bonus = v.get_f64("jingle_bonus", 0.0);
        s.unanswered_fan_mails = v.get_u32("unanswered_fan_mails", 1);

        if let Some(arr) = v.get("rivals").and_then(|a| a.as_array()) {
            let parsed: Vec<RivalStudio> = arr.iter().map(RivalStudio::from_json).collect();
            if !parsed.is_empty() {
                s.rivals = parsed;
            }
        }
        if let Some(arr) = v.get("emails").and_then(|a| a.as_array()) {
            s.emails = arr.iter().map(Email::from_json).collect();
        }
        if let Some(list) = str_list("event_log") {
            s.event_log = list;
        }
        if let Some(list) = str_list("tutorials_completed") {
            s.tutorials_completed = list;
        }
        if let Some(sv) = v.get("settings") {
            s.settings = Settings::from_json(sv);
        }
        s
    }

    pub fn save_to_file(&self, path: &Path) -> Result<(), String> {
        let json_str = self.to_json().to_string_pretty();
        fs::write(path, json_str).map_err(|e| format!("Save error: {}", e))
    }

    pub fn load_from_file(path: &Path) -> Result<Self, String> {
        let content = fs::read_to_string(path).map_err(|e| format!("Load error: {}", e))?;
        let val = parse_json(&content)?;
        Ok(Self::from_json(&val))
    }

    pub fn slot_filename(slot: usize) -> String {
        format!("save_slot_{}.json", slot.clamp(1, 99))
    }

    pub fn save_slot(&self, slot: usize) -> Result<String, String> {
        let fname = Self::slot_filename(slot);
        self.save_to_file(Path::new(&fname))?;
        Ok(if self.is_en() {
            format!("Game saved to Slot {} ({}).", slot, fname)
        } else {
            format!("Spielstand erfolgreich auf Platz {} ({}) gespeichert.", slot, fname)
        })
    }

    pub fn load_slot(&mut self, slot: usize) -> Result<String, String> {
        let fname = Self::slot_filename(slot);
        let loaded = Self::load_from_file(Path::new(&fname))?;
        let is_en = loaded.is_en();
        let cname = loaded.company_name.clone();
        *self = loaded;
        Ok(if is_en {
            format!("Loaded studio '{}' from Slot {}.", cname, slot)
        } else {
            format!("Studio '{}' von Platz {} geladen.", cname, slot)
        })
    }

    pub fn save_global_settings(&self) {
        let _ = fs::write("settings.json", self.settings.to_json().to_string_pretty());
    }

    pub fn load_global_settings(&mut self) {
        if let Ok(content) = fs::read_to_string("settings.json") {
            if let Ok(val) = parse_json(&content) {
                self.settings = Settings::from_json(&val);
            }
        }
    }
}
