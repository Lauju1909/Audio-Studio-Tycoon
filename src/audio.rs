//! Screenreader (Prism 64-bit FFI, Tolk FFI, SAPI/Console fallback) and Audio/SFX Engine.
//! Strictly adheres to `lessons_learned.md`:
//! - Explicit 64-bit pointer signatures (`*mut c_void`, `u64`, `usize`).
//! - NEVER calls `prism_backend_is_speaking` or `prism_backend_get_volume` (avoids OneCore null-vtable crash).
//! - Clean shutdown cascade: `prism_backend_stop` -> `prism_backend_free` -> `prism_shutdown`.

use std::ffi::{c_char, c_int, c_void, CStr, CString};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::mpsc::{self, Sender};
use std::sync::{Arc, Mutex};
use std::thread;

#[cfg(windows)]
#[link(name = "kernel32")]
extern "system" {
    fn LoadLibraryW(lpLibFileName: *const u16) -> *mut c_void;
    fn GetProcAddress(hModule: *mut c_void, lpProcName: *const c_char) -> *mut c_void;
    fn FreeLibrary(hLibModule: *mut c_void) -> c_int;
}

#[cfg(windows)]
#[link(name = "winmm")]
extern "system" {
    fn PlaySoundW(pszSound: *const u16, hmod: *mut c_void, fdwSound: u32) -> c_int;
    fn mciSendStringW(
        lpszCommand: *const u16,
        lpszReturnString: *mut u16,
        cchReturn: u32,
        hwndCallback: *mut c_void,
    ) -> u32;
}

#[cfg(windows)]
const SND_ASYNC: u32 = 0x0001;
#[cfg(windows)]
const SND_NODEFAULT: u32 = 0x0002;
#[cfg(windows)]
const SND_FILENAME: u32 = 0x00020000;

type PrismInitFn = unsafe extern "C" fn(*const c_void) -> *mut c_void;
type PrismShutdownFn = unsafe extern "C" fn(*mut c_void);
type PrismRegistryCreateBestFn = unsafe extern "C" fn(*mut c_void) -> *mut c_void;
type PrismBackendNameFn = unsafe extern "C" fn(*mut c_void) -> *const c_char;
type PrismBackendInitializeFn = unsafe extern "C" fn(*mut c_void) -> c_int;
type PrismBackendSpeakFn = unsafe extern "C" fn(*mut c_void, *const c_char, bool) -> c_int;
type PrismBackendStopFn = unsafe extern "C" fn(*mut c_void) -> c_int;
type PrismBackendBrailleFn = unsafe extern "C" fn(*mut c_void, *const c_char) -> c_int;
type PrismBackendFreeFn = unsafe extern "C" fn(*mut c_void);

type TolkLoadFn = unsafe extern "C" fn();
type TolkIsLoadedFn = unsafe extern "C" fn() -> bool;
type TolkTrySapiFn = unsafe extern "C" fn(bool);
type TolkOutputFn = unsafe extern "C" fn(*const u16, bool) -> bool;
type TolkSilenceFn = unsafe extern "C" fn() -> bool;
type TolkUnloadFn = unsafe extern "C" fn();

enum SpeechCommand {
    Speak { text: String, interrupt: bool },
    Stop,
    Shutdown,
}

pub struct PrismBindings {
    pub handle: *mut c_void,
    pub ctx: *mut c_void,
    pub backend: *mut c_void,
    pub backend_name: String,
    pub prism_shutdown: PrismShutdownFn,
    pub prism_backend_speak: PrismBackendSpeakFn,
    pub prism_backend_stop: PrismBackendStopFn,
    pub prism_backend_braille: Option<PrismBackendBrailleFn>,
    pub prism_backend_free: PrismBackendFreeFn,
}

unsafe impl Send for PrismBindings {}

pub struct TolkBindings {
    pub handle: *mut c_void,
    pub tolk_output: TolkOutputFn,
    pub tolk_silence: TolkSilenceFn,
    pub tolk_unload: TolkUnloadFn,
}

unsafe impl Send for TolkBindings {}

