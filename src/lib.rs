//! Audio Studio Tycoon - Native Rust Edition
//! Complete, coherent studio & game development simulation with 100% screenreader accessibility.

pub mod audio;
pub mod data;
pub mod gui;
pub mod i18n;
pub mod json;
pub mod menus;
pub mod models;
pub mod state;

#[cfg(test)]
mod tests {
    use crate::audio::AudioManager;
    use crate::data::*;
    use crate::i18n::{build_dictionary, Lang};
    use crate::json::parse_json;
    use crate::menus::{KeyInput, MenuAction, MenuController, MenuId, ALL_MENU_IDS};
    use crate::models::{GameProject, ReviewScore};
    use crate::state::GameState;
    use std::collections::HashSet;
    use std::fs;
    use std::path::Path;

    #[test]
    fn test_i18n_symmetry_and_utf8_cleanliness() {
        let de = build_dictionary(Lang::De);
        let en = build_dictionary(Lang::En);
        assert_eq!(de.len(), en.len(), "DE and EN dictionaries must have identical key counts");
        for k in de.keys() {
            assert!(en.contains_key(k), "Missing key in EN: {}", k);
        }

        // Verify no Mojibake sequences per lessons_learned.md
        let forbidden = ["Ã¼", "Ã¶", "Ã¤", "ÃŸ", "Ã„", "Ã–", "Ãœ"];
        for (&k, &val) in de.iter().chain(en.iter()) {
            for bad in forbidden {
                assert!(
                    !val.contains(bad),
                    "Mojibake '{}' found in key '{}': {}",
                    bad,
                    k,
                    val
                );
            }
        }
    }

    #[test]
    fn test_timeline_start_year_and_era_clamping() {
        // 1. Start year 1930 initialization must actively set up platforms, topics, trend, and year event
        let state_1930 = GameState::new(1, 1930);
        assert_eq!(state_1930.calendar_year(), 1930);
        assert_eq!(state_1930.week_in_year(), 1);
        assert!(!state_1930.bought_platforms.is_empty());
        assert_eq!(state_1930.bought_platforms[0], "Radio-Sendernetz (AM)");
        assert!(!state_1930.event_log.is_empty());
        assert_eq!(state_1930.current_era().id, "era_radio");

        // 2. Clamping for years before 1930 and after 2026 (must never wrap back to 1930!)
        assert_eq!(get_current_era(1900).id, "era_radio");
        assert_eq!(get_current_era(2026).id, "era_spatial");
        assert_eq!(get_current_era(2035).id, "era_spatial");
        assert_eq!(get_current_era(2099).id, "era_spatial");
    }

    #[test]
    fn test_logical_topic_genre_compatibility_and_sliders() {
        // Verify that the nonsensical Python combinations are fixed:
        // Fantasy + RPG = 3 (Perfect!), Fantasy + Sport = 0 (Unpassend)
        assert_eq!(get_compatibility("Fantasy", "RPG"), 3);
        assert_eq!(get_compatibility("Fantasy", "Sport"), 0);

        // Rennwagen + Rennspiel = 3 (Perfect!)
        assert_eq!(get_compatibility("Rennwagen", "Rennspiel"), 3);
        assert_eq!(get_compatibility("Rennwagen", "Horror"), 0);

        // Schach + Strategie/Puzzle = 3, Schach + Horror = 0
        assert_eq!(get_compatibility("Schach", "Strategie"), 3);
        assert_eq!(get_compatibility("Schach", "Puzzle"), 3);
        assert_eq!(get_compatibility("Schach", "Horror"), 0);

        // Radio-Drama + Abenteuer/Horror = 3
        assert_eq!(get_compatibility("Radio-Drama", "Abenteuer"), 3);
        assert_eq!(get_compatibility("Radio-Drama", "Horror"), 3);

        // Verify all genre ideal sliders sum to 30
        for &g in GENRES {
            let ideal = get_ideal_sliders(g);
            let sum: u32 = ideal.iter().map(|&x| x as u32).sum();
            assert_eq!(sum, 30, "Ideal sliders for genre '{}' must sum to 30", g);
        }
    }

    #[test]
    fn test_game_development_and_coherent_review_scoring() {
        let mut state = GameState::new(1, 1930);
        // 1. Develop a well-matched game (Radio-Drama + Abenteuer, ideal sliders, 0 bugs)
        state.current_draft.name = "Geheimnis im Äther".to_string();
        state.current_draft.topic = "Radio-Drama".to_string();
        state.current_draft.genre = "Abenteuer".to_string();
        state.current_draft.sliders = get_ideal_sliders("Abenteuer");
        state.start_game_project().expect("Should start project");
        assert_eq!(state.active_projects.len(), 1);

        // Advance until ready
        for _ in 0..6 {
            state.tick_week();
        }
        assert!(state.active_projects[0].ready_to_finish);
        state.active_projects[0].bugs = 0;
        let finished_good = state.finish_ready_project(0).expect("Should finish");
        let good_score = finished_good.review.as_ref().unwrap().average();

        // 2. Compare with a poorly matched game (Schach + Horror, terrible sliders, 15 bugs)
        state.current_draft.name = "Schach des Grauens".to_string();
        state.current_draft.topic = "Schach".to_string();
        state.current_draft.genre = "Horror".to_string();
        state.current_draft.sliders = [10, 10, 0, 0, 10, 0];
        let bad_proj = state.game_history[0].clone();
        let mut bad_proj_test = bad_proj;
        bad_proj_test.topic = "Schach".to_string();
        bad_proj_test.genre = "Horror".to_string();
        bad_proj_test.sliders = [10, 10, 0, 0, 10, 0];
        let bad_review = state.calculate_review(&bad_proj_test, 15);

        assert!(
            good_score >= 7.5,
            "Well-matched game with ideal sliders and 0 bugs should score >= 7.5 (got {})",
            good_score
        );
        assert!(
            bad_review.average() <= 4.5,
            "Poorly matched game with wrong sliders and 15 bugs should score <= 4.5 (got {})",
            bad_review.average()
        );
        assert!(good_score > bad_review.average() + 3.0);
    }

    #[test]
    fn test_year_gating_on_subsystems() {
        let mut state = GameState::new(1, 1930);
        // SoundCon is locked in 1930 (unlocks in 1995)
        assert!(state.attend_soundcon(0).is_err());

        // Custom Soundcard & Console are locked in 1930 without Hardware-Labor (unlocks 1975)
        assert!(state.develop_soundcard("RetroCard").is_err());
        assert!(state.develop_console("RetroBox").is_err());

        // Researching a 2022 technology in 1930 must fail
        assert!(
            state
                .start_research("tech", "KI-Soundtrack & Mastering", 220_000, 2022, 5, 20)
                .is_err()
        );

        // Jump to 1996: SoundCon and Hardware Lab work!
        let mut state_1996 = GameState::new(0, 1996);
        state_1996.money = 500_000;
        assert!(state_1996.attend_soundcon(1).is_ok());
        // Cannot attend SoundCon twice in the same year
        assert!(state_1996.attend_soundcon(0).is_err());
        assert!(state_1996.develop_soundcard("SoundStar 96").is_ok());
        assert!(state_1996.develop_console("AudioBox 64").is_ok());
    }

