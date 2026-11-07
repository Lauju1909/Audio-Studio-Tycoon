//! Coherent, logically structured historical game data (1930 - 2030+).
//! Overhauled so every era, platform, topic-genre compatibility, slider profile,
//! technology unlock, and economic parameter makes complete sense.

pub const START_YEAR: u32 = 1930;
pub const WEEKS_PER_YEAR: u32 = 48;
pub const WEEKS_PER_MONTH: u32 = 4;

pub const SLIDER_NAMES: [&str; 6] = ["Gameplay", "Grafik", "Sound", "Story", "KI", "Welt"];

#[derive(Debug, Clone)]
pub struct EraInfo {
    pub id: &'static str,
    pub name_de: &'static str,
    pub name_en: &'static str,
    pub start_year: u32,
    pub end_year: u32,
    pub desc_de: &'static str,
    pub desc_en: &'static str,
    pub base_market_scale: f64,
}

pub const HISTORICAL_ERAS: &[EraInfo] = &[
    EraInfo {
        id: "era_radio",
        name_de: "Goldene Radio- & Schellack-Ära (1930–1949)",
        name_en: "Golden Radio & Shellac Era (1930–1949)",
        start_year: 1930,
        end_year: 1949,
        desc_de: "Live-Hörspiele, Schellackplatten, Relais-Logik und die Geburt der Magnetbandtechnik.",
        desc_en: "Live radio dramas, shellac records, relay logic, and the birth of magnetic tape.",
        base_market_scale: 1.0,
    },
    EraInfo {
        id: "era_tape",
        name_de: "Magnetband-, Stereo- & Mainframe-Ära (1950–1969)",
        name_en: "Magnetic Tape, Stereo & Mainframe Era (1950–1969)",
        start_year: 1950,
        end_year: 1969,
        desc_de: "Vinyl-LPs, Stereo-Abmischung, Moog-Synthesizer und erste Großrechner-Spiele.",
        desc_en: "Vinyl LPs, stereo mixing, Moog synthesizers, and early mainframe games.",
        base_market_scale: 1.8,
    },
    EraInfo {
        id: "era_arcade",
        name_de: "Arcade- & Analog-Synthesizer-Ära (1970–1979)",
        name_en: "Arcade & Analog Synthesizer Era (1970–1979)",
        start_year: 1970,
        end_year: 1979,
        desc_de: "Spielhallen-Automaten, erste Heimkonsolen, PCM-Audio und der Sony Walkman.",
        desc_en: "Arcade cabinets, first home consoles, PCM audio, and the Sony Walkman.",
        base_market_scale: 3.0,
    },
    EraInfo {
        id: "era_8bit",
        name_de: "8-Bit Heimcomputer, FM-Synthese & CD-Ära (1980–1989)",
        name_en: "8-Bit Home Computers, FM Synth & CD Era (1980–1989)",
        start_year: 1980,
        end_year: 1989,
        desc_de: "C64 SID-Chip, NES, MIDI-Standard, FM-Soundkarten und die ersten Audio-CDs.",
        desc_en: "C64 SID chip, NES, MIDI standard, FM soundcards, and the first audio CDs.",
        base_market_scale: 5.0,
    },
    EraInfo {
        id: "era_multimedia",
        name_de: "16/32-Bit Multimedia & 3D-Audio-Ära (1990–1999)",
        name_en: "16/32-Bit Multimedia & 3D Audio Era (1990–1999)",
        start_year: 1990,
        end_year: 1999,
        desc_de: "CD-ROM Sprachausgabe, Sound Blaster 16, PlayStation, MP3 und die SoundCon Messe.",
        desc_en: "CD-ROM voice acting, Sound Blaster 16, PlayStation, MP3, and the SoundCon Expo.",
        base_market_scale: 8.0,
    },
    EraInfo {
        id: "era_digital",
        name_de: "Online-, Digitalvertrieb- & HD-Audio-Ära (2000–2014)",
        name_en: "Online, Digital Distribution & HD Audio Era (2000–2014)",
        start_year: 2000,
        end_year: 2014,
        desc_de: "Steam, Smartphones, Surround-Headsets, Dolby Atmos, Streaming und Live-Services.",
        desc_en: "Steam, smartphones, surround headsets, Dolby Atmos, streaming, and live services.",
        base_market_scale: 12.0,
    },
    EraInfo {
        id: "era_spatial",
        name_de: "Spatial Audio, VR, KI & Neural-Ära (2015–2035+)",
        name_en: "Spatial Audio, VR, AI & Neural Era (2015–2035+)",
        start_year: 2015,
        end_year: 2050,
        desc_de: "Binaurales VR-Audio, Tempest 3D, KI-Sounddesign und direkte neuronale Klangwelten.",
        desc_en: "Binaural VR audio, Tempest 3D, AI sound design, and direct neural soundscapes.",
        base_market_scale: 16.0,
    },
];

/// Returns the historical era for a given calendar year.
/// Clamps cleanly to the first era for `year <= 1930` and the last era for `year >= 2015`
/// (preventing the 2026->1930 wraparound bug documented in `lessons_learned.md`).
pub fn get_current_era(year: u32) -> &'static EraInfo {
    for era in HISTORICAL_ERAS {
        if year >= era.start_year && year <= era.end_year {
            return era;
        }
    }
    if year < HISTORICAL_ERAS[0].start_year {
        &HISTORICAL_ERAS[0]
    } else {
        &HISTORICAL_ERAS[HISTORICAL_ERAS.len() - 1]
    }
}

#[derive(Debug, Clone)]
pub struct PlatformSpec {
    pub name: &'static str,
    pub license_fee: i64,
    pub market_multi: f64,
    pub unlock_year: u32,
    pub end_year: u32,
    pub category: &'static str,
    pub audio_capabilities: &'static str,
}