#[derive(Clone)]
pub struct AudioManager {
    tx: Option<Sender<SpeechCommand>>,
    pub headless: bool,
    pub music_enabled: bool,
    pub music_volume: u8,
    pub sfx_volume: u8,
    pub speech_volume: u8,
    pub backend_info: String,
    pub speech_log: Arc<Mutex<Vec<String>>>,
    pub sound_log: Arc<Mutex<Vec<String>>>,
    assets_dir: PathBuf,
}

fn to_wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

fn find_file_in_paths(filename: &str) -> Option<PathBuf> {
    let mut candidates = Vec::new();
    if let Ok(cwd) = std::env::current_dir() {
        candidates.push(cwd.join(filename));
    }
    if let Ok(exe) = std::env::current_exe() {
        if let Some(dir) = exe.parent() {
            candidates.push(dir.join(filename));
            if let Some(parent) = dir.parent() {
                candidates.push(parent.join(filename));
                if let Some(grand) = parent.parent() {
                    candidates.push(grand.join(filename));
                }
            }
        }
    }
    for p in candidates {
        if p.exists() {
            return Some(p);
        }
    }
    None
}

#[cfg(windows)]
unsafe fn get_proc(module: *mut c_void, name: &str) -> Option<*mut c_void> {
    let c_name = CString::new(name).ok()?;
    let ptr = GetProcAddress(module, c_name.as_ptr());
    if ptr.is_null() {
        None
    } else {
        Some(ptr)
    }
}

#[cfg(windows)]
unsafe fn try_init_prism() -> Option<PrismBindings> {
    let dll_path = find_file_in_paths("prism.dll")?;
    let wide = to_wide(&dll_path.to_string_lossy());
    let handle = LoadLibraryW(wide.as_ptr());
    if handle.is_null() {
        return None;
    }

    let prism_init: PrismInitFn = std::mem::transmute(get_proc(handle, "prism_init")?);
    let prism_shutdown: PrismShutdownFn = std::mem::transmute(get_proc(handle, "prism_shutdown")?);
    let prism_registry_create_best: PrismRegistryCreateBestFn =
        std::mem::transmute(get_proc(handle, "prism_registry_create_best")?);
    let prism_backend_name: PrismBackendNameFn =
        std::mem::transmute(get_proc(handle, "prism_backend_name")?);
    let prism_backend_initialize: PrismBackendInitializeFn =
        std::mem::transmute(get_proc(handle, "prism_backend_initialize")?);
    let prism_backend_speak: PrismBackendSpeakFn =
        std::mem::transmute(get_proc(handle, "prism_backend_speak")?);
    let prism_backend_stop: PrismBackendStopFn =
        std::mem::transmute(get_proc(handle, "prism_backend_stop")?);
    let prism_backend_braille: Option<PrismBackendBrailleFn> =
        get_proc(handle, "prism_backend_braille").map(|p| std::mem::transmute(p));
    let prism_backend_free: PrismBackendFreeFn =
        std::mem::transmute(get_proc(handle, "prism_backend_free")?);

    let ctx = prism_init(std::ptr::null());
    if ctx.is_null() {
        FreeLibrary(handle);
        return None;
    }

    let backend = prism_registry_create_best(ctx);
    if backend.is_null() {
        prism_shutdown(ctx);
        FreeLibrary(handle);
        return None;
    }

    prism_backend_initialize(backend);
    let name_ptr = prism_backend_name(backend);
    let backend_name = if !name_ptr.is_null() {
        CStr::from_ptr(name_ptr).to_string_lossy().into_owned()
    } else {
        "Prism-Standard".to_string()
    };

    Some(PrismBindings {
        handle,
        ctx,
        backend,
        backend_name,
        prism_shutdown,
        prism_backend_speak,
        prism_backend_stop,
        prism_backend_braille,
        prism_backend_free,
    })
}

