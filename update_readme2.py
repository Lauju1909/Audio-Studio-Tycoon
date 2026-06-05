import sys
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find the end of "### Implementierte Features" or similar
if '### Features (Aktuell)' in content:
    idx = content.find('### Features (Aktuell)')
    idx2 = content.find('###', idx + 10)
    
    new_features = '''
- **Merchandising**: Aktive Marken (IPs) können genutzt werden, um T-Shirts, Figuren und Soundtracks zu produzieren. Diese Kampagnen generieren zusätzliches Einkommen und Fan-Hype basierend auf der Stärke der jeweiligen Marke.'''
    
    content = content[:idx2] + new_features + '\n\n' + content[idx2:]
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