pub const PLATFORMS: &[PlatformSpec] = &[
    // 1930s - 1940s
    PlatformSpec {
        name: "Radio-Sendernetz (AM)",
        license_fee: 0,
        market_multi: 1.1,
        unlock_year: 1930,
        end_year: 1958,
        category: "Rundfunk",
        audio_capabilities: "Live-Mikrofon & Geräuschkulisse (Foley)",
    },
    PlatformSpec {
        name: "Schellack-Schallplatte (78 RPM)",
        license_fee: 5_000,
        market_multi: 1.3,
        unlock_year: 1930,
        end_year: 1952,
        category: "Tonträger",
        audio_capabilities: "Akustisch-elektrische Mono-Aufnahme",
    },
    PlatformSpec {
        name: "Mechanischer Spielautomat",
        license_fee: 8_000,
        market_multi: 1.4,
        unlock_year: 1933,
        end_year: 1955,
        category: "Automat",
        audio_capabilities: "Mechanische Glocken & Relais-Klang",
    },
    PlatformSpec {
        name: "Zuse Z3 (Relais-Rechner)",
        license_fee: 15_000,
        market_multi: 1.6,
        unlock_year: 1941,
        end_year: 1954,
        category: "Frührechner",
        audio_capabilities: "Rhythmische Relais-Taktung",
    },
    PlatformSpec {
        name: "ENIAC Röhrenrechner",
        license_fee: 18_000,
        market_multi: 2.0,
        unlock_year: 1946,
        end_year: 1958,
        category: "Großrechner",
        audio_capabilities: "Röhren-Summer & Lochkarten-Ausgabe",
    },
    PlatformSpec {
        name: "Vinyl-LP (33 RPM)",
        license_fee: 20_000,
        market_multi: 2.4,
        unlock_year: 1948,
        end_year: 1975,
        category: "Tonträger",
        audio_capabilities: "Hi-Fi Mikrorillen-Langspielplatte",
    },
    // 1950s - 1960s
    PlatformSpec {
        name: "UNIVAC I Mainframe",
        license_fee: 25_000,
        market_multi: 2.8,
        unlock_year: 1951,
        end_year: 1964,
        category: "Großrechner",
        audio_capabilities: "Magnetband-Synthese & Konsolenton",
    },
    PlatformSpec {
        name: "UKW-Transistorradio (FM)",
        license_fee: 15_000,
        market_multi: 3.2,
        unlock_year: 1954,
        end_year: 1978,
        category: "Rundfunk",
        audio_capabilities: "Rauschfreier UKW-Hörfunk",
    },
    PlatformSpec {
        name: "PDP-1 (Spacewar-System)",
        license_fee: 35_000,
        market_multi: 3.8,
        unlock_year: 1960,
        end_year: 1972,
        category: "Minicomputer",
        audio_capabilities: "4-stimmiger Rechteck-Tongenerator",
    },
    PlatformSpec {
        name: "Kompaktkassette (MC Stereo)",
        license_fee: 30_000,
        market_multi: 4.5,
        unlock_year: 1963,
        end_year: 1992,
        category: "Tonträger",
        audio_capabilities: "Magnetband-Stereo für Hörspiele & Daten",
    },
    PlatformSpec {
        name: "IBM System/360",
        license_fee: 45_000,
        market_multi: 4.8,
        unlock_year: 1965,
        end_year: 1978,
        category: "Großrechner",
        audio_capabilities: "Digitale Klangberechnung",
    },
    // 1970s
    PlatformSpec {
        name: "Arcade-Automat (Münzspiel)",
        license_fee: 50_000,
        market_multi: 5.8,
        unlock_year: 1971,
        end_year: 1994,
        category: "Arcade",
        audio_capabilities: "Dedizierte Analog-/FM-Soundchips",
    },
    PlatformSpec {
        name: "Magnavox Odyssey",
        license_fee: 55_000,
        market_multi: 5.5,
        unlock_year: 1972,
        end_year: 1980,
        category: "Konsole",
        audio_capabilities: "Analoge TV-Klangausgabe",
    },
    PlatformSpec {
        name: "Atari 2600 (VCS)",
        license_fee: 65_000,
        market_multi: 7.0,
        unlock_year: 1977,
        end_year: 1989,
        category: "Konsole",
        audio_capabilities: "TIA 2-Kanal Chiptune-Synthese",
    },
    PlatformSpec {
        name: "Apple II",
        license_fee: 40_000,
        market_multi: 6.8,
        unlock_year: 1977,
        end_year: 1990,
        category: "Heimcomputer",
        audio_capabilities: "1-Bit Speaker & Mockingboard Soundkarte",
    },
    // 1980s
    PlatformSpec {
        name: "PC (MS-DOS / Soundkarte)",
        license_fee: 0,
        market_multi: 7.8,
        unlock_year: 1981,
        end_year: 2002,
        category: "PC",
        audio_capabilities: "PC-Speaker, AdLib FM & Sound Blaster",
    },
    PlatformSpec {
        name: "Commodore 64 (SID 6581)",
        license_fee: 45_000,
        market_multi: 8.2,
        unlock_year: 1982,
        end_year: 1994,
        category: "Heimcomputer",
        audio_capabilities: "Legendärer 3-Kanal SID-Synthesizer",
    },
    PlatformSpec {
        name: "ZX Spectrum",
        license_fee: 35_000,
        market_multi: 7.2,
        unlock_year: 1982,
        end_year: 1992,
        category: "Heimcomputer",
        audio_capabilities: "Beeper & AY-3-8912 Soundchip",
    },
    PlatformSpec {
        name: "Famicom (NES)",
        license_fee: 75_000,
        market_multi: 8.8,
        unlock_year: 1983,
        end_year: 1995,
        category: "Konsole",
        audio_capabilities: "5-Kanal Ricoh 2A03 APU (Puls, Dreieck, DPCM)",
    },
    PlatformSpec {
        name: "Commodore Amiga (Paula)",
        license_fee: 60_000,
        market_multi: 8.5,
        unlock_year: 1985,
        end_year: 1996,
        category: "Heimcomputer",
        audio_capabilities: "4-Kanal 8-Bit PCM Hardware-MOD-Tracker",
    },
    PlatformSpec {
        name: "Sega Genesis (Mega Drive)",
        license_fee: 85_000,
        market_multi: 9.0,
        unlock_year: 1988,
        end_year: 1998,
        category: "Konsole",
        audio_capabilities: "Yamaha YM2612 FM-Synthese",
    },
    PlatformSpec {
        name: "Game Boy",
        license_fee: 80_000,
        market_multi: 9.2,
        unlock_year: 1989,
        end_year: 2001,
        category: "Handheld",
        audio_capabilities: "4-Kanal Stereo-Chiptune über Kopfhörer",
    },
    // 1990s
    PlatformSpec {
        name: "SNES (Super Nintendo)",
        license_fee: 90_000,
        market_multi: 9.5,
        unlock_year: 1990,
        end_year: 2000,
        category: "Konsole",
        audio_capabilities: "Sony SPC700 8-Kanal Wavetable-DSP",
    },
    PlatformSpec {
        name: "PlayStation 1",
        license_fee: 95_000,
        market_multi: 10.2,
        unlock_year: 1994,
        end_year: 2005,
        category: "Konsole",
        audio_capabilities: "24-Kanal ADPCM & CD-Audio Redbook",
    },
    PlatformSpec {
        name: "Nintendo 64",
        license_fee: 98_000,
        market_multi: 9.8,
        unlock_year: 1996,
        end_year: 2004,
        category: "Konsole",
        audio_capabilities: "Software-gemischtes 64-Kanal Audio",
    },
    PlatformSpec {
        name: "Dreamcast",
        license_fee: 95_000,
        market_multi: 9.4,
        unlock_year: 1998,
        end_year: 2006,
        category: "Konsole",
        audio_capabilities: "Yamaha AICA 64-Kanal DSP",
    },
    // 2000s - 2010s
    PlatformSpec {
        name: "PlayStation 2",
        license_fee: 100_000,
        market_multi: 11.5,
        unlock_year: 2000,
        end_year: 2012,
        category: "Konsole",
        audio_capabilities: "48-Kanal SPU2 & Dolby Digital 5.1",
    },
    PlatformSpec {
        name: "PC (Digital / Steam)",
        license_fee: 0,
        market_multi: 12.0,
        unlock_year: 2000,
        end_year: 2099,
        category: "PC",
        audio_capabilities: "Mehrkanal-HD-Audio, VST & Spatial Sound",
    },
    PlatformSpec {
        name: "Xbox 360",
        license_fee: 100_000,
        market_multi: 11.0,
        unlock_year: 2005,
        end_year: 2016,
        category: "Konsole",
        audio_capabilities: "XMA Surround-Audio & Voice-Chat",
    },
    PlatformSpec {
        name: "PlayStation 3",
        license_fee: 105_000,
        market_multi: 11.2,
        unlock_year: 2006,
        end_year: 2017,
        category: "Konsole",
        audio_capabilities: "7.1 Unkomprimiertes Blu-Ray PCM-Audio",
    },
    PlatformSpec {
        name: "Smartphone (iOS / Android)",
        license_fee: 25_000,
        market_multi: 12.5,
        unlock_year: 2007,
        end_year: 2099,
        category: "Mobile",
        audio_capabilities: "Kopfhörer-Binaural & Screenreader-Zugänglichkeit",
    },
    PlatformSpec {
        name: "PlayStation 4",
        license_fee: 110_000,
        market_multi: 12.2,
        unlock_year: 2013,
        end_year: 2026,
        category: "Konsole",
        audio_capabilities: "AMD TrueAudio DSP & Controller-Speaker",
    },
    // 2016 - 2030+
    PlatformSpec {
        name: "VR-Headset (Spatial Audio)",
        license_fee: 140_000,
        market_multi: 10.5,
        unlock_year: 2016,
        end_year: 2099,
        category: "VR",
        audio_capabilities: "Kopfbewegungs-gesteuertes HRTF 3D-Audio",
    },
    PlatformSpec {
        name: "Switch",
        license_fee: 105_000,
        market_multi: 12.8,
        unlock_year: 2017,
        end_year: 2099,
        category: "Handheld",
        audio_capabilities: "HD-Rumble Akustik-Feedback & Portable Stereo",
    },
    PlatformSpec {
        name: "PlayStation 5",
        license_fee: 120_000,
        market_multi: 13.5,
        unlock_year: 2020,
        end_year: 2099,
        category: "Konsole",
        audio_capabilities: "Tempest 3D AudioTech (Objektbasiert)",
    },
    PlatformSpec {
        name: "Steam Deck",
        license_fee: 50_000,
        market_multi: 11.8,
        unlock_year: 2022,
        end_year: 2099,
        category: "Handheld",
        audio_capabilities: "Dual-DSP Hi-Res Handheld-Audio",
    },
    PlatformSpec {
        name: "Neural-Box 1 (BCI Audio)",
        license_fee: 200_000,
        market_multi: 15.0,
        unlock_year: 2026,
        end_year: 2099,
        category: "Neural",
        audio_capabilities: "Direkte kortikale Klangprojektion",
    },
];

