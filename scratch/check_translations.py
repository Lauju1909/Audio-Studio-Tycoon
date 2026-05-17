import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translations


keys_to_check = [
    'review_prefix', 'review_intro_1', 'review_intro_2', 'review_intro_3', 'review_intro_4', 'review_intro_5',
    'review_pos_1', 'review_pos_2', 'review_pos_3', 'review_neg_1', 'review_neg_2', 'review_neg_3',
    'review_bad_gameplay', 'review_good_gameplay', 'review_concl_1', 'review_concl_2'
]

langs = ['de', 'en']
for lang in langs:
    print(f"--- Language: {lang} ---")
    translations.set_language(lang)
    for key in keys_to_check:
        text = translations.get_text(key)
        if text == f"[{key}]":
            print(f"MISSING: {key}")
        else:
            print(f"OK: {key} = {text[:30]}...")
