c = open('logic.py', encoding='utf-8').read()

target = '''        # --- ANTI-CHEAT ---
        import hashlib, ctypes
        try:
            bak_path = f"save_slot_{slot}.bak"
            expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
            with open(bak_path, "w", encoding="utf-8") as f:
                json.dump({"hash": expected_hash}, f)
            ctypes.windll.kernel32.SetFileAttributesW(bak_path, 2)
        except Exception:
            pass'''

replacement = '''        # --- ANTI-CHEAT ---
        import hashlib, ctypes
        try:
            bak_path = f"save_slot_{slot}.bak"
            if os.path.exists(bak_path):
                ctypes.windll.kernel32.SetFileAttributesW(bak_path, 128)
            expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
            with open(bak_path, "w", encoding="utf-8") as f:
                json.dump({"hash": expected_hash}, f)
            ctypes.windll.kernel32.SetFileAttributesW(bak_path, 2)
        except Exception as e:
            print(f"[Anti-Cheat] Error: {e}")'''

c = c.replace(target, replacement)
open('logic.py', 'w', encoding='utf-8').write(c)
