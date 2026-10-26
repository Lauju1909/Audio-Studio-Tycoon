import subprocess, types, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
old_src = subprocess.check_output(["git", "show", "pre-rebuild-backup:game_data.py"]).decode("utf-8-sig")
old = types.ModuleType("old"); exec(compile(old_src, "old", "exec"), old.__dict__)
import game_data as new
missing = [k for k in old.__dict__ if not k.startswith("__") and not hasattr(new, k)]
diff = [k for k in old.__dict__ if not k.startswith("__") and hasattr(new, k) and not callable(getattr(old, k)) and getattr(old, k) != getattr(new, k)]
print("missing", missing, "different", diff)
sys.exit(1 if missing or diff else 0)