#[cfg(windows)]
unsafe fn try_init_tolk() -> Option<TolkBindings> {
    let dll_path = find_file_in_paths("Tolk.dll")?;
    let wide = to_wide(&dll_path.to_string_lossy());
    let handle = LoadLibraryW(wide.as_ptr());
    if handle.is_null() {
        return None;
    }

    let tolk_load: TolkLoadFn = std::mem::transmute(get_proc(handle, "Tolk_Load")?);
    let tolk_is_loaded: TolkIsLoadedFn = std::mem::transmute(get_proc(handle, "Tolk_IsLoaded")?);
    let tolk_try_sapi: TolkTrySapiFn = std::mem::transmute(get_proc(handle, "Tolk_TrySAPI")?);
    let tolk_output: TolkOutputFn = std::mem::transmute(get_proc(handle, "Tolk_Output")?);
    let tolk_silence: TolkSilenceFn = std::mem::transmute(get_proc(handle, "Tolk_Silence")?);
    let tolk_unload: TolkUnloadFn = std::mem::transmute(get_proc(handle, "Tolk_Unload")?);

    tolk_load();
    if !tolk_is_loaded() {
        FreeLibrary(handle);
        return None;
    }
    tolk_try_sapi(true);

    Some(TolkBindings {
        handle,
        tolk_output,
        tolk_silence,
        tolk_unload,
    })
}

/// Generates a clean 16-bit 44.1kHz mono WAV file on disk if missing so all earcons work via WinMM.
fn ensure_synthesized_wav(path: &Path, freqs: &[(f64, u32)]) {
    if path.exists() {
        return;
    }
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let sample_rate = 44100u32;
    let mut samples: Vec<i16> = Vec::new();
    for &(freq, duration_ms) in freqs {
        let num_samples = (sample_rate * duration_ms) / 1000;
        for i in 0..num_samples {
            let t = i as f64 / sample_rate as f64;
            let env = 1.0 - (i as f64 / num_samples.max(1) as f64);
            let s = (2.0 * std::f64::consts::PI * freq * t).sin() * env * 12000.0;
            samples.push(s as i16);
        }
    }

    let data_bytes = (samples.len() * 2) as u32;
    let file_size = 36 + data_bytes;
    let mut bytes = Vec::with_capacity(file_size as usize + 8);
    bytes.extend_from_slice(b"RIFF");
    bytes.extend_from_slice(&file_size.to_le_bytes());
    bytes.extend_from_slice(b"WAVEfmt ");
    bytes.extend_from_slice(&16u32.to_le_bytes());
    bytes.extend_from_slice(&1u16.to_le_bytes()); // PCM
    bytes.extend_from_slice(&1u16.to_le_bytes()); // 1 channel
    bytes.extend_from_slice(&sample_rate.to_le_bytes());
    bytes.extend_from_slice(&(sample_rate * 2).to_le_bytes());
    bytes.extend_from_slice(&2u16.to_le_bytes());
    bytes.extend_from_slice(&16u16.to_le_bytes());
    bytes.extend_from_slice(b"data");
    bytes.extend_from_slice(&data_bytes.to_le_bytes());
    for sample in samples {
        bytes.extend_from_slice(&sample.to_le_bytes());
    }
    let _ = fs::write(path, bytes);
}