pub fn get_available_platforms(year: u32) -> Vec<&'static PlatformSpec> {
    let mut list: Vec<&'static PlatformSpec> = PLATFORMS
        .iter()
        .filter(|p| year >= p.unlock_year && year <= p.end_year)
        .collect();
    if list.is_empty() {
        // Fallback so the player never has 0 platforms
        list.push(&PLATFORMS[PLATFORMS.len() - 1]);
    }
    list
}

pub const GENRES: &[&str] = &[
    "Abenteuer",
    "Puzzle",
    "Casual",
    "Strategie",
    "Simulation",
    "RPG",
    "Action",
    "Sport",
    "Rennspiel",
    "Horror",
    "Kampfspiel",
];

pub const START_GENRES: &[&str] = &["Abenteuer", "Puzzle", "Casual", "Strategie"];

#[derive(Debug, Clone)]
pub struct ResearchableItem {
    pub name: &'static str,
    pub cost: i64,
    pub unlock_year: u32,
    pub weeks: u32,
    pub desc_de: &'static str,
    pub desc_en: &'static str,
}

pub const RESEARCHABLE_GENRES: &[ResearchableItem] = &[
    ResearchableItem {
        name: "Simulation",
        cost: 8_000,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Realistische Technik-, Wirtschafts- und Alltags-Simulationen.",
        desc_en: "Realistic technical, economic, and life simulations.",
    },
    ResearchableItem {
        name: "Horror",
        cost: 12_000,
        unlock_year: 1935,
        weeks: 3,
        desc_de: "Spannende Gänsehaut-Produktionen mit intensiver Geräuschkulisse.",
        desc_en: "Thrilling suspense productions with intense soundscapes.",
    },
    ResearchableItem {
        name: "Sport",
        cost: 10_000,
        unlock_year: 1936,
        weeks: 2,
        desc_de: "Dynamische Wettkampf- und Stadion-Atmosphäre.",
        desc_en: "Dynamic competition and stadium atmosphere.",
    },
    ResearchableItem {
        name: "Action",
        cost: 15_000,
        unlock_year: 1938,
        weeks: 3,
        desc_de: "Schnelle Reaktionen, packendes Tempo und wuchtige Soundeffekte.",
        desc_en: "Fast reflexes, gripping pace, and punchy sound effects.",
    },
    ResearchableItem {
        name: "Rennspiel",
        cost: 14_000,
        unlock_year: 1950,
        weeks: 3,
        desc_de: "Dröhnende Motoren, Reifenquietschen und Hochgeschwindigkeit.",
        desc_en: "Roaring engines, screeching tires, and high speed.",
    },
    ResearchableItem {
        name: "RPG",
        cost: 18_000,
        unlock_year: 1962,
        weeks: 4,
        desc_de: "Epische Rollenspiele mit tiefgründiger Geschichte und Charakterentwicklung.",
        desc_en: "Epic role-playing games with deep narrative and character progression.",
    },
    ResearchableItem {
        name: "Kampfspiel",
        cost: 20_000,
        unlock_year: 1970,
        weeks: 3,
        desc_de: "Präzise Schlagabtausche und markante Treffer-Akustik.",
        desc_en: "Precise martial combat and striking hit acoustics.",
    },
];

