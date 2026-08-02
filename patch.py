lines = open('logic.py', encoding='utf-8').readlines()
out = []
for i, l in enumerate(lines):
    if 'from managers.conventions import ConventionManager' in l:
        out.append(l)
        out.append('from managers.real_estate import RealEstateManager\n')
    elif 'self.convention_manager = ConventionManager()' in l:
        out.append(l)
        out.append('        self.real_estate_manager = RealEstateManager()\n')
    elif 'self.convention_manager.tick(self)' in l:
        out.append(l)
        out.append('        self.real_estate_manager.tick(self)\n')
    elif '"convention_manager": getattr(self.convention_manager, "to_dict", lambda: {})()' in l:
        out.append(l)
        out.append('            "real_estate_manager": getattr(self.real_estate_manager, "to_dict", lambda: {})(),\n')
    elif 'state.convention_manager.from_dict(data["convention_manager"])' in l:
        out.append(l)
        out.append('            \n')
        out.append('        if hasattr(state.real_estate_manager, "from_dict") and "real_estate_manager" in data:\n')
        out.append('            state.real_estate_manager.from_dict(data["real_estate_manager"])\n')
    else:
        out.append(l)
open('logic.py', 'w', encoding='utf-8').write("".join(out))