    #[test]
    fn test_employee_hiring_vacation_and_monthly_payroll() {
        let mut state = GameState::new(0, 1930);
        // Hire 1 candidate (Garage allows max 2 employees: CEO + 1)
        assert_eq!(state.employees.len(), 1);
        state.hire_candidate(0).expect("Should hire 1st candidate");
        assert_eq!(state.employees.len(), 2);

        // Hiring a 3rd employee in the Garage must fail until studio is upgraded
        assert!(state.hire_candidate(0).is_err());

        // Upgrade studio -> now max 4 employees
        state.upgrade_office().expect("Should upgrade studio");
        assert_eq!(state.office_level, 1);
        state.hire_candidate(0).expect("Should hire 2nd candidate after upgrade");
        assert_eq!(state.employees.len(), 3);

        // Give employee 1 fatigue and send on vacation
        state.employees[1].fatigue = 80;
        assert_eq!(state.active_employees().len(), 3);
        state
            .send_employee_on_vacation(1)
            .expect("Should send on vacation");
        // While on vacation, active_employees() must exclude them!
        assert_eq!(state.active_employees().len(), 2);
        // Cannot train an employee who is on vacation
        assert!(state.train_employee(1).is_err());

        // Advance 3 weeks -> employee returns from vacation with reduced fatigue
        for _ in 0..3 {
            state.tick_week();
        }
        assert_eq!(state.employees[1].vacation_weeks_left, 0);
        assert!(state.employees[1].fatigue < 10);
        assert_eq!(state.active_employees().len(), 3);
    }

    #[test]
    fn test_contract_work_and_bank_loans() {
        let mut state = GameState::new(1, 1930);
        let initial_money = state.money;
        let c = state.available_contracts.remove(0);
        let reward = c.reward;
        state.active_contract = Some(c);

        // Tick weeks until contract finishes
        for _ in 0..3 {
            state.tick_week();
        }
        assert!(state.active_contract.is_none());
        assert_eq!(state.money, initial_money + reward);

        // Test bank loan and repayment
        state.take_loan(50_000).expect("Should take loan");
        assert_eq!(state.bank_loan, 50_000);
        state.repay_loan(20_000).expect("Should repay partial loan");
        assert_eq!(state.bank_loan, 30_000);
    }

    #[test]
    fn test_json_save_and_load_roundtrip() {
        let mut state = GameState::new(1, 1982);
        state.company_name = "Rust Sonic Foundry".to_string();
        state.money = 345_678;
        state.fans = 12_345;
        // Developing a custom soundcard costs 60,000 EUR -> 285,678 EUR remaining
        state.develop_soundcard("SID-Master 82").unwrap();
        assert_eq!(state.money, 285_678);

        let test_path = Path::new("save_slot_98.json");
        state.save_to_file(test_path).expect("Should save JSON");
        let loaded = GameState::load_from_file(test_path).expect("Should load JSON");
        let _ = fs::remove_file(test_path);

        assert_eq!(loaded.company_name, "Rust Sonic Foundry");
        assert_eq!(loaded.money, 285_678);
        assert_eq!(loaded.fans, 12_345);
        assert_eq!(loaded.calendar_year(), 1982);
        assert_eq!(loaded.custom_soundcards.len(), 1);
        assert_eq!(loaded.custom_soundcards[0].name, "SID-Master 82");

        // Also test edge cases in JSON parser (escapes, negative numbers, nested arrays)
        let raw = r#"{"text": "Größe & \"Klang\"\nTest", "num": -42.5, "arr": [true, false, null]}"#;
        let parsed = parse_json(raw).expect("Should parse complex JSON");
        assert_eq!(parsed.get_str("text", ""), "Größe & \"Klang\"\nTest");
        assert_eq!(parsed.get_f64("num", 0.0), -42.5);
    }

    #[test]
    fn test_all_menus_build_and_acoustic_boundary_bump() {
        let mut state = GameState::new(1, 1996);
        let mut audio = AudioManager::new(true);
        let mut ctrl = MenuController::new(&state);

        // 1. Verify every single MenuId builds cleanly with non-empty options and valid title
        for &menu_id in ALL_MENU_IDS {
            ctrl.switch_to(menu_id, &state, &audio);
            assert!(
                !ctrl.title.is_empty(),
                "Menu {:?} must have a non-empty title",
                menu_id
            );
            assert!(
                !ctrl.options.is_empty(),
                "Menu {:?} must have at least 1 option",
                menu_id
            );
        }

        // 2. Verify acoustic boundary bump at top and bottom of menu
        ctrl.switch_to(MenuId::MainMenu, &state, &audio);
        assert_eq!(ctrl.current_index, 0);
        ctrl.handle_input(KeyInput::Up, &mut state, &mut audio);
        assert_eq!(ctrl.current_index, 0);
        assert_eq!(
            audio.last_sound(),
            "bump",
            "Pressing Up at index 0 must play 'bump' sound"
        );

        let last_idx = ctrl.options.len() - 1;
        for _ in 0..last_idx {
            ctrl.handle_input(KeyInput::Down, &mut state, &mut audio);
        }
        assert_eq!(ctrl.current_index, last_idx);
        assert_eq!(audio.last_sound(), "click");

        // Pressing Down at the last item must play "bump" and stay at last_idx
        ctrl.handle_input(KeyInput::Down, &mut state, &mut audio);
        assert_eq!(ctrl.current_index, last_idx);
        assert_eq!(
            audio.last_sound(),
            "bump",
            "Pressing Down at the last index must play 'bump' sound"
        );

        // 3. Verify F8 language toggle preserves cursor index and switches DE <-> EN
        ctrl.current_index = 2;
        assert_eq!(state.lang(), Lang::De);
        ctrl.handle_input(KeyInput::ToggleLang, &mut state, &mut audio);
        assert_eq!(state.lang(), Lang::En);
        assert_eq!(ctrl.current_index, 2);
        assert!(ctrl.title.contains("Main Menu"));
        ctrl.handle_input(KeyInput::ToggleLang, &mut state, &mut audio);
        assert_eq!(state.lang(), Lang::De);
    }

    #[test]
    fn test_prism_ffi_initialization_and_clean_shutdown() {
        // Verify that non-headless AudioManager initializes Prism/Tolk without crashing
        // and shuts down cleanly
        let audio = AudioManager::new(false);
        assert!(!audio.backend_info.is_empty());
        audio.say_interrupt("Rust Audio Test");
        audio.cleanup();
    }

