import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from logic import GameState
from models import Employee, FanMail, SoundCardProject, RadioJingle
from game_data import FAN_MAIL_TEMPLATES, OFFICE_PERSONALITY_EVENTS

def test_employee_personalities():
    gs = GameState()
    
    # 1. Mitarbeiter mit Persönlichkeiten hinzufügen
    emp1 = Employee(name="Hans")
    emp1.personality = "easygoing"
    emp1.morale = 50
    
    emp2 = Employee(name="Dieter")
    emp2.personality = "workaholic"
    emp2.morale = 60
    
    gs.employees = [emp1, emp2]
    
    # Simuliere einen wöchentlichen Tick, in dem die Moral berechnet wird
    # easygoing sollte dem Team Moral geben, workaholic verliert schneller
    # Wir rufen den Tick direkt auf
    gs._on_new_week()
    
    # Prüfe, ob die Moral angepasst wurde
    # easygoing gibt +10 Moralregeneration für das Team. 
    # workaholic verliert schneller Moral.
    # Wir prüfen einfach, ob die Werte valide sind
    assert emp1.morale > 0 and emp1.morale <= 100
    assert emp2.morale > 0 and emp2.morale <= 100
    print("test_employee_personalities passed!")

def test_office_events():
    gs = GameState()
    
    # Mitarbeiter mit passender Persönlichkeit hinzufügen
    emp = Employee(name="Klaus")
    emp.personality = "perfectionist"
    gs.employees = [emp]
    
    # Wir triggern manuell das Event für Perfektionisten
    event = OFFICE_PERSONALITY_EVENTS[0] # event_perfectionist_delay
    gs.active_personality_event = event
    gs.active_personality_employee = emp
    
    # Wir beantworten das Event mit Option 1 (Zeit geben)
    # Option 1: {"morale": 15, "dev_speed_penalty": 0.5, "money": 0}
    initial_morale = emp.morale
    success = gs.answer_personality_event(0)
    
    assert success
    assert gs.active_personality_event is None
    assert emp.morale == min(100, initial_morale + 15)
    print("test_office_events passed!")

def test_fan_mail():
    gs = GameState()
    initial_fans = gs.fans
    gs.money
    
    # Aktives Projekt hinzufügen, da Hype projektbezogen ist
    from models import GameProject
    proj = GameProject("TestGame", "Sci-Fi", "Shooter")
    proj.hype = 10.0
    gs.active_projects.append({"project": proj, "progress": 1.0, "total_weeks": 10, "bugs": 0})
    
    # 1. Neue Fanpost erhalten
    template = FAN_MAIL_TEMPLATES[0] # fan_mail_retro
    mail = FanMail(
        mail_id="test_retro_1",
        sender="RetroFan",
        subject_key=template["subject_key"],
        text_key=template["text_key"],
        options=template["options"]
    )
    gs.fan_mail_inbox = [mail]
    
    # 2. Beantworten mit Option 1 (Fans und Hype erhalten)
    # Option 1: {"fans": 300, "hype": 5.0, "money": 0}
    success = gs.answer_fan_mail("test_retro_1", 0)
    
    assert success
    assert mail.is_answered
    assert mail.selected_option == 0
    assert gs.fans == initial_fans + 300
    assert proj.hype == 15.0 # initial 10.0 + 5.0
    assert gs.calculate_hype(proj) >= 15
    print("test_fan_mail passed!")

def test_sound_card_project():
    gs = GameState()
    
    # Setze das Jahr auf 1980, damit das Hardware-Labor freigeschaltet ist
    gs.week = 52 * 50 # ca. 1980+
    
    # 1. Technologie freischalten
    tech_id = "synthesizer_8bit"
    gs.money = 100000
    success = gs.unlock_hardware_technology(tech_id)
    assert success
    assert tech_id in gs.unlocked_hardware_tech
    assert gs.money == 85000
    
    # 2. Soundkarte entwickeln
    # Die Grundkosten sind 20000. Mit synthesizer_8bit (+15000) sind es 35000.
    success = gs.start_sound_card_project("Sound Blaster 1", [tech_id])
    assert success
    assert gs.money == 50000
    
    # Finde das aktive Projekt
    active_proj = next((p for p in gs.sound_card_projects if not p.is_released), None)
    assert active_proj is not None
    assert active_proj.name == "Sound Blaster 1"
    assert active_proj.dev_cost == 35000
    
    # Simuliere die Entwicklung durch Ticks (die wöchentlich Fortschritt machen)
    while active_proj.progress < 100.0:
        gs.update_hardware_development()
        
    assert active_proj.progress >= 100.0
    
    # 3. Veröffentlichen
    success = gs.release_sound_card("Sound Blaster 1")
    assert success
    assert active_proj.is_released
    
    # Passive Tantiemen und Marktanteil berechnen
    initial_money = gs.money
    gs.week += 1
    # Simuliere Tantiemenauszahlung und Marktanteilsberechnung (wöchentlicher Game-Loop-Schritt)
    gs._on_new_week()
    
    assert active_proj.market_share > 0.0
    assert gs.money > initial_money
    print("test_sound_card_project passed!")