impl AudioManager {
    pub fn new(headless: bool) -> Self {
        let assets_dir = find_file_in_paths("assets").unwrap_or_else(|| PathBuf::from("assets"));

        // Ensure all required WAV earcons exist in assets/
        ensure_synthesized_wav(&assets_dir.join("bump.wav"), &[(150.0, 75)]);
        ensure_synthesized_wav(
            &assets_dir.join("cash.wav"),
            &[(880.0, 60), (1174.66, 90)],
        );
        ensure_synthesized_wav(&assets_dir.join("buy.wav"), &[(660.0, 55), (880.0, 80)]);
        ensure_synthesized_wav(&assets_dir.join("select.wav"), &[(587.33, 45)]);
        ensure_synthesized_wav(&assets_dir.join("typing.wav"), &[(750.0, 20)]);
        ensure_synthesized_wav(&assets_dir.join("click.wav"), &[(520.0, 25)]);
        ensure_synthesized_wav(
            &assets_dir.join("confirm.wav"),
            &[(523.25, 50), (659.25, 70)],
        );
        ensure_synthesized_wav(&assets_dir.join("error.wav"), &[(220.0, 110), (165.0, 130)]);
        ensure_synthesized_wav(
            &assets_dir.join("success.wav"),
            &[(523.25, 60), (659.25, 60), (783.99, 100)],
        );
        ensure_synthesized_wav(
            &assets_dir.join("drumroll.wav"),
            &[
                (220.0, 40),
                (246.94, 40),
                (261.63, 40),
                (293.66, 40),
                (329.63, 55),
                (392.0, 85),
            ],
        );

        let speech_log = Arc::new(Mutex::new(Vec::new()));
        let sound_log = Arc::new(Mutex::new(Vec::new()));

        if headless {
            return Self {
                tx: None,
                headless: true,
                music_enabled: true,
                music_volume: 50,
                sfx_volume: 100,
                speech_volume: 100,
                backend_info: "Headless-Test".to_string(),
                speech_log,
                sound_log,
                assets_dir,
            };
        }

        let (tx, rx) = mpsc::channel::<SpeechCommand>();
        let info_holder = Arc::new(Mutex::new("Console-Fallback".to_string()));
        let info_clone = Arc::clone(&info_holder);

        thread::spawn(move || {
            #[cfg(windows)]
            let prism = unsafe { try_init_prism() };
            #[cfg(not(windows))]
            let prism: Option<PrismBindings> = None;

            #[cfg(windows)]
            let tolk = if prism.is_none() {
                unsafe { try_init_tolk() }
            } else {
                None
            };
            #[cfg(not(windows))]
            let tolk: Option<TolkBindings> = None;

            if let Some(ref p) = prism {
                if let Ok(mut g) = info_clone.lock() {
                    *g = format!("Prism ({})", p.backend_name);
                }
                println!(
                    "[Audio] Prism 64-Bit Screenreader/TTS initialisiert mit Backend: {}",
                    p.backend_name
                );
            } else if tolk.is_some() {
                if let Ok(mut g) = info_clone.lock() {
                    *g = "Tolk".to_string();
                }
                println!("[Audio] Tolk Screenreader-Schnittstelle initialisiert.");
            } else {
                println!("[Audio] Nutze Konsolen-Sprachausgabe-Fallback.");
            }

            while let Ok(cmd) = rx.recv() {
                match cmd {
                    SpeechCommand::Speak { text, interrupt } => {
                        let clean = text.replace(['\r', '\n'], " ");
                        if let Some(ref p) = prism {
                            if let Ok(c_str) = CString::new(clean.clone()) {
                                unsafe {
                                    if interrupt {
                                        (p.prism_backend_stop)(p.backend);
                                    }
                                    (p.prism_backend_speak)(p.backend, c_str.as_ptr(), interrupt);
                                    if let Some(braille_fn) = p.prism_backend_braille {
                                        braille_fn(p.backend, c_str.as_ptr());
                                    }
                                }
                            }
                        } else if let Some(ref t) = tolk {
                            let wide = to_wide(&clean);
                            unsafe {
                                (t.tolk_output)(wide.as_ptr(), interrupt);
                            }
                        }
                    }
                    SpeechCommand::Stop => {
                        if let Some(ref p) = prism {
                            unsafe {
                                (p.prism_backend_stop)(p.backend);
                            }
                        } else if let Some(ref t) = tolk {
                            unsafe {
                                (t.tolk_silence)();
                            }
                        }
                    }
                    SpeechCommand::Shutdown => {
                        if let Some(ref p) = prism {
                            unsafe {
                                // Clean cascade per lessons_learned.md: stop -> free -> shutdown
                                (p.prism_backend_stop)(p.backend);
                                (p.prism_backend_free)(p.backend);
                                (p.prism_shutdown)(p.ctx);
                                #[cfg(windows)]
                                FreeLibrary(p.handle);
                            }
                        }
                        if let Some(ref t) = tolk {
                            unsafe {
                                (t.tolk_silence)();
                                (t.tolk_unload)();
                                #[cfg(windows)]
                                FreeLibrary(t.handle);
                            }
                        }
                        break;
                    }
                }
            }
        });

        // Wait briefly for worker thread to populate backend_info
        thread::sleep(std::time::Duration::from_millis(25));
        let backend_info = info_holder
            .lock()
            .map(|g| g.clone())
            .unwrap_or_else(|_| "Auto".to_string());

        Self {
            tx: Some(tx),
            headless: false,
            music_enabled: true,
            music_volume: 50,
            sfx_volume: 100,
            speech_volume: 100,
            backend_info,
            speech_log,
            sound_log,
            assets_dir,
        }
    }

