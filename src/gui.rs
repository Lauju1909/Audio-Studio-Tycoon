//! Native Win32 Window & Double-Buffered GDI Renderer for Audio Studio Tycoon (Rust Edition).
//! Provides dual visualization (sighted companions can watch while blind players navigate
//! at 60 FPS with zero latency via keyboard & Prism/Tolk screenreader output).

use crate::audio::AudioManager;
use crate::i18n::tr;
use crate::menus::{KeyInput, MenuController, MenuId};
use crate::state::GameState;
use std::collections::VecDeque;
use std::ffi::{c_int, c_void};
use std::sync::Mutex;
use std::time::{Duration, Instant};

static INPUT_QUEUE: Mutex<VecDeque<RawWinEvent>> = Mutex::new(VecDeque::new());

#[derive(Debug, Clone)]
enum RawWinEvent {
    KeyDown { vk: u32, ctrl: bool, shift: bool },
    Char(char),
    Quit,
}

#[cfg(windows)]
#[repr(C)]
struct WndClassExW {
    cb_size: u32,
    style: u32,
    lpfn_wnd_proc: unsafe extern "system" fn(*mut c_void, u32, usize, isize) -> isize,
    cb_cls_extra: c_int,
    cb_wnd_extra: c_int,
    h_instance: *mut c_void,
    h_icon: *mut c_void,
    h_cursor: *mut c_void,
    hbr_background: *mut c_void,
    lpsz_menu_name: *const u16,
    lpsz_class_name: *const u16,
    h_icon_sm: *mut c_void,
}

#[cfg(windows)]
#[repr(C)]
#[derive(Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

#[cfg(windows)]
#[repr(C)]
#[derive(Clone, Copy)]
struct Msg {
    hwnd: *mut c_void,
    message: u32,
    w_param: usize,
    l_param: isize,
    time: u32,
    pt: Point,
}

#[cfg(windows)]
#[repr(C)]
#[derive(Clone, Copy)]
struct Rect {
    left: i32,
    top: i32,
    right: i32,
    bottom: i32,
}

#[cfg(windows)]
#[link(name = "kernel32")]
extern "system" {
    fn GetModuleHandleW(lpModuleName: *const u16) -> *mut c_void;
}

#[cfg(windows)]
#[link(name = "user32")]
extern "system" {
    fn RegisterClassExW(lpwcx: *const WndClassExW) -> u16;
    fn CreateWindowExW(
        dwExStyle: u32,
        lpClassName: *const u16,
        lpWindowName: *const u16,
        dwStyle: u32,
        x: c_int,
        y: c_int,
        nWidth: c_int,
        nHeight: c_int,
        hWndParent: *mut c_void,
        hMenu: *mut c_void,
        hInstance: *mut c_void,
        lpParam: *mut c_void,
    ) -> *mut c_void;
    fn ShowWindow(hWnd: *mut c_void, nCmdShow: c_int) -> c_int;
    fn SetForegroundWindow(hWnd: *mut c_void) -> c_int;
    fn PeekMessageW(
        lpMsg: *mut Msg,
        hWnd: *mut c_void,
        wMsgFilterMin: u32,
        wMsgFilterMax: u32,
        wRemoveMsg: u32,
    ) -> c_int;
    fn TranslateMessage(lpMsg: *const Msg) -> c_int;
    fn DispatchMessageW(lpMsg: *const Msg) -> isize;
    fn DefWindowProcW(hWnd: *mut c_void, msg: u32, wParam: usize, lParam: isize) -> isize;
    fn PostQuitMessage(nExitCode: c_int);
    fn GetKeyState(nVirtKey: c_int) -> i16;
    fn GetDC(hWnd: *mut c_void) -> *mut c_void;
    fn ReleaseDC(hWnd: *mut c_void, hDC: *mut c_void) -> c_int;
    fn GetClientRect(hWnd: *mut c_void, lpRect: *mut Rect) -> c_int;
    fn FillRect(hDC: *mut c_void, lprc: *const Rect, hbr: *mut c_void) -> c_int;
    fn DrawTextW(
        hDC: *mut c_void,
        lpchText: *const u16,
        cchText: c_int,
        lprc: *mut Rect,
        format: u32,
    ) -> c_int;
}