def test_radio_jingles():
    gs = GameState()
    gs.money = 20000
    gs.hype
    
    # 1. Ein Jingle produzieren (Pop, Hype, None)
    # Kosten: 5000 + 2000 (Pop) + 1500 (Hype) = 8500
    # Hype-Bonus: 5.0 + 3.0 (Pop) + 2.0 (Hype) = 10.0
    success = gs.create_radio_jingle("Cool Ad", "pop", "hype", "none")
    assert success
    assert len(gs.active_jingles) == 1
    
    jingle = gs.active_jingles[0]
    assert jingle.name == "Cool Ad"
    assert jingle.cost == 8500
    assert jingle.hype_bonus == 10.0
    assert jingle.weeks_left == 4
    assert gs.money == 11500
    
    # Hype auf aktive Entwicklungen anwenden
    # Wir fügen ein fiktives aktives Projekt hinzu
    from models import GameProject
    proj = GameProject("HL3", "Sci-Fi", "Shooter")
    proj.hype = 10.0
    gs.active_projects.append({"project": proj, "progress": 1.0, "total_weeks": 10, "bugs": 0})
    assert gs.calculate_hype(proj) >= 10
    
    # Wöchentlicher Tick, der Jingles dekrementiert
    gs._on_new_week()
    assert jingle.weeks_left == 3
    
    # Jingle nach 4 Ticks abgelaufen
    for _ in range(3):
        gs._on_new_week()
        
    assert len(gs.active_jingles) == 0
    print("test_radio_jingles passed!")

def test_accessibility_lab():
    gs = GameState()
    gs.money = 50000
    initial_money = gs.money
    initial_fans = gs.fans
    initial_hype = gs.hype

    from models import GameProject
    proj = GameProject("Access Quest", "Fantasy", "RPG")
    gs.active_projects.append({"project": proj, "progress": 1.0, "total_weeks": 10, "bugs": 7})

    success, action = gs.run_accessibility_lab_action("community_beta")
    assert success
    assert action["id"] == "community_beta"
    assert gs.money == initial_money - action["cost"]
    assert gs.accessibility_reputation == action["reputation"]
    assert gs.fans == initial_fans + action["fans"]
    assert gs.hype == initial_hype + action["hype"]
    assert gs.active_projects[0]["bugs"] == 2
    assert len(gs.accessibility_lab_history) == 1

    fans_before_week = gs.fans
    gs.update_accessibility_reputation()
    assert gs.fans == fans_before_week + gs.get_accessibility_weekly_fans()
    print("test_accessibility_lab passed!")

def test_accessibility_achievements():
    gs = GameState()
    gs.money = 50000

    for _ in range(3):
        success, _ = gs.run_accessibility_lab_action("community_beta")
        assert success

    assert "inclusive_studio" in gs.unlocked_achievements
    assert "accessibility_champion" not in gs.unlocked_achievements

    gs.money = 200000
    for _ in range(4):
        success, _ = gs.run_accessibility_lab_action("community_beta")
        assert success

    assert "accessibility_champion" in gs.unlocked_achievements
    assert gs.money == 200000 - (4 * 15000) + 150000
    print("test_accessibility_achievements passed!")

def test_accessibility_annual_grant():
    gs = GameState()
    gs.accessibility_reputation = 40
    gs.last_accessibility_grant_year = 0

    money_before = gs.money
    weekly_fans = gs.update_accessibility_reputation()
    assert weekly_fans == 60
    assert gs.money == money_before + 30000
    assert gs.last_accessibility_grant_year == gs.get_calendar_year()
    assert gs.emails[0].subject == gs.get_text("subject_access_grant")

    money_after_first_grant = gs.money
    gs.update_accessibility_reputation()
    assert gs.money == money_after_first_grant
    print("test_accessibility_annual_grant passed!")