    #[test]
    fn test_edge_cases_empty_inputs_boundaries_post_release_and_goty() {
        let mut state = GameState::new(1, 1998);
        let mut audio = AudioManager::new(true);
        let mut ctrl = MenuController::new(&state);

        // 1. Empty JSON input and malformed JSON error path
        assert!(parse_json("").is_err());
        assert!(parse_json("{unclosed").is_err());

        // 2. Slider boundaries (0, 30-point total budget cap, and 10-point individual slider cap)
        ctrl.switch_to(MenuId::DevelopSlidersMenu, &state, &audio);
        ctrl.current_index = 1; // Gameplay slider (starts at [5, 5, 5, 5, 5, 5])
        for _ in 0..15 {
            ctrl.handle_input(KeyInput::Left, &mut state, &mut audio);
        }
        assert_eq!(state.current_draft.sliders[0], 0, "Slider must clamp at 0");
        assert_eq!(audio.last_sound(), "bump");
        // With other 5 sliders at 5 (sum = 25), 30-point budget caps slider[0] at 5
        for _ in 0..15 {
            ctrl.handle_input(KeyInput::Right, &mut state, &mut audio);
        }
        assert_eq!(
            state.current_draft.sliders[0], 5,
            "Slider must respect 30-point total budget cap"
        );
        assert_eq!(audio.last_sound(), "bump");
        // When other sliders are 0, individual slider caps at 10
        state.current_draft.sliders = [0, 0, 0, 0, 0, 0];
        for _ in 0..15 {
            ctrl.handle_input(KeyInput::Right, &mut state, &mut audio);
        }
        assert_eq!(
            state.current_draft.sliders[0], 10,
            "Slider must clamp at individual max 10"
        );
        assert_eq!(audio.last_sound(), "bump");

        // 3. Loan limit boundary and negative/zero repayment edge cases
        assert!(state.take_loan(0).is_err());
        assert!(state.take_loan(-5000).is_err());
        assert!(state.take_loan(10_000_000).is_err()); // Exceeds credit limit
        assert!(state.repay_loan(10_000).is_err()); // No active loan yet

        // 4. Post-release lifecycle: Patch, DLC, Label OST (1985+), AudioPass (1995+), and GOTY
        state.money = 500_000;
        state.current_draft.name = "Symphony of 1998".to_string();
        state.current_draft.topic = "Cyberpunk".to_string();
        state.current_draft.genre = "RPG".to_string();
        state.current_draft.sliders = get_ideal_sliders("RPG");
        state.start_game_project().unwrap();
        for _ in 0..8 {
            state.tick_week();
        }
        state.active_projects[0].bugs = 4;
        state.finish_ready_project(0).unwrap();
        assert_eq!(state.game_history.len(), 1);
        assert_eq!(state.game_history[0].bugs, 4);

        // Execute post-release Patch and DLC via MenuId::ActiveProjectsMenu
        ctrl.switch_to(MenuId::ActiveProjectsMenu, &state, &audio);
        // Find ReleasePatch(0) option and trigger it
        let patch_idx = ctrl
            .options
            .iter()
            .position(|o| matches!(o.action, crate::menus::MenuAction::ReleasePatch(0)))
            .expect("ReleasePatch(0) option should exist when bugs > 0");
        ctrl.current_index = patch_idx;
        ctrl.handle_input(KeyInput::Enter, &mut state, &mut audio);
        assert_eq!(state.game_history[0].bugs, 0);
        assert_eq!(state.game_history[0].patches_released, 1);

        // Find ReleaseDlc(0) option and trigger it
        let dlc_idx = ctrl
            .options
            .iter()
            .position(|o| matches!(o.action, crate::menus::MenuAction::ReleaseDlc(0)))
            .expect("ReleaseDlc(0) option should exist");
        ctrl.current_index = dlc_idx;
        ctrl.handle_input(KeyInput::Enter, &mut state, &mut audio);
        assert_eq!(state.game_history[0].dlc_count, 1);

        // Advance to end of year (week 48 -> week 1 of 1999) and verify GOTY evaluation runs cleanly
        while state.week_in_year() < WEEKS_PER_YEAR {
            state.tick_week();
        }
        state.tick_week();
        assert_eq!(state.calendar_year(), 1999);
    }

    #[test]
    fn test_fan_mail_and_dlc_exploit_prevention() {
        let mut state = GameState::new(1, 1998);
        state.money = 500_000;

        // 1. Fan mail starts at 1 unanswered batch; 1st call succeeds, 2nd call in same week fails
        assert_eq!(state.unanswered_fan_mails, 1);
        let fans_before = state.fans;
        assert!(state.answer_fan_mail().is_ok());
        assert_eq!(state.unanswered_fan_mails, 0);
        assert_eq!(state.fans, fans_before + 200);
        assert!(
            state.answer_fan_mail().is_err(),
            "Spamming AnswerFanMail when unanswered_fan_mails == 0 must fail"
        );
        assert_eq!(state.fans, fans_before + 200);

        // 2. Develop and release a game with 3 bugs
        state.current_draft.name = "Exploit Test 98".to_string();
        state.current_draft.topic = "Cyberpunk".to_string();
        state.current_draft.genre = "RPG".to_string();
        state.current_draft.sliders = get_ideal_sliders("RPG");
        state.start_game_project().unwrap();
        for _ in 0..8 {
            state.tick_week();
        }
        state.active_projects[0].bugs = 3;
        state.finish_ready_project(0).unwrap();

        // 3. First patch fixes all bugs; second patch when bugs == 0 must fail
        assert!(state.release_patch(0).is_ok());
        assert_eq!(state.game_history[0].bugs, 0);
        assert!(
            state.release_patch(0).is_err(),
            "Releasing a patch when bugs == 0 must fail"
        );

        // 4. Up to 2 DLCs per game succeed; 3rd DLC attempt must fail (preventing infinite compounding)
        assert!(state.release_dlc(0).is_ok());
        assert_eq!(state.game_history[0].dlc_count, 1);
        assert!(state.release_dlc(0).is_ok());
        assert_eq!(state.game_history[0].dlc_count, 2);
        let sales_after_two_dlcs = state.game_history[0].sales;
        assert!(
            state.release_dlc(0).is_err(),
            "Releasing more than 2 DLCs for the same game must fail"
        );
        assert_eq!(state.game_history[0].sales, sales_after_two_dlcs);
    }

    #[test]
    fn test_studio_perks_and_office_level_boost_review_score() {
        let mut base_state = GameState::new(1, 1985);
        base_state.current_draft.name = "Synth Quest".to_string();
        base_state.current_draft.topic = "Sci-Fi".to_string();
        base_state.current_draft.genre = "Abenteuer".to_string();
        base_state.current_draft.sliders = get_ideal_sliders("Abenteuer");
        base_state.start_game_project().unwrap();
        let test_proj = base_state.active_projects[0].project.clone();

        let base_review = base_state.calculate_review(&test_proj, 0);

        let mut upgraded_state = base_state.clone();
        upgraded_state.office_level = 3;
        upgraded_state.office_upgrades.push("mixing_desk".to_string());
        upgraded_state.office_upgrades.push("foley_stage".to_string());
        let upgraded_review = upgraded_state.calculate_review(&test_proj, 0);

        assert!(
            upgraded_review.average() > base_review.average(),
            "Studio upgrades ('mixing_desk', 'foley_stage') and office_level must boost review score ({} vs {})",
            upgraded_review.average(),
            base_review.average()
        );
    }

