import sys
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find the end of "### Implementierte Features" or similar
if '### Features (Aktuell)' in content:
    idx = content.find('### Features (Aktuell)')
    idx2 = content.find('###', idx + 10)
    
    new_features = '''
- **Mitarbeiter-Urlaub & Burnout-System**: Mitarbeiter bauen Fatigue (Erschöpfung) auf, besonders im Crunch. Über das "Urlaub"-Menü können Mitarbeiter zur Erholung in den Urlaub geschickt werden. Ist der Fatigue-Wert bei 100, erkranken sie an Burnout und fallen unkontrolliert länger aus.
- **Game-Updates & DLCs**: Eigene Menüs zur detaillierten Nachbetreuung von Spielen. Es können Patches (Bugs fixen), Content-Updates (Fans/Hype generieren) und kostenpflichtige DLCs (Umsatz ankurbeln) entwickelt werden.'''
    
    content = content[:idx2] + new_features + '\n\n' + content[idx2:]
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