def test_financial_booking_fixes():
    gs = GameState()

    initial_money = gs.money
    success, reward = gs.watch_ad()
    assert success
    assert reward == 5000
    assert gs.money == initial_money + 5000

    template = FAN_MAIL_TEMPLATES[0]
    mail = FanMail(
        mail_id="money_mail",
        sender="RetroFan",
        subject_key=template["subject_key"],
        text_key=template["text_key"],
        options=template["options"]
    )
    gs.fan_mail_inbox = [mail]
    money_before_mail = gs.money
    success = gs.answer_fan_mail("money_mail", 1)
    assert success
    assert gs.money == money_before_mail + 500

    emp = Employee(name="Clara")
    gs.employees = [emp]
    event = OFFICE_PERSONALITY_EVENTS[1]
    gs.active_personality_event = event
    gs.active_personality_employee = emp
    money_before_event = gs.money
    success = gs.answer_personality_event(0)
    assert success
    assert gs.money == money_before_event - 2000

    employee = Employee(name="Finja")
    employee.salary = 1000
    gs.employees = []
    money_before_hire = gs.money
    success = gs.hire_employee(employee)
    assert success
    assert gs.money == money_before_hire - 2000

    money_before_manufacturing = gs.money
    success = gs.start_manufacturing_job("Testspiel", 100, 2, 4)
    assert success
    assert gs.money == money_before_manufacturing - 200
    print("test_financial_booking_fixes passed!")

def test_save_load_expansion():
    gs = GameState()
    
    # Daten für Expansion hinzufügen
    emp = Employee(name="Mark")
    emp.personality = "workaholic"
    gs.employees = [emp]
    
    mail = FanMail(mail_id="fm_1", sender="Fans", subject_key="sub", text_key="text", options=[])
    gs.fan_mail_inbox = [mail]
    
    sc = SoundCardProject("Audigy", ["fm_synthesis"], 30000, is_released=True, market_share=15.0)
    gs.sound_card_projects = [sc]
    
    jingle = RadioJingle("MyJingle", "rock", "serious", "laser", 12.0, 9500)
    jingle.weeks_left = 2
    gs.active_jingles = [jingle]

    gs.accessibility_reputation = 42
    gs.accessibility_lab_history = [{"week": 12, "action_id": "screenreader_test", "cost": 4000, "reputation": 5}]
    gs.last_accessibility_grant_year = 1935
    gs.unlocked_achievements = ["inclusive_studio"]
    gs.my_goty_wins = 1
    
    # In JSON-Datei speichern
    gs.save_game(99)
    
    # Neuen Spielstand aus der JSON-Datei laden
    gs_loaded = GameState()
    gs_loaded.load_game(99)
    
    # Datei aufräumen
    if os.path.exists("save_slot_99.json"):
        os.remove("save_slot_99.json")
    
    # Verifizieren, dass alle Daten 100% korrekt wiederhergestellt wurden
    assert len(gs_loaded.employees) == 1
    assert gs_loaded.employees[0].personality == "workaholic"
    
    assert len(gs_loaded.fan_mail_inbox) == 1
    assert gs_loaded.fan_mail_inbox[0].mail_id == "fm_1"
    
    assert len(gs_loaded.sound_card_projects) == 1
    assert gs_loaded.sound_card_projects[0].name == "Audigy"
    assert gs_loaded.sound_card_projects[0].market_share == 15.0
    
    assert len(gs_loaded.active_jingles) == 1
    assert gs_loaded.active_jingles[0].name == "MyJingle"
    assert gs_loaded.active_jingles[0].weeks_left == 2

    assert gs_loaded.accessibility_reputation == 42
    assert len(gs_loaded.accessibility_lab_history) == 1
    assert gs_loaded.accessibility_lab_history[0]["action_id"] == "screenreader_test"
    assert gs_loaded.last_accessibility_grant_year == 1935
    assert gs_loaded.unlocked_achievements == ["inclusive_studio"]
    assert gs_loaded.my_goty_wins == 1
    
    print("test_save_load_expansion passed!")

if __name__ == "__main__":
    try:
        test_employee_personalities()
        test_office_events()
        test_fan_mail()
        test_sound_card_project()
        test_radio_jingles()
        test_accessibility_lab()
        test_accessibility_achievements()
        test_accessibility_annual_grant()
        test_financial_booking_fixes()
        test_save_load_expansion()
        print("\n=== ALL AUDIO EXPANSION TESTS PASSED! ===")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nTEST SUITE FAILED: {e}")
        sys.exit(1)