    #[test]
    fn test_complete_save_load_and_legacy_python_save_migration() {
        let mut state = GameState::new(1, 1996);
        state.company_name = "Full State Studio".to_string();
        state.office_upgrades = vec!["mixing_desk".to_string(), "foley_stage".to_string()];
        state.jingle_bonus = 25.0;
        state.unanswered_fan_mails = 4;
        state.active_contract = state.available_contracts.pop();
        state.soundcon_history.push("1996: SoundCon Stage".to_string());
        state.tutorials_completed = vec!["ch1".to_string(), "ch2".to_string()];
        state.developer_mode = true;

        let json_val = state.to_json();
        let restored = GameState::from_json(&json_val);
        assert_eq!(restored.office_upgrades, state.office_upgrades);
        assert_eq!(restored.jingle_bonus, 25.0);
        assert_eq!(restored.unanswered_fan_mails, 4);
        assert!(restored.active_contract.is_some());
        assert_eq!(restored.soundcon_history, state.soundcon_history);
        assert_eq!(
            restored.tutorials_completed,
            vec!["ch1".to_string(), "ch2".to_string()]
        );
        assert!(restored.developer_mode);

        // Test legacy Python v3.x/v4.x save migration
        let legacy_raw = r#"{
            "company_name": "Legacy Python Studio",
            "money": 120000,
            "fans": 4500,
            "week": 1,
            "bought_platforms": ["PC (MS-DOS)"],
            "unlocked_features": [
                {"name": "16-Bit Stereo PCM", "category": "Sound", "cost": 25000, "tech_bonus": 15}
            ],
            "bank_loan": {"borrowed": 35000, "interest_rate": 0.01},
            "soundtrack_label": {"founded": true, "name": "Legacy OST Records"},
            "current_trend": {"topic": "Detektiv", "genre": "Abenteuer", "weeks_left": 10},
            "soundcon_last_year": 1995,
            "my_goty_wins": 3
        }"#;
        let legacy_parsed = parse_json(legacy_raw).expect("Should parse legacy Python save");
        let migrated = GameState::from_json(&legacy_parsed);
        assert_eq!(migrated.company_name, "Legacy Python Studio");
        assert_eq!(migrated.bank_loan, 35_000);
        assert!(migrated.label_active);
        assert_eq!(migrated.label_name, "Legacy OST Records");
        assert_eq!(migrated.trend_topic, "Detektiv");
        assert_eq!(migrated.trend_genre, "Abenteuer");
        assert_eq!(migrated.last_soundcon_year, 1995);
        assert_eq!(migrated.goty_awards, 3);
        assert_eq!(
            migrated.unlocked_features,
            vec!["16-Bit Stereo PCM".to_string()]
        );
        // Anachronistic 1930 "PC (MS-DOS)" from old Python saves must be migrated to "Radio-Sendernetz (AM)"
        assert_eq!(
            migrated.bought_platforms,
            vec!["Radio-Sendernetz (AM)".to_string()]
        );
    }

    #[test]
    fn test_escape_key_in_text_input_and_english_localization_completeness() {
        let mut state = GameState::new(1, 1996);
        let mut audio = AudioManager::new(true);
        let mut ctrl = MenuController::new(&state);

        // 1. Enter CompanyNameInput, type "Klang", verify Backspace deletes 1 char while Escape exits immediately
        ctrl.switch_to(MenuId::CompanyNameInput, &state, &audio);
        for ch in "Klang".chars() {
            ctrl.handle_input(KeyInput::Char(ch), &mut state, &mut audio);
        }
        assert_eq!(ctrl.text_buffer, "Klang");

        // Rapid F8 language toggle during text input must preserve text_buffer
        ctrl.handle_input(KeyInput::ToggleLang, &mut state, &mut audio);
        assert_eq!(state.lang(), Lang::En);
        assert_eq!(ctrl.text_buffer, "Klang");

        // Backspace deletes 'g', staying in CompanyNameInput
        ctrl.handle_input(KeyInput::Back, &mut state, &mut audio);
        assert_eq!(ctrl.current_menu, MenuId::CompanyNameInput);
        assert_eq!(ctrl.text_buffer, "Klan");

        // Escape cancels immediately back to DifficultyMenu even when text_buffer is non-empty
        ctrl.handle_input(KeyInput::Escape, &mut state, &mut audio);
        assert_eq!(ctrl.current_menu, MenuId::DifficultyMenu);

        // 2. Verify all 30 menus in English mode contain no leftover German UI labels
        assert_eq!(state.lang(), Lang::En);
        let forbidden_german_labels = [
            "Speicherplatz",
            "Hintergrundmusik",
            "Musik-Lautstärke",
            "Empfehlung für",
            "Entwickler-Menü",
        ];
        for &menu_id in ALL_MENU_IDS {
            ctrl.switch_to(menu_id, &state, &audio);
            for bad in forbidden_german_labels {
                assert!(
                    !ctrl.title.contains(bad),
                    "English title of {:?} still contains German string '{}': {}",
                    menu_id,
                    bad,
                    ctrl.title
                );
                for opt in &ctrl.options {
                    assert!(
                        !opt.text.contains(bad),
                        "English option of {:?} still contains German string '{}': {}",
                        menu_id,
                        bad,
                        opt.text
                    );
                }
            }
        }
    }

    #[test]
    fn test_tycoon_core_loop_sequels_publishers_audience_polish_and_post_mortem() {
        // 1. Target Audience Compatibility
        assert_eq!(get_audience_compatibility("Horrorhaus", "Horror", "Jeder"), 1);
        assert_eq!(
            get_audience_compatibility("Horrorhaus", "Horror", "Hardcore-Gamer"),
            3
        );
        assert_eq!(get_audience_compatibility("Freizeitpark", "Casual", "Jeder"), 3);
        assert_eq!(
            get_audience_compatibility("Freizeitpark", "Casual", "Hardcore-Gamer"),
            1
        );

        // 2. Publisher advance enables cash-strapped / slightly overdrawn studio to fund production
        let mut state = GameState::new(2, 1930);
        state.money = 10_000;
        // Unlicensed platform (Mechanischer Spielautomat = 8,000 EUR) + Small project (6,000 EUR) = 14,000 EUR > 10,000 EUR
        state.current_draft.platform = "Mechanischer Spielautomat".to_string();
        state.current_draft.publisher_idx = 0;
        assert!(
            state.start_game_project().is_err(),
            "Must reject unlicensed platform + dev cost exceeding cash before mutating state"
        );
        assert!(
            !state
                .bought_platforms
                .iter()
                .any(|p| p == "Mechanischer Spielautomat"),
            "Failed project start must not auto-buy platform license"
        );
        assert_eq!(state.money, 10_000);

        state.current_draft.platform = "Radio-Sendernetz (AM)".to_string();
        state.money = -1_000; // Overdrawn after monthly overhead; Small project costs 6,000 EUR
        state.current_draft.name = "Aether Detective".to_string();
        state.current_draft.topic = "Detektiv".to_string();
        state.current_draft.genre = "Abenteuer".to_string();
        state.current_draft.sliders = get_ideal_sliders("Abenteuer");
        state.current_draft.publisher_idx = 0; // Self-publishing -> should fail with -1,000 EUR
        assert!(state.start_game_project().is_err());

        // Sign with AetherWave Publishing (+8,000 EUR advance) -> net cash becomes -1,000 - 6,000 + 8,000 = 1,000 EUR
        state.current_draft.publisher_idx = 1;
        state
            .start_game_project()
            .expect("Publisher advance should rescue overdrawn studio and fund project");
        assert_eq!(state.money, 1_000);
        assert_eq!(state.active_projects[0].project.publisher_idx, 1);

        // 3. Mid-production creative studio decision & Pre-Release QA Polish
        state.money = 50_000;
        state.active_projects[0].bugs = 6;
        assert!(state.apply_studio_decision(0, 0).is_ok());
        assert!(
            state.apply_studio_decision(0, 1).is_err(),
            "Only one studio decision allowed per project"
        );
        assert!(state.polish_active_project(0).is_ok());
        assert_eq!(state.active_projects[0].bugs, 2);
        assert_eq!(state.active_projects[0].polish_passes, 1);

        for _ in 0..6 {
            state.tick_week();
        }
        state.active_projects[0].bugs = 0;
        let finished = state.finish_ready_project(0).expect("Should finish project");
        assert!(finished.review.unwrap().average() >= 7.0);

        // 4. Post-Mortem Game Report (once per released game, syncs last_finished_game too)
        let fans_before = state.fans;
        let rep_before = state.accessibility_reputation;
        assert!(state.analyze_post_mortem(0).is_ok());
        assert!(state.game_history[0].post_mortem_done);
        assert!(
            state
                .last_finished_game
                .as_ref()
                .map(|g| g.post_mortem_done)
                .unwrap_or(false),
            "last_finished_game must also mark post_mortem_done = true"
        );
        assert_eq!(state.fans, fans_before + 200);
        assert_eq!(state.accessibility_reputation, rep_before + 15);
        assert!(
            state.analyze_post_mortem(0).is_err(),
            "Post-Mortem must not be repeatable on the same game"
        );

        // 5. Sequel on an upgraded Custom Audio Engine + Save/Load Roundtrip
        state.money = 200_000;
        state.unlocked_features.push("Magnetband-Aufnahme".to_string());
        state
            .unlocked_features
            .push("Vakuum-Röhren-Verstärker".to_string());
        state.build_custom_engine("KlangEngine V2").unwrap();
        state.current_draft.sequel_of = Some("Aether Detective".to_string());
        state.current_draft.topic = "Detektiv".to_string();
        state.current_draft.genre = "Abenteuer".to_string();
        state.current_draft.sliders = get_ideal_sliders("Abenteuer");
        let hype_before = state.hype;
        state.start_game_project().expect("Should start sequel");
        assert_eq!(state.active_projects[0].project.name, "Aether Detective 2");
        assert_eq!(state.active_projects[0].project.sequel_number, 2);
        assert!(
            state.active_projects[0].project.quality_boost > 0.0,
            "Sequel on newer engine must receive positive quality boost"
        );
        assert!(state.hype > hype_before);

        // Verify JSON roundtrip preserves all new fields
        let json = state.to_json();
        let restored = GameState::from_json(&json);
        assert!(restored.game_history[0].post_mortem_done);
        assert_eq!(restored.game_history[0].publisher_idx, 1);
        assert_eq!(restored.active_projects[0].project.name, "Aether Detective 2");
        assert_eq!(restored.active_projects[0].project.sequel_number, 2);
        assert!(restored.active_projects[0].project.quality_boost > 0.0);
    }

    #[test]
    fn test_all_97_historical_year_events_1930_to_2026() {
        assert_eq!(
            HISTORICAL_YEAR_EVENTS.len(),
            97,
            "Must cover every single year from 1930 to 2026 (97 years)"
        );

        let forbidden = ["Ã¼", "Ã¶", "Ã¤", "ÃŸ", "Ã„", "Ã–", "Ãœ"];
        let mut titles_de = HashSet::new();
        let mut titles_en = HashSet::new();
        let mut descs_de = HashSet::new();
        let mut descs_en = HashSet::new();

        for year in 1930..=2026 {
            let ev = get_year_event(year);
            assert_eq!(ev.year, year);
            assert!(!ev.title_de.trim().is_empty(), "Empty title_de for {}", year);
            assert!(!ev.title_en.trim().is_empty(), "Empty title_en for {}", year);
            assert!(!ev.desc_de.trim().is_empty(), "Empty desc_de for {}", year);
            assert!(!ev.desc_en.trim().is_empty(), "Empty desc_en for {}", year);

            for bad in forbidden {
                assert!(!ev.title_de.contains(bad), "Mojibake in title_de {}", year);
                assert!(!ev.title_en.contains(bad), "Mojibake in title_en {}", year);
                assert!(!ev.desc_de.contains(bad), "Mojibake in desc_de {}", year);
                assert!(!ev.desc_en.contains(bad), "Mojibake in desc_en {}", year);
            }

            assert!(
                titles_de.insert(ev.title_de),
                "Duplicate title_de at year {}: {}",
                year,
                ev.title_de
            );
            assert!(
                titles_en.insert(ev.title_en),
                "Duplicate title_en at year {}: {}",
                year,
                ev.title_en
            );
            assert!(
                descs_de.insert(ev.desc_de),
                "Duplicate desc_de at year {}",
                year
            );
            assert!(
                descs_en.insert(ev.desc_en),
                "Duplicate desc_en at year {}",
                year
            );

            let topic = ev
                .trend_topic
                .unwrap_or_else(|| panic!("Missing trend_topic for {}", year));
            let topic_unlocked = START_TOPICS.contains(&topic)
                || RESEARCHABLE_TOPICS
                    .iter()
                    .any(|rt| rt.name == topic && rt.unlock_year <= year);
            assert!(
                topic_unlocked,
                "Year {} trend_topic '{}' is missing or locked in {}",
                year, topic, year
            );

            let genre = ev
                .trend_genre
                .unwrap_or_else(|| panic!("Missing trend_genre for {}", year));
            let genre_unlocked = START_GENRES.contains(&genre)
                || RESEARCHABLE_GENRES
                    .iter()
                    .any(|rg| rg.name == genre && rg.unlock_year <= year);
            assert!(
                genre_unlocked,
                "Year {} trend_genre '{}' is missing or locked in {}",
                year, genre, year
            );
        }

        // Verify fallback events outside 1930..=2026 are also well-formed
        for year in [1929u32, 2027u32, 2040u32] {
            let ev = get_year_event(year);
            assert_eq!(ev.year, year);
            assert!(!ev.title_de.is_empty() && !ev.title_en.is_empty());
            assert!(!ev.desc_de.is_empty() && !ev.desc_en.is_empty());
            let topic = ev.trend_topic.unwrap();
            let genre = ev.trend_genre.unwrap();
            assert!(START_TOPICS.contains(&topic));
            assert!(GENRES.contains(&genre));
        }
    }

    #[test]
    fn test_all_51_platforms_lifecycle_and_zero_softlock_invariant() {
        assert_eq!(PLATFORMS.len(), 51, "PLATFORMS must contain exactly 51 entries");

        let mut names = HashSet::new();
        for p in PLATFORMS {
            assert!(!p.name.is_empty());
            assert!(names.insert(p.name), "Duplicate platform name: {}", p.name);
            assert!(
                p.unlock_year <= p.end_year,
                "Platform '{}' has unlock_year {} > end_year {}",
                p.name,
                p.unlock_year,
                p.end_year
            );
            assert!(!p.category.is_empty());
            assert!(!p.audio_capabilities.is_empty());
            assert!(p.market_multi > 0.0);
        }

        // Every year 1930..=2050 (including 1930..=2035) must have >= 1 active platform and >= 1 free platform
        for year in 1930..=2050 {
            let active = get_available_platforms(year);
            assert!(
                !active.is_empty(),
                "Year {} must have at least 1 active platform",
                year
            );
            for p in &active {
                assert!(
                    year >= p.unlock_year && year <= p.end_year,
                    "Year {} returned fallback or inactive platform '{}'",
                    year,
                    p.name
                );
            }
            assert!(
                active.iter().any(|p| p.license_fee == 0),
                "Year {} must have at least 1 free (license_fee == 0) active platform",
                year
            );
        }

        // Helper checks: get_newly_unlocked_platforms, get_newly_retired_platforms, is_platform_active
        let unlocked_1930: Vec<&str> = get_newly_unlocked_platforms(1930)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(unlocked_1930.contains(&"Radio-Sendernetz (AM)"));
        assert!(unlocked_1930.contains(&"Schellack-Schallplatte (78 RPM)"));
        assert!(unlocked_1930.contains(&"Hand-Abakus"));

        let unlocked_1982: Vec<&str> = get_newly_unlocked_platforms(1982)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(unlocked_1982.contains(&"Commodore 64 (SID 6581)"));

        let unlocked_2026: Vec<&str> = get_newly_unlocked_platforms(2026)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(unlocked_2026.contains(&"Neural-Box 1 (BCI Audio)"));

        let retired_1958: Vec<&str> = get_newly_retired_platforms(1958)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(!retired_1958.contains(&"Radio-Sendernetz (AM)"));

        let retired_1959: Vec<&str> = get_newly_retired_platforms(1959)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(retired_1959.contains(&"Radio-Sendernetz (AM)"));

        let retired_1947: Vec<&str> = get_newly_retired_platforms(1947)
            .iter()
            .map(|p| p.name)
            .collect();
        assert!(retired_1947.contains(&"Zuse Z1"));

        assert!(is_platform_active("Radio-Sendernetz (AM)", 1930));
        assert!(is_platform_active("Radio-Sendernetz (AM)", 1958));
        assert!(!is_platform_active("Radio-Sendernetz (AM)", 1959));
        assert!(!is_platform_active("Commodore 64 (SID 6581)", 1981));
        assert!(is_platform_active("Commodore 64 (SID 6581)", 1982));
        assert!(is_platform_active("Commodore 64 (SID 6581)", 1994));
        assert!(!is_platform_active("Commodore 64 (SID 6581)", 1995));
        assert!(!is_platform_active("Unknown Platform", 2000));
    }

    #[test]
    fn test_retired_platform_draft_fallback_and_retro_niche_sales_factor() {
        // 1. Automatic fallback when current_draft.platform retires (1958 -> 1959)
        let mut state = GameState::new(1, 1958);
        assert_eq!(state.current_draft.platform, "Radio-Sendernetz (AM)");
        assert!(state
            .bought_platforms
            .iter()
            .any(|p| p == "UKW-Transistorradio (FM)"));

        let mut year_notes = Vec::new();
        for _ in 0..WEEKS_PER_YEAR {
            year_notes.extend(state.tick_week());
        }
        assert_eq!(state.calendar_year(), 1959);
        assert_ne!(state.current_draft.platform, "Radio-Sendernetz (AM)");
        assert_eq!(state.current_draft.platform, "UKW-Transistorradio (FM)");
        assert!(is_platform_active(&state.current_draft.platform, 1959));
        assert!(
            year_notes
                .iter()
                .any(|n| n.contains("Radio-Sendernetz (AM)")
                    && n.contains("UKW-Transistorradio (FM)")),
            "Year transition notifications must announce draft platform switch: {:?}",
            year_notes
        );
        assert!(state.emails[0].body.contains("Radio-Sendernetz (AM)"));

        // Verify EN switch message and custom console preservation
        let mut en_state = GameState::new(1, 1958);
        en_state.settings.language = "en".to_string();
        en_state.apply_year_event(1959);
        assert_eq!(en_state.current_draft.platform, "UKW-Transistorradio (FM)");
        assert!(en_state.emails[0]
            .body
            .contains("Draft platform 'Radio-Sendernetz (AM)' retired; automatically switched to 'UKW-Transistorradio (FM)'"));

        let mut custom_state = GameState::new(0, 1985);
        custom_state.money = 500_000;
        custom_state.develop_console("SonicCustom 85").unwrap();
        custom_state.current_draft.platform = "SonicCustom 85".to_string();
        custom_state.apply_year_event(1986);
        assert_eq!(
            custom_state.current_draft.platform, "SonicCustom 85",
            "Custom console must never be overwritten by standard retirement fallback"
        );

        // 2. Retro-niche 0.55x market factor on retired standard platforms
        let mut market_state = GameState::new(1, 1958);
        market_state.fans = 10_000;
        market_state.hype = 60.0;
        market_state.sales_multiplier = 1.0;

        let retro_proj = GameProject {
            name: "Äther Klassiker".to_string(),
            topic: "Radio-Drama".to_string(),
            genre: "Abenteuer".to_string(),
            sub_genre: "Klassisch".to_string(),
            platform: "Radio-Sendernetz (AM)".to_string(),
            audience: "Jeder".to_string(),
            size: "Groß".to_string(),
            marketing: "Kein Marketing".to_string(),
            engine_name: "Basis-Tonstudio V1".to_string(),
            sliders: get_ideal_sliders("Abenteuer"),
            review: Some(ReviewScore::new([8, 8, 8, 8], vec![])),
            sales: 0,
            revenue: 0,
            dev_cost: 55_000,
            release_week: 1,
            release_year: 1958,
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
            quality_boost: 0.0,
        };
        let mut active_control_proj = retro_proj.clone();
        active_control_proj.platform = "UKW-Transistorradio (FM)".to_string();

        let (units_1958, rev_1958) = market_state.compute_weekly_game_sales(&retro_proj, true);
        let (fm_1958, _) = market_state.compute_weekly_game_sales(&active_control_proj, true);

        // Move state to 1959 week 1 without altering fans/hype/sales_multiplier
        market_state.week = (1959 - START_YEAR) * WEEKS_PER_YEAR + 1;
        let (units_1959, rev_1959) = market_state.compute_weekly_game_sales(&retro_proj, true);
        let (fm_1959, _) = market_state.compute_weekly_game_sales(&active_control_proj, true);

        assert_eq!(
            fm_1959, fm_1958,
            "Active platform sales must remain identical across 1958->1959"
        );
        assert!(units_1959 < units_1958);
        assert!(rev_1959 < rev_1958);
        let ratio = units_1959 as f64 / units_1958 as f64;
        assert!(
            (0.53..=0.57).contains(&ratio),
            "Retired platform should apply 0.55x retro-niche factor (got ratio {:.4}: {} / {})",
            ratio,
            units_1959,
            units_1958
        );
    }

    #[test]
    fn test_custom_engine_third_party_licensing_and_weekly_royalties() {
        let mut state = GameState::new(1, 1985);
        state.money = 200_000;

        // Starter engine (idx 0) and invalid indices must be rejected in both DE and EN
        assert!(state.toggle_engine_license(0).is_err());
        assert!(state.toggle_engine_license(99).is_err());
        state.settings.language = "en".to_string();
        assert!(state
            .toggle_engine_license(0)
            .unwrap_err()
            .contains("starter engine"));
        assert!(state.toggle_engine_license(42).is_err());
        state.settings.language = "de".to_string();

        // Build custom engine (idx 1)
        state.build_custom_engine("SonicForge V2").unwrap();
        assert_eq!(state.engines.len(), 2);
        assert!(!state.engines[1].licensed_out);
        let expected_royalty = (state.engines[1].tech_level as i64) * 350;
        assert!(expected_royalty > 0);

        let on_msg = state.toggle_engine_license(1).unwrap();
        assert!(state.engines[1].licensed_out);
        assert!(on_msg.contains("SonicForge V2"));
        assert!(on_msg.contains(&expected_royalty.to_string()));

        // Tick week 1 -> week 2 (same month_index 0, no monthly expenses, no other passive sources)
        let money_before = state.money;
        let rev_before = state.total_revenue;
        state.tick_week();
        assert_eq!(
            state.money,
            money_before + expected_royalty,
            "Licensed custom engine must pay tech_level * 350 EUR/week"
        );
        assert_eq!(state.total_revenue, rev_before + expected_royalty);

        // Save/Load roundtrip preserves licensed_out = true
        let temp_path = Path::new("save_slot_97.json");
        state.save_to_file(temp_path).expect("Should save engine state");
        let restored = GameState::load_from_file(temp_path).expect("Should load engine state");
        let _ = fs::remove_file(temp_path);
        assert!(restored.engines[1].licensed_out);

        // Pause licensing -> next week pays 0 engine royalties
        state.settings.language = "en".to_string();
        let off_msg = state.toggle_engine_license(1).unwrap();
        assert!(!state.engines[1].licensed_out);
        assert!(off_msg.contains("paused"));

        let money_after_pause = state.money;
        let rev_after_pause = state.total_revenue;
        state.tick_week(); // week 2 -> week 3 (still month_index 0)
        assert_eq!(state.money, money_after_pause);
        assert_eq!(state.total_revenue, rev_after_pause);
    }

    #[test]
    fn test_annual_best_audio_design_award_golden_microphone() {
        // 1. Ineligible: low Sound slider (< 7) even with high score
        let mut low_sound_state = GameState::new(1, 1995);
        low_sound_state.game_history.push(GameProject {
            name: "Silent Tactics".to_string(),
            topic: "Schach".to_string(),
            genre: "Strategie".to_string(),
            sub_genre: "Klassisch".to_string(),
            platform: "PC (MS-DOS / Soundkarte)".to_string(),
            audience: "Hardcore-Gamer".to_string(),
            size: "Mittel".to_string(),
            marketing: "Kein Marketing".to_string(),
            engine_name: "Basis-Tonstudio V1".to_string(),
            sliders: [9, 4, 6, 3, 6, 2], // Sound = 6 (< 7)
            review: Some(ReviewScore::new([9, 9, 9, 9], vec![])),
            sales: 1000,
            revenue: 25_000,
            dev_cost: 18_000,
            release_week: 10,
            release_year: 1995,
            weeks_on_market: 10,
            is_active: false,
            bugs: 0,
            patches_released: 0,
            dlc_count: 0,
            in_soundtrack_label: false,
            in_subscription_vault: false,
            sequel_number: 0,
            publisher_idx: 0,
            post_mortem_done: false,
            quality_boost: 0.0,
        });
        assert!(low_sound_state.evaluate_annual_audio_award(1995).is_none());
        assert_eq!(low_sound_state.audio_awards, 0);

        // 2. Ineligible: Sound >= 7, but review score < 7.5
        let mut low_score_state = low_sound_state.clone();
        low_score_state.game_history[0].sliders = [5, 5, 9, 6, 2, 3];
        low_score_state.game_history[0].review = Some(ReviewScore::new([7, 7, 7, 8], vec![])); // avg 7.25 < 7.5
        assert!(low_score_state.evaluate_annual_audio_award(1995).is_none());
        assert_eq!(low_score_state.audio_awards, 0);

        // 3. Eligible: Sound >= 7 AND review avg >= 7.5 via full tick_week() year transition (DE)
        let mut state = GameState::new(1, 1995);
        state.money = 200_000;
        state.fans = 500;
        state.hype = 20.0;
        state.rivals[3].reputation = 8.5; // Rival score 8.8 > 8.0 so only Audio Award triggers
        state.game_history.push(GameProject {
            name: "Echoes of Darkness".to_string(),
            topic: "Horrorhaus".to_string(),
            genre: "Horror".to_string(),
            sub_genre: "Klassisch".to_string(),
            platform: "PC (MS-DOS / Soundkarte)".to_string(),
            audience: "Hardcore-Gamer".to_string(),
            size: "Mittel".to_string(),
            marketing: "Kein Marketing".to_string(),
            engine_name: "Basis-Tonstudio V1".to_string(),
            sliders: [5, 5, 9, 6, 2, 3], // Sound = 9 (>= 7)
            review: Some(ReviewScore::new([8, 8, 8, 8], vec![])), // avg = 8.0 (>= 7.5)
            sales: 1000,
            revenue: 25_000,
            dev_cost: 18_000,
            release_week: 10,
            release_year: 1995,
            weeks_on_market: 24,
            is_active: false, // Isolate year-end award payout from weekly sales
            bugs: 0,
            patches_released: 0,
            dlc_count: 0,
            in_soundtrack_label: false,
            in_subscription_vault: false,
            sequel_number: 0,
            publisher_idx: 0,
            post_mortem_done: false,
            quality_boost: 0.0,
        });

        // Advance to week 48 of 1995, then cross into 1996
        state.week = (1995 - START_YEAR) * WEEKS_PER_YEAR + WEEKS_PER_YEAR;
        let hype_before_transition = (state.hype - 1.5).max(0.0); // week decay
        let money_before = state.money;
        let fans_before = state.fans;
        let notes = state.tick_week();

        assert_eq!(state.calendar_year(), 1996);
        assert_eq!(state.goty_awards, 0);
        assert_eq!(state.audio_awards, 1);
        // Monthly rent in Garage is 200 EUR, award prize is +15,000 EUR
        assert_eq!(state.money, money_before - 200 + 15_000);
        assert_eq!(state.fans, fans_before + 400);
        assert!((state.hype - (hype_before_transition + 26.0 + 15.0)).abs() < 1e-6);
        assert!(
            notes
                .iter()
                .any(|n| n.contains("Goldenes Mikrofon") && n.contains("Echoes of Darkness")),
            "Notifications must announce Goldenes Mikrofon: {:?}",
            notes
        );
        assert!(state
            .emails
            .iter()
            .any(|e| e.subject.contains("Goldenes Mikrofon") && e.body.contains("Echoes of Darkness")));

        // 4. Verify English notification & JSON roundtrip
        let mut en_state = GameState::new(1, 1996);
        en_state.settings.language = "en".to_string();
        en_state.game_history = state.game_history.clone();
        en_state.game_history[0].release_year = 1996;
        let en_msg = en_state
            .evaluate_annual_audio_award(1996)
            .expect("Should award Golden Microphone in EN");
        assert!(en_msg.contains("Golden Microphone (Best Audio Design 1996)"));
        assert_eq!(en_state.audio_awards, 1);

        let restored = GameState::from_json(&en_state.to_json());
        assert_eq!(restored.audio_awards, 1);
    }

    #[test]
    fn test_full_multi_decade_timeline_progression_1930_to_2026() {
        let mut state = GameState::new(0, 1930);
        assert_eq!(state.calendar_year(), 1930);
        assert_eq!(state.current_era().id, "era_radio");
        assert_eq!(state.event_log.len(), 1);

        let mut saw_1975 = false;
        let mut saw_1985 = false;
        let mut saw_1995 = false;
        let mut saw_2026 = false;

        for expected_year in 1931..=2026 {
            let mut year_notes = Vec::new();
            for _ in 0..WEEKS_PER_YEAR {
                year_notes.extend(state.tick_week());
            }
            assert_eq!(state.calendar_year(), expected_year);

            let expected_era_id = match expected_year {
                1930..=1949 => "era_radio",
                1950..=1969 => "era_tape",
                1970..=1979 => "era_arcade",
                1980..=1989 => "era_8bit",
                1990..=1999 => "era_multimedia",
                2000..=2014 => "era_digital",
                _ => "era_spatial",
            };
            assert_eq!(
                state.current_era().id,
                expected_era_id,
                "Wrong era at year {}",
                expected_year
            );

            assert!(
                is_platform_active(&state.current_draft.platform, expected_year),
                "Draft platform '{}' must remain active in {}",
                state.current_draft.platform,
                expected_year
            );
            assert!(
                state
                    .bought_platforms
                    .iter()
                    .any(|bp| is_platform_active(bp, expected_year)),
                "Studio must always own at least one active platform in {}",
                expected_year
            );

            if expected_year == 1975 {
                saw_1975 = year_notes.iter().any(|n| n.contains("Hardware-Labor"));
            }
            if expected_year == 1985 {
                saw_1985 = year_notes.iter().any(|n| n.contains("Soundtrack-Label"));
            }
            if expected_year == 1995 {
                saw_1995 = year_notes.iter().any(|n| n.contains("SoundCon"));
            }
            if expected_year == 2026 {
                saw_2026 = year_notes.iter().any(|n| n.contains("Endlosmodus"));
            }
        }

        assert!(saw_1975, "Missing 1975 Hardware-Labor milestone notification");
        assert!(saw_1985, "Missing 1985 Soundtrack-Label milestone notification");
        assert!(saw_1995, "Missing 1995 SoundCon milestone notification");
        assert!(saw_2026, "Missing 2026 Endless Mode milestone notification");
        assert_eq!(state.event_log.len(), 97);
        assert_eq!(state.trend_topic, "Neural-Link");
        assert_eq!(state.trend_genre, "RPG");

        // Advance into Endless Mode (2027..=2030) and confirm era stays at era_spatial
        for yr in 2027..=2030 {
            for _ in 0..WEEKS_PER_YEAR {
                state.tick_week();
            }
            assert_eq!(state.calendar_year(), yr);
            assert_eq!(state.current_era().id, "era_spatial");
            assert!(is_platform_active(&state.current_draft.platform, yr));
        }
    }

    #[test]
    fn test_new_menus_and_i18n_symmetry_for_timeline_platforms_and_licensing() {
        // 1. Verify all new i18n keys exist in both DE and EN with clean non-empty text
        let de = build_dictionary(Lang::De);
        let en = build_dictionary(Lang::En);
        let new_keys = [
            "menu_main_menu_return",
            "platform_licensed",
            "platform_retro_retired",
            "platform_market_label",
            "platform_custom_console",
            "engine_status_licensed",
            "engine_status_private",
            "engine_starter_label",
            "timeline_chronicle_title",
            "timeline_active_platforms",
            "timeline_milestones_prefix",
            "timeline_no_events",
            "audio_awards_label",
        ];
        for key in new_keys {
            let de_val = de.get(key).unwrap_or_else(|| panic!("Missing DE key: {}", key));
            let en_val = en.get(key).unwrap_or_else(|| panic!("Missing EN key: {}", key));
            assert!(!de_val.trim().is_empty());
            assert!(!en_val.trim().is_empty());
        }

        // 2. DevelopPlatformMenu in 1985: era windows, category, audio capabilities & retired retro tag
        let mut state = GameState::new(1, 1985);
        state.money = 250_000;
        // Simulate a legacy licensed platform retired in 1958
        state
            .bought_platforms
            .push("Radio-Sendernetz (AM)".to_string());
        let mut audio = AudioManager::new(true);
        let mut ctrl = MenuController::new(&state);

        ctrl.switch_to(MenuId::DevelopPlatformMenu, &state, &audio);
        let amiga_de = ctrl
            .options
            .iter()
            .find(|o| o.text.contains("Commodore Amiga (Paula)"))
            .expect("Amiga must appear in 1985 DevelopPlatformMenu");
        assert!(amiga_de.text.contains("Heimcomputer | 1985–1996"));
        assert!(amiga_de.text.contains("4-Kanal 8-Bit PCM Hardware-MOD-Tracker"));

        let retro_de = ctrl
            .options
            .iter()
            .find(|o| o.text.contains("Radio-Sendernetz (AM)"))
            .expect("Owned legacy platform must appear with retro tag");
        assert!(retro_de.text.contains("Retro / Eingestellt (0,55x Markt)"));

        // 3. ResearchMenu: starter engine (NoOp) vs custom engine ToggleEngineLicense(1)
        state.build_custom_engine("KlangMaster 85").unwrap();
        ctrl.switch_to(MenuId::ResearchMenu, &state, &audio);
        let starter_opt = ctrl
            .options
            .iter()
            .find(|o| o.text.contains("Basis-Tonstudio V1"))
            .expect("Starter engine option missing");
        assert!(matches!(starter_opt.action, MenuAction::NoOp));
        assert!(starter_opt.text.contains("Basis-Engine (Nicht lizenzierbar)"));

        let custom_idx = ctrl
            .options
            .iter()
            .position(|o| matches!(o.action, MenuAction::ToggleEngineLicense(1)))
            .expect("Custom engine license toggle option missing");
        assert!(ctrl.options[custom_idx].text.contains("[Privat]"));
        assert!(ctrl.options[custom_idx].text.contains("EUR/Woche"));

        ctrl.current_index = custom_idx;
        ctrl.handle_input(KeyInput::Enter, &mut state, &mut audio);
        assert!(state.engines[1].licensed_out);
        assert!(ctrl.options[custom_idx].text.contains("[Lizenziert]"));

        // 4. ChartsGotyMenu: audio_awards in title + Timeline & Era Chronicle in DE and EN
        state.audio_awards = 2;
        ctrl.switch_to(MenuId::ChartsGotyMenu, &state, &audio);
        assert!(ctrl.title.contains("Audio-Preise: 2"));
        assert!(ctrl
            .options
            .iter()
            .any(|o| o.text.contains("Zeitstrahl & Epochen-Chronik (1930–2026)")));
        assert!(ctrl
            .options
            .iter()
            .any(|o| o.text.contains(&format!("/{}", PLATFORMS.len()))));
        assert!(ctrl
            .options
            .iter()
            .any(|o| o.text.contains("1975 Hardware-Labor [Frei]")
                && o.text.contains("1985 Soundtrack-Label [Frei]")
                && o.text.contains("1995 SoundCon & AudioPass [Gesperrt]")));

        // Verify EN rendering of all 3 updated menus on an EN state
        let mut en_state = GameState::new(1, 1985);
        en_state.settings.language = "en".to_string();
        en_state.money = 250_000;
        en_state
            .bought_platforms
            .push("Radio-Sendernetz (AM)".to_string());
        en_state.build_custom_engine("KlangMaster EN").unwrap();
        en_state.audio_awards = 3;
        en_state.apply_year_event(1986);

        let mut en_ctrl = MenuController::new(&en_state);
        en_ctrl.switch_to(MenuId::DevelopPlatformMenu, &en_state, &audio);
        let amiga_en = en_ctrl
            .options
            .iter()
            .find(|o| o.text.contains("Commodore Amiga (Paula)"))
            .unwrap();
        assert!(amiga_en.text.contains("Home Computer | 1985–1996"));
        let retro_en = en_ctrl
            .options
            .iter()
            .find(|o| o.text.contains("Radio-Sendernetz (AM)"))
            .unwrap();
        assert!(retro_en.text.contains("Retro / Retired (0.55x Market)"));

        en_ctrl.switch_to(MenuId::ResearchMenu, &en_state, &audio);
        assert!(en_ctrl
            .options
            .iter()
            .any(|o| o.text.contains("Starter Engine (Non-licensable)")));
        assert!(en_ctrl
            .options
            .iter()
            .any(|o| o.text.contains("[Private]") && o.text.contains("EUR/week")));

        en_ctrl.switch_to(MenuId::ChartsGotyMenu, &en_state, &audio);
        assert!(en_ctrl.title.contains("Audio Awards: 3"));
        assert!(en_ctrl
            .options
            .iter()
            .any(|o| o.text.contains("Timeline & Era Chronicle (1930–2026)")));
        assert!(en_ctrl
            .options
            .iter()
            .any(|o| o.text.contains("1975 Hardware Lab [Unlocked]")
                && o.text.contains("1995 SoundCon & AudioPass [Locked]")));
        for opt in &en_ctrl.options {
            for bad_de in [
                "Aktive Plattformen",
                "Meilensteine:",
                "Aktuelle Ära:",
                "[Chronik]",
                "[Frei]",
                "[Gesperrt]",
            ] {
                assert!(
                    !opt.text.contains(bad_de),
                    "EN ChartsGotyMenu leaked German string '{}': {}",
                    bad_de,
                    opt.text
                );
            }
        }
    }

    #[test]
    fn test_custom_console_menu_display_and_legacy_save_defaults() {
        let mut state = GameState::new(0, 1985);
        state.money = 500_000;
        state.develop_console("AetherStation 85").unwrap();

        let audio = AudioManager::new(true);
        let mut ctrl = MenuController::new(&state);
        ctrl.switch_to(MenuId::DevelopPlatformMenu, &state, &audio);
        assert!(ctrl
            .options
            .iter()
            .any(|o| o.text.contains("AetherStation 85") && o.text.contains("Eigene Konsole | 1985+")));

        state.settings.language = "en".to_string();
        ctrl.switch_to(MenuId::DevelopPlatformMenu, &state, &audio);
        assert!(ctrl
            .options
            .iter()
            .any(|o| o.text.contains("AetherStation 85") && o.text.contains("Custom Console | 1985+")));

        // Legacy save missing audio_awards & licensed_out must deserialize cleanly with safe defaults
        let legacy = parse_json(
            r#"{
                "company_name": "Old Save",
                "week": 1,
                "engines": [{"name": "Basis-Tonstudio V1", "tech_level": 1}]
            }"#,
        )
        .unwrap();
        let loaded = GameState::from_json(&legacy);
        assert_eq!(loaded.audio_awards, 0);
        assert!(!loaded.engines[0].licensed_out);
    }
}
