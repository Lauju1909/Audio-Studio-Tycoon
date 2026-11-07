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
    use crate::menus::{KeyInput, MenuController, MenuId, ALL_MENU_IDS};
    use crate::state::GameState;
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
}
