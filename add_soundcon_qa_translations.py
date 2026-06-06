import json

# Update translations.py
with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# English QA
en_qa_translations = """        "soundcon_qa_question_1": "Journalist: 'Will your next game have groundbreaking new audio features?'",
        "soundcon_qa_ans_1_1": "Yes, it will revolutionize the industry! (High risk, high hype)",
        "soundcon_qa_ans_1_2": "We are focusing on solid mechanics. (Safe, low hype)",
        "soundcon_qa_ans_1_3": "No comment. (Neutral)",
        
        "soundcon_qa_question_2": "Journalist: 'Are you planning to support older hardware?'",
        "soundcon_qa_ans_2_1": "We are pushing the boundaries of modern technology! (+Hype, -Prestige)",
        "soundcon_qa_ans_2_2": "Yes, we want everyone to enjoy our games! (+Prestige, +Fans)",
        
        "soundcon_qa_question_3": "Journalist: 'Is there a multiplayer mode planned?'",
        "soundcon_qa_ans_3_1": "Absolutely, with crossplay! (+Hype)",
        "soundcon_qa_ans_3_2": "It will be a strong single-player experience. (+Prestige)",
        
        "soundcon_qa_result_hype": "The crowd goes wild! Hype +{hype}",
        "soundcon_qa_result_prestige": "The critics are impressed. Prestige +{prestige}, Fans +{fans}",
        "soundcon_qa_result_neutral": "The response was moderate. Fans +{fans}",
"""

# German QA
de_qa_translations = """        "soundcon_qa_question_1": "Journalist: 'Wird euer nächstes Spiel bahnbrechende Audio-Features haben?'",
        "soundcon_qa_ans_1_1": "Ja, es wird die Industrie revolutionieren! (Hohes Risiko, viel Hype)",
        "soundcon_qa_ans_1_2": "Wir konzentrieren uns auf solide Mechaniken. (Sicher, wenig Hype)",
        "soundcon_qa_ans_1_3": "Kein Kommentar. (Neutral)",
        
        "soundcon_qa_question_2": "Journalist: 'Plant ihr, ältere Hardware zu unterstützen?'",
        "soundcon_qa_ans_2_1": "Wir reizen moderne Technik voll aus! (+Hype, -Prestige)",
        "soundcon_qa_ans_2_2": "Ja, jeder soll unsere Spiele genießen können! (+Prestige, +Fans)",
        
        "soundcon_qa_question_3": "Journalist: 'Ist ein Multiplayer-Modus geplant?'",
        "soundcon_qa_ans_3_1": "Absolut, inklusive Crossplay! (+Hype)",
        "soundcon_qa_ans_3_2": "Es wird eine starke Singleplayer-Erfahrung. (+Prestige)",
        
        "soundcon_qa_result_hype": "Die Menge tobt! Hype +{hype}",
        "soundcon_qa_result_prestige": "Die Kritiker sind beeindruckt. Prestige +{prestige}, Fans +{fans}",
        "soundcon_qa_result_neutral": "Die Reaktionen waren verhalten. Fans +{fans}",
"""

if "soundcon_qa_question_1" not in content:
    content = content.replace('        "soundcon_qa_success": "Q&A successful.",\n', '        "soundcon_qa_success": "Q&A successful.",\n' + en_qa_translations)
    content = content.replace('        "soundcon_qa_success": "Q&A erfolgreich.",\n', '        "soundcon_qa_success": "Q&A erfolgreich.",\n' + de_qa_translations)
    
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("translations.py updated.")

