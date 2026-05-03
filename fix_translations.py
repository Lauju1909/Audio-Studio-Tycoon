"""Behebt den Zeilenumbruch-Bug in translations.py."""

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

# Ersetze das fehlerhafte multiline body_new_month (de)
bad_de = '"body_new_month": "Ein neuer Monat hat begonnen: {date}.\n\nAktuelles Kapital: {money:,.0f} EUR\nFans: {fans:,.0f}"'
good_de = '"body_new_month": "Ein neuer Monat hat begonnen: {date}. Aktuelles Kapital: {money:,.0f} EUR. Fans: {fans:,.0f}"'

bad_en = '"body_new_month": "A new month has begun: {date}.\n\nCurrent capital: {money:,.0f} EUR\nFans: {fans:,.0f}"'
good_en = '"body_new_month": "A new month has begun: {date}. Current capital: {money:,.0f} EUR. Fans: {fans:,.0f}"'

content = content.replace(bad_de, good_de)
content = content.replace(bad_en, good_en)

# Ersetze auch das fehlerhafte "subject_monthly_statement" mit dem falschen Zeichen
import re
# Fix das Dash-Zeichen-Problem
content = content.replace('"Ihr Kontoauszug \x00e2\x00 80\x00 93 {date}"', '"Ihr Kontoauszug - {date}"')
# Allgemeiner Fix: seltsame Zeichen im subject_monthly_statement
content = re.sub(
    r'"subject_monthly_statement":\s*"Ihr Kontoauszug[^"]*\{date\}"',
    '"subject_monthly_statement": "Ihr Kontoauszug - {date}"',
    content
)
content = re.sub(
    r'"subject_monthly_statement":\s*"Your Bank Statement[^"]*\{date\}"',
    '"subject_monthly_statement": "Your Bank Statement - {date}"',
    content
)

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done!")