pub const START_TOPICS: &[&str] = &[
    "Radio-Drama",
    "Detektiv",
    "Swing-Musik",
    "Abenteuer-Reise",
    "Schach",
    "Fantasy",
    "Sci-Fi",
    "Sport",
];

pub const RESEARCHABLE_TOPICS: &[ResearchableItem] = &[
    ResearchableItem {
        name: "Kryptografie",
        cost: 5_000,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Geheimcodes, Chiffriermaschinen und logische Entschlüsselung.",
        desc_en: "Secret codes, cipher machines, and logical decryption.",
    },
    ResearchableItem {
        name: "Eisenbahn",
        cost: 6_000,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Dampflokomotiven, Fahrpläne und Logistiknetze.",
        desc_en: "Steam locomotives, timetables, and logistics networks.",
    },
    ResearchableItem {
        name: "Mittelalter",
        cost: 6_500,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Burgen, Ritter, Handel und historische Schlachten.",
        desc_en: "Castles, knights, trade, and historical battles.",
    },
    ResearchableItem {
        name: "Mars-Invasion",
        cost: 8_500,
        unlock_year: 1938,
        weeks: 2,
        desc_de: "Außerirdische Landung nach dem berühmten Radio-Hörspiel von 1938.",
        desc_en: "Alien landing inspired by the famous 1938 radio broadcast.",
    },
    ResearchableItem {
        name: "Spionage",
        cost: 10_000,
        unlock_year: 1940,
        weeks: 2,
        desc_de: "Geheimagenten, Abhörtechnik und verdeckte Operationen.",
        desc_en: "Secret agents, wiretapping, and covert operations.",
    },
    ResearchableItem {
        name: "U-Boot",
        cost: 11_000,
        unlock_year: 1940,
        weeks: 2,
        desc_de: "Sonar-Ortung, Unterwasser-Spannung und Taktik im Echolot.",
        desc_en: "Sonar tracking, underwater tension, and echolocation tactics.",
    },
    ResearchableItem {
        name: "Rock 'n' Roll",
        cost: 14_000,
        unlock_year: 1950,
        weeks: 2,
        desc_de: "Elektrische Gitarren, Musik-Rhythmus und Jugendkultur.",
        desc_en: "Electric guitars, musical rhythm, and youth culture.",
    },
    ResearchableItem {
        name: "Weltraum",
        cost: 15_000,
        unlock_year: 1951,
        weeks: 2,
        desc_de: "Raumfahrt, ferne Galaxien und kosmische Erkundung.",
        desc_en: "Spaceflight, distant galaxies, and cosmic exploration.",
    },
    ResearchableItem {
        name: "Rennwagen",
        cost: 16_000,
        unlock_year: 1955,
        weeks: 2,
        desc_de: "Motorsport, Boxenstopps und dröhnende Motoren.",
        desc_en: "Motorsports, pit stops, and roaring engines.",
    },
    ResearchableItem {
        name: "Synthesizer",
        cost: 20_000,
        unlock_year: 1968,
        weeks: 2,
        desc_de: "Elektronische Klangerzeugung, Sequencer und Klangexperimente.",
        desc_en: "Electronic sound synthesis, sequencers, and sonic experiments.",
    },
    ResearchableItem {
        name: "Kung-Fu",
        cost: 22_000,
        unlock_year: 1970,
        weeks: 2,
        desc_de: "Fernöstliche Kampfkunst, Turniere und Disziplin.",
        desc_en: "Martial arts tournaments and discipline.",
    },
    ResearchableItem {
        name: "Piraten",
        cost: 24_000,
        unlock_year: 1971,
        weeks: 2,
        desc_de: "Freibeuter, Schatzkarten und Seeschlachten.",
        desc_en: "Privateers, treasure maps, and naval battles.",
    },
    ResearchableItem {
        name: "Horrorhaus",
        cost: 26_000,
        unlock_year: 1975,
        weeks: 2,
        desc_de: "Spukschlösser, knarrende Dielen und psychologischer Grusel.",
        desc_en: "Haunted mansions, creaking floorboards, and psychological terror.",
    },
    ResearchableItem {
        name: "Cyberpunk",
        cost: 30_000,
        unlock_year: 1982,
        weeks: 3,
        desc_de: "Megakonzerne, Neon-Metropolen, Hacker und Synthesizer-Bässe.",
        desc_en: "Megacorporations, neon metropolises, hackers, and synth basslines.",
    },
    ResearchableItem {
        name: "Krankenhaus",
        cost: 32_000,
        unlock_year: 1988,
        weeks: 2,
        desc_de: "Klinik-Management, skurrile Krankheiten und Rettungsdienst.",
        desc_en: "Hospital management, quirky illnesses, and emergency care.",
    },
    ResearchableItem {
        name: "Freizeitpark",
        cost: 34_000,
        unlock_year: 1990,
        weeks: 2,
        desc_de: "Achterbahnen, Park-Architektur und fröhliche Jahrmarkt-Akustik.",
        desc_en: "Rollercoasters, park architecture, and lively fairground acoustics.",
    },
    ResearchableItem {
        name: "Zombies",
        cost: 38_000,
        unlock_year: 1996,
        weeks: 3,
        desc_de: "Überlebenskampf in einer von Untoten überrannten Welt.",
        desc_en: "Survival in a world overrun by the undead.",
    },
    ResearchableItem {
        name: "E-Sport",
        cost: 42_000,
        unlock_year: 2002,
        weeks: 3,
        desc_de: "Professionelle Liga-Wettkämpfe, Live-Kommentatoren und Arenen.",
        desc_en: "Professional league competitions, live shoutcasting, and arenas.",
    },
    ResearchableItem {
        name: "Sandbox/Voxel",
        cost: 45_000,
        unlock_year: 2005,
        weeks: 3,
        desc_de: "Offene Baukasten-Welten, Crafting und dynamische Naturklänge.",
        desc_en: "Open sandbox worlds, crafting, and dynamic nature sounds.",
    },
    ResearchableItem {
        name: "KI-Utopie",
        cost: 50_000,
        unlock_year: 2020,
        weeks: 3,
        desc_de: "Vernetzte künstliche Intelligenzen, Bewusstsein und Zukunftsmusik.",
        desc_en: "Networked artificial intelligence, consciousness, and futuristic sound.",
    },
    ResearchableItem {
        name: "Neural-Link",
        cost: 55_000,
        unlock_year: 2025,
        weeks: 4,
        desc_de: "Direkte Gedankensteuerung und synästhetische Klangwelten.",
        desc_en: "Direct neural interface and synesthetic soundscapes.",
    },
];

