//! Strongly-typed data models for Audio Studio Tycoon (Rust Edition)
//! with complete JSON serialization and deserialization.

use crate::data::SLIDER_NAMES;
use crate::json::JsonValue;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq)]
pub struct ReviewScore {
    pub scores: [u8; 4],
    pub comments: Vec<String>,
}

impl ReviewScore {
    pub fn new(scores: [u8; 4], comments: Vec<String>) -> Self {
        Self { scores, comments }
    }

    pub fn average(&self) -> f64 {
        let sum: u32 = self.scores.iter().map(|&s| s as u32).sum();
        sum as f64 / 4.0
    }

    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert(
            "scores".to_string(),
            JsonValue::Array(
                self.scores
                    .iter()
                    .map(|&s| JsonValue::Number(s as f64))
                    .collect(),
            ),
        );
        m.insert(
            "comments".to_string(),
            JsonValue::Array(
                self.comments
                    .iter()
                    .map(|c| JsonValue::Str(c.clone()))
                    .collect(),
            ),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Option<Self> {
        let arr = v.get("scores")?.as_array()?;
        if arr.len() < 4 {
            return None;
        }
        let mut scores = [5u8; 4];
        for i in 0..4 {
            scores[i] = arr[i].as_f64().unwrap_or(5.0).round().clamp(1.0, 10.0) as u8;
        }
        let comments = v
            .get("comments")
            .and_then(|c| c.as_array())
            .map(|list| {
                list.iter()
                    .filter_map(|item| item.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_default();
        Some(Self { scores, comments })
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct GameProject {
    pub name: String,
    pub topic: String,
    pub genre: String,
    pub sub_genre: String,
    pub platform: String,
    pub audience: String,
    pub size: String,
    pub marketing: String,
    pub engine_name: String,
    pub sliders: [u8; 6],
    pub review: Option<ReviewScore>,
    pub sales: u64,
    pub revenue: i64,
    pub dev_cost: i64,
    pub release_week: u32,
    pub release_year: u32,
    pub weeks_on_market: u32,
    pub is_active: bool,
    pub bugs: u32,
    pub patches_released: u32,
    pub dlc_count: u32,
    pub in_soundtrack_label: bool,
    pub in_subscription_vault: bool,
    pub sequel_number: u32,
}

impl GameProject {
    pub fn profit(&self) -> i64 {
        self.revenue - self.dev_cost
    }

    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert("topic".into(), JsonValue::Str(self.topic.clone()));
        m.insert("genre".into(), JsonValue::Str(self.genre.clone()));
        m.insert("sub_genre".into(), JsonValue::Str(self.sub_genre.clone()));
        m.insert("platform".into(), JsonValue::Str(self.platform.clone()));
        m.insert("audience".into(), JsonValue::Str(self.audience.clone()));
        m.insert("size".into(), JsonValue::Str(self.size.clone()));
        m.insert("marketing".into(), JsonValue::Str(self.marketing.clone()));
        m.insert("engine_name".into(), JsonValue::Str(self.engine_name.clone()));
        m.insert(
            "sliders".into(),
            JsonValue::Array(
                self.sliders
                    .iter()
                    .map(|&s| JsonValue::Number(s as f64))
                    .collect(),
            ),
        );
        if let Some(ref rev) = self.review {
            m.insert("review".into(), rev.to_json());
        }
        m.insert("sales".into(), JsonValue::Number(self.sales as f64));
        m.insert("revenue".into(), JsonValue::Number(self.revenue as f64));
        m.insert("dev_cost".into(), JsonValue::Number(self.dev_cost as f64));
        m.insert("release_week".into(), JsonValue::Number(self.release_week as f64));
        m.insert("release_year".into(), JsonValue::Number(self.release_year as f64));
        m.insert(
            "weeks_on_market".into(),
            JsonValue::Number(self.weeks_on_market as f64),
        );
        m.insert("is_active".into(), JsonValue::Bool(self.is_active));
        m.insert("bugs".into(), JsonValue::Number(self.bugs as f64));
        m.insert(
            "patches_released".into(),
            JsonValue::Number(self.patches_released as f64),
        );
        m.insert("dlc_count".into(), JsonValue::Number(self.dlc_count as f64));
        m.insert(
            "in_soundtrack_label".into(),
            JsonValue::Bool(self.in_soundtrack_label),
        );
        m.insert(
            "in_subscription_vault".into(),
            JsonValue::Bool(self.in_subscription_vault),
        );
        m.insert(
            "sequel_number".into(),
            JsonValue::Number(self.sequel_number as f64),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let mut sliders = [5u8; 6];
        if let Some(arr) = v.get("sliders").and_then(|s| s.as_array()) {
            for i in 0..arr.len().min(6) {
                sliders[i] = arr[i].as_f64().unwrap_or(5.0).round().clamp(0.0, 10.0) as u8;
            }
        }
        Self {
            name: v.get_str("name", "Unbenannt"),
            topic: v.get_str("topic", "Radio-Drama"),
            genre: v.get_str("genre", "Abenteuer"),
            sub_genre: v.get_str("sub_genre", "Standard"),
            platform: v.get_str("platform", "Radio-Sendernetz (AM)"),
            audience: v.get_str("audience", "Jeder"),
            size: v.get_str("size", "Mittel"),
            marketing: v.get_str("marketing", "Kein Marketing"),
            engine_name: v.get_str("engine_name", "Basis-Tonstudio V1"),
            sliders,
            review: v.get("review").and_then(ReviewScore::from_json),
            sales: v.get_i64("sales", 0).max(0) as u64,
            revenue: v.get_i64("revenue", 0),
            dev_cost: v.get_i64("dev_cost", 0),
            release_week: v.get_u32("release_week", 1),
            release_year: v.get_u32("release_year", 1930),
            weeks_on_market: v.get_u32("weeks_on_market", 0),
            is_active: v.get_bool("is_active", true),
            bugs: v.get_u32("bugs", 0),
            patches_released: v.get_u32("patches_released", 0),
            dlc_count: v.get_u32("dlc_count", 0),
            in_soundtrack_label: v.get_bool("in_soundtrack_label", false),
            in_subscription_vault: v.get_bool("in_subscription_vault", false),
            sequel_number: v.get_u32("sequel_number", 0),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ActiveProject {
    pub project: GameProject,
    pub progress_weeks: f64,
    pub total_weeks: u32,
    pub bugs: u32,
    pub crunch_active: bool,
    pub ready_to_finish: bool,
}

impl ActiveProject {
    pub fn percent(&self) -> u32 {
        if self.total_weeks == 0 {
            return 100;
        }
        ((self.progress_weeks / self.total_weeks as f64) * 100.0)
            .round()
            .clamp(0.0, 100.0) as u32
    }

    pub fn current_phase_name(&self, is_en: bool) -> &'static str {
        let p = self.percent();
        if is_en {
            match p {
                0..=19 => "1. Concept & Script",
                20..=39 => "2. Audio Engine & Setup",
                40..=59 => "3. Sound & World Design",
                60..=84 => "4. Studio Recording & Production",
                _ => "5. Mixing, Mastering & QA",
            }
        } else {
            match p {
                0..=19 => "1. Konzept & Drehbuch",
                20..=39 => "2. Audio-Engine & Technik",
                40..=59 => "3. Klang- & Welt-Design",
                60..=84 => "4. Studioaufnahme & Produktion",
                _ => "5. Abmischung, Mastering & QA",
            }
        }
    }

    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("project".into(), self.project.to_json());
        m.insert(
            "progress_weeks".into(),
            JsonValue::Number(self.progress_weeks),
        );
        m.insert(
            "total_weeks".into(),
            JsonValue::Number(self.total_weeks as f64),
        );
        m.insert("bugs".into(), JsonValue::Number(self.bugs as f64));
        m.insert("crunch_active".into(), JsonValue::Bool(self.crunch_active));
        m.insert(
            "ready_to_finish".into(),
            JsonValue::Bool(self.ready_to_finish),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let proj = v
            .get("project")
            .map(GameProject::from_json)
            .unwrap_or_else(|| GameProject::from_json(&JsonValue::Object(BTreeMap::new())));
        let progress_weeks = v
            .get("progress_weeks")
            .and_then(|x| x.as_f64())
            .unwrap_or_else(|| v.get_f64("progress", 0.0));
        let crunch_active = if v.get("crunch_active").is_some() {
            v.get_bool("crunch_active", false)
        } else {
            v.get_bool("crunch", false)
        };
        Self {
            project: proj,
            progress_weeks,
            total_weeks: v.get_u32("total_weeks", 6).max(1),
            bugs: v.get_u32("bugs", 0),
            crunch_active,
            ready_to_finish: v.get_bool("ready_to_finish", false),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ContractProject {
    pub id: u32,
    pub name_de: String,
    pub name_en: String,
    pub category: String, // "Sound", "Story", "Code", "Mastering"
    pub reward: i64,
    pub penalty: i64,
    pub required_points: f64,
    pub current_points: f64,
    pub weeks_left: u32,
}

impl ContractProject {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("id".into(), JsonValue::Number(self.id as f64));
        m.insert("name_de".into(), JsonValue::Str(self.name_de.clone()));
        m.insert("name_en".into(), JsonValue::Str(self.name_en.clone()));
        m.insert("category".into(), JsonValue::Str(self.category.clone()));
        m.insert("reward".into(), JsonValue::Number(self.reward as f64));
        m.insert("penalty".into(), JsonValue::Number(self.penalty as f64));
        m.insert(
            "required_points".into(),
            JsonValue::Number(self.required_points),
        );
        m.insert(
            "current_points".into(),
            JsonValue::Number(self.current_points),
        );
        m.insert(
            "weeks_left".into(),
            JsonValue::Number(self.weeks_left as f64),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            id: v.get_u32("id", 1),
            name_de: v.get_str("name_de", "Radio-Jingle Produktion"),
            name_en: v.get_str("name_en", "Radio Jingle Production"),
            category: v.get_str("category", "Sound"),
            reward: v.get_i64("reward", 8_000),
            penalty: v.get_i64("penalty", 2_000),
            required_points: v.get_f64("required_points", 20.0),
            current_points: v.get_f64("current_points", 0.0),
            weeks_left: v.get_u32("weeks_left", 4),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Employee {
    pub id: u32,
    pub name: String,
    pub role: String, // "Sound-Designer", "Programmierer", "Autor & Regie", "Grafik & Kulisse"
    pub trait_name: String,
    pub skill_sound: u32,
    pub skill_code: u32,
    pub skill_story: u32,
    pub skill_graphics: u32,
    pub salary: i64, // Monthly salary
    pub morale: u32, // 0..=100
    pub fatigue: u32, // 0..=100 (100 = burnout if not sent on vacation)
    pub is_ceo: bool,
    pub vacation_weeks_left: u32,
    pub training_weeks_left: u32,
    pub level: u32,
}

impl Employee {
    pub fn is_available(&self) -> bool {
        self.vacation_weeks_left == 0 && self.training_weeks_left == 0 && self.fatigue < 100
    }

    pub fn total_skill(&self) -> u32 {
        self.skill_sound + self.skill_code + self.skill_story + self.skill_graphics
    }

    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("id".into(), JsonValue::Number(self.id as f64));
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert("role".into(), JsonValue::Str(self.role.clone()));
        m.insert("trait_name".into(), JsonValue::Str(self.trait_name.clone()));
        m.insert("skill_sound".into(), JsonValue::Number(self.skill_sound as f64));
        m.insert("skill_code".into(), JsonValue::Number(self.skill_code as f64));
        m.insert("skill_story".into(), JsonValue::Number(self.skill_story as f64));
        m.insert(
            "skill_graphics".into(),
            JsonValue::Number(self.skill_graphics as f64),
        );
        m.insert("salary".into(), JsonValue::Number(self.salary as f64));
        m.insert("morale".into(), JsonValue::Number(self.morale as f64));
        m.insert("fatigue".into(), JsonValue::Number(self.fatigue as f64));
        m.insert("is_ceo".into(), JsonValue::Bool(self.is_ceo));
        m.insert(
            "vacation_weeks_left".into(),
            JsonValue::Number(self.vacation_weeks_left as f64),
        );
        m.insert(
            "training_weeks_left".into(),
            JsonValue::Number(self.training_weeks_left as f64),
        );
        m.insert("level".into(), JsonValue::Number(self.level as f64));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let skills_obj = v.get("skills");
        let s_sound = if v.get("skill_sound").is_some() {
            v.get_u32("skill_sound", 55)
        } else if let Some(sk) = skills_obj {
            sk.get_u32("Sound", 55)
        } else {
            55
        };
        let s_code = if v.get("skill_code").is_some() {
            v.get_u32("skill_code", 45)
        } else if let Some(sk) = skills_obj {
            sk.get_u32("Programmierung", sk.get_u32("Code", 45))
        } else {
            45
        };
        let s_story = if v.get("skill_story").is_some() {
            v.get_u32("skill_story", 50)
        } else if let Some(sk) = skills_obj {
            sk.get_u32("Story", 50)
        } else {
            50
        };
        let s_gfx = if v.get("skill_graphics").is_some() {
            v.get_u32("skill_graphics", 40)
        } else if let Some(sk) = skills_obj {
            sk.get_u32("Grafik", 40)
        } else {
            40
        };
        let trait_name = if v.get("trait_name").is_some() {
            v.get_str("trait_name", "Perfektionist")
        } else {
            v.get_str("trait", "Perfektionist")
        };
        Self {
            id: v.get_u32("id", 1),
            name: v.get_str("name", "Studio-Gründer (CEO)"),
            role: v.get_str("role", "Sound-Designer"),
            trait_name,
            skill_sound: s_sound,
            skill_code: s_code,
            skill_story: s_story,
            skill_graphics: s_gfx,
            salary: v.get_i64("salary", 0),
            morale: v.get_u32("morale", 100).min(100),
            fatigue: v.get_u32("fatigue", 0).min(100),
            is_ceo: v.get_bool("is_ceo", false),
            vacation_weeks_left: v.get_u32("vacation_weeks_left", v.get_u32("vacation_weeks", 0)),
            training_weeks_left: v.get_u32("training_weeks_left", 0),
            level: v.get_u32("level", 1).max(1),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Engine {
    pub name: String,
    pub features: Vec<String>,
    pub tech_level: u32,
    pub quality_bonus: f64, // 0.05 .. 0.60
    pub license_fee: i64,
    pub licensed_out: bool,
}

impl Engine {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert(
            "features".into(),
            JsonValue::Array(
                self.features
                    .iter()
                    .map(|f| JsonValue::Str(f.clone()))
                    .collect(),
            ),
        );
        m.insert(
            "tech_level".into(),
            JsonValue::Number(self.tech_level as f64),
        );
        m.insert(
            "quality_bonus".into(),
            JsonValue::Number(self.quality_bonus),
        );
        m.insert(
            "license_fee".into(),
            JsonValue::Number(self.license_fee as f64),
        );
        m.insert("licensed_out".into(), JsonValue::Bool(self.licensed_out));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let features: Vec<String> = v
            .get("features")
            .and_then(|a| a.as_array())
            .map(|list| {
                list.iter()
                    .filter_map(|i| {
                        if let Some(s) = i.as_str() {
                            Some(s.to_string())
                        } else {
                            i.get("name").and_then(|n| n.as_str()).map(|s| s.to_string())
                        }
                    })
                    .collect()
            })
            .unwrap_or_default();
        let default_bonus = (0.05 + features.len() as f64 * 0.03).min(0.60);
        Self {
            name: v.get_str("name", "Basis-Tonstudio V1"),
            tech_level: v.get_u32("tech_level", (features.len() as u32 / 2).max(1)),
            quality_bonus: v.get_f64("quality_bonus", default_bonus),
            license_fee: v.get_i64("license_fee", 10_000),
            licensed_out: v.get_bool("licensed_out", v.get_bool("is_licensed", false)),
            features,
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct CustomSoundCard {
    pub name: String,
    pub generation_year: u32,
    pub sound_bonus: f64,
    pub units_sold: u64,
    pub weekly_royalty: i64,
}

impl CustomSoundCard {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert(
            "generation_year".into(),
            JsonValue::Number(self.generation_year as f64),
        );
        m.insert("sound_bonus".into(), JsonValue::Number(self.sound_bonus));
        m.insert("units_sold".into(), JsonValue::Number(self.units_sold as f64));
        m.insert(
            "weekly_royalty".into(),
            JsonValue::Number(self.weekly_royalty as f64),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            name: v.get_str("name", "AudioBlaster Pro"),
            generation_year: v.get_u32("generation_year", 1980),
            sound_bonus: v.get_f64("sound_bonus", 0.10),
            units_sold: v.get_i64("units_sold", 0).max(0) as u64,
            weekly_royalty: v.get_i64("weekly_royalty", 1_500),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct CustomConsole {
    pub name: String,
    pub release_year: u32,
    pub market_share: f64,
    pub units_sold: u64,
    pub hype: f64,
}

impl CustomConsole {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert(
            "release_year".into(),
            JsonValue::Number(self.release_year as f64),
        );
        m.insert("market_share".into(), JsonValue::Number(self.market_share));
        m.insert("units_sold".into(), JsonValue::Number(self.units_sold as f64));
        m.insert("hype".into(), JsonValue::Number(self.hype));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            name: v.get_str("name", "SonicStation 1"),
            release_year: v.get_u32("release_year", 1985),
            market_share: v.get_f64("market_share", 0.15),
            units_sold: v.get_i64("units_sold", 10_000).max(0) as u64,
            hype: v.get_f64("hype", 30.0),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct RivalStudio {
    pub name: String,
    pub reputation: f64,
    pub valuation: i64,
    pub best_year_score: f64,
    pub best_year_game: String,
    pub acquired_by_player: bool,
}

impl RivalStudio {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("name".into(), JsonValue::Str(self.name.clone()));
        m.insert("reputation".into(), JsonValue::Number(self.reputation));
        m.insert("valuation".into(), JsonValue::Number(self.valuation as f64));
        m.insert(
            "best_year_score".into(),
            JsonValue::Number(self.best_year_score),
        );
        m.insert(
            "best_year_game".into(),
            JsonValue::Str(self.best_year_game.clone()),
        );
        m.insert(
            "acquired_by_player".into(),
            JsonValue::Bool(self.acquired_by_player),
        );
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            name: v.get_str("name", "Klangwerk Entertainment"),
            reputation: v.get_f64("reputation", 6.5),
            valuation: v.get_i64("valuation", 250_000),
            best_year_score: v.get_f64("best_year_score", 6.8),
            best_year_game: v.get_str("best_year_game", "Symphonie der Sterne"),
            acquired_by_player: v.get_bool("acquired_by_player", false),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Email {
    pub sender: String,
    pub subject: String,
    pub body: String,
    pub week: u32,
    pub year: u32,
    pub read: bool,
}

impl Email {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("sender".into(), JsonValue::Str(self.sender.clone()));
        m.insert("subject".into(), JsonValue::Str(self.subject.clone()));
        m.insert("body".into(), JsonValue::Str(self.body.clone()));
        m.insert("week".into(), JsonValue::Number(self.week as f64));
        m.insert("year".into(), JsonValue::Number(self.year as f64));
        m.insert("read".into(), JsonValue::Bool(self.read));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        let week = v.get_u32("week", v.get_u32("date_week", 1));
        let default_year = 1930 + (week.saturating_sub(1)) / 48;
        Self {
            sender: v.get_str("sender", "System"),
            subject: v.get_str("subject", "Info"),
            body: v.get_str("body", ""),
            week,
            year: v.get_u32("year", default_year),
            read: v.get_bool("read", v.get_bool("is_read", false)),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct GameDraft {
    pub name: String,
    pub topic: String,
    pub genre: String,
    pub sub_genre: String,
    pub platform: String,
    pub audience: String,
    pub size: String,
    pub marketing: String,
    pub engine_idx: usize,
    pub sliders: [u8; 6],
    pub sequel_of: Option<String>,
}

impl Default for GameDraft {
    fn default() -> Self {
        Self {
            name: String::new(),
            topic: "Radio-Drama".to_string(),
            genre: "Abenteuer".to_string(),
            sub_genre: "Klassisch".to_string(),
            platform: "Radio-Sendernetz (AM)".to_string(),
            audience: "Jeder".to_string(),
            size: "Klein".to_string(),
            marketing: "Kein Marketing".to_string(),
            engine_idx: 0,
            // Matches ideal profile of Abenteuer (sums to 30)
            sliders: [5, 4, 7, 8, 2, 4],
            sequel_of: None,
        }
    }
}

impl GameDraft {
    pub fn slider_budget(&self) -> u32 {
        match self.size.as_str() {
            "Klein" => 30,
            "Mittel" => 34,
            "Groß" => 38,
            "AAA" => 42,
            "MMO" => 45,
            _ => 30,
        }
    }

    pub fn used_points(&self) -> u32 {
        self.sliders.iter().map(|&s| s as u32).sum()
    }

    pub fn remaining_points(&self) -> i32 {
        self.slider_budget() as i32 - self.used_points() as i32
    }

    pub fn base_dev_cost(&self) -> i64 {
        let size_cost = match self.size.as_str() {
            "Klein" => 6_000,
            "Mittel" => 18_000,
            "Groß" => 55_000,
            "AAA" => 180_000,
            "MMO" => 350_000,
            _ => 12_000,
        };
        let mkt_cost = match self.marketing.as_str() {
            "Kleine Kampagne" => 5_000,
            "Mittlere Kampagne" => 20_000,
            "Große Kampagne" => 75_000,
            _ => 0,
        };
        size_cost + mkt_cost
    }

    pub fn dev_weeks(&self) -> u32 {
        match self.size.as_str() {
            "Klein" => 4,
            "Mittel" => 6,
            "Groß" => 10,
            "AAA" => 14,
            "MMO" => 18,
            _ => 6,
        }
    }

    pub fn slider_summary(&self) -> String {
        let mut parts = Vec::new();
        for (i, name) in SLIDER_NAMES.iter().enumerate() {
            parts.push(format!("{}: {}", name, self.sliders[i]));
        }
        parts.join(", ")
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Settings {
    pub language: String,
    pub music_enabled: bool,
    pub music_volume: u8,
    pub sfx_volume: u8,
    pub speech_volume: u8,
    pub tts_engine: String,
}

impl Default for Settings {
    fn default() -> Self {
        Self {
            language: "de".to_string(),
            music_enabled: true,
            music_volume: 50,
            sfx_volume: 100,
            speech_volume: 100,
            tts_engine: "auto".to_string(),
        }
    }
}

impl Settings {
    pub fn to_json(&self) -> JsonValue {
        let mut m = BTreeMap::new();
        m.insert("language".into(), JsonValue::Str(self.language.clone()));
        m.insert("music_enabled".into(), JsonValue::Bool(self.music_enabled));
        m.insert(
            "music_volume".into(),
            JsonValue::Number(self.music_volume as f64),
        );
        m.insert(
            "sfx_volume".into(),
            JsonValue::Number(self.sfx_volume as f64),
        );
        m.insert(
            "speech_volume".into(),
            JsonValue::Number(self.speech_volume as f64),
        );
        m.insert("tts_engine".into(), JsonValue::Str(self.tts_engine.clone()));
        JsonValue::Object(m)
    }

    pub fn from_json(v: &JsonValue) -> Self {
        Self {
            language: v.get_str("language", "de"),
            music_enabled: v.get_bool("music_enabled", true),
            music_volume: v.get_u32("music_volume", 50).min(100) as u8,
            sfx_volume: v.get_u32("sfx_volume", 100).min(100) as u8,
            speech_volume: v.get_u32("speech_volume", 100).min(100) as u8,
            tts_engine: v.get_str("tts_engine", "auto"),
        }
    }
}
