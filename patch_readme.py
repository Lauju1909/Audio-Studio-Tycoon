import sys

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_feature = "\n- **Subsidiary Management & Merchandising (Neu!)**: Voll funktionsfähiges Merch-Menü, Sponsoring von Content Creators und erweiterte Firmenübernahmen (M&A) mit der Möglichkeit, Töchter zu investieren, sie auf eine eigene Konsole festzulegen oder sie aufzulösen."

if "Subsidiary Management & Merchandising" not in content:
    content += new_feature

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)