/// Returns a completely logical compatibility rating (0..=3) between any Topic and Genre:
/// - 3 = Perfekte Synergie! (Super)
/// - 2 = Gute Kombination (Good)
/// - 1 = Solide Kombination (Okay)
/// - 0 = Unpassende Kombination (Poor)
pub fn get_compatibility(topic: &str, genre: &str) -> u8 {
    match (topic, genre) {
        // Radio-Drama & Hörspiel
        ("Radio-Drama", "Abenteuer" | "Horror") => 3,
        ("Radio-Drama", "RPG" | "Puzzle" | "Casual") => 2,
        ("Radio-Drama", "Strategie" | "Simulation") => 1,
        ("Radio-Drama", _) => 0,

        // Detektiv & Spionage
        ("Detektiv" | "Spionage", "Abenteuer" | "Puzzle") => 3,
        ("Detektiv" | "Spionage", "Strategie" | "RPG" | "Action" | "Horror") => 2,
        ("Detektiv" | "Spionage", "Simulation" | "Casual") => 1,
        ("Detektiv" | "Spionage", _) => 0,

        // Musik-Themen (Swing, Rock 'n' Roll, Synthesizer)
        ("Swing-Musik" | "Rock 'n' Roll" | "Synthesizer", "Casual" | "Puzzle") => 3,
        ("Swing-Musik" | "Rock 'n' Roll" | "Synthesizer", "Simulation" | "Abenteuer" | "Action") => 2,
        ("Swing-Musik" | "Rock 'n' Roll" | "Synthesizer", "RPG" | "Strategie") => 1,
        ("Swing-Musik" | "Rock 'n' Roll" | "Synthesizer", _) => 0,

        // Abenteuer-Reise & Piraten
        ("Abenteuer-Reise" | "Piraten", "Abenteuer" | "Action" | "RPG") => 3,
        ("Abenteuer-Reise" | "Piraten", "Strategie" | "Simulation" | "Puzzle") => 2,
        ("Abenteuer-Reise" | "Piraten", "Casual" | "Kampfspiel") => 1,
        ("Abenteuer-Reise" | "Piraten", _) => 0,

        // Schach & Kryptografie
        ("Schach" | "Kryptografie", "Puzzle" | "Strategie") => 3,
        ("Schach" | "Kryptografie", "Simulation" | "Casual") => 2,
        ("Schach" | "Kryptografie", "Abenteuer" | "RPG") => 1,
        ("Schach" | "Kryptografie", _) => 0,

        // Fantasy & Mittelalter
        ("Fantasy" | "Mittelalter", "RPG" | "Abenteuer" | "Strategie") => 3,
        ("Fantasy" | "Mittelalter", "Action" | "Kampfspiel" | "Simulation") => 2,
        ("Fantasy" | "Mittelalter", "Puzzle" | "Horror" | "Casual") => 1,
        ("Fantasy" | "Mittelalter", _) => 0,

        // Sci-Fi, Weltraum, Cyberpunk, Mars-Invasion, KI-Utopie, Neural-Link
        (
            "Sci-Fi" | "Weltraum" | "Cyberpunk" | "Mars-Invasion" | "KI-Utopie" | "Neural-Link",
            "Action" | "RPG" | "Strategie" | "Simulation",
        ) => 3,
        (
            "Sci-Fi" | "Weltraum" | "Cyberpunk" | "Mars-Invasion" | "KI-Utopie" | "Neural-Link",
            "Abenteuer" | "Horror" | "Puzzle",
        ) => 2,
        (
            "Sci-Fi" | "Weltraum" | "Cyberpunk" | "Mars-Invasion" | "KI-Utopie" | "Neural-Link",
            "Rennspiel" | "Kampfspiel" | "Casual",
        ) => 1,
        ("Sci-Fi" | "Weltraum" | "Cyberpunk" | "Mars-Invasion" | "KI-Utopie" | "Neural-Link", _) => 0,

        // Sport & E-Sport
        ("Sport" | "E-Sport", "Sport" | "Simulation") => 3,
        ("Sport" | "E-Sport", "Action" | "Strategie" | "Casual" | "Rennspiel" | "Kampfspiel") => 2,
        ("Sport" | "E-Sport", "RPG" | "Puzzle") => 1,
        ("Sport" | "E-Sport", _) => 0,

        // Rennwagen & Rennen
        ("Rennwagen" | "Rennen", "Rennspiel" | "Simulation" | "Sport") => 3,
        ("Rennwagen" | "Rennen", "Action" | "Casual") => 2,
        ("Rennwagen" | "Rennen", "Strategie") => 1,
        ("Rennwagen" | "Rennen", _) => 0,

        // Eisenbahn, Krankenhaus, Freizeitpark, U-Boot
        (
            "Eisenbahn" | "Krankenhaus" | "Freizeitpark" | "U-Boot",
            "Simulation" | "Strategie",
        ) => 3,
        (
            "Eisenbahn" | "Krankenhaus" | "Freizeitpark" | "U-Boot",
            "Puzzle" | "Casual" | "Abenteuer",
        ) => 2,
        ("Eisenbahn" | "Krankenhaus" | "Freizeitpark" | "U-Boot", "Action") => 1,
        ("Eisenbahn" | "Krankenhaus" | "Freizeitpark" | "U-Boot", _) => 0,

        // Horrorhaus & Zombies
        ("Horrorhaus" | "Zombies", "Horror" | "Action" | "Abenteuer") => 3,
        ("Horrorhaus" | "Zombies", "RPG" | "Strategie" | "Puzzle") => 2,
        ("Horrorhaus" | "Zombies", "Simulation" | "Kampfspiel") => 1,
        ("Horrorhaus" | "Zombies", _) => 0,

        // Kung-Fu
        ("Kung-Fu", "Kampfspiel" | "Action") => 3,
        ("Kung-Fu", "RPG" | "Abenteuer" | "Sport") => 2,
        ("Kung-Fu", "Casual" | "Strategie") => 1,
        ("Kung-Fu", _) => 0,

        // Sandbox/Voxel
        ("Sandbox/Voxel", "Simulation" | "Abenteuer" | "Casual") => 3,
        ("Sandbox/Voxel", "RPG" | "Strategie" | "Puzzle" | "Action") => 2,
        ("Sandbox/Voxel", _) => 1,

        // Default sensible fallback
        _ => 2,
    }
}