#[cfg(windows)]
#[link(name = "gdi32")]
extern "system" {
    fn CreateCompatibleDC(hdc: *mut c_void) -> *mut c_void;
    fn CreateCompatibleBitmap(hdc: *mut c_void, cx: c_int, cy: c_int) -> *mut c_void;
    fn SelectObject(hdc: *mut c_void, h: *mut c_void) -> *mut c_void;
    fn DeleteObject(ho: *mut c_void) -> c_int;
    fn DeleteDC(hdc: *mut c_void) -> c_int;
    fn BitBlt(
        hdc: *mut c_void,
        x: c_int,
        y: c_int,
        cx: c_int,
        cy: c_int,
        hdcSrc: *mut c_void,
        x1: c_int,
        y1: c_int,
        rop: u32,
    ) -> c_int;
    fn CreateSolidBrush(color: u32) -> *mut c_void;
    fn SetBkMode(hdc: *mut c_void, mode: c_int) -> c_int;
    fn SetTextColor(hdc: *mut c_void, color: u32) -> u32;
    fn CreateFontW(
        cHeight: c_int,
        cWidth: c_int,
        cEscapement: c_int,
        cOrientation: c_int,
        cWeight: c_int,
        bItalic: u32,
        bUnderline: u32,
        bStrikeOut: u32,
        iCharSet: u32,
        iOutPrecision: u32,
        iClipPrecision: u32,
        iQuality: u32,
        iPitchAndFamily: u32,
        pszFaceName: *const u16,
    ) -> *mut c_void;
}

#[cfg(windows)]
const WM_DESTROY: u32 = 0x0002;
#[cfg(windows)]
const WM_CLOSE: u32 = 0x0010;
#[cfg(windows)]
const WM_KEYDOWN: u32 = 0x0100;
#[cfg(windows)]
const WM_CHAR: u32 = 0x0102;
#[cfg(windows)]
const PM_REMOVE: u32 = 0x0001;
#[cfg(windows)]
const WS_OVERLAPPEDWINDOW: u32 = 0x00CF0000;
#[cfg(windows)]
const WS_VISIBLE: u32 = 0x10000000;
#[cfg(windows)]
const SW_SHOW: c_int = 5;
#[cfg(windows)]
const SRCCOPY: u32 = 0x00CC0020;
#[cfg(windows)]
const TRANSPARENT: c_int = 1;
#[cfg(windows)]
const DT_SINGLELINE: u32 = 0x0020;
#[cfg(windows)]
const DT_VCENTER: u32 = 0x0004;
#[cfg(windows)]
const DT_NOPREFIX: u32 = 0x0800;

#[cfg(windows)]
const VK_BACK: u32 = 0x08;
#[cfg(windows)]
const VK_RETURN: u32 = 0x0D;
#[cfg(windows)]
const VK_SHIFT: c_int = 0x10;
#[cfg(windows)]
const VK_CONTROL: c_int = 0x11;
#[cfg(windows)]
const VK_ESCAPE: u32 = 0x1B;
#[cfg(windows)]
const VK_SPACE: u32 = 0x20;
#[cfg(windows)]
const VK_LEFT: u32 = 0x25;
#[cfg(windows)]
const VK_UP: u32 = 0x26;
#[cfg(windows)]
const VK_RIGHT: u32 = 0x27;
#[cfg(windows)]
const VK_DOWN: u32 = 0x28;
#[cfg(windows)]
const VK_F8: u32 = 0x77;

#[cfg(windows)]
fn rgb(r: u8, g: u8, b: u8) -> u32 {
    (r as u32) | ((g as u32) << 8) | ((b as u32) << 16)
}

#[cfg(windows)]
fn to_wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

#[cfg(windows)]
unsafe extern "system" fn wnd_proc(
    hwnd: *mut c_void,
    msg: u32,
    w_param: usize,
    l_param: isize,
) -> isize {
    match msg {
        WM_CLOSE | WM_DESTROY => {
            if let Ok(mut q) = INPUT_QUEUE.lock() {
                q.push_back(RawWinEvent::Quit);
            }
            PostQuitMessage(0);
            0
        }
        WM_KEYDOWN => {
            let vk = w_param as u32;
            let ctrl = (GetKeyState(VK_CONTROL) as u16 & 0x8000) != 0;
            let shift = (GetKeyState(VK_SHIFT) as u16 & 0x8000) != 0;
            if let Ok(mut q) = INPUT_QUEUE.lock() {
                q.push_back(RawWinEvent::KeyDown { vk, ctrl, shift });
            }
            0
        }
        WM_CHAR => {
            if let Some(ch) = char::from_u32(w_param as u32) {
                if !ch.is_control() {
                    if let Ok(mut q) = INPUT_QUEUE.lock() {
                        q.push_back(RawWinEvent::Char(ch));
                    }
                }
            }
            0
        }
        _ => DefWindowProcW(hwnd, msg, w_param, l_param),
    }
}