    pub fn speak(&self, text: &str, interrupt: bool) {
        if text.trim().is_empty() {
            return;
        }
        if let Ok(mut log) = self.speech_log.lock() {
            if interrupt {
                // Keep log bounded
                if log.len() > 200 {
                    log.drain(0..100);
                }
            }
            log.push(text.to_string());
        }
        if let Some(ref tx) = self.tx {
            let _ = tx.send(SpeechCommand::Speak {
                text: text.to_string(),
                interrupt,
            });
        }
    }

    pub fn say(&self, text: &str) {
        self.speak(text, false);
    }

    pub fn say_interrupt(&self, text: &str) {
        self.speak(text, true);
    }

    pub fn stop_speech(&self) {
        if let Some(ref tx) = self.tx {
            let _ = tx.send(SpeechCommand::Stop);
        }
    }

    pub fn play_sound(&self, sound_name: &str) {
        if let Ok(mut log) = self.sound_log.lock() {
            if log.len() > 200 {
                log.drain(0..100);
            }
            log.push(sound_name.to_string());
        }
        if self.headless || self.sfx_volume == 0 {
            return;
        }
        #[cfg(windows)]
        {
            let wav_file = self.assets_dir.join(format!("{}.wav", sound_name));
            if wav_file.exists() {
                let wide = to_wide(&wav_file.to_string_lossy());
                unsafe {
                    PlaySoundW(
                        wide.as_ptr(),
                        std::ptr::null_mut(),
                        SND_FILENAME | SND_ASYNC | SND_NODEFAULT,
                    );
                }
            }
        }
    }

    pub fn play_music(&self, track_name: &str) {
        if self.headless || !self.music_enabled || self.music_volume == 0 {
            return;
        }
        #[cfg(windows)]
        {
            let mp3_file = self.assets_dir.join(format!("{}.mp3", track_name));
            if mp3_file.exists() {
                let close_cmd = to_wide("close bgm");
                let open_cmd = to_wide(&format!(
                    "open \"{}\" type mpegvideo alias bgm",
                    mp3_file.to_string_lossy()
                ));
                let vol_cmd = to_wide(&format!(
                    "setaudio bgm volume to {}",
                    (self.music_volume as u32) * 10
                ));
                let play_cmd = to_wide("play bgm repeat");
                unsafe {
                    mciSendStringW(close_cmd.as_ptr(), std::ptr::null_mut(), 0, std::ptr::null_mut());
                    mciSendStringW(open_cmd.as_ptr(), std::ptr::null_mut(), 0, std::ptr::null_mut());
                    mciSendStringW(vol_cmd.as_ptr(), std::ptr::null_mut(), 0, std::ptr::null_mut());
                    mciSendStringW(play_cmd.as_ptr(), std::ptr::null_mut(), 0, std::ptr::null_mut());
                }
            }
        }
    }

    pub fn stop_music(&self) {
        if self.headless {
            return;
        }
        #[cfg(windows)]
        {
            let close_cmd = to_wide("close bgm");
            unsafe {
                mciSendStringW(close_cmd.as_ptr(), std::ptr::null_mut(), 0, std::ptr::null_mut());
            }
        }
    }

    pub fn last_spoken(&self) -> String {
        self.speech_log
            .lock()
            .ok()
            .and_then(|l| l.last().cloned())
            .unwrap_or_default()
    }

    pub fn last_sound(&self) -> String {
        self.sound_log
            .lock()
            .ok()
            .and_then(|l| l.last().cloned())
            .unwrap_or_default()
    }

    pub fn cleanup(&self) {
        self.stop_music();
        if let Some(ref tx) = self.tx {
            let _ = tx.send(SpeechCommand::Shutdown);
        }
    }
}