/// Ideal slider values (summing to 30) for each Genre.
/// Notice how Sound is always meaningful in Audio Studio Tycoon!
pub fn get_ideal_sliders(genre: &str) -> [u8; 6] {
    // Order: ["Gameplay", "Grafik", "Sound", "Story", "KI", "Welt"]
    match genre {
        "Abenteuer" => [5, 4, 7, 8, 2, 4],   // Focus: Story (8), Sound (7), Gameplay (5)
        "Puzzle" => [9, 3, 6, 2, 7, 3],      // Focus: Gameplay (9), KI/Logik (7), Sound (6)
        "Casual" => [8, 4, 8, 2, 4, 4],      // Focus: Gameplay (8), Sound/Musik (8)
        "Strategie" => [7, 3, 5, 3, 8, 4],   // Focus: KI/Taktik (8), Gameplay (7), Sound (5)
        "Simulation" => [7, 4, 6, 2, 6, 5],  // Focus: Gameplay (7), Sound (6), KI (6), Welt (5)
        "RPG" => [5, 4, 6, 8, 3, 4],         // Focus: Story (8), Sound (6), Gameplay (5), Welt (4)
        "Action" => [8, 6, 7, 2, 4, 3],      // Focus: Gameplay (8), Sound (7), Grafik (6)
        "Sport" => [8, 5, 6, 1, 6, 4],       // Focus: Gameplay (8), Sound/Stadion (6), KI (6)
        "Rennspiel" => [8, 6, 7, 1, 5, 3],   // Focus: Gameplay (8), Sound/Motor (7), Grafik (6)
        "Horror" => [5, 5, 9, 6, 2, 3],      // Focus: Sound/Grusel-Akustik (9!), Story (6), Gameplay (5)
        "Kampfspiel" => [9, 6, 7, 1, 5, 2],  // Focus: Gameplay (9), Sound/Treffer (7), Grafik (6)
        _ => [5, 5, 5, 5, 5, 5],
    }
}

#[derive(Debug, Clone)]
pub struct EngineFeatureSpec {
    pub name: &'static str,
    pub category: &'static str,
    pub cost: i64,
    pub tech_bonus: u32,
    pub unlock_year: u32,
}

pub const ENGINE_FEATURES: &[EngineFeatureSpec] = &[
    EngineFeatureSpec { name: "Papier- & Relais-Logik", category: "Technik", cost: 2_000, tech_bonus: 10, unlock_year: 1930 },
    EngineFeatureSpec { name: "Foley-Geräuschkulisse", category: "Sound", cost: 2_500, tech_bonus: 15, unlock_year: 1930 },
    EngineFeatureSpec { name: "Magnetband-Aufnahme", category: "Sound", cost: 4_000, tech_bonus: 20, unlock_year: 1935 },
    EngineFeatureSpec { name: "Vakuum-Röhren-Verstärker", category: "Technik", cost: 8_000, tech_bonus: 20, unlock_year: 1941 },
    EngineFeatureSpec { name: "Mehrspur-Tonband (Multitrack)", category: "Sound", cost: 15_000, tech_bonus: 25, unlock_year: 1948 },
    EngineFeatureSpec { name: "Stereo-Panorama-Mischung", category: "Sound", cost: 25_000, tech_bonus: 30, unlock_year: 1958 },
    EngineFeatureSpec { name: "Moog Analog-Synthesizer", category: "Sound", cost: 35_000, tech_bonus: 35, unlock_year: 1964 },
    EngineFeatureSpec { name: "PCM Digital-Audio", category: "Sound", cost: 45_000, tech_bonus: 40, unlock_year: 1972 },
    EngineFeatureSpec { name: "FM-Klangsynthese", category: "Sound", cost: 55_000, tech_bonus: 45, unlock_year: 1980 },
    EngineFeatureSpec { name: "MIDI-Sequencer-Standard", category: "Sound", cost: 65_000, tech_bonus: 50, unlock_year: 1983 },
    EngineFeatureSpec { name: "Savegame-Speicherbatterie", category: "Gameplay", cost: 60_000, tech_bonus: 35, unlock_year: 1985 },
    EngineFeatureSpec { name: "Wavetable-Sampling", category: "Sound", cost: 75_000, tech_bonus: 55, unlock_year: 1988 },
    EngineFeatureSpec { name: "CD-Audio & Vollvertonung", category: "Sound", cost: 90_000, tech_bonus: 65, unlock_year: 1994 },
    EngineFeatureSpec { name: "VST-Effekt-Pipeline", category: "Sound", cost: 110_000, tech_bonus: 70, unlock_year: 1996 },
    EngineFeatureSpec { name: "A*-Pfadfindung & Taktik-KI", category: "KI", cost: 100_000, tech_bonus: 50, unlock_year: 1997 },
    EngineFeatureSpec { name: "Binaurales HRTF 3D-Audio", category: "Sound", cost: 130_000, tech_bonus: 85, unlock_year: 2000 },
    EngineFeatureSpec { name: "Dynamische Physik-Akustik", category: "Technik", cost: 145_000, tech_bonus: 80, unlock_year: 2005 },
    EngineFeatureSpec { name: "Dolby Atmos Objekt-Audio", category: "Sound", cost: 170_000, tech_bonus: 100, unlock_year: 2012 },
    EngineFeatureSpec { name: "VR Spatial-Audio-Raytracing", category: "Sound", cost: 200_000, tech_bonus: 120, unlock_year: 2017 },
    EngineFeatureSpec { name: "Prozedurale KI-Klangwelt", category: "KI", cost: 240_000, tech_bonus: 140, unlock_year: 2022 },
    EngineFeatureSpec { name: "Neural-Sync Synästhesie", category: "Sound", cost: 300_000, tech_bonus: 180, unlock_year: 2026 },
];

