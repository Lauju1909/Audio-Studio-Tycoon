import translations

de_keys = set(translations.TRANSLATIONS['de'].keys())
en_keys = set(translations.TRANSLATIONS['en'].keys())

missing_in_de = en_keys - de_keys
missing_in_en = de_keys - en_keys

print(f"Missing in DE: {missing_in_de}")
print(f"Missing in EN: {missing_in_en}")
