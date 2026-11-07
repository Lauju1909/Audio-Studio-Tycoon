//! Accessible, zero-dead-ends Menu System & Router for Audio Studio Tycoon (Rust Edition).
//! Implements:
//! - Acoustic boundary bump (`bump.wav`) at top/bottom of every linear menu.
//! - Instant screenreader speech interruption on navigation (`click.wav` + `say_interrupt`).
//! - Left/Right arrow slider adjustment with spoken value & budget feedback.
//! - Text input with spoken character echo, backspace feedback, and smart default on Enter.

use crate::audio::AudioManager;
use crate::data::*;
use crate::i18n::{tr, Lang};
use crate::state::GameState;
use std::path::Path;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MenuId {
    MainMenu,
    DifficultyMenu,
    CompanyNameInput,
    GameMenu,
    DevelopTopicMenu,
    DevelopGenreMenu,
    DevelopPlatformMenu,
    DevelopSizeAudienceMenu,
    DevelopSlidersMenu,
    DevelopNameInput,
    ActiveProjectsMenu,
    ReviewResultMenu,
    ContractsMenu,
    ResearchMenu,
    CustomEngineNameInput,
    HrMenu,
    OfficeMenu,
    MarketingCommunityMenu,
    SoundConMenu,
    LabelSubscriptionMenu,
    HardwareLabMenu,
    BankRivalsMenu,
    InboxMenu,
    ChartsGotyMenu,
    TutorialsMenu,
    SettingsMenu,
    SaveMenu,
    LoadMenu,
    CreditsMenu,
    DeveloperMenu,
}