pub const RESEARCHABLE_TECHNOLOGIES: &[ResearchableItem] = &[
    ResearchableItem {
        name: "Studios & Schallkabinen",
        cost: 12_000,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Schallisolierte Aufnahmekabinen (+10% Sound-Qualität).",
        desc_en: "Soundproof recording booths (+10% sound quality).",
    },
    ResearchableItem {
        name: "Radio-Werbung",
        cost: 10_000,
        unlock_year: 1930,
        weeks: 2,
        desc_de: "Steigert die Marketing-Effizienz um +15%.",
        desc_en: "Increases marketing efficiency by +15%.",
    },
    ResearchableItem {
        name: "Automatische Qualitätsprüfung (QA)",
        cost: 20_000,
        unlock_year: 1945,
        weeks: 3,
        desc_de: "Reduziert neu entstehende Bugs in Projekten um 25%.",
        desc_en: "Reduces newly generated bugs in projects by 25%.",
    },
    ResearchableItem {
        name: "Audio-Meisterschaft",
        cost: 40_000,
        unlock_year: 1955,
        weeks: 3,
        desc_de: "Meisterhafte Mastering-Technik (+15% Bewertung auf Sound).",
        desc_en: "Masterful audio mastering (+15% review bonus on sound).",
    },
    ResearchableItem {
        name: "Hardware-Labor",
        cost: 75_000,
        unlock_year: 1975,
        weeks: 4,
        desc_de: "Schaltet die Entwicklung eigener Soundkarten und Konsolen frei.",
        desc_en: "Unlocks development of custom soundcards and consoles.",
    },
    ResearchableItem {
        name: "CD-Presswerk",
        cost: 80_000,
        unlock_year: 1982,
        weeks: 4,
        desc_de: "Senkt die Produktionskosten und steigert Verkaufszahlen um +15%.",
        desc_en: "Lowers manufacturing costs and boosts sales by +15%.",
    },
    ResearchableItem {
        name: "Gesundes Arbeiten & Ergonomie",
        cost: 45_000,
        unlock_year: 1985,
        weeks: 3,
        desc_de: "Verringert Erschöpfung und Burnout-Risiko im Team um 30%.",
        desc_en: "Reduces team fatigue and burnout risk by 30%.",
    },
    ResearchableItem {
        name: "Digitaler Eigenvertrieb",
        cost: 120_000,
        unlock_year: 2000,
        weeks: 4,
        desc_de: "Steigert den Netto-Gewinn pro verkauftem Spiel um +20%.",
        desc_en: "Increases net profit per copy sold by +20%.",
    },
    ResearchableItem {
        name: "Live-Service Architektur",
        cost: 180_000,
        unlock_year: 2004,
        weeks: 5,
        desc_de: "Schaltet MMO- und Live-Service-Großprojekte frei.",
        desc_en: "Unlocks MMO and live-service large-scale projects.",
    },
    ResearchableItem {
        name: "KI-Soundtrack & Mastering",
        cost: 220_000,
        unlock_year: 2022,
        weeks: 5,
        desc_de: "Beschleunigt die Entwicklungsgeschwindigkeit um +25%.",
        desc_en: "Accelerates development speed by +25%.",
    },
];

#[derive(Debug, Clone)]
pub struct OfficeLevelSpec {
    pub level: usize,
    pub name_de: &'static str,
    pub name_en: &'static str,
    pub max_employees: usize,
    pub upgrade_cost: i64,
    pub monthly_rent: i64,
    pub prestige: u32,
}

pub const OFFICE_LEVELS: &[OfficeLevelSpec] = &[
    OfficeLevelSpec {
        level: 0,
        name_de: "Hinterhof-Tonkabine (Garage)",
        name_en: "Backyard Sound Booth (Garage)",
        max_employees: 2,
        upgrade_cost: 0,
        monthly_rent: 200,
        prestige: 1,
    },
    OfficeLevelSpec {
        level: 1,
        name_de: "Kleines Tonstudio",
        name_en: "Small Recording Studio",
        max_employees: 4,
        upgrade_cost: 35_000,
        monthly_rent: 1_000,
        prestige: 2,
    },
    OfficeLevelSpec {
        level: 2,
        name_de: "Professionelles Funkhaus-Studio",
        name_en: "Professional Broadcast Studio",
        max_employees: 8,
        upgrade_cost: 120_000,
        monthly_rent: 3_500,
        prestige: 4,
    },
    OfficeLevelSpec {
        level: 3,
        name_de: "Großes Audio- & Entwicklungszentrum",
        name_en: "Large Audio & Dev Center",
        max_employees: 14,
        upgrade_cost: 400_000,
        monthly_rent: 9_000,
        prestige: 7,
    },
    OfficeLevelSpec {
        level: 4,
        name_de: "Internationaler Audio-Campus (HQ)",
        name_en: "International Audio Campus (HQ)",
        max_employees: 24,
        upgrade_cost: 1_200_000,
        monthly_rent: 22_000,
        prestige: 12,
    },
];

#[derive(Debug, Clone)]
pub struct YearEventSpec {
    pub year: u32,
    pub title_de: &'static str,
    pub title_en: &'static str,
    pub desc_de: &'static str,
    pub desc_en: &'static str,
    pub trend_topic: Option<&'static str>,
    pub trend_genre: Option<&'static str>,
    pub sales_multi_delta: f64,
    pub cash_grant: i64,
    pub hype_bonus: f64,
}

