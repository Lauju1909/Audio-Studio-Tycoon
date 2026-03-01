"""
Crash-Catcher Wrapper für main.py.
Startet das Spiel normal, aber fängt alle Exceptions ab und 
schreibt sie in crash_log.txt.
"""
import sys
import traceback

try:
    # Umleite sys.excepthook um ALLE Crashes zu fangen
    def crash_handler(exc_type, exc_value, exc_tb):
        crash_info = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("\n" + "="*60)
        print("!!! CRASH DETECTED !!!")
        print("="*60)
        print(crash_info)
        
        with open("crash_log.txt", "w", encoding="utf-8") as f:
            f.write(crash_info)
        
        print("\nCrash-Log gespeichert in: crash_log.txt")
        print("Drücke Enter zum Beenden...")
        input()
    
    sys.excepthook = crash_handler
    
    # Importiere und starte main
    
except Exception:
    crash_info = traceback.format_exc()
    print("\n" + "="*60)
    print("!!! CRASH DETECTED !!!")
    print("="*60)
    print(crash_info)
    
    with open("crash_log.txt", "w", encoding="utf-8") as f:
        f.write(crash_info)
    
    print("\nCrash-Log gespeichert in: crash_log.txt")
    print("Drücke Enter zum Beenden...")
    input()
