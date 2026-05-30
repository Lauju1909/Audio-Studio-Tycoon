import json
import codecs

# We can import translations directly
import translations

en_dict = translations.TRANSLATIONS['en']
de_dict = translations.TRANSLATIONS['de']

missing = {k: v for k, v in en_dict.items() if k not in de_dict}

if missing:
    with codecs.open('translations.py', 'r', 'utf-8') as f:
        content = f.read()
    
    # We will just append the missing keys at the very beginning of 'de' dictionary
    # by replacing '\"de\": {'
    
    adds = ''
    for k, v in missing.items():
        val_str = json.dumps(v, ensure_ascii=False)
        adds += f'        \"{k}\": {val_str},\n'
        
    content = content.replace('\"de\": {', '\"de\": {\n' + adds)
    
    with codecs.open('translations.py', 'w', 'utf-8') as f:
        f.write(content)
    print(f'Added {len(missing)} missing keys to de')
else:
    print('No keys missing')