#[cfg(windows)]
unsafe fn render_frame(
    hwnd: *mut c_void,
    state: &GameState,
    menu: &MenuController,
    font_title: *mut c_void,
    font_item: *mut c_void,
    font_footer: *mut c_void,
) {
    let mut rc = Rect {
        left: 0,
        top: 0,
        right: 880,
        bottom: 640,
    };
    GetClientRect(hwnd, &mut rc);
    let w = (rc.right - rc.left).max(400);
    let h = (rc.bottom - rc.top).max(300);

    let hdc = GetDC(hwnd);
    if hdc.is_null() {
        return;
    }
    let mem_dc = CreateCompatibleDC(hdc);
    let mem_bmp = CreateCompatibleBitmap(hdc, w, h);
    let old_bmp = SelectObject(mem_dc, mem_bmp);

    // 1. Dark slate background
    let bg_brush = CreateSolidBrush(rgb(15, 23, 42));
    FillRect(mem_dc, &rc, bg_brush);
    DeleteObject(bg_brush);

    // 2. Menu Card Box
    let card_rc = Rect {
        left: 40,
        top: 50,
        right: w - 40,
        bottom: h - 70,
    };
    let card_brush = CreateSolidBrush(rgb(30, 41, 59));
    FillRect(mem_dc, &card_rc, card_brush);
    DeleteObject(card_brush);

    SetBkMode(mem_dc, TRANSPARENT);

    // 3. Title
    SelectObject(mem_dc, font_title);
    SetTextColor(mem_dc, rgb(0, 242, 254));
    let mut title_rc = Rect {
        left: 65,
        top: 65,
        right: w - 65,
        bottom: 110,
    };
    let title_w: Vec<u16> = menu.title.encode_utf16().collect();
    DrawTextW(
        mem_dc,
        title_w.as_ptr(),
        title_w.len() as c_int,
        &mut title_rc,
        DT_SINGLELINE | DT_VCENTER | DT_NOPREFIX,
    );

    // 4. Active Development Ticker (top right)
    if let Some(first_ap) = state.active_projects.first() {
        SelectObject(mem_dc, font_footer);
        SetTextColor(mem_dc, rgb(56, 189, 248));
        let ticker = format!(
            "DEV: {} ({}%)",
            first_ap.project.name,
            first_ap.percent()
        );
        let ticker_w: Vec<u16> = ticker.encode_utf16().collect();
        let mut t_rc = Rect {
            left: w - 340,
            top: 12,
            right: w - 40,
            bottom: 45,
        };
        DrawTextW(
            mem_dc,
            ticker_w.as_ptr(),
            ticker_w.len() as c_int,
            &mut t_rc,
            DT_SINGLELINE | DT_VCENTER | DT_NOPREFIX,
        );
    }

    // 5. Menu Options (with automatic scrolling window of 9 visible items)
    let max_visible = 9usize;
    let start_idx = if menu.current_index >= max_visible {
        menu.current_index + 1 - max_visible
    } else {
        0
    };
    let end_idx = (start_idx + max_visible).min(menu.options.len());

    SelectObject(mem_dc, font_item);
    for (vis_row, i) in (start_idx..end_idx).enumerate() {
        let y_top = 120 + (vis_row as i32) * 42;
        let mut item_rc = Rect {
            left: 65,
            top: y_top,
            right: w - 65,
            bottom: y_top + 36,
        };
        if i == menu.current_index {
            let hl_brush = CreateSolidBrush(rgb(14, 116, 144));
            let hl_rc = Rect {
                left: 55,
                top: y_top,
                right: w - 55,
                bottom: y_top + 36,
            };
            FillRect(mem_dc, &hl_rc, hl_brush);
            DeleteObject(hl_brush);
            SetTextColor(mem_dc, rgb(255, 255, 255));
        } else {
            SetTextColor(mem_dc, rgb(186, 198, 216));
        }
        let line = &menu.options[i].text;
        let line_w: Vec<u16> = line.encode_utf16().collect();
        DrawTextW(
            mem_dc,
            line_w.as_ptr(),
            line_w.len() as c_int,
            &mut item_rc,
            DT_SINGLELINE | DT_VCENTER | DT_NOPREFIX,
        );
    }

    // 6. Footer Status Bar
    SelectObject(mem_dc, font_footer);
    SetTextColor(mem_dc, rgb(226, 232, 240));
    let footer_text = format!(
        "{} | {}: {} EUR | Fans: {} | Hype: {:.0} | Trend: {} + {} | {}",
        state.company_name,
        tr(state.lang(), "money_label"),
        state.money,
        state.fans,
        state.hype,
        state.trend_topic,
        state.trend_genre,
        state.calendar_text()
    );
    let footer_w: Vec<u16> = footer_text.encode_utf16().collect();
    let mut footer_rc = Rect {
        left: 45,
        top: h - 55,
        right: w - 45,
        bottom: h - 15,
    };
    DrawTextW(
        mem_dc,
        footer_w.as_ptr(),
        footer_w.len() as c_int,
        &mut footer_rc,
        DT_SINGLELINE | DT_VCENTER | DT_NOPREFIX,
    );

    BitBlt(hdc, 0, 0, w, h, mem_dc, 0, 0, SRCCOPY);

    SelectObject(mem_dc, old_bmp);
    DeleteObject(mem_bmp);
    DeleteDC(mem_dc);
    ReleaseDC(hwnd, hdc);
}

