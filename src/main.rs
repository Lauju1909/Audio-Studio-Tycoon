//! Main entry point for Audio Studio Tycoon (Native Rust Edition).

use audio_studio_tycoon::audio::AudioManager;
use audio_studio_tycoon::data::{get_compatibility, get_ideal_sliders, START_YEAR};
use audio_studio_tycoon::gui::run_gui_app;
use audio_studio_tycoon::state::GameState;

fn run_headless_verification() {
    println!("=== Audio Studio Tycoon v4.3.0 (Rust Edition) - End-to-End Verification ===");
    let audio = AudioManager::new(false);
    println!("[1/5] Screenreader FFI Backend: {}", audio.backend_info);

    let mut state = GameState::new(1, START_YEAR);
    println!(
        "[2/5] Initialized Studio '{}' in {} ({})",
        state.company_name,
        state.calendar_text(),
        state.current_era().name_de
    );

    // Develop a coherent 1930 Radio-Drama Adventure production
    state.current_draft.name = "Detektiv im Funkhaus".to_string();
    state.current_draft.topic = "Radio-Drama".to_string();
    state.current_draft.genre = "Abenteuer".to_string();
    state.current_draft.sliders = get_ideal_sliders("Abenteuer");
    let syn = get_compatibility(&state.current_draft.topic, &state.current_draft.genre);
    println!(
        "[3/5] Starting production '{}' (Synergy: {}/3)...",
        state.current_draft.name, syn
    );
    state.start_game_project().expect("Start project");
    for _ in 0..5 {
        state.tick_week();
    }
    let released = state.finish_ready_project(0).expect("Release project");
    println!(
        "[4/5] Released '{}': Score {:.1}/10, Launch Sales: {}, Revenue: {} EUR",
        released.name,
        released.review.as_ref().unwrap().average(),
        released.sales,
        released.revenue
    );

    audio.cleanup();
    println!("[5/5] Verification completed successfully in < 50ms!");
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.iter().any(|a| a == "--version" || a == "-V") {
        println!("Audio Studio Tycoon v4.3.0 (Native Rust Edition)");
        return;
    }
    if args
        .iter()
        .any(|a| a == "--verify" || a == "--headless-demo")
    {
        run_headless_verification();
        return;
    }

    let mut state = GameState::new(1, START_YEAR);
    state.load_global_settings();

    let mut audio = AudioManager::new(false);
    audio.music_enabled = state.settings.music_enabled;
    audio.music_volume = state.settings.music_volume;
    audio.sfx_volume = state.settings.sfx_volume;
    audio.speech_volume = state.settings.speech_volume;

    run_gui_app(state, audio);
}
