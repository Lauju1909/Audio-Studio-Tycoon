# ruff: noqa
import os
import re

BRAIN_DIR = r"C:\Users\lauri\.gemini\antigravity\brain\e61ce625-940f-4ce1-8f44-154988c37952"

# ---------------- EVENTS ----------------
def generate_events():
    with open(os.path.join(BRAIN_DIR, "encyclopedia_events.md"), "r", encoding="utf-8") as f:
        content = f.read()

    events = {}
    for line in content.split('\n'):
        if line.startswith('| ') and not line.startswith('| :'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 3 and parts[0].isdigit():
                year = int(parts[0])
                event_name = parts[1]
                auswirkung = parts[2]
                effect = "hype"
                value = 20
                if any(x in auswirkung for x in ["Sales", "Profit", "Kosten", "$", "€", "Zinsen"]):
                    effect = "money"
                    value = 10000 if "+" in auswirkung else -10000
                elif any(x in auswirkung for x in ["Fans", "Markt", "Trend", "Fieber", "Boom", "Industrie explodiert", "Gigantisch", "Massen"]):
                    effect = "fans"
                    value = 5000 if ("+" in auswirkung or "Trend" in auswirkung or "Boom" in auswirkung or "Gigantisch" in auswirkung) else -5000
                events[year] = {"text": f"{event_name}. {auswirkung}", "effect": effect, "value": value}
    
    out_lines = ["# AUTOMATICALLY GENERATED", "HISTORICAL_YEAR_EVENTS = {"]
    for year, data in sorted(events.items()):
        t = data['text'].replace('"', "'")
        out_lines.append(f'    {year}: {{"text": "{t}", "effect": "{data["effect"]}", "value": {data["value"]}}},')
    out_lines.append("}\n")
    with open("tmp_events.py", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

# ---------------- TOPICS ----------------
def generate_topics():
    with open(os.path.join(BRAIN_DIR, "encyclopedia_topics.md"), "r", encoding="utf-8") as f:
        content = f.read()
    
    topics = []
    for line in content.split('\n'):
        if line.startswith('| ') and not line.startswith('| :'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 4 and parts[0].isdigit():
                year = int(parts[0])
                name = parts[1]
                # Week berechnen: Jahr - 1930 * 48
                week = max(1, (year - 1930) * 48)
                cost = 5000 + (year - 1930) * 500
                topics.append({"name": name, "cost": cost, "week": week, "research_weeks": 2})

    out_lines = ["# AUTOMATICALLY GENERATED", "RESEARCHABLE_TOPICS = ["]
    for t in topics:
        out_lines.append(f'    {{"name": "{t["name"]}", "cost": {t["cost"]}, "week": {t["week"]}, "research_weeks": {t["research_weeks"]}}},')
    out_lines.append("]\n")

    # Compat Matrix - default values 1, with a bit of randomness 
    # to avoid huge hand-written array for 250 topics right now
    # Action, RPG, Sim, Strat, Adv, Puz, Spo, Cas, Hor, Fight, Race
    import random
    random.seed(42)
    out_lines.append("TOPIC_GENRE_COMPAT = {")
    for t in topics:
        vals = [random.randint(0, 3) for _ in range(11)]
        vals_str = ", ".join(f"{v:2d}" for v in vals)
        out_lines.append(f'    "{t["name"]}":[{vals_str}],')
    out_lines.append("}\n")
    
    with open("tmp_topics.py", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

# ---------------- HARDWARE ----------------
def generate_hardware():
    with open(os.path.join(BRAIN_DIR, "encyclopedia_hardware.md"), "r", encoding="utf-8") as f:
        content = f.read()

    platforms = []
    for line in content.split('\n'):
        if line.startswith('| ') and not line.startswith('| :'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            # columns: Jahr | Name | Typ/CPU | ...
            if len(parts) >= 3 and parts[0].isdigit():
                year = int(parts[0])
                name = parts[1].replace("**", "")
                week = max(1, (year - 1930) * 48)
                end_week = week + (10 * 48) # 10 Jahre Lebensdauer
                
                ptype = "Konsole"
                if "PC" in name or "Computer" in name or "UNIVAC" in name or "ENIAC" in name or "EDSAC" in name or "IBM" in name or "C64" in name: ptype = "Heimcomputer"
                if "Boy" in name or "Handheld" in name or "Pocket" in name or "EXP" in name or "Gizmondo" in name or "Switch" in name or "Playdate" in name: ptype = "Handheld"
                if "Cloud" in name: ptype = "Streaming"
                
                market_multi = round(min(10.0, max(1.0, (year - 1930) * 0.15)), 1)
                fee = int(market_multi * 10000)
                if ptype == "Heimcomputer": fee = 0
                
                platforms.append({
                    "name": name, "license_fee": fee, "market_multi": market_multi,
                    "available_week": week, "end_week": end_week, "type": ptype
                })
    
    out_lines = ["# AUTOMATICALLY GENERATED", "PLATFORMS = ["]
    for p in platforms:
        out_lines.append(f'    {{"name": "{p["name"]}", "license_fee": {p["license_fee"]}, "market_multi": {p["market_multi"]}, "available_week": {p["available_week"]}, "end_week": {p["end_week"]}, "type": "{p["type"]}"}},')
    out_lines.append("]\n")
    
    with open("tmp_hardware.py", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

# ---------------- RESEARCH ----------------
def generate_research():
    with open(os.path.join(BRAIN_DIR, "encyclopedia_research.md"), "r", encoding="utf-8") as f:
        content = f.read()

    features = []
    for line in content.split('\n'):
        if line.startswith('| ') and not line.startswith('| :'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 4 and parts[0].isdigit():
                year = int(parts[0])
                name = parts[1].replace("**", "")
                cat = parts[2]
                effect = parts[3]
                desc = parts[4] if len(parts) > 4 else ""
                
                week = max(1, (year - 1930) * 48)
                bonus = 10
                if "+" in effect:
                    try:
                        bonus = int(re.search(r'\d+', effect).group())
                    except:
                        bonus = 50
                
                cost = 1000 + (year - 1930) * 2000
                
                features.append({
                    "category": cat, "name": name, "cost": cost, 
                    "tech_bonus": bonus, "week": week
                })
    
    out_lines = ["# AUTOMATICALLY GENERATED", "ENGINE_FEATURES = ["]
    for f in features:
        out_lines.append(f'    {{"category": "{f["category"]}", "name": "{f["name"]}", "cost": {f["cost"]}, "tech_bonus": {f["tech_bonus"]}, "week": {f["week"]}}},')
    out_lines.append("]\n")
    
    with open("tmp_research.py", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    generate_events()
    generate_topics()
    generate_hardware()
    generate_research()
    print("All python temp files generated.")