pub fn run_gui_app(mut state: GameState, mut audio: AudioManager) {
    let mut menu = MenuController::new(&state);

    audio.say(&tr(state.lang(), "main_welcome"));
    audio.play_music("music_back");
    menu.announce_entry(&audio);

    #[cfg(windows)]
    unsafe {
        let h_instance = GetModuleHandleW(std::ptr::null());
        let class_name = to_wide("AudioStudioTycoonRustWndClass");
        let wcx = WndClassExW {
            cb_size: std::mem::size_of::<WndClassExW>() as u32,
            style: 0x0003,
            lpfn_wnd_proc: wnd_proc,
            cb_cls_extra: 0,
            cb_wnd_extra: 0,
            h_instance,
            h_icon: std::ptr::null_mut(),
            h_cursor: std::ptr::null_mut(),
            hbr_background: std::ptr::null_mut(),
            lpsz_menu_name: std::ptr::null(),
            lpsz_class_name: class_name.as_ptr(),
            h_icon_sm: std::ptr::null_mut(),
        };
        RegisterClassExW(&wcx);

        let title = to_wide("Audio Studio Tycoon v4.3.0 - Native Rust Edition");
        let hwnd = CreateWindowExW(
            0,
            class_name.as_ptr(),
            title.as_ptr(),
            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
            100,
            80,
            920,
            660,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            h_instance,
            std::ptr::null_mut(),
        );
        if !hwnd.is_null() {
            ShowWindow(hwnd, SW_SHOW);
            SetForegroundWindow(hwnd);
        }

        let font_face = to_wide("Segoe UI");
        let font_title = CreateFontW(
            -28,
            0,
            0,
            0,
            700,
            0,
            0,
            0,
            1,
            0,
            0,
            5,
            0,
            font_face.as_ptr(),
        );
        let font_item = CreateFontW(
            -20,
            0,
            0,
            0,
            400,
            0,
            0,
            0,
            1,
            0,
            0,
            5,
            0,
            font_face.as_ptr(),
        );
        let font_footer = CreateFontW(
            -16,
            0,
            0,
            0,
            600,
            0,
            0,
            0,
            1,
            0,
            0,
            5,
            0,
            font_face.as_ptr(),
        );

        let mut last_tick = Instant::now();
        let mut msg = Msg {
            hwnd: std::ptr::null_mut(),
            message: 0,
            w_param: 0,
            l_param: 0,
            time: 0,
            pt: Point { x: 0, y: 0 },
        };

        while !menu.should_quit {
            while PeekMessageW(&mut msg, std::ptr::null_mut(), 0, 0, PM_REMOVE) != 0 {
                TranslateMessage(&msg);
                DispatchMessageW(&msg);
            }

            let events: Vec<RawWinEvent> = if let Ok(mut q) = INPUT_QUEUE.lock() {
                q.drain(..).collect()
            } else {
                Vec::new()
            };

            for ev in events {
                match ev {
                    RawWinEvent::Quit => {
                        menu.should_quit = true;
                    }
                    RawWinEvent::KeyDown { vk, ctrl, shift } => {
                        if vk == VK_F8 || (ctrl && vk == b'L' as u32) {
                            menu.handle_input(KeyInput::ToggleLang, &mut state, &mut audio);
                        } else if ctrl && shift && vk == b'D' as u32 {
                            menu.handle_input(KeyInput::ToggleDevMode, &mut state, &mut audio);
                        } else if vk == VK_UP {
                            menu.handle_input(KeyInput::Up, &mut state, &mut audio);
                        } else if vk == VK_DOWN {
                            menu.handle_input(KeyInput::Down, &mut state, &mut audio);
                        } else if vk == VK_LEFT {
                            menu.handle_input(KeyInput::Left, &mut state, &mut audio);
                        } else if vk == VK_RIGHT {
                            menu.handle_input(KeyInput::Right, &mut state, &mut audio);
                        } else if vk == VK_RETURN {
                            menu.handle_input(KeyInput::Enter, &mut state, &mut audio);
                        } else if vk == VK_ESCAPE {
                            menu.handle_input(KeyInput::Escape, &mut state, &mut audio);
                        } else if vk == VK_BACK {
                            menu.handle_input(KeyInput::Back, &mut state, &mut audio);
                        } else if !menu.is_text_input {
                            match vk {
                                VK_SPACE | 0x30 => menu.handle_input(
                                    KeyInput::SpeedPauseToggle,
                                    &mut state,
                                    &mut audio,
                                ),
                                0x31 => menu.handle_input(KeyInput::Speed1, &mut state, &mut audio),
                                0x32 => menu.handle_input(KeyInput::Speed2, &mut state, &mut audio),
                                0x33 => menu.handle_input(KeyInput::Speed3, &mut state, &mut audio),
                                0x57 => {
                                    // 'W'
                                    menu.handle_input(KeyInput::NextWeek, &mut state, &mut audio)
                                }
                                0x46 => {
                                    // 'F'
                                    menu.handle_input(
                                        KeyInput::FinanceSummary,
                                        &mut state,
                                        &mut audio,
                                    )
                                }
                                0x53 => {
                                    // 'S'
                                    menu.handle_input(
                                        KeyInput::StatusSummary,
                                        &mut state,
                                        &mut audio,
                                    )
                                }
                                0x48 => {
                                    // 'H'
                                    menu.handle_input(KeyInput::Help, &mut state, &mut audio)
                                }
                                0x44 => {
                                    // 'D'
                                    menu.handle_input(KeyInput::OpenDevMenu, &mut state, &mut audio)
                                }
                                _ => {}
                            }
                        }
                    }
                    RawWinEvent::Char(ch) => {
                        if menu.is_text_input {
                            menu.handle_input(KeyInput::Char(ch), &mut state, &mut audio);
                        }
                    }
                }
            }

            // Real-time week progression when in-game and unpaused
            let dt_ms = last_tick.elapsed().as_secs_f64() * 1000.0;
            last_tick = Instant::now();
            if menu.current_menu != MenuId::MainMenu
                && menu.current_menu != MenuId::DifficultyMenu
                && !menu.is_text_input
                && state.time_speed > 0.0
            {
                let ms_per_week = 15_000.0 / state.time_speed;
                state.week_progress += dt_ms / ms_per_week;
                if state.week_progress >= 1.0 {
                    state.week_progress -= 1.0;
                    let notes = state.tick_week();
                    let keep = menu.current_index;
                    menu.rebuild(&state);
                    menu.current_index = keep.min(menu.options.len().saturating_sub(1));
                    for n in notes {
                        audio.say(&n);
                    }
                }
            }

            if !hwnd.is_null() {
                render_frame(hwnd, &state, &menu, font_title, font_item, font_footer);
            }

            std::thread::sleep(Duration::from_millis(16));
        }

        DeleteObject(font_title);
        DeleteObject(font_item);
        DeleteObject(font_footer);
    }

    audio.cleanup();
}
