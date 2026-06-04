import sys

with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_code = '''
from .hardware import HardwareLabMenu, HardwareLicensingMenu, SoundCardCreateMenu, SoundCardFeaturesMenu, SoundCardOverviewMenu
'''
new_import_code = import_code + '''
from .hardware import ConsoleCreateMenu, ConsoleComponentsMenu
'''
content = content.replace(import_code, new_import_code)

dict_code = '''
    "hardware_menu": HardwareLabMenu,
    "hardware_licensing": HardwareLicensingMenu,
    "hardware_create_name": SoundCardCreateMenu,
    "hardware_features": SoundCardFeaturesMenu,
    "hardware_overview": SoundCardOverviewMenu,
'''
new_dict_code = dict_code + '''
    "console_create": ConsoleCreateMenu,
    "console_components": ConsoleComponentsMenu,
'''
content = content.replace(dict_code, new_dict_code)

all_code = '''
    "HardwareOverviewMenu"
]
'''
new_all_code = '''    "HardwareOverviewMenu",
    "ConsoleCreateMenu", "ConsoleComponentsMenu"
]
'''
content = content.replace(all_code, new_all_code)

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched __init__.py")
