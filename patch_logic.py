import re

c = open('logic.py', encoding='utf-8').read()

save_replacement = """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        # --- ANTI-CHEAT ---
        import hashlib, ctypes
        try:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            bak_path = f"save_slot_{slot}.bak"
            expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
            with open(bak_path, "w", encoding="utf-8") as f:
                json.dump({"hash": expected_hash}, f)
            ctypes.windll.kernel32.SetFileAttributesW(bak_path, 2)
        except Exception:
            pass
            
        return True
"""

c = re.sub(r'        with open\(filepath, "w", encoding="utf-8"\) as f:\n            json\.dump\(data, f, indent=2, ensure_ascii=False\)\n        return True', save_replacement.strip('\n'), c)

load_replacement = """
        with open(filepath, "r", encoding="utf-8") as f:
            json_str = f.read()
            data = json.loads(json_str)

        # --- ANTI-CHEAT ---
        bak_path = f"save_slot_{slot}.bak"
        if os.path.exists(bak_path):
            import hashlib
            try:
                with open(bak_path, "r", encoding="utf-8") as f:
                    bak_data = json.load(f)
                expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
                if bak_data.get("hash") != expected_hash:
                    print("[Anti-Cheat] Manipulation detected!")
                    return False
            except Exception:
                return False
"""

c = re.sub(r'        with open\(filepath, "r", encoding="utf-8"\) as f:\n            data = json\.load\(f\)', load_replacement.strip('\n'), c)

open('logic.py', 'w', encoding='utf-8').write(c)
