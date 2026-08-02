
with open('menus/hardware.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add HardwareTypeSelectMenu at the top
hw_type_menu = """
class HardwareTypeSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Hardware-Art wählen", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': "Soundkarte", 'action': self._select_soundcard}
        ]
        if self.game_state.is_feature_unlocked("vr_headset"):
            self.options.append({'text': "VR-Brille", 'action': self._select_vr})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hardware_menu"})
        
    def _select_soundcard(self):
        self.game_state.temp_hw_type = "soundcard"
        return "hardware_create_name"
        
    def _select_vr(self):
        self.game_state.temp_hw_type = "vr"
        return "hardware_create_name"
"""

if "class HardwareTypeSelectMenu" not in content:
    content = content.replace("class HardwareLabMenu(Menu):", hw_type_menu + "\nclass HardwareLabMenu(Menu):")

# Modify HardwareLabMenu to redirect to HardwareTypeSelectMenu
target_create = "self.options.append({'text': gs.get_text('hardware_opt_develop'), 'action': lambda: \"hardware_create_name\"})"
replace_create = "self.options.append({'text': gs.get_text('hardware_opt_develop'), 'action': lambda: \"hardware_type_select\" if gs.is_feature_unlocked('vr_headset') else \"hardware_create_name\"})"
if target_create in content:
    content = content.replace(target_create, replace_create)

# Modify SoundCardCreateMenu to handle VR names
target_name = 'prefixes = ["Sound Blaster", "Gravis UltraSound", "AdLib", "Sound Canvas", "AWE", "Covox Speech", "WaveBlaster"]\n        suffixes = ["1.0", "2.0", "Pro", "16", "32", "64", "Gold", "Classic", "Max", "Ultra"]\n        return f"{random.choice(prefixes)} {random.choice(suffixes)}"'
replace_name = """hw_type = getattr(self.game_state, 'temp_hw_type', 'soundcard')
        if hw_type == "vr":
            prefixes = ["Oculus", "Vive", "Index", "Quest", "PSVR", "Gear"]
            suffixes = ["Rift", "Pro", "2", "3", "S", "Elite"]
            return f"{random.choice(prefixes)} {random.choice(suffixes)}"
        else:
            prefixes = ["Sound Blaster", "Gravis UltraSound", "AdLib", "Sound Canvas", "AWE", "Covox Speech", "WaveBlaster"]
            suffixes = ["1.0", "2.0", "Pro", "16", "32", "64", "Gold", "Classic", "Max", "Ultra"]
            return f"{random.choice(prefixes)} {random.choice(suffixes)}\""""
if target_name in content:
    content = content.replace(target_name, replace_name)

# Modify SoundCardFeaturesMenu to load VR features
target_features = """AVAILABLE_FEATURES = [
        {"id": "f_16bit", "name": "16-Bit Audio", "cost": 50000, "year": 1990},
        {"id": "f_midi", "name": "Hardware MIDI Synth", "cost": 150000, "year": 1992},
        {"id": "f_3d_sound", "name": "3D Spatial Audio", "cost": 300000, "year": 1996},
        {"id": "f_optical", "name": "Optischer Ausgang (SPDIF)", "cost": 450000, "year": 1998},
        {"id": "f_7_1", "name": "7.1 Surround", "cost": 600000, "year": 2002},
        {"id": "f_dsd", "name": "DSD (Direct Stream Digital)", "cost": 1000000, "year": 2006},
    ]"""
replace_features = """AVAILABLE_FEATURES = [
        {"id": "f_16bit", "name": "16-Bit Audio", "cost": 50000, "year": 1990},
        {"id": "f_midi", "name": "Hardware MIDI Synth", "cost": 150000, "year": 1992},
        {"id": "f_3d_sound", "name": "3D Spatial Audio", "cost": 300000, "year": 1996},
        {"id": "f_optical", "name": "Optischer Ausgang (SPDIF)", "cost": 450000, "year": 1998},
        {"id": "f_7_1", "name": "7.1 Surround", "cost": 600000, "year": 2002},
        {"id": "f_dsd", "name": "DSD (Direct Stream Digital)", "cost": 1000000, "year": 2006},
    ]
    VR_FEATURES = [
        {"id": "vr_oled", "name": "OLED Display", "cost": 2000000, "year": 2016},
        {"id": "vr_inside_out", "name": "Inside-Out Tracking", "cost": 3000000, "year": 2018},
        {"id": "vr_wireless", "name": "Wireless Link", "cost": 4500000, "year": 2019},
        {"id": "vr_eye_tracking", "name": "Eye Tracking (Foveated Rendering)", "cost": 6000000, "year": 2021},
    ]"""
if target_features in content:
    content = content.replace(target_features, replace_features)

target_filter = '        for f in self.AVAILABLE_FEATURES:\n            if gs.get_calendar_year() >= f["year"]:'
replace_filter = """        hw_type = getattr(gs, 'temp_hw_type', 'soundcard')
        feats = self.VR_FEATURES if hw_type == 'vr' else self.AVAILABLE_FEATURES
        for f in feats:
            if gs.get_calendar_year() >= f["year"]:"""
if target_filter in content:
    content = content.replace(target_filter, replace_filter)

target_total = 'total_cost = sum(f["cost"] for f in self.AVAILABLE_FEATURES if f["id"] in self.selected_techs)'
replace_total = """hw_type = getattr(self.game_state, 'temp_hw_type', 'soundcard')
        feats = self.VR_FEATURES if hw_type == 'vr' else self.AVAILABLE_FEATURES
        total_cost = sum(f["cost"] for f in feats if f["id"] in self.selected_techs)"""
if target_total in content:
    content = content.replace(target_total, replace_total)
    
target_start = '        proj = SoundCardProject(name, self.selected_techs, total_cost)'
replace_start = """        hw_type = getattr(gs, 'temp_hw_type', 'soundcard')
        proj = SoundCardProject(name, self.selected_techs, total_cost)
        proj.hw_type = hw_type"""
if target_start in content:
    content = content.replace(target_start, replace_start)

with open('menus/hardware.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched menus/hardware.py for VR")