pub const ALL_MENU_IDS: &[MenuId] = &[
    MenuId::MainMenu,
    MenuId::DifficultyMenu,
    MenuId::CompanyNameInput,
    MenuId::GameMenu,
    MenuId::DevelopTopicMenu,
    MenuId::DevelopGenreMenu,
    MenuId::DevelopPlatformMenu,
    MenuId::DevelopSizeAudienceMenu,
    MenuId::DevelopSlidersMenu,
    MenuId::DevelopNameInput,
    MenuId::ActiveProjectsMenu,
    MenuId::ReviewResultMenu,
    MenuId::ContractsMenu,
    MenuId::ResearchMenu,
    MenuId::CustomEngineNameInput,
    MenuId::HrMenu,
    MenuId::OfficeMenu,
    MenuId::MarketingCommunityMenu,
    MenuId::SoundConMenu,
    MenuId::LabelSubscriptionMenu,
    MenuId::HardwareLabMenu,
    MenuId::BankRivalsMenu,
    MenuId::InboxMenu,
    MenuId::ChartsGotyMenu,
    MenuId::TutorialsMenu,
    MenuId::SettingsMenu,
    MenuId::SaveMenu,
    MenuId::LoadMenu,
    MenuId::CreditsMenu,
    MenuId::DeveloperMenu,
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KeyInput {
    Up,
    Down,
    Left,
    Right,
    Enter,
    Back,
    Escape,
    Char(char),
    ToggleLang,
    SpeedPauseToggle,
    Speed1,
    Speed2,
    Speed3,
    NextWeek,
    FinanceSummary,
    StatusSummary,
    Help,
    ToggleDevMode,
    OpenDevMenu,
}

#[derive(Debug, Clone)]
pub struct MenuOption {
    pub text: String,
    pub speech_hint: String,
    pub action: MenuAction,
}

#[derive(Debug, Clone)]
pub enum MenuAction {
    Navigate(MenuId),
    Quit,
    StartNewGame { difficulty: usize, start_year: u32 },
    ConfirmCompanyName,
    SelectTopic(String),
    SelectGenre(String),
    SelectPlatform(String),
    CycleAudience,
    CycleGameSize,
    CycleMarketing,
    CycleEngine,
    ApplyIdealSliders,
    AdjustSlider { idx: usize },
    ConfirmGameStart,
    FinishProject(usize),
    ToggleCrunch(usize),
    ReleasePatch(usize),
    ReleaseDlc(usize),
    AcceptContract(usize),
    RefreshContracts,
    ResearchTopic(usize),
    ResearchGenre(usize),
    ResearchFeature(usize),
    ResearchTech(usize),
    ConfirmCustomEngine,
    HireCandidate(usize),
    TrainEmployee(usize),
    VacationEmployee(usize),
    FireEmployee(usize),
    UpgradeOffice,
    BuyStudioPerk { id: String, cost: i64, desc_de: String, desc_en: String },
    RunMarketingCampaign { cost: i64, hype_gain: f64, fan_gain: u64, label: String },
    ComposeJingle,
    AnswerFanMail,
    ProduceMerch,
    AttendSoundCon(usize),
    FoundLabel,
    AddGameToLabel(usize),
    OrganizeConcert,
    ToggleSubscription,
    AdjustSubscriptionPrice,
    AddGameToSubscription(usize),
    DevelopSoundcard,
    DevelopConsole,
    TakeLoan(i64),
    RepayLoan(i64),
    AcquireRival(usize),
    ReadEmail(usize),
    PlayTutorial(usize),
    ToggleLanguage,
    ToggleMusic,
    AdjustMusicVolume,
    AdjustSfxVolume,
    AdjustSpeechVolume,
    SaveSlot(usize),
    LoadSlot(usize),
    AdvanceWeek,
    DevAddMoney,
    DevAddFans,
    DevAdvanceYear,
    DevUnlockAll,
    NoOp,
}

pub struct MenuController {
    pub current_menu: MenuId,
    pub current_index: usize,
    pub title: String,
    pub options: Vec<MenuOption>,
    pub text_buffer: String,
    pub is_text_input: bool,
    pub settings_return_menu: MenuId,
    pub should_quit: bool,
}

impl MenuController {
    pub fn new(state: &GameState) -> Self {
        let mut ctrl = Self {
            current_menu: MenuId::MainMenu,
            current_index: 0,
            title: String::new(),
            options: Vec::new(),
            text_buffer: String::new(),
            is_text_input: false,
            settings_return_menu: MenuId::MainMenu,
            should_quit: false,
        };
        ctrl.rebuild(state);
        ctrl
    }

    pub fn switch_to(&mut self, menu_id: MenuId, state: &GameState, audio: &AudioManager) {
        if menu_id == MenuId::SettingsMenu && self.current_menu != MenuId::SettingsMenu {
            self.settings_return_menu = if self.current_menu == MenuId::MainMenu {
                MenuId::MainMenu
            } else {
                MenuId::GameMenu
            };
        }
        self.current_menu = menu_id;
        self.current_index = 0;
        self.text_buffer.clear();
        self.rebuild(state);
        self.announce_entry(audio);
    }

    pub fn announce_entry(&self, audio: &AudioManager) {
        let mut msg = self.title.clone();
        if let Some(first) = self.options.get(self.current_index) {
            msg.push_str(". ");
            msg.push_str(&first.text);
            if !first.speech_hint.is_empty() {
                msg.push_str(". ");
                msg.push_str(&first.speech_hint);
            }
        }
        audio.say_interrupt(&msg);
    }

    pub fn speak_current(&self, audio: &AudioManager, interrupt: bool) {
        if let Some(opt) = self.options.get(self.current_index) {
            let full = if opt.speech_hint.is_empty() {
                format!(
                    "{} ({}/{})",
                    opt.text,
                    self.current_index + 1,
                    self.options.len()
                )
            } else {
                format!(
                    "{}. {} ({}/{})",
                    opt.text,
                    opt.speech_hint,
                    self.current_index + 1,
                    self.options.len()
                )
            };
            audio.speak(&full, interrupt);
        }
    }

    pub fn rebuild(&mut self, state: &GameState) {
        let lang = state.lang();
        let is_en = state.is_en();
        self.is_text_input = matches!(
            self.current_menu,
            MenuId::CompanyNameInput | MenuId::DevelopNameInput | MenuId::CustomEngineNameInput
        );
        self.options.clear();

        match self.current_menu {
            MenuId::MainMenu => {
                self.title = tr(lang, "main_menu_title");
                self.options.push(MenuOption {
                    text: tr(lang, "menu_new_game"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DifficultyMenu),
                });
                if !state.company_name.is_empty() {
                    self.options.push(MenuOption {
                        text: format!("{} ({})", tr(lang, "menu_continue_game"), state.company_name),
                        speech_hint: String::new(),
                        action: MenuAction::Navigate(MenuId::GameMenu),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_load_game"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::LoadMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_tutorials"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::TutorialsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_settings"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::SettingsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_credits"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::CreditsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_quit"),
                    speech_hint: String::new(),
                    action: MenuAction::Quit,
                });
            }

            MenuId::DifficultyMenu => {
                self.title = tr(lang, "difficulty_title");
                self.options.push(MenuOption {
                    text: format!("1930 - {}", tr(lang, "difficulty_easy")),
                    speech_hint: if is_en {
                        "Start in the Golden Radio Era with generous funds.".to_string()
                    } else {
                        "Start in der Goldenen Radio-Ära mit großzügigem Polster.".to_string()
                    },
                    action: MenuAction::StartNewGame {
                        difficulty: 0,
                        start_year: 1930,
                    },
                });
                self.options.push(MenuOption {
                    text: format!("1930 - {}", tr(lang, "difficulty_normal")),
                    speech_hint: if is_en {
                        "Recommended historical progression from 1930.".to_string()
                    } else {
                        "Empfohlene historische Kampagne ab 1930.".to_string()
                    },
                    action: MenuAction::StartNewGame {
                        difficulty: 1,
                        start_year: 1930,
                    },
                });
                self.options.push(MenuOption {
                    text: format!("1930 - {}", tr(lang, "difficulty_hard")),
                    speech_hint: String::new(),
                    action: MenuAction::StartNewGame {
                        difficulty: 2,
                        start_year: 1930,
                    },
                });
                self.options.push(MenuOption {
                    text: format!("1930 - {}", tr(lang, "difficulty_legendary")),
                    speech_hint: String::new(),
                    action: MenuAction::StartNewGame {
                        difficulty: 3,
                        start_year: 1930,
                    },
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "1980 - Start in the 8-Bit & Synth Era (Normal)"
                    } else {
                        "1980 - Einstieg in der 8-Bit & Synthesizer-Ära (Normal)"
                    }
                    .to_string(),
                    speech_hint: String::new(),
                    action: MenuAction::StartNewGame {
                        difficulty: 1,
                        start_year: 1980,
                    },
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "1995 - Start in the Multimedia & SoundCon Era (Normal)"
                    } else {
                        "1995 - Einstieg in der Multimedia- & SoundCon-Ära (Normal)"
                    }
                    .to_string(),
                    speech_hint: String::new(),
                    action: MenuAction::StartNewGame {
                        difficulty: 1,
                        start_year: 1995,
                    },
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::MainMenu),
                });
            }

            MenuId::CompanyNameInput => {
                self.title = tr(lang, "company_name_title");
                let display = if self.text_buffer.is_empty() {
                    if is_en {
                        "[Default: Klangpionier Tonstudio] - Press Enter to confirm".to_string()
                    } else {
                        "[Vorschlag: Klangpionier Tonstudio] - Drücke Enter zum Bestätigen".to_string()
                    }
                } else {
                    format!("Name: {} (Enter)", self.text_buffer)
                };
                self.options.push(MenuOption {
                    text: display,
                    speech_hint: String::new(),
                    action: MenuAction::ConfirmCompanyName,
                });
            }

            MenuId::GameMenu => {
                self.title = format!(
                    "{} - {} ({})",
                    tr(lang, "game_menu_title"),
                    state.company_name,
                    state.calendar_text()
                );
                self.options.push(MenuOption {
                    text: tr(lang, "hub_develop_game"),
                    speech_hint: if is_en {
                        format!(
                            "Current trend: {} + {}",
                            state.trend_topic, state.trend_genre
                        )
                    } else {
                        format!(
                            "Aktueller Markttrend: {} mit {}",
                            state.trend_topic, state.trend_genre
                        )
                    },
                    action: MenuAction::Navigate(MenuId::DevelopTopicMenu),
                });
                self.options.push(MenuOption {
                    text: format!(
                        "{} ({})",
                        tr(lang, "hub_active_projects"),
                        state.active_projects.len()
                    ),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::ActiveProjectsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_contracts"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::ContractsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_research"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::ResearchMenu),
                });
                self.options.push(MenuOption {
                    text: format!(
                        "{} ({}/{})",
                        tr(lang, "hub_hr"),
                        state.employees.len(),
                        state.max_employees()
                    ),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::HrMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_office"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::OfficeMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_marketing"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::MarketingCommunityMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_soundcon"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::SoundConMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_label_sub"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::LabelSubscriptionMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_hardware"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::HardwareLabMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_bank_rivals"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::BankRivalsMenu),
                });
                self.options.push(MenuOption {
                    text: format!("{} ({})", tr(lang, "hub_inbox"), state.emails.len()),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::InboxMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_charts_goty"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::ChartsGotyMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "hub_next_week"),
                    speech_hint: String::new(),
                    action: MenuAction::AdvanceWeek,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_save_game"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::SaveMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_settings"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::SettingsMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_main_menu_return")
                        .replace("menu_main_menu_return", if is_en { "Return to Main Menu" } else { "Zurück zum Hauptmenü" }),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::MainMenu),
                });
            }

            MenuId::DevelopTopicMenu => {
                self.title = if is_en {
                    format!("Step 1: Choose Topic (Trend: {})", state.trend_topic)
                } else {
                    format!("Schritt 1: Thema wählen (Trend: {})", state.trend_topic)
                };
                for topic in &state.unlocked_topics {
                    let is_trend = *topic == state.trend_topic;
                    let badge = if is_trend {
                        if is_en {
                            " [HOT TREND!]"
                        } else {
                            " [IM TREND!]"
                        }
                    } else {
                        ""
                    };
                    self.options.push(MenuOption {
                        text: format!("{}{}", topic, badge),
                        speech_hint: String::new(),
                        action: MenuAction::SelectTopic(topic.clone()),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::DevelopGenreMenu => {
                self.title = if is_en {
                    format!(
                        "Step 2: Choose Genre for '{}' (Trend: {})",
                        state.current_draft.topic, state.trend_genre
                    )
                } else {
                    format!(
                        "Schritt 2: Genre für '{}' wählen (Trend: {})",
                        state.current_draft.topic, state.trend_genre
                    )
                };
                for genre in &state.unlocked_genres {
                    let compat = get_compatibility(&state.current_draft.topic, genre);
                    let compat_key = match compat {
                        3 => "compat_3",
                        2 => "compat_2",
                        1 => "compat_1",
                        _ => "compat_0",
                    };
                    let trend_str = if *genre == state.trend_genre {
                        if is_en {
                            " [TREND!]"
                        } else {
                            " [TREND!]"
                        }
                    } else {
                        ""
                    };
                    self.options.push(MenuOption {
                        text: format!("{}{} - {}", genre, trend_str, tr(lang, compat_key)),
                        speech_hint: String::new(),
                        action: MenuAction::SelectGenre(genre.clone()),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopTopicMenu),
                });
            }

            MenuId::DevelopPlatformMenu => {
                let year = state.calendar_year();
                self.title = if is_en {
                    format!("Step 3: Choose Platform ({})", year)
                } else {
                    format!("Schritt 3: Zielplattform wählen ({})", year)
                };
                for p in get_available_platforms(year) {
                    let owned = state.bought_platforms.iter().any(|bp| bp == p.name);
                    let status = if owned || p.license_fee == 0 {
                        if is_en {
                            "Licensed".to_string()
                        } else {
                            "Lizenziert".to_string()
                        }
                    } else if is_en {
                        format!("License: {} EUR", p.license_fee)
                    } else {
                        format!("Lizenz: {} Euro", p.license_fee)
                    };
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "{} [{}] - Market x{:.1}",
                                p.name, status, p.market_multi
                            )
                        } else {
                            format!(
                                "{} [{}] - Markt x{:.1}",
                                p.name, status, p.market_multi
                            )
                        },
                        speech_hint: p.audio_capabilities.to_string(),
                        action: MenuAction::SelectPlatform(p.name.to_string()),
                    });
                }
                for cc in &state.custom_consoles {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "{} [Custom Console] - Market Share {:.0}%",
                                cc.name,
                                cc.market_share * 100.0
                            )
                        } else {
                            format!(
                                "{} [Eigene Konsole] - Marktanteil {:.0}%",
                                cc.name,
                                cc.market_share * 100.0
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::SelectPlatform(cc.name.clone()),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopGenreMenu),
                });
            }

            MenuId::DevelopSizeAudienceMenu => {
                self.title = if is_en {
                    "Step 4: Production Scope, Engine & Marketing".to_string()
                } else {
                    "Schritt 4: Umfang, Zielgruppe, Engine & Marketing".to_string()
                };
                let eng_name = state
                    .engines
                    .get(state.current_draft.engine_idx)
                    .or_else(|| state.engines.first())
                    .map(|e| format!("{} (+{:.0}%)", e.name, e.quality_bonus * 100.0))
                    .unwrap_or_else(|| "Standard".to_string());

                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Project Size: {} (Press Enter to cycle)", state.current_draft.size)
                    } else {
                        format!("Projektgröße: {} (Enter zum Wechseln)", state.current_draft.size)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::CycleGameSize,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Target Audience: {} (Press Enter to cycle)", state.current_draft.audience)
                    } else {
                        format!("Zielgruppe: {} (Enter zum Wechseln)", state.current_draft.audience)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::CycleAudience,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Audio Engine: {} (Press Enter to cycle)", eng_name)
                    } else {
                        format!("Audio-Engine: {} (Enter zum Wechseln)", eng_name)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::CycleEngine,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Launch Marketing: {} (Press Enter to cycle)", state.current_draft.marketing)
                    } else {
                        format!("Marketing: {} (Enter zum Wechseln)", state.current_draft.marketing)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::CycleMarketing,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Continue to Studio Sliders (Total Cost: {} EUR, {} weeks)",
                            state.current_draft.base_dev_cost(),
                            state.current_draft.dev_weeks()
                        )
                    } else {
                        format!(
                            "Weiter zu den Studio-Slidern (Gesamtkosten: {} Euro, {} Wochen)",
                            state.current_draft.base_dev_cost(),
                            state.current_draft.dev_weeks()
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopSlidersMenu),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopPlatformMenu),
                });
            }

            MenuId::DevelopSlidersMenu => {
                let rem = state.current_draft.remaining_points();
                let ideal = get_ideal_sliders(&state.current_draft.genre);
                self.title = if is_en {
                    format!(
                        "Step 5: Studio Sliders for {} (Remaining Budget: {})",
                        state.current_draft.genre, rem
                    )
                } else {
                    format!(
                        "Schritt 5: Studio-Slider für {} (Freie Punkte: {})",
                        state.current_draft.genre, rem
                    )
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Auto-Set Ideal Profile for '{}' (Enter)",
                            state.current_draft.genre
                        )
                    } else {
                        format!(
                            "Ideale Verteilung für '{}' automatisch setzen (Enter)",
                            state.current_draft.genre
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ApplyIdealSliders,
                });
                let slider_labels_en = [
                    "Gameplay",
                    "Graphics",
                    "Sound",
                    "Story",
                    "AI",
                    "World",
                ];
                for (i, sname) in SLIDER_NAMES.iter().enumerate() {
                    let label = if is_en { slider_labels_en[i] } else { *sname };
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "{}: {} / 10 (Recommended for {}: {}) [Left/Right]",
                                label, state.current_draft.sliders[i], state.current_draft.genre, ideal[i]
                            )
                        } else {
                            format!(
                                "{}: {} / 10 (Empfehlung für {}: {}) [Links/Rechts]",
                                label, state.current_draft.sliders[i], state.current_draft.genre, ideal[i]
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::AdjustSlider { idx: i },
                    });
                }
                self.options.push(MenuOption {
                    text: if is_en {
                        "Continue to Title & Start Production".to_string()
                    } else {
                        "Weiter zur Titelvergabe & Produktionsstart".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopNameInput),
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::DevelopSizeAudienceMenu),
                });
            }

            MenuId::DevelopNameInput => {
                self.title = if is_en {
                    "Step 6: Enter Production Title (or press Enter for auto-title)".to_string()
                } else {
                    "Schritt 6: Projekttitel eingeben (oder direkt Enter für Vorschlag)".to_string()
                };
                let preview = if self.text_buffer.trim().is_empty() {
                    format!(
                        "{} {} #{}",
                        state.current_draft.topic,
                        state.current_draft.genre,
                        state.game_history.len() + state.active_projects.len() + 1
                    )
                } else {
                    self.text_buffer.clone()
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Start Production: '{}' (Cost: {} EUR) [Press Enter]",
                            preview,
                            state.current_draft.base_dev_cost()
                        )
                    } else {
                        format!(
                            "Produktion starten: '{}' (Kosten: {} Euro) [Enter drücken]",
                            preview,
                            state.current_draft.base_dev_cost()
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ConfirmGameStart,
                });
            }

            MenuId::ActiveProjectsMenu => {
                self.title = tr(lang, "hub_active_projects");
                if state.active_projects.is_empty() {
                    self.options.push(MenuOption {
                        text: if is_en {
                            "No active productions in development.".to_string()
                        } else {
                            "Aktuell keine Produktion in Entwicklung.".to_string()
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                } else {
                    for (i, ap) in state.active_projects.iter().enumerate() {
                        if ap.ready_to_finish {
                            self.options.push(MenuOption {
                                text: if is_en {
                                    format!(
                                        "RELEASE NOW: '{}' (100% complete, {} bugs) [Press Enter]",
                                        ap.project.name, ap.bugs
                                    )
                                } else {
                                    format!(
                                        "JETZT VERÖFFENTLICHEN: '{}' (100% fertig, {} Bugs) [Enter]",
                                        ap.project.name, ap.bugs
                                    )
                                },
                                speech_hint: String::new(),
                                action: MenuAction::FinishProject(i),
                            });
                        } else {
                            let crunch_label = if ap.crunch_active {
                                if is_en { "ON" } else { "AN" }
                            } else if is_en {
                                "OFF"
                            } else {
                                "AUS"
                            };
                            self.options.push(MenuOption {
                                text: if is_en {
                                    format!(
                                        "'{}' - {}% ({}) | Bugs: {} | Crunch Mode: {}",
                                        ap.project.name,
                                        ap.percent(),
                                        ap.current_phase_name(is_en),
                                        ap.bugs,
                                        crunch_label
                                    )
                                } else {
                                    format!(
                                        "'{}' - {}% ({}) | Bugs: {} | Überstunden/Crunch: {}",
                                        ap.project.name,
                                        ap.percent(),
                                        ap.current_phase_name(is_en),
                                        ap.bugs,
                                        crunch_label
                                    )
                                },
                                speech_hint: if is_en {
                                    "Press Enter to toggle Crunch mode".to_string()
                                } else {
                                    "Enter schaltet Überstunden-Modus (Crunch) um".to_string()
                                },
                                action: MenuAction::ToggleCrunch(i),
                            });
                        }
                    }
                }
                self.options.push(MenuOption {
                    text: tr(lang, "hub_next_week"),
                    speech_hint: String::new(),
                    action: MenuAction::AdvanceWeek,
                });
                // Post-release support for recent games on the market
                for (idx, g) in state.game_history.iter().enumerate().rev().take(4) {
                    let avg = g.review.as_ref().map(|r| r.average()).unwrap_or(0.0);
                    if g.bugs > 0 {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "Release Patch for '{}' (Score: {:.1}/10, Sales: {}, Bugs: {}) - 2,000 EUR",
                                    g.name, avg, g.sales, g.bugs
                                )
                            } else {
                                format!(
                                    "Patch veröffentlichen für '{}' (Wertung: {:.1}/10, Verkäufe: {}, Bugs: {}) - 2.000 Euro",
                                    g.name, avg, g.sales, g.bugs
                                )
                            },
                            speech_hint: String::new(),
                            action: MenuAction::ReleasePatch(idx),
                        });
                    }
                    if g.dlc_count < 2 {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "Produce Addon/DLC for '{}' (DLCs: {}/2) - 6,000 EUR",
                                    g.name, g.dlc_count
                                )
                            } else {
                                format!(
                                    "Addon/DLC produzieren für '{}' (DLCs: {}/2) - 6.000 Euro",
                                    g.name, g.dlc_count
                                )
                            },
                            speech_hint: String::new(),
                            action: MenuAction::ReleaseDlc(idx),
                        });
                    }
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::ReviewResultMenu => {
                if let Some(ref game) = state.last_finished_game {
                    let rev = game.review.as_ref();
                    let avg = rev.map(|r| r.average()).unwrap_or(5.0);
                    self.title = if is_en {
                        format!("Press Reviews for '{}' - Average: {:.1}/10", game.name, avg)
                    } else {
                        format!(
                            "Presse-Bewertungen für '{}' - Schnitt: {:.1} von 10",
                            game.name, avg
                        )
                    };
                    if let Some(r) = rev {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "Scores: [{} / 10], [{} / 10], [{} / 10], [{} / 10] -> {:.1} / 10",
                                    r.scores[0], r.scores[1], r.scores[2], r.scores[3], avg
                                )
                            } else {
                                format!(
                                    "Wertungen: [{} / 10], [{} / 10], [{} / 10], [{} / 10] -> {:.1} / 10",
                                    r.scores[0], r.scores[1], r.scores[2], r.scores[3], avg
                                )
                            },
                            speech_hint: String::new(),
                            action: MenuAction::NoOp,
                        });
                        for c in &r.comments {
                            self.options.push(MenuOption {
                                text: c.clone(),
                                speech_hint: String::new(),
                                action: MenuAction::NoOp,
                            });
                        }
                    }
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "Launch Sales: {} copies | Launch Revenue: {} EUR",
                                game.sales, game.revenue
                            )
                        } else {
                            format!(
                                "Startverkäufe: {} Exemplare | Startumsatz: {} Euro",
                                game.sales, game.revenue
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                } else {
                    self.title = "Review".to_string();
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::ContractsMenu => {
                self.title = tr(lang, "hub_contracts");
                if let Some(ref ac) = state.active_contract {
                    let pct = ((ac.current_points / ac.required_points.max(1.0)) * 100.0)
                        .round()
                        .clamp(0.0, 100.0) as u32;
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "ACTIVE CONTRACT: '{}' - {}% complete ({} weeks left, reward: {} EUR)",
                                ac.name_en, pct, ac.weeks_left, ac.reward
                            )
                        } else {
                            format!(
                                "AKTIVER AUFTRAG: '{}' - {}% fertig (noch {} Wochen, Vergütung: {} Euro)",
                                ac.name_de, pct, ac.weeks_left, ac.reward
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::AdvanceWeek,
                    });
                }
                for (i, c) in state.available_contracts.iter().enumerate() {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "{} [{}] - Reward: {} EUR, Deadline: {} weeks (Penalty: {} EUR)",
                                c.name_en, c.category, c.reward, c.weeks_left, c.penalty
                            )
                        } else {
                            format!(
                                "{} [{}] - Vergütung: {} Euro, Frist: {} Wochen (Strafe: {} Euro)",
                                c.name_de, c.category, c.reward, c.weeks_left, c.penalty
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::AcceptContract(i),
                    });
                }
                self.options.push(MenuOption {
                    text: if is_en {
                        "Request New Contract Offers".to_string()
                    } else {
                        "Neue Auftragsangebote einholen".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::RefreshContracts,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::ResearchMenu => {
                let year = state.calendar_year();
                self.title = format!("{} ({})", tr(lang, "hub_research"), year);
                if let Some(ref pr) = state.pending_research {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "ACTIVE RESEARCH: '{}' ({} weeks remaining)",
                                pr.name, pr.weeks_left
                            )
                        } else {
                            format!(
                                "LAUFENDE FORSCHUNG: '{}' (noch {} Wochen)",
                                pr.name, pr.weeks_left
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::AdvanceWeek,
                    });
                }
                let eng_cost = 15_000 + (state.unlocked_features.len() as i64 * 5_000);
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Build New Custom Audio Engine ({} features, {} EUR)",
                            state.unlocked_features.len(),
                            eng_cost
                        )
                    } else {
                        format!(
                            "Neue eigene Audio-Engine bauen ({} Features, {} Euro)",
                            state.unlocked_features.len(),
                            eng_cost
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::CustomEngineNameInput),
                });

                for (i, g) in RESEARCHABLE_GENRES.iter().enumerate() {
                    if !state.unlocked_genres.iter().any(|ug| ug == g.name) && year >= g.unlock_year
                    {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "[Genre] {} ({} EUR, {} weeks)",
                                    g.name, g.cost, g.weeks
                                )
                            } else {
                                format!(
                                    "[Genre] {} ({} EUR, {} Wochen)",
                                    g.name, g.cost, g.weeks
                                )
                            },
                            speech_hint: if is_en {
                                g.desc_en.to_string()
                            } else {
                                g.desc_de.to_string()
                            },
                            action: MenuAction::ResearchGenre(i),
                        });
                    }
                }
                for (i, t) in RESEARCHABLE_TOPICS.iter().enumerate() {
                    if !state.unlocked_topics.iter().any(|ut| ut == t.name) && year >= t.unlock_year
                    {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "[Topic] {} ({} EUR, {} weeks)",
                                    t.name, t.cost, t.weeks
                                )
                            } else {
                                format!(
                                    "[Thema] {} ({} EUR, {} Wochen)",
                                    t.name, t.cost, t.weeks
                                )
                            },
                            speech_hint: if is_en {
                                t.desc_en.to_string()
                            } else {
                                t.desc_de.to_string()
                            },
                            action: MenuAction::ResearchTopic(i),
                        });
                    }
                }
                for (i, f) in ENGINE_FEATURES.iter().enumerate() {
                    if !state.unlocked_features.iter().any(|uf| uf == f.name)
                        && year >= f.unlock_year
                    {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "[Engine Feature] {} ({}, {} EUR)",
                                    f.name, f.category, f.cost
                                )
                            } else {
                                format!(
                                    "[Engine-Feature] {} ({}, {} EUR)",
                                    f.name, f.category, f.cost
                                )
                            },
                            speech_hint: String::new(),
                            action: MenuAction::ResearchFeature(i),
                        });
                    }
                }
                for (i, tech) in RESEARCHABLE_TECHNOLOGIES.iter().enumerate() {
                    if !state
                        .unlocked_technologies
                        .iter()
                        .any(|ut| ut == tech.name)
                        && year >= tech.unlock_year
                    {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "[Studio Tech] {} ({} EUR, {} weeks)",
                                    tech.name, tech.cost, tech.weeks
                                )
                            } else {
                                format!(
                                    "[Studio-Technologie] {} ({} EUR, {} Wochen)",
                                    tech.name, tech.cost, tech.weeks
                                )
                            },
                            speech_hint: if is_en {
                                tech.desc_en.to_string()
                            } else {
                                tech.desc_de.to_string()
                            },
                            action: MenuAction::ResearchTech(i),
                        });
                    }
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::CustomEngineNameInput => {
                self.title = if is_en {
                    "Enter Custom Audio Engine Name (or press Enter for default)".to_string()
                } else {
                    "Name der eigenen Audio-Engine eingeben (oder Enter für Vorschlag)".to_string()
                };
                let preview = if self.text_buffer.trim().is_empty() {
                    format!("AudioEngine V{}", state.engines.len() + 1)
                } else {
                    self.text_buffer.clone()
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Build Engine: '{}' (Enter)", preview)
                    } else {
                        format!("Engine erstellen: '{}' (Enter)", preview)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ConfirmCustomEngine,
                });
            }

            MenuId::HrMenu => {
                self.title = format!(
                    "{} ({}/{})",
                    tr(lang, "hub_hr"),
                    state.employees.len(),
                    state.max_employees()
                );
                for (i, emp) in state.employees.iter().enumerate() {
                    let status = if emp.vacation_weeks_left > 0 {
                        if is_en {
                            format!("Vacation ({} wk)", emp.vacation_weeks_left)
                        } else {
                            format!("Urlaub ({} Wo.)", emp.vacation_weeks_left)
                        }
                    } else if emp.training_weeks_left > 0 {
                        if is_en {
                            format!("Training ({} wk)", emp.training_weeks_left)
                        } else {
                            format!("Schulung ({} Wo.)", emp.training_weeks_left)
                        }
                    } else if is_en {
                        "Ready".to_string()
                    } else {
                        "Einsatzbereit".to_string()
                    };
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "[Team] {} ({}, Lv.{}) | Sound:{} Code:{} Story:{} | Fatigue:{}% | {} -> Enter: Training (5,000 EUR)",
                                emp.name, emp.role, emp.level, emp.skill_sound, emp.skill_code, emp.skill_story, emp.fatigue, status
                            )
                        } else {
                            format!(
                                "[Team] {} ({}, St.{}) | Sound:{} Code:{} Story:{} | Erschöpfung:{}% | {} -> Enter: Fortbildung (5.000 EUR)",
                                emp.name, emp.role, emp.level, emp.skill_sound, emp.skill_code, emp.skill_story, emp.fatigue, status
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::TrainEmployee(i),
                    });
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "Send {} on 3-Week Vacation (Fatigue: {}%, Cost: 1,000 EUR)",
                                emp.name, emp.fatigue
                            )
                        } else {
                            format!(
                                "{} in 3-wöchigen Erholungsurlaub schicken (Erschöpfung: {}%, 1.000 Euro)",
                                emp.name, emp.fatigue
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::VacationEmployee(i),
                    });
                    if !emp.is_ceo {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!("Dismiss {} (Salary: {} EUR/month)", emp.name, emp.salary)
                            } else {
                                format!("{} entlassen (Gehalt: {} Euro/Monat)", emp.name, emp.salary)
                            },
                            speech_hint: String::new(),
                            action: MenuAction::FireEmployee(i),
                        });
                    }
                }
                for (i, cand) in state.hire_candidates.iter().enumerate() {
                    let fee = cand.salary * 2;
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "[Hire] {} ({}, {}) | Sound:{} Code:{} Story:{} | Salary: {} EUR/m (Bonus: {} EUR)",
                                cand.name, cand.role, cand.trait_name, cand.skill_sound, cand.skill_code, cand.skill_story, cand.salary, fee
                            )
                        } else {
                            format!(
                                "[Bewerber einstellen] {} ({}, {}) | Sound:{} Code:{} Story:{} | Gehalt: {} EUR/M (Handgeld: {} EUR)",
                                cand.name, cand.role, cand.trait_name, cand.skill_sound, cand.skill_code, cand.skill_story, cand.salary, fee
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::HireCandidate(i),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::OfficeMenu => {
                let curr = &OFFICE_LEVELS[state.office_level];
                self.title = format!(
                    "{} - {}",
                    tr(lang, "hub_office"),
                    if is_en { curr.name_en } else { curr.name_de }
                );
                if let Some(next) = OFFICE_LEVELS.get(state.office_level + 1) {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "Upgrade Studio to '{}' ({} EUR, max {} employees, rent {} EUR/m)",
                                next.name_en, next.upgrade_cost, next.max_employees, next.monthly_rent
                            )
                        } else {
                            format!(
                                "Tonstudio ausbauen zu '{}' ({} Euro, bis zu {} Mitarbeiter, Miete {} Euro/M)",
                                next.name_de, next.upgrade_cost, next.max_employees, next.monthly_rent
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::UpgradeOffice,
                    });
                } else {
                    self.options.push(MenuOption {
                        text: if is_en {
                            "Maximum Studio Campus Level Reached!".to_string()
                        } else {
                            "Maximale Ausbaustufe (Audio-Campus) erreicht!".to_string()
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                }
                let perks = [
                    (
                        "mixing_desk",
                        "Neve Analog-Mischpult (+Sound & Prestige)",
                        "Neve Analog Mixing Console (+Sound & Prestige)",
                        15_000,
                    ),
                    (
                        "foley_stage",
                        "Akustische Geräuschemacher-Bühne (Foley Stage)",
                        "Acoustic Foley Stage",
                        20_000,
                    ),
                    (
                        "accessibility_lab",
                        "Barrierefreiheits- & Screenreader-Testlabor (+Reputation)",
                        "Accessibility & Screenreader QA Lab (+Reputation)",
                        18_000,
                    ),
                    (
                        "espresso_lounge",
                        "Studio-Kaffeebar & Ruheraum (+Moral, -Erschöpfung)",
                        "Studio Espresso Bar & Lounge (+Morale, -Fatigue)",
                        8_000,
                    ),
                ];
                for (id, de, en, cost) in perks {
                    let owned = state.office_upgrades.iter().any(|u| u == id);
                    let status = if owned {
                        if is_en { " [Installed]" } else { " [Installiert]" }
                    } else {
                        ""
                    };
                    self.options.push(MenuOption {
                        text: format!(
                            "{}{} ({} EUR)",
                            if is_en { en } else { de },
                            status,
                            cost
                        ),
                        speech_hint: String::new(),
                        action: MenuAction::BuyStudioPerk {
                            id: id.to_string(),
                            cost,
                            desc_de: de.to_string(),
                            desc_en: en.to_string(),
                        },
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::MarketingCommunityMenu => {
                self.title = format!(
                    "{} (Hype: {:.0}, Fans: {})",
                    tr(lang, "hub_marketing"),
                    state.hype,
                    state.fans
                );
                self.options.push(MenuOption {
                    text: if is_en {
                        "Radio & Press Spot (5,000 EUR -> +20 Hype, +250 Fans)".to_string()
                    } else {
                        "Radio- & Presse-Kampagne (5.000 Euro -> +20 Hype, +250 Fans)".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::RunMarketingCampaign {
                        cost: 5_000,
                        hype_gain: 20.0,
                        fan_gain: 250,
                        label: if is_en {
                            "Radio & Press Spot".to_string()
                        } else {
                            "Radio & Presse".to_string()
                        },
                    },
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "National Broadcast Special (25,000 EUR -> +65 Hype, +1,500 Fans)".to_string()
                    } else {
                        "Große Rundfunk-Sondersendung (25.000 Euro -> +65 Hype, +1.500 Fans)".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::RunMarketingCampaign {
                        cost: 25_000,
                        hype_gain: 65.0,
                        fan_gain: 1_500,
                        label: if is_en {
                            "Broadcast Special".to_string()
                        } else {
                            "Rundfunk-Special".to_string()
                        },
                    },
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Compose Studio Marketing Jingle (3,000 EUR -> Permanent Jingle Bonus +{:.0})",
                            state.jingle_bonus + 5.0
                        )
                    } else {
                        format!(
                            "Studio-Jingle komponieren (3.000 Euro -> Dauerhafter Jingle-Bonus +{:.0})",
                            state.jingle_bonus + 5.0
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ComposeJingle,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Answer Community Fan Mail (+200 Fans, +5 Hype | Unanswered: {})",
                            state.unanswered_fan_mails
                        )
                    } else {
                        format!(
                            "Fanpost der Hörer-Community beantworten (+200 Fans, +5 Hype | Offen: {})",
                            state.unanswered_fan_mails
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AnswerFanMail,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Produce Fan Merchandise Batch (5,000 EUR for 500 items, Stock: {})",
                            state.merch_stock
                        )
                    } else {
                        format!(
                            "Fan-Merchandise produzieren (5.000 Euro für 500 Stück, Lager: {})",
                            state.merch_stock
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ProduceMerch,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::SoundConMenu => {
                let year = state.calendar_year();
                self.title = format!("{} ({})", tr(lang, "hub_soundcon"), year);
                self.options.push(MenuOption {
                    text: if is_en {
                        "Small Listening Booth (15,000 EUR -> +30 Hype, +800 Fans) [Requires 1995+]".to_string()
                    } else {
                        "Kleiner Hörstand (15.000 Euro -> +30 Hype, +800 Fans) [Ab 1995]".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AttendSoundCon(0),
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Large Acoustic Stage (50,000 EUR -> +75 Hype, +3,000 Fans) [Requires 1995+]".to_string()
                    } else {
                        "Große Klangbühne (50.000 Euro -> +75 Hype, +3.000 Fans) [Ab 1995]".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AttendSoundCon(1),
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Giant 3D Sound Dome (150,000 EUR -> +150 Hype, +10,000 Fans) [Requires 1995+]".to_string()
                    } else {
                        "Gigantischer 3D-Sound-Dome (150.000 Euro -> +150 Hype, +10.000 Fans) [Ab 1995]".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AttendSoundCon(2),
                });
                for h in state.soundcon_history.iter().rev().take(5) {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!("[History] {}", h)
                        } else {
                            format!("[Historie] {}", h)
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::LabelSubscriptionMenu => {
                self.title = tr(lang, "hub_label_sub");
                if !state.label_active {
                    self.options.push(MenuOption {
                        text: if is_en {
                            "Found Own Soundtrack Label (25,000 EUR, available from 1985)".to_string()
                        } else {
                            "Eigenes Soundtrack-Label gründen (25.000 Euro, ab 1985)".to_string()
                        },
                        speech_hint: String::new(),
                        action: MenuAction::FoundLabel,
                    });
                } else {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "Organize Live Orchestra Soundtrack Concert for '{}' (20,000 EUR -> Revenue & Fans)",
                                state.label_name
                            )
                        } else {
                            format!(
                                "Live-Orchester-Konzert für Label '{}' veranstalten (20.000 Euro -> Einnahmen & Fans)",
                                state.label_name
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::OrganizeConcert,
                    });
                    for (idx, g) in state.game_history.iter().enumerate() {
                        if !g.in_soundtrack_label {
                            self.options.push(MenuOption {
                                text: if is_en {
                                    format!("Add '{}' Soundtrack to Label", g.name)
                                } else {
                                    format!("Soundtrack von '{}' ins Label aufnehmen", g.name)
                                },
                                speech_hint: String::new(),
                                action: MenuAction::AddGameToLabel(idx),
                            });
                        }
                    }
                }

                let sub_status = if state.subscription_active {
                    if is_en { "ACTIVE" } else { "AKTIV" }
                } else if is_en {
                    "INACTIVE"
                } else {
                    "INAKTIV"
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "AudioPass Subscription Service [{}] (Subscribers: {}, Price: {:.2} EUR) [From 1995]",
                            sub_status, state.subscription_subscribers, state.subscription_price
                        )
                    } else {
                        format!(
                            "AudioPass Abo-Dienst [{}] (Abonnenten: {}, Preis: {:.2} Euro) [Ab 1995]",
                            sub_status, state.subscription_subscribers, state.subscription_price
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ToggleSubscription,
                });
                if state.subscription_active {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "Adjust Monthly Subscription Price: {:.2} EUR [Left/Right]",
                                state.subscription_price
                            )
                        } else {
                            format!(
                                "Abo-Monatspreis anpassen: {:.2} Euro [Links/Rechts]",
                                state.subscription_price
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::AdjustSubscriptionPrice,
                    });
                    for (idx, g) in state.game_history.iter().enumerate() {
                        if !g.in_subscription_vault {
                            self.options.push(MenuOption {
                                text: if is_en {
                                    format!("Add '{}' to AudioPass Vault", g.name)
                                } else {
                                    format!("'{}' in den AudioPass aufnehmen", g.name)
                                },
                                speech_hint: String::new(),
                                action: MenuAction::AddGameToSubscription(idx),
                            });
                        }
                    }
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::HardwareLabMenu => {
                self.title = tr(lang, "hub_hardware");
                self.options.push(MenuOption {
                    text: if is_en {
                        "Develop Custom Soundcard (60,000 EUR, passive weekly royalties) [From 1975]".to_string()
                    } else {
                        "Eigene Soundkarte entwickeln (60.000 Euro, laufende Lizenzeinnahmen) [Ab 1975]".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::DevelopSoundcard,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Develop Custom Audio Console (200,000 EUR, own platform & hardware sales) [From 1975]".to_string()
                    } else {
                        "Eigene Audio-Konsole entwickeln (200.000 Euro, eigene Plattform & Hardware-Verkäufe) [Ab 1975]".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::DevelopConsole,
                });
                for sc in &state.custom_soundcards {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "[Soundcard] {} ({}) - Sold: {}, Royalty: +{} EUR/week",
                                sc.name, sc.generation_year, sc.units_sold, sc.weekly_royalty
                            )
                        } else {
                            format!(
                                "[Soundkarte] {} ({}) - Verkauft: {}, Lizenz: +{} EUR/Woche",
                                sc.name, sc.generation_year, sc.units_sold, sc.weekly_royalty
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                }
                for cc in &state.custom_consoles {
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "[Console] {} ({}) - Sold: {}, Market Share: {:.0}%",
                                cc.name,
                                cc.release_year,
                                cc.units_sold,
                                cc.market_share * 100.0
                            )
                        } else {
                            format!(
                                "[Konsole] {} ({}) - Verkauft: {}, Marktanteil: {:.0}%",
                                cc.name,
                                cc.release_year,
                                cc.units_sold,
                                cc.market_share * 100.0
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::BankRivalsMenu => {
                self.title = if is_en {
                    format!(
                        "{} (Loan: {} EUR)",
                        tr(lang, "hub_bank_rivals"),
                        state.bank_loan
                    )
                } else {
                    format!(
                        "{} (Kredit: {} EUR)",
                        tr(lang, "hub_bank_rivals"),
                        state.bank_loan
                    )
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        "Take Bank Loan: +50,000 EUR (1% monthly interest)".to_string()
                    } else {
                        "Bankkredit aufnehmen: +50.000 Euro (1% Monatszins)".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::TakeLoan(50_000),
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Repay Bank Loan: -50,000 EUR".to_string()
                    } else {
                        "Bankkredit tilgen: -50.000 Euro".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::RepayLoan(50_000),
                });
                for (i, r) in state.rivals.iter().enumerate() {
                    if r.acquired_by_player {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!("[Owned Subsidiary] {}", r.name)
                            } else {
                                format!("[Tochterstudio im Besitz] {}", r.name)
                            },
                            speech_hint: String::new(),
                            action: MenuAction::NoOp,
                        });
                    } else {
                        self.options.push(MenuOption {
                            text: if is_en {
                                format!(
                                    "[Acquire Rival] {} (Reputation: {:.1}/10, Price: {} EUR)",
                                    r.name, r.reputation, r.valuation
                                )
                            } else {
                                format!(
                                    "[Konkurrent übernehmen] {} (Reputation: {:.1}/10, Kaufpreis: {} EUR)",
                                    r.name, r.reputation, r.valuation
                                )
                            },
                            speech_hint: String::new(),
                            action: MenuAction::AcquireRival(i),
                        });
                    }
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::InboxMenu => {
                self.title = format!("{} ({})", tr(lang, "hub_inbox"), state.emails.len());
                for (i, mail) in state.emails.iter().enumerate() {
                    self.options.push(MenuOption {
                        text: format!("[{}] {}: {}", mail.year, mail.sender, mail.subject),
                        speech_hint: mail.body.clone(),
                        action: MenuAction::ReadEmail(i),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::ChartsGotyMenu => {
                self.title = if is_en {
                    format!(
                        "{} (Best Score: {:.1}/10, GOTY Awards: {})",
                        tr(lang, "hub_charts_goty"),
                        state.high_score,
                        state.goty_awards
                    )
                } else {
                    format!(
                        "{} (Rekord: {:.1}/10, GOTY-Preise: {})",
                        tr(lang, "hub_charts_goty"),
                        state.high_score,
                        state.goty_awards
                    )
                };
                let era = state.current_era();
                self.options.push(MenuOption {
                    text: if is_en {
                        format!("Current Era: {} - {}", era.name_en, era.desc_en)
                    } else {
                        format!("Aktuelle Ära: {} - {}", era.name_de, era.desc_de)
                    },
                    speech_hint: String::new(),
                    action: MenuAction::NoOp,
                });
                for g in state.game_history.iter().rev() {
                    let avg = g.review.as_ref().map(|r| r.average()).unwrap_or(0.0);
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!(
                                "{} ({}) - {} / {} on {} | Score: {:.1}/10 | Sales: {} | Profit: {} EUR",
                                g.name,
                                g.release_year,
                                g.topic,
                                g.genre,
                                g.platform,
                                avg,
                                g.sales,
                                g.profit()
                            )
                        } else {
                            format!(
                                "{} ({}) - {} / {} auf {} | Wertung: {:.1}/10 | Verkäufe: {} | Gewinn: {} EUR",
                                g.name,
                                g.release_year,
                                g.topic,
                                g.genre,
                                g.platform,
                                avg,
                                g.sales,
                                g.profit()
                            )
                        },
                        speech_hint: String::new(),
                        action: MenuAction::NoOp,
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::TutorialsMenu => {
                self.title = tr(lang, "menu_tutorials");
                let chapters = if is_en {
                    [
                        (
                            "1. Welcome & Keyboard Controls",
                            "Use Up and Down arrows to navigate menus. Press Enter to activate an item, and Backspace or Escape to go back. At the top or bottom of a list, a bump sound alerts you.",
                        ),
                        (
                            "2. Studio Hub, Time & Hotkeys",
                            "Press W to advance one week immediately, or Space to pause real-time progression. Press F at any time for your financial summary, and S for your studio status.",
                        ),
                        (
                            "3. Coherent Production & Synergy",
                            "When developing a production, pick a Topic and Genre that fit logically together (shown as 3/3 Perfect Synergy). In Step 5, use Left/Right arrows or press Enter on Auto-Set Ideal Profile to match the genre's acoustic needs.",
                        ),
                        (
                            "4. Contract Work (Safe Early Income)",
                            "Need cash without risk? Open Contract Work in the Studio Hub to produce radio jingles, Foley soundscapes, or voice recordings for guaranteed payouts.",
                        ),
                        (
                            "5. Research & Custom Audio Engines",
                            "In the Research menu, unlock new historical topics, genres, and audio technologies from magnetic tape to binaural 3D sound, then combine them into your own Custom Audio Engine.",
                        ),
                        (
                            "6. Team, Training & Vacation",
                            "Employees gain fatigue during long productions. Send tired employees on a 3-week vacation in the HR menu so they recover 100% morale and never suffer burnout.",
                        ),
                        (
                            "7. SoundCon Expo, Label & Hardware Lab",
                            "From 1975 you can build custom soundcards and consoles; from 1985 found your own Soundtrack Label; and from 1995 showcase your studio at the annual SoundCon Expo.",
                        ),
                        (
                            "8. Instant Language Switch (F8 / Ctrl+L)",
                            "Press F8 or Ctrl+L at any time to switch seamlessly between German and English.",
                        ),
                    ]
                } else {
                    [
                        (
                            "1. Willkommen & Tastatursteuerung",
                            "Steuere alle Menüs mit Pfeil hoch und runter. Bestätige mit Enter und gehe mit Rücktaste oder Escape zurück. Am oberen und unteren Listenende hörst du einen akustischen Anschlagton (Bump).",
                        ),
                        (
                            "2. Tonstudio-Zentrale, Zeit & Schnellzugriffe",
                            "Drücke die Taste W, um sofort eine Woche weiterzuschalten, oder Leertaste zum Pausieren. Mit Taste F hörst du jederzeit deinen Finanzbericht und mit Taste S den Studio-Status.",
                        ),
                        (
                            "3. Logische Spielentwicklung & Synergien",
                            "Wähle ein Thema und Genre, die inhaltlich zusammenpassen (3 von 3 bedeutet Perfekte Synergie!). Bei den Studio-Slidern kannst du mit Enter die ideale Verteilung für das gewählte Genre automatisch einstellen lassen.",
                        ),
                        (
                            "4. Auftragsarbeiten (Sichere Einnahmen)",
                            "Über das Menü Auftragsarbeiten kannst du jederzeit Radio-Jingles, Hörspiel-Geräusche oder Synchronisationen für sicheres Sofortgeld produzieren.",
                        ),
                        (
                            "5. Forschung & Eigene Audio-Engine",
                            "Erforsche neue Themen, Genres und historische Meilensteine vom Magnetband über FM-Synthese bis hin zu Dolby Atmos und baue daraus deine eigene Audio-Engine.",
                        ),
                        (
                            "6. Personal, Schulung & Erholungsurlaub",
                            "Mitarbeiter ermüden während großer Projekte. Schicke erschöpfte Teammitglieder in der Personalabteilung rechtzeitig in den Urlaub, damit sie frisch erholt zurückkehren.",
                        ),
                        (
                            "7. SoundCon Messe, Label & Hardware-Labor",
                            "Ab 1975 baust du eigene Soundkarten und Konsolen, ab 1985 gründest du dein eigenes Soundtrack-Label und ab 1995 präsentierst du deine Hits auf der SoundCon Messe.",
                        ),
                        (
                            "8. Sofortiger Sprachwechsel (F8 / Strg+L)",
                            "Drücke jederzeit F8 oder Strg+L, um verzögerungsfrei zwischen Deutsch und Englisch umzuschalten.",
                        ),
                    ]
                };
                for (i, (title, body)) in chapters.iter().enumerate() {
                    self.options.push(MenuOption {
                        text: title.to_string(),
                        speech_hint: body.to_string(),
                        action: MenuAction::PlayTutorial(i),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(if state.company_name.is_empty() {
                        MenuId::MainMenu
                    } else {
                        MenuId::GameMenu
                    }),
                });
            }

            MenuId::SettingsMenu => {
                self.title = tr(lang, "menu_settings");
                let lang_label = if is_en {
                    "Language: English (Press Enter or F8 for Deutsch)"
                } else {
                    "Sprache: Deutsch (Enter oder F8 für Englisch)"
                };
                self.options.push(MenuOption {
                    text: lang_label.to_string(),
                    speech_hint: String::new(),
                    action: MenuAction::ToggleLanguage,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Background Music: {} (Enter)",
                            if state.settings.music_enabled {
                                "ON"
                            } else {
                                "OFF"
                            }
                        )
                    } else {
                        format!(
                            "Hintergrundmusik: {} (Enter)",
                            if state.settings.music_enabled {
                                "AN"
                            } else {
                                "AUS"
                            }
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::ToggleMusic,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Music Volume: {}% [Left/Right]",
                            state.settings.music_volume
                        )
                    } else {
                        format!(
                            "Musik-Lautstärke: {}% [Links/Rechts]",
                            state.settings.music_volume
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AdjustMusicVolume,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Sound Effects Volume (SFX): {}% [Left/Right]",
                            state.settings.sfx_volume
                        )
                    } else {
                        format!(
                            "Soundeffekt-Lautstärke (SFX): {}% [Links/Rechts]",
                            state.settings.sfx_volume
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AdjustSfxVolume,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        format!(
                            "Speech Output Volume: {}% [Left/Right]",
                            state.settings.speech_volume
                        )
                    } else {
                        format!(
                            "Sprachausgabe-Lautstärke: {}% [Links/Rechts]",
                            state.settings.speech_volume
                        )
                    },
                    speech_hint: String::new(),
                    action: MenuAction::AdjustSpeechVolume,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(self.settings_return_menu),
                });
            }

            MenuId::SaveMenu => {
                self.title = tr(lang, "menu_save_game");
                for slot in 1..=5 {
                    let fname = GameState::slot_filename(slot);
                    let exists = Path::new(&fname).exists();
                    let status = if exists {
                        if is_en {
                            "Occupied - Press Enter to overwrite"
                        } else {
                            "Belegt - Enter zum Überschreiben"
                        }
                    } else if is_en {
                        "Empty"
                    } else {
                        "Frei"
                    };
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!("Save Slot {} ({})", slot, status)
                        } else {
                            format!("Speicherplatz {} ({})", slot, status)
                        },
                        speech_hint: String::new(),
                        action: MenuAction::SaveSlot(slot),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }

            MenuId::LoadMenu => {
                self.title = tr(lang, "menu_load_game");
                for slot in 1..=5 {
                    let fname = GameState::slot_filename(slot);
                    let exists = Path::new(&fname).exists();
                    let status = if exists {
                        if is_en {
                            "Savegame available - Press Enter to load"
                        } else {
                            "Spielstand vorhanden - Enter zum Laden"
                        }
                    } else if is_en {
                        "Empty"
                    } else {
                        "Leer"
                    };
                    self.options.push(MenuOption {
                        text: if is_en {
                            format!("Save Slot {} ({})", slot, status)
                        } else {
                            format!("Speicherplatz {} ({})", slot, status)
                        },
                        speech_hint: String::new(),
                        action: MenuAction::LoadSlot(slot),
                    });
                }
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::MainMenu),
                });
            }

            MenuId::CreditsMenu => {
                self.title = tr(lang, "menu_credits");
                self.options.push(MenuOption {
                    text: "Audio Studio Tycoon v4.3.0 - Native Rust Edition".to_string(),
                    speech_hint: if is_en {
                        "100% accessible for screenreaders via 64-bit Prism.dll & Tolk.dll FFI."
                            .to_string()
                    } else {
                        "100% barrierefrei für Screenreader via 64-Bit Prism.dll & Tolk.dll FFI."
                            .to_string()
                    },
                    action: MenuAction::NoOp,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::MainMenu),
                });
            }

            MenuId::DeveloperMenu => {
                self.title = if is_en {
                    "Developer Menu (Developer Mode)".to_string()
                } else {
                    "Entwickler-Menü (Developer Mode)".to_string()
                };
                self.options.push(MenuOption {
                    text: if is_en {
                        "+100,000 EUR Instant Cash".to_string()
                    } else {
                        "+100.000 Euro Sofortgeld".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::DevAddMoney,
                });
                self.options.push(MenuOption {
                    text: "+10,000 Fans".to_string(),
                    speech_hint: String::new(),
                    action: MenuAction::DevAddFans,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Advance +1 Year (48 weeks)".to_string()
                    } else {
                        "+1 Jahr vorspringen (48 Wochen)".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::DevAdvanceYear,
                });
                self.options.push(MenuOption {
                    text: if is_en {
                        "Unlock All Topics, Genres & Technologies".to_string()
                    } else {
                        "Alle Themen, Genres & Technologien freischalten".to_string()
                    },
                    speech_hint: String::new(),
                    action: MenuAction::DevUnlockAll,
                });
                self.options.push(MenuOption {
                    text: tr(lang, "menu_back"),
                    speech_hint: String::new(),
                    action: MenuAction::Navigate(MenuId::GameMenu),
                });
            }
        }

        if self.current_index >= self.options.len() && !self.options.is_empty() {
            self.current_index = self.options.len() - 1;
        }
    }

    pub fn handle_input(
        &mut self,
        input: KeyInput,
        state: &mut GameState,
        audio: &mut AudioManager,
    ) {
        // 1. Global language toggle (F8 / Ctrl+L) works everywhere
        if input == KeyInput::ToggleLang {
            let new_lang = state.toggle_language();
            state.save_global_settings();
            audio.play_sound("confirm");
            let old_idx = self.current_index;
            self.rebuild(state);
            self.current_index = old_idx.min(self.options.len().saturating_sub(1));
            let msg = match new_lang {
                Lang::En => tr(new_lang, "language_switched_en"),
                Lang::De => tr(new_lang, "language_switched_de"),
            };
            audio.say_interrupt(&msg);
            self.speak_current(audio, false);
            return;
        }

        if input == KeyInput::ToggleDevMode {
            state.developer_mode = !state.developer_mode;
            audio.play_sound("confirm");
            audio.say_interrupt(if state.developer_mode {
                if state.is_en() {
                    "Developer Mode enabled. Press D for Developer Menu."
                } else {
                    "Entwickler-Modus aktiviert. Drücke D für das Entwickler-Menü."
                }
            } else if state.is_en() {
                "Developer Mode disabled."
            } else {
                "Entwickler-Modus deaktiviert."
            });
            return;
        }

        // 2. Text input mode handling
        if self.is_text_input {
            match input {
                KeyInput::Char(ch) => {
                    if !ch.is_control() && self.text_buffer.chars().count() < 32 {
                        self.text_buffer.push(ch);
                        audio.play_sound("typing");
                        self.rebuild(state);
                        audio.say_interrupt(&ch.to_string());
                    }
                    return;
                }
                KeyInput::Escape => {
                    // Escape immediately cancels text input and returns to parent menu
                    audio.play_sound("click");
                    let back_target = match self.current_menu {
                        MenuId::CompanyNameInput => MenuId::DifficultyMenu,
                        MenuId::DevelopNameInput => MenuId::DevelopSlidersMenu,
                        MenuId::CustomEngineNameInput => MenuId::ResearchMenu,
                        _ => MenuId::GameMenu,
                    };
                    self.switch_to(back_target, state, audio);
                    return;
                }
                KeyInput::Back => {
                    if let Some(removed) = self.text_buffer.pop() {
                        audio.play_sound("click");
                        self.rebuild(state);
                        if state.is_en() {
                            audio.say_interrupt(&format!("Deleted: {}", removed));
                        } else {
                            audio.say_interrupt(&format!("Gelöscht: {}", removed));
                        }
                    } else {
                        // Back out of text input menu if buffer is already empty
                        audio.play_sound("click");
                        let back_target = match self.current_menu {
                            MenuId::CompanyNameInput => MenuId::DifficultyMenu,
                            MenuId::DevelopNameInput => MenuId::DevelopSlidersMenu,
                            MenuId::CustomEngineNameInput => MenuId::ResearchMenu,
                            _ => MenuId::GameMenu,
                        };
                        self.switch_to(back_target, state, audio);
                    }
                    return;
                }
                KeyInput::Enter => {
                    // Proceed to execute the confirm action below
                }
                _ => return,
            }
        }

        // 3. Global shortcuts when not typing
        match input {
            KeyInput::SpeedPauseToggle => {
                if state.time_speed > 0.0 {
                    state.last_speed = state.time_speed;
                    state.time_speed = 0.0;
                    audio.say_interrupt(&tr(state.lang(), "paused"));
                } else {
                    state.time_speed = state.last_speed.max(1.0);
                    audio.say_interrupt(&tr(state.lang(), "speed_normal"));
                }
                return;
            }
            KeyInput::Speed1 => {
                state.time_speed = 1.0;
                audio.say_interrupt(&tr(state.lang(), "speed_normal"));
                return;
            }
            KeyInput::Speed2 => {
                state.time_speed = 2.0;
                audio.say_interrupt(&tr(state.lang(), "speed_fast"));
                return;
            }
            KeyInput::Speed3 => {
                state.time_speed = 4.0;
                audio.say_interrupt(&tr(state.lang(), "speed_ultra"));
                return;
            }
            KeyInput::FinanceSummary => {
                audio.play_sound("select");
                audio.say_interrupt(&state.financial_summary());
                return;
            }
            KeyInput::StatusSummary => {
                audio.play_sound("select");
                audio.say_interrupt(&state.status_summary());
                return;
            }
            KeyInput::Help => {
                audio.play_sound("select");
                let help_txt = if state.is_en() {
                    "Controls: Arrow Up/Down to navigate, Left/Right for sliders, Enter to confirm, Backspace/Esc to go back, W for next week, F for finances, S for studio status, F8 to switch language."
                } else {
                    "Steuerung: Pfeil Hoch/Runter zum Navigieren, Links/Rechts für Regler, Enter zum Bestätigen, Rücktaste/Escape für Zurück, W für nächste Woche, F für Finanzen, S für Status, F8 für Sprachwechsel."
                };
                audio.say_interrupt(help_txt);
                return;
            }
            KeyInput::NextWeek => {
                self.execute_action(MenuAction::AdvanceWeek, state, audio);
                return;
            }
            KeyInput::OpenDevMenu => {
                if state.developer_mode {
                    self.switch_to(MenuId::DeveloperMenu, state, audio);
                }
                return;
            }
            KeyInput::Up => {
                if self.options.is_empty() {
                    return;
                }
                if self.current_index == 0 {
                    // Acoustic boundary bump per lessons_learned.md!
                    audio.play_sound("bump");
                    self.speak_current(audio, true);
                } else {
                    self.current_index -= 1;
                    audio.play_sound("click");
                    self.speak_current(audio, true);
                }
                return;
            }
            KeyInput::Down => {
                if self.options.is_empty() {
                    return;
                }
                if self.current_index + 1 >= self.options.len() {
                    // Acoustic boundary bump per lessons_learned.md!
                    audio.play_sound("bump");
                    self.speak_current(audio, true);
                } else {
                    self.current_index += 1;
                    audio.play_sound("click");
                    self.speak_current(audio, true);
                }
                return;
            }
            KeyInput::Left | KeyInput::Right => {
                let delta: i32 = if input == KeyInput::Right { 1 } else { -1 };
                self.handle_horizontal_adjust(delta, state, audio);
                return;
            }
            KeyInput::Back | KeyInput::Escape => {
                audio.play_sound("click");
                let back_menu = match self.current_menu {
                    MenuId::MainMenu => return,
                    MenuId::DifficultyMenu | MenuId::LoadMenu | MenuId::CreditsMenu => {
                        MenuId::MainMenu
                    }
                    MenuId::SettingsMenu => self.settings_return_menu,
                    MenuId::DevelopGenreMenu => MenuId::DevelopTopicMenu,
                    MenuId::DevelopPlatformMenu => MenuId::DevelopGenreMenu,
                    MenuId::DevelopSizeAudienceMenu => MenuId::DevelopPlatformMenu,
                    MenuId::DevelopSlidersMenu => MenuId::DevelopSizeAudienceMenu,
                    _ => MenuId::GameMenu,
                };
                self.switch_to(back_menu, state, audio);
                return;
            }
            KeyInput::Enter => {
                if let Some(opt) = self.options.get(self.current_index).cloned() {
                    self.execute_action(opt.action, state, audio);
                }
            }
            _ => {}
        }
    }

    fn handle_horizontal_adjust(
        &mut self,
        delta: i32,
        state: &mut GameState,
        audio: &mut AudioManager,
    ) {
        let Some(opt) = self.options.get(self.current_index).cloned() else {
            return;
        };
        match opt.action {
            MenuAction::AdjustSlider { idx } => {
                let cur = state.current_draft.sliders[idx] as i32;
                let rem = state.current_draft.remaining_points();
                let slider_labels_en = [
                    "Gameplay",
                    "Graphics",
                    "Sound",
                    "Story",
                    "AI",
                    "World",
                ];
                let sname = if state.is_en() {
                    slider_labels_en[idx]
                } else {
                    SLIDER_NAMES[idx]
                };
                if delta > 0 && (cur >= 10 || rem <= 0) {
                    audio.play_sound("bump");
                    if state.is_en() {
                        audio.say_interrupt(&format!(
                            "{}: {} (No remaining points or maximum reached)",
                            sname, cur
                        ));
                    } else {
                        audio.say_interrupt(&format!(
                            "{}: {} (Keine freien Punkte mehr oder Maximum erreicht)",
                            sname, cur
                        ));
                    }
                    return;
                }
                if delta < 0 && cur <= 0 {
                    audio.play_sound("bump");
                    return;
                }
                state.current_draft.sliders[idx] = (cur + delta).clamp(0, 10) as u8;
                audio.play_sound("click");
                let idx_keep = self.current_index;
                self.rebuild(state);
                self.current_index = idx_keep;
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "{}: {}, remaining points: {}",
                        sname,
                        state.current_draft.sliders[idx],
                        state.current_draft.remaining_points()
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "{}: {}, freie Punkte: {}",
                        sname,
                        state.current_draft.sliders[idx],
                        state.current_draft.remaining_points()
                    ));
                }
            }
            MenuAction::AdjustMusicVolume => {
                let next = (state.settings.music_volume as i32 + delta * 10).clamp(0, 100) as u8;
                state.settings.music_volume = next;
                audio.music_volume = next;
                state.save_global_settings();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::AdjustSfxVolume => {
                let next = (state.settings.sfx_volume as i32 + delta * 10).clamp(0, 100) as u8;
                state.settings.sfx_volume = next;
                audio.sfx_volume = next;
                state.save_global_settings();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::AdjustSpeechVolume => {
                let next = (state.settings.speech_volume as i32 + delta * 10).clamp(0, 100) as u8;
                state.settings.speech_volume = next;
                audio.speech_volume = next;
                state.save_global_settings();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::AdjustSubscriptionPrice => {
                state.subscription_price =
                    (state.subscription_price + (delta as f64) * 1.0).clamp(2.99, 29.99);
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            _ => {}
        }
    }

    pub fn execute_action(
        &mut self,
        action: MenuAction,
        state: &mut GameState,
        audio: &mut AudioManager,
    ) {
        match action {
            MenuAction::Navigate(target) => {
                audio.play_sound("confirm");
                self.switch_to(target, state, audio);
            }
            MenuAction::Quit => {
                audio.play_sound("confirm");
                self.should_quit = true;
            }
            MenuAction::StartNewGame {
                difficulty,
                start_year,
            } => {
                let saved_settings = state.settings.clone();
                *state = GameState::new(difficulty, start_year);
                state.settings = saved_settings;
                audio.play_sound("confirm");
                self.switch_to(MenuId::CompanyNameInput, state, audio);
            }
            MenuAction::ConfirmCompanyName => {
                let name = if self.text_buffer.trim().is_empty() {
                    "Klangpionier Tonstudio".to_string()
                } else {
                    self.text_buffer.trim().to_string()
                };
                state.company_name = name;
                audio.play_sound("success");
                self.switch_to(MenuId::GameMenu, state, audio);
            }
            MenuAction::SelectTopic(topic) => {
                state.current_draft.topic = topic;
                audio.play_sound("confirm");
                self.switch_to(MenuId::DevelopGenreMenu, state, audio);
            }
            MenuAction::SelectGenre(genre) => {
                state.current_draft.sliders = get_ideal_sliders(&genre);
                state.current_draft.genre = genre;
                audio.play_sound("confirm");
                self.switch_to(MenuId::DevelopPlatformMenu, state, audio);
            }
            MenuAction::SelectPlatform(plat) => {
                if !state.bought_platforms.iter().any(|bp| bp == &plat) {
                    if let Err(err) = state.buy_platform_license(&plat) {
                        audio.play_sound("error");
                        audio.say_interrupt(&err);
                        return;
                    }
                }
                state.current_draft.platform = plat;
                audio.play_sound("confirm");
                self.switch_to(MenuId::DevelopSizeAudienceMenu, state, audio);
            }
            MenuAction::CycleGameSize => {
                let sizes = ["Klein", "Mittel", "Groß", "AAA", "MMO"];
                let pos = sizes
                    .iter()
                    .position(|&s| s == state.current_draft.size)
                    .unwrap_or(0);
                state.current_draft.size = sizes[(pos + 1) % sizes.len()].to_string();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::CycleAudience => {
                let auds = ["Jeder", "Jugendliche", "Hardcore-Gamer"];
                let pos = auds
                    .iter()
                    .position(|&a| a == state.current_draft.audience)
                    .unwrap_or(0);
                state.current_draft.audience = auds[(pos + 1) % auds.len()].to_string();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::CycleEngine => {
                if !state.engines.is_empty() {
                    state.current_draft.engine_idx =
                        (state.current_draft.engine_idx + 1) % state.engines.len();
                }
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::CycleMarketing => {
                let mkts = [
                    "Kein Marketing",
                    "Kleine Kampagne",
                    "Mittlere Kampagne",
                    "Große Kampagne",
                ];
                let pos = mkts
                    .iter()
                    .position(|&m| m == state.current_draft.marketing)
                    .unwrap_or(0);
                state.current_draft.marketing = mkts[(pos + 1) % mkts.len()].to_string();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::ApplyIdealSliders => {
                state.current_draft.sliders = get_ideal_sliders(&state.current_draft.genre);
                audio.play_sound("confirm");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "Ideal sliders set for {}: {}",
                        state.current_draft.genre,
                        state.current_draft.slider_summary()
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "Ideale Slider für {} gesetzt: {}",
                        state.current_draft.genre,
                        state.current_draft.slider_summary()
                    ));
                }
            }
            MenuAction::AdjustSlider { .. } => {
                self.handle_horizontal_adjust(1, state, audio);
            }
            MenuAction::ConfirmGameStart => {
                state.current_draft.name = self.text_buffer.trim().to_string();
                match state.start_game_project() {
                    Ok(msg) => {
                        audio.play_sound("success");
                        self.switch_to(MenuId::ActiveProjectsMenu, state, audio);
                        audio.say_interrupt(&msg);
                    }
                    Err(err) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&err);
                    }
                }
            }
            MenuAction::FinishProject(idx) => {
                if let Some(_finished) = state.finish_ready_project(idx) {
                    audio.play_sound("drumroll");
                    self.switch_to(MenuId::ReviewResultMenu, state, audio);
                }
            }
            MenuAction::ToggleCrunch(idx) => {
                if let Some(ap) = state.active_projects.get_mut(idx) {
                    ap.crunch_active = !ap.crunch_active;
                    audio.play_sound("click");
                    let keep = self.current_index;
                    self.rebuild(state);
                    self.current_index = keep;
                    self.speak_current(audio, true);
                }
            }
            MenuAction::ReleasePatch(idx) => match state.release_patch(idx) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::ReleaseDlc(idx) => match state.release_dlc(idx) {
                Ok(msg) => {
                    audio.play_sound("cash");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::AcceptContract(idx) => {
                if state.active_contract.is_some() {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "An active contract is already in progress!"
                    } else {
                        "Es läuft bereits ein aktiver Auftrag!"
                    });
                    return;
                }
                if idx < state.available_contracts.len() {
                    let c = state.available_contracts.remove(idx);
                    let name = if state.is_en() {
                        c.name_en.clone()
                    } else {
                        c.name_de.clone()
                    };
                    state.active_contract = Some(c);
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    if state.is_en() {
                        audio.say_interrupt(&format!("Contract '{}' accepted!", name));
                    } else {
                        audio.say_interrupt(&format!("Auftrag '{}' angenommen!", name));
                    }
                }
            }
            MenuAction::RefreshContracts => {
                state.refresh_contracts();
                audio.play_sound("confirm");
                self.rebuild(state);
                audio.say_interrupt(if state.is_en() {
                    "New contract offers loaded."
                } else {
                    "Neue Auftragsangebote geladen."
                });
            }
            MenuAction::ResearchGenre(idx) => {
                let item = &RESEARCHABLE_GENRES[idx];
                match state.start_research(
                    "genre",
                    item.name,
                    item.cost,
                    item.unlock_year,
                    item.weeks,
                    15,
                ) {
                    Ok(msg) => {
                        audio.play_sound("confirm");
                        self.rebuild(state);
                        audio.say_interrupt(&msg);
                    }
                    Err(e) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&e);
                    }
                }
            }
            MenuAction::ResearchTopic(idx) => {
                let item = &RESEARCHABLE_TOPICS[idx];
                match state.start_research(
                    "topic",
                    item.name,
                    item.cost,
                    item.unlock_year,
                    item.weeks,
                    10,
                ) {
                    Ok(msg) => {
                        audio.play_sound("confirm");
                        self.rebuild(state);
                        audio.say_interrupt(&msg);
                    }
                    Err(e) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&e);
                    }
                }
            }
            MenuAction::ResearchFeature(idx) => {
                let item = &ENGINE_FEATURES[idx];
                match state.start_research(
                    "feature",
                    item.name,
                    item.cost,
                    item.unlock_year,
                    2,
                    item.tech_bonus,
                ) {
                    Ok(msg) => {
                        audio.play_sound("confirm");
                        self.rebuild(state);
                        audio.say_interrupt(&msg);
                    }
                    Err(e) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&e);
                    }
                }
            }
            MenuAction::ResearchTech(idx) => {
                let item = &RESEARCHABLE_TECHNOLOGIES[idx];
                match state.start_research(
                    "tech",
                    item.name,
                    item.cost,
                    item.unlock_year,
                    item.weeks,
                    20,
                ) {
                    Ok(msg) => {
                        audio.play_sound("confirm");
                        self.rebuild(state);
                        audio.say_interrupt(&msg);
                    }
                    Err(e) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&e);
                    }
                }
            }
            MenuAction::ConfirmCustomEngine => {
                let name = self.text_buffer.clone();
                match state.build_custom_engine(&name) {
                    Ok(msg) => {
                        audio.play_sound("success");
                        self.switch_to(MenuId::ResearchMenu, state, audio);
                        audio.say_interrupt(&msg);
                    }
                    Err(e) => {
                        audio.play_sound("error");
                        audio.say_interrupt(&e);
                    }
                }
            }
            MenuAction::HireCandidate(idx) => match state.hire_candidate(idx) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::TrainEmployee(idx) => match state.train_employee(idx) {
                Ok(msg) => {
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::VacationEmployee(idx) => match state.send_employee_on_vacation(idx) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::FireEmployee(idx) => match state.fire_employee(idx) {
                Ok(msg) => {
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::UpgradeOffice => match state.upgrade_office() {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::BuyStudioPerk {
                id,
                cost,
                desc_de,
                desc_en,
            } => {
                if state.office_upgrades.contains(&id) {
                    audio.play_sound("bump");
                    audio.say_interrupt(if state.is_en() {
                        "Already installed!"
                    } else {
                        "Bereits installiert!"
                    });
                    return;
                }
                if state.money < cost {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money!"
                    } else {
                        "Nicht genug Geld!"
                    });
                    return;
                }
                state.money -= cost;
                state.office_upgrades.push(id.clone());
                if id == "accessibility_lab" {
                    state.accessibility_reputation += 40;
                } else if id == "espresso_lounge" {
                    for e in &mut state.employees {
                        e.morale = 100;
                        e.fatigue = e.fatigue.saturating_sub(20);
                    }
                }
                audio.play_sound("buy");
                self.rebuild(state);
                audio.say_interrupt(if state.is_en() { &desc_en } else { &desc_de });
            }
            MenuAction::RunMarketingCampaign {
                cost,
                hype_gain,
                fan_gain,
                label,
            } => {
                if state.money < cost {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money for this campaign!"
                    } else {
                        "Nicht genug Geld für diese Kampagne!"
                    });
                    return;
                }
                state.money -= cost;
                let eff_hype = hype_gain * state.marketing_efficiency;
                state.hype = (state.hype + eff_hype).clamp(0.0, 250.0);
                state.fans += fan_gain;
                audio.play_sound("cash");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "{} launched: +{:.0} Hype, +{} Fans!",
                        label, eff_hype, fan_gain
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "{} gestartet: +{:.0} Hype, +{} Fans!",
                        label, eff_hype, fan_gain
                    ));
                }
            }
            MenuAction::ComposeJingle => {
                if state.money < 3_000 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money (3,000 EUR)!"
                    } else {
                        "Nicht genug Geld (3.000 Euro)!"
                    });
                    return;
                }
                state.money -= 3_000;
                state.jingle_bonus = (state.jingle_bonus + 5.0).min(40.0);
                state.hype = (state.hype + 10.0).min(250.0);
                audio.play_sound("success");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "New studio jingle produced! Jingle bonus now +{:.0}.",
                        state.jingle_bonus
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "Neuer Studio-Jingle produziert! Jingle-Bonus jetzt +{:.0}.",
                        state.jingle_bonus
                    ));
                }
            }
            MenuAction::AnswerFanMail => match state.answer_fan_mail() {
                Ok(msg) => {
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::ProduceMerch => {
                if state.money < 5_000 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money (5,000 EUR)!"
                    } else {
                        "Nicht genug Geld (5.000 Euro)!"
                    });
                    return;
                }
                state.money -= 5_000;
                state.merch_stock += 500;
                audio.play_sound("buy");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "500 fan merchandise items produced! Stock: {}.",
                        state.merch_stock
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "500 Fan-Artikel produziert! Lagerbestand: {}.",
                        state.merch_stock
                    ));
                }
            }
            MenuAction::AttendSoundCon(tier) => match state.attend_soundcon(tier) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::FoundLabel => {
                if state.calendar_year() < 1985 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "The Soundtrack Label is only available from 1985!"
                    } else {
                        "Das Soundtrack-Label ist erst ab dem Jahr 1985 verfügbar!"
                    });
                    return;
                }
                if state.money < 25_000 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money (25,000 EUR)!"
                    } else {
                        "Nicht genug Geld (25.000 Euro)!"
                    });
                    return;
                }
                state.money -= 25_000;
                state.label_active = true;
                state.label_name = format!("{} Records", state.company_name);
                audio.play_sound("success");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "Soundtrack Label '{}' founded successfully!",
                        state.label_name
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "Soundtrack-Label '{}' erfolgreich gegründet!",
                        state.label_name
                    ));
                }
            }
            MenuAction::AddGameToLabel(idx) => {
                if let Some(g) = state.game_history.get_mut(idx) {
                    g.in_soundtrack_label = true;
                    let name = g.name.clone();
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    if state.is_en() {
                        audio.say_interrupt(&format!(
                            "Soundtrack of '{}' added to Label!",
                            name
                        ));
                    } else {
                        audio.say_interrupt(&format!(
                            "Soundtrack von '{}' ins Label aufgenommen!",
                            name
                        ));
                    }
                }
            }
            MenuAction::OrganizeConcert => {
                if state.money < 20_000 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "Not enough money (20,000 EUR)!"
                    } else {
                        "Nicht genug Geld (20.000 Euro)!"
                    });
                    return;
                }
                state.money -= 20_000;
                let ticket_rev = 35_000 + (state.fans as i64 * 2).min(80_000);
                state.money += ticket_rev;
                state.total_revenue += ticket_rev;
                state.fans += 1_200;
                audio.play_sound("cash");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!(
                        "Live Concert was a triumph! Revenue: {} EUR, +1,200 Fans!",
                        ticket_rev
                    ));
                } else {
                    audio.say_interrupt(&format!(
                        "Live-Konzert war ein Triumph! Einnahmen: {} Euro, +1.200 Fans!",
                        ticket_rev
                    ));
                }
            }
            MenuAction::ToggleSubscription => {
                if state.calendar_year() < 1995 {
                    audio.play_sound("error");
                    audio.say_interrupt(if state.is_en() {
                        "The AudioPass subscription service is only available from 1995!"
                    } else {
                        "Der AudioPass Abo-Dienst ist erst ab dem Jahr 1995 verfügbar!"
                    });
                    return;
                }
                state.subscription_active = !state.subscription_active;
                if state.subscription_active && state.subscription_subscribers == 0 {
                    state.subscription_subscribers = 250;
                }
                audio.play_sound("confirm");
                self.rebuild(state);
                audio.say_interrupt(if state.subscription_active {
                    if state.is_en() {
                        "AudioPass subscription service activated!"
                    } else {
                        "AudioPass Abo-Dienst aktiviert!"
                    }
                } else if state.is_en() {
                    "AudioPass subscription service paused."
                } else {
                    "AudioPass Abo-Dienst pausiert."
                });
            }
            MenuAction::AdjustSubscriptionPrice => {
                self.handle_horizontal_adjust(1, state, audio);
            }
            MenuAction::AddGameToSubscription(idx) => {
                if let Some(g) = state.game_history.get_mut(idx) {
                    g.in_subscription_vault = true;
                    let name = g.name.clone();
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    if state.is_en() {
                        audio.say_interrupt(&format!("'{}' added to AudioPass!", name));
                    } else {
                        audio.say_interrupt(&format!("'{}' in den AudioPass aufgenommen!", name));
                    }
                }
            }
            MenuAction::DevelopSoundcard => match state.develop_soundcard("") {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::DevelopConsole => match state.develop_console("") {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::TakeLoan(amt) => match state.take_loan(amt) {
                Ok(msg) => {
                    audio.play_sound("cash");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::RepayLoan(amt) => match state.repay_loan(amt) {
                Ok(msg) => {
                    audio.play_sound("confirm");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::AcquireRival(idx) => {
                if idx < state.rivals.len() {
                    let price = state.rivals[idx].valuation;
                    if state.money < price {
                        audio.play_sound("error");
                        if state.is_en() {
                            audio.say_interrupt(&format!(
                                "Not enough money for acquisition ({} EUR required).",
                                price
                            ));
                        } else {
                            audio.say_interrupt(&format!(
                                "Nicht genug Geld für die Übernahme ({} Euro benötigt).",
                                price
                            ));
                        }
                        return;
                    }
                    state.money -= price;
                    state.rivals[idx].acquired_by_player = true;
                    state.fans += 5_000;
                    let rname = state.rivals[idx].name.clone();
                    audio.play_sound("success");
                    self.rebuild(state);
                    if state.is_en() {
                        audio.say_interrupt(&format!(
                            "{} acquired successfully! +5,000 Fans!",
                            rname
                        ));
                    } else {
                        audio.say_interrupt(&format!(
                            "{} erfolgreich übernommen! +5.000 Fans!",
                            rname
                        ));
                    }
                }
            }
            MenuAction::ReadEmail(idx) => {
                if let Some(m) = state.emails.get_mut(idx) {
                    m.read = true;
                    let text = format!("{}: {}. {}", m.sender, m.subject, m.body);
                    audio.play_sound("select");
                    audio.say_interrupt(&text);
                }
            }
            MenuAction::PlayTutorial(_idx) => {
                audio.play_sound("select");
                self.speak_current(audio, true);
            }
            MenuAction::ToggleLanguage => {
                self.handle_input(KeyInput::ToggleLang, state, audio);
            }
            MenuAction::ToggleMusic => {
                state.settings.music_enabled = !state.settings.music_enabled;
                audio.music_enabled = state.settings.music_enabled;
                if audio.music_enabled {
                    audio.play_music("music_back");
                } else {
                    audio.stop_music();
                }
                state.save_global_settings();
                audio.play_sound("confirm");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep;
                self.speak_current(audio, true);
            }
            MenuAction::AdjustMusicVolume
            | MenuAction::AdjustSfxVolume
            | MenuAction::AdjustSpeechVolume => {
                self.handle_horizontal_adjust(1, state, audio);
            }
            MenuAction::SaveSlot(slot) => match state.save_slot(slot) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.rebuild(state);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::LoadSlot(slot) => match state.load_slot(slot) {
                Ok(msg) => {
                    audio.play_sound("success");
                    self.switch_to(MenuId::GameMenu, state, audio);
                    audio.say_interrupt(&msg);
                }
                Err(e) => {
                    audio.play_sound("error");
                    audio.say_interrupt(&e);
                }
            },
            MenuAction::AdvanceWeek => {
                let notes = state.tick_week();
                audio.play_sound("click");
                let keep = self.current_index;
                self.rebuild(state);
                self.current_index = keep.min(self.options.len().saturating_sub(1));
                let cal = state.calendar_text();
                if notes.is_empty() {
                    if state.is_en() {
                        audio.say_interrupt(&format!("{}. Balance: {} EUR.", cal, state.money));
                    } else {
                        audio.say_interrupt(&format!("{}. Kontostand: {} Euro.", cal, state.money));
                    }
                } else {
                    audio.say_interrupt(&format!("{}. {}", cal, notes.join(" ")));
                }
            }
            MenuAction::DevAddMoney => {
                state.money += 100_000;
                audio.play_sound("cash");
                if state.is_en() {
                    audio.say_interrupt(&format!("Balance: {} EUR.", state.money));
                } else {
                    audio.say_interrupt(&format!("Kontostand: {} Euro.", state.money));
                }
            }
            MenuAction::DevAddFans => {
                state.fans += 10_000;
                audio.play_sound("success");
                audio.say_interrupt(&format!("Fans: {}.", state.fans));
            }
            MenuAction::DevAdvanceYear => {
                for _ in 0..WEEKS_PER_YEAR {
                    state.tick_week();
                }
                audio.play_sound("confirm");
                self.rebuild(state);
                if state.is_en() {
                    audio.say_interrupt(&format!("Year advanced: {}", state.calendar_text()));
                } else {
                    audio.say_interrupt(&format!("Jahr vorgespult: {}", state.calendar_text()));
                }
            }
            MenuAction::DevUnlockAll => {
                for g in GENRES {
                    if !state.unlocked_genres.iter().any(|ug| ug == *g) {
                        state.unlocked_genres.push(g.to_string());
                    }
                }
                for t in RESEARCHABLE_TOPICS {
                    if !state.unlocked_topics.iter().any(|ut| ut == t.name) {
                        state.unlocked_topics.push(t.name.to_string());
                    }
                }
                for f in ENGINE_FEATURES {
                    if !state.unlocked_features.iter().any(|uf| uf == f.name) {
                        state.unlocked_features.push(f.name.to_string());
                    }
                }
                for tech in RESEARCHABLE_TECHNOLOGIES {
                    if !state.unlocked_technologies.iter().any(|ut| ut == tech.name) {
                        state.unlocked_technologies.push(tech.name.to_string());
                    }
                }
                audio.play_sound("success");
                if state.is_en() {
                    audio.say_interrupt(
                        "All topics, genres, engine features and technologies unlocked!",
                    );
                } else {
                    audio.say_interrupt(
                        "Alle Themen, Genres, Engine-Features und Technologien freigeschaltet!",
                    );
                }
            }
            MenuAction::NoOp => {
                self.speak_current(audio, true);
            }
        }
    }
}
