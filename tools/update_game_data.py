import re

GAME_DATA = r"C:\Users\lauri\.gemini\antigravity\scratch\game_dev_tycoon_2\game_data.py"

def read_tmp(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def inject_or_replace(content, block_name, new_block_content):
    # Finde den start des Blocks, z.B. "BLOCK_NAME = [" oder "BLOCK_NAME = {"
    # und ersetze ihn bis zum nächsten "]" der auf Ebene 0 steht.
    # Da RegEx für geschachtelte Klammern schwer ist, machen wir es simpler:
    
    # regex looking for "BLOCK_NAME = [" or "BLOCK_NAME = {"
    pattern = rf"^{block_name}\s*=\s*[\[{{]"
    match = re.search(pattern, content, re.MULTILINE)
    
    if match:
        start_idx = match.start()
        # finde das korrespondierende Ende
        is_dict = content[match.end()-1] == '{'
        open_char = '{' if is_dict else '['
        close_char = '}' if is_dict else ']'
        
        depth = 0
        end_idx = -1
        for i in range(match.end()-1, len(content)):
            if content[i] == open_char:
                depth += 1
            elif content[i] == close_char:
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
        if end_idx != -1:
            return content[:start_idx] + new_block_content + content[end_idx:]
    
    # Falls nicht gefunden, einfach ans Ende packen
    return content + "\n\n" + new_block_content

def main():
    with open(GAME_DATA, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Lade die Teil-Strings
    events_code = read_tmp("tmp_events.py")
    topics_code = read_tmp("tmp_topics.py")
    hardware_code = read_tmp("tmp_hardware.py")
    research_code = read_tmp("tmp_research.py")
    
    # Extrahiere die spezifischen Definitionen aus den tmp_files, um sie blockweise zu ersetzen.
    # Das ist nur notwendig, falls mehrere in einer Datei stehen (wie beim topics_code)
    
    # events_code ist im wesentlichen nur HISTORICAL_YEAR_EVENTS
    content = inject_or_replace(content, "HISTORICAL_YEAR_EVENTS", events_code.replace("# AUTOMATICALLY GENERATED\n", ""))
    
    # research_code ist ENGINE_FEATURES
    content = inject_or_replace(content, "ENGINE_FEATURES", research_code.replace("# AUTOMATICALLY GENERATED\n", ""))
    
    # Hardware
    content = inject_or_replace(content, "PLATFORMS", hardware_code.replace("# AUTOMATICALLY GENERATED\n", ""))

    # Topics besteht aus RESEARCHABLE_TOPICS und TOPIC_GENRE_COMPAT
    parts = topics_code.split("TOPIC_GENRE_COMPAT = {")
    res_topics = parts[0].replace("# AUTOMATICALLY GENERATED\n", "")
    compat = "TOPIC_GENRE_COMPAT = {" + parts[1]
    
    content = inject_or_replace(content, "RESEARCHABLE_TOPICS", res_topics)
    content = inject_or_replace(content, "TOPIC_GENRE_COMPAT", compat)
    
    # Topic-Array TOPICS aktualisieren
    content = re.sub(r"^TOPICS\s*=\s*\[.*?\]", "TOPICS = START_TOPICS + [t[\"name\"] for t in RESEARCHABLE_TOPICS]", content, flags=re.MULTILINE|re.DOTALL)
    
    with open(GAME_DATA, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("game_data.py erfolgreich aktualisiert!")

if __name__ == "__main__":
    main()