pub fn get_year_event(year: u32) -> YearEventSpec {
    match year {
        1930 => YearEventSpec {
            year: 1930,
            title_de: "1930: Aufstieg des Rundfunks & Hörspiels",
            title_en: "1930: Rise of Radio Broadcasting & Audio Drama",
            desc_de: "Trotz der Weltwirtschaftskrise boomt das Radio als Unterhaltungsmedium. Radio-Dramen und Detektiv-Hörspiele begeistern Millionen Hörer!",
            desc_en: "Despite the Great Depression, radio booms as an entertainment medium. Radio dramas and detective stories captivate millions!",
            trend_topic: Some("Radio-Drama"),
            trend_genre: Some("Abenteuer"),
            sales_multi_delta: 0.0,
            cash_grant: 0,
            hype_bonus: 10.0,
        },
        1935 => YearEventSpec {
            year: 1935,
            title_de: "1935: Vorstellung des Magnetophon-Tonbands",
            title_en: "1935: Introduction of Magnetophon Tape Recording",
            desc_de: "Auf der Berliner Funkausstellung wird das Magnetband vorgestellt. Tonstudios können Produktionen nun vorab aufzeichnen und schneiden!",
            desc_en: "Magnetic tape recording is unveiled at the Berlin Radio Exhibition, allowing studios to record and edit productions!",
            trend_topic: Some("Detektiv"),
            trend_genre: Some("Puzzle"),
            sales_multi_delta: 0.1,
            cash_grant: 0,
            hype_bonus: 15.0,
        },
        1938 => YearEventSpec {
            year: 1938,
            title_de: "1938: Krieg der Welten erschüttert das Radio",
            title_en: "1938: War of the Worlds Shakes Radio",
            desc_de: "Orson Welles' realistisches Sci-Fi-Hörspiel löst einen riesigen Boom für Mars-Invasion und Action-Hörspiele aus!",
            desc_en: "Orson Welles' realistic sci-fi broadcast triggers a massive boom for Mars Invasion and action audio productions!",
            trend_topic: Some("Mars-Invasion"),
            trend_genre: Some("Action"),
            sales_multi_delta: 0.15,
            cash_grant: 0,
            hype_bonus: 25.0,
        },
        1941 => YearEventSpec {
            year: 1941,
            title_de: "1941: Konrad Zuse präsentiert die Z3",
            title_en: "1941: Konrad Zuse Presents the Z3 Computer",
            desc_de: "Der erste frei programmierbare Rechner eröffnet das Zeitalter digitaler Logik und Kryptografie.",
            desc_en: "The first programmable computer opens the era of digital logic and cryptography.",
            trend_topic: Some("Kryptografie"),
            trend_genre: Some("Strategie"),
            sales_multi_delta: 0.05,
            cash_grant: 0,
            hype_bonus: 20.0,
        },
        1948 => YearEventSpec {
            year: 1948,
            title_de: "1948: Wirtschaftsförderung & Die Vinyl-Langspielplatte",
            title_en: "1948: Reconstruction Grant & The Vinyl LP",
            desc_de: "Die 33-RPM Vinyl-LP revolutioniert den Tonträgermarkt. Dein Studio erhält 10.000 EUR Aufbauförderung!",
            desc_en: "The 33 RPM Vinyl LP revolutionizes audio media. Your studio receives a 10,000 EUR reconstruction grant!",
            trend_topic: Some("Swing-Musik"),
            trend_genre: Some("Casual"),
            sales_multi_delta: 0.2,
            cash_grant: 10_000,
            hype_bonus: 20.0,
        },
        1954 => YearEventSpec {
            year: 1954,
            title_de: "1954: Transistorradio & Fußball-Weltmeisterschaft",
            title_en: "1954: Pocket Transistor Radio & World Cup Fever",
            desc_de: "Tragbare Transistorradios und das Wunder von Bern sorgen für Rekordumsätze bei Sport- und Unterhaltungsproduktionen.",
            desc_en: "Portable transistor radios and World Cup fever drive record sales for sports and entertainment productions.",
            trend_topic: Some("Sport"),
            trend_genre: Some("Sport"),
            sales_multi_delta: 0.15,
            cash_grant: 0,
            hype_bonus: 25.0,
        },
        1963 => YearEventSpec {
            year: 1963,
            title_de: "1963: Die Kompaktkassette (MC) erobert die Welt",
            title_en: "1963: The Compact Cassette Conquers the World",
            desc_de: "Philips stellt die Kompaktkassette vor – perfekt für Hörspiele und später auch als Datenspeicher für Heimcomputer!",
            desc_en: "Philips introduces the Compact Cassette – ideal for audio dramas and later home computer data storage!",
            trend_topic: Some("Spionage"),
            trend_genre: Some("Abenteuer"),
            sales_multi_delta: 0.2,
            cash_grant: 0,
            hype_bonus: 20.0,
        },
        1972 => YearEventSpec {
            year: 1972,
            title_de: "1972: Arcade-Boom & Magnavox Odyssey",
            title_en: "1972: Arcade Boom & Magnavox Odyssey",
            desc_de: "Videospiele und elektronische Klänge erobern Spielhallen und Wohnzimmer!",
            desc_en: "Video games and electronic soundscapes conquer arcades and living rooms!",
            trend_topic: Some("Weltraum"),
            trend_genre: Some("Action"),
            sales_multi_delta: 0.25,
            cash_grant: 0,
            hype_bonus: 35.0,
        },
        1982 => YearEventSpec {
            year: 1982,
            title_de: "1982: Commodore 64 (SID-Chip) & Die Audio-CD",
            title_en: "1982: Commodore 64 (SID Chip) & The Audio CD",
            desc_de: "Der SID-Synthesizer im C64 und die Einführung der Compact Disc läuten das goldene Zeitalter der Spielemusik ein!",
            desc_en: "The C64 SID synthesizer and the Compact Disc usher in the golden age of game music!",
            trend_topic: Some("Cyberpunk"),
            trend_genre: Some("RPG"),
            sales_multi_delta: 0.25,
            cash_grant: 0,
            hype_bonus: 40.0,
        },
        1995 => YearEventSpec {
            year: 1995,
            title_de: "1995: MP3, 3D-Konsolen & Erste SoundCon Messe",
            title_en: "1995: MP3, 3D Consoles & First SoundCon Expo",
            desc_de: "CD-ROM-Konsolen, MP3-Kompression und die Eröffnung der SoundCon Messe bringen gigantisches Wachstum!",
            desc_en: "CD-ROM consoles, MP3 compression, and the launch of the SoundCon Expo bring massive growth!",
            trend_topic: Some("Fantasy"),
            trend_genre: Some("RPG"),
            sales_multi_delta: 0.3,
            cash_grant: 0,
            hype_bonus: 50.0,
        },
        2003 => YearEventSpec {
            year: 2003,
            title_de: "2003: Digitaler Vertrieb & Online-Plattformen",
            title_en: "2003: Digital Distribution & Online Platforms",
            desc_de: "Studios können ihre Spiele und Hörspiele nun weltweit direkt über das Internet vertreiben!",
            desc_en: "Studios can now distribute their games and audio productions directly worldwide via the Internet!",
            trend_topic: Some("E-Sport"),
            trend_genre: Some("Action"),
            sales_multi_delta: 0.25,
            cash_grant: 0,
            hype_bonus: 40.0,
        },
        2016 => YearEventSpec {
            year: 2016,
            title_de: "2016: VR-Revolution & Binaurales 3D-Audio",
            title_en: "2016: VR Revolution & Binaural 3D Audio",
            desc_de: "Räumliches 3D-Audio wird zum wichtigsten Immersionsfaktor für moderne Spiele und Virtual Reality.",
            desc_en: "Spatial 3D audio becomes the key immersion factor for modern games and Virtual Reality.",
            trend_topic: Some("Sci-Fi"),
            trend_genre: Some("Simulation"),
            sales_multi_delta: 0.2,
            cash_grant: 0,
            hype_bonus: 45.0,
        },
        2026 => YearEventSpec {
            year: 2026,
            title_de: "2026: Neural-Audio & Synästhetische Immersion",
            title_en: "2026: Neural Audio & Synesthetic Immersion",
            desc_de: "Die Neural-Box 1 ermöglicht direkte kortikale Klangwelten – der Höhepunkt der Audio-Evolution (Endlosspiel aktiv)!",
            desc_en: "The Neural-Box 1 enables direct cortical soundscapes – the pinnacle of audio evolution (Endless mode active)!",
            trend_topic: Some("Neural-Link"),
            trend_genre: Some("RPG"),
            sales_multi_delta: 0.3,
            cash_grant: 50_000,
            hype_bonus: 60.0,
        },
        other => {
            let topics = START_TOPICS;
            let genres = GENRES;
            let t = topics[(other as usize) % topics.len()];
            let g = genres[(other as usize * 3) % genres.len()];
            YearEventSpec {
                year: other,
                title_de: "Neues Geschäftsjahr & Markttrend-Wechsel",
                title_en: "New Fiscal Year & Market Trend Shift",
                desc_de: "Die Hörerschaft und Spieler suchen nach frischen Ideen im neuen Jahr.",
                desc_en: "Listeners and players are looking for fresh ideas in the new year.",
                trend_topic: Some(t),
                trend_genre: Some(g),
                sales_multi_delta: 0.02,
                cash_grant: 0,
                hype_bonus: 5.0,
            }
        }
    }
}
