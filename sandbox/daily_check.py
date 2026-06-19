"""
Daily System Health Check - Run manually or via scheduler
"""
import requests, subprocess, os, json, time
from datetime import datetime

OLLAMA = "http://localhost:11434"
TOOLBOX = "http://localhost:8888"
LOG = r"D:\Lobster_Workspace\sandbox\daily_check.log"
PLUGINS_DIR = r"D:\Lobster_Workspace\chrome_extensions"
REQUIRED_FILES = ["manifest.json", "popup.html", "popup.js", "icon.png", "icon_128.png"]
REQUIRED_PLUGINS = ["ai_summarizer", "privacy_cleaner", "ai_translator", "reader_mode", "code_reviewer", "smart_bookmarks", "page_monitor", "tab_manager", "screenshot_tool", "password_gen"]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def check_ollama():
    try:
        r = requests.get(f"{OLLAMA}/api/tags", timeout=10)
        if r.status_code == 200:
            models = r.json().get("models", [])
            return True, f"{len(models)} models online"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:80]

def check_toolbox():
    try:
        r = requests.get(f"{TOOLBOX}/health", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return True, f"ok, {data.get('doc_count',0)} docs"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:80]

def check_docker():
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            containers = [c for c in result.stdout.strip().split("\n") if c]
            return True, f"{len(containers)} containers"
        return False, f"exit {result.returncode}: {result.stderr[:80]}"
    except Exception as e:
        return False, str(e)[:80]

def check_plugins():
    missing_files = []
    for plugin in REQUIRED_PLUGINS:
        base = os.path.join(PLUGINS_DIR, plugin)
        for f in REQUIRED_FILES:
            if not os.path.isfile(os.path.join(base, f)):
                missing_files.append(f"{plugin}/{f}")
    if missing_files:
        return False, f"Missing: {missing_files[:5]}"
    store_ok = all(
        os.path.isdir(os.path.join(PLUGINS_DIR, p, "store_listing"))
        for p in REQUIRED_PLUGINS
    )
    return True, f"{len(REQUIRED_PLUGINS)} plugins OK (stores: {store_ok})"

def restart_toolbox():
    try:
        subprocess.Popen([
            r"C:\Users\鹈垣\AppData\Local\Programs\Python\Python313\python.exe",
            r"D:\Lobster_Workspace\projects\ai_toolbox\toolbox_backend.py"
        ], creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    log("=" * 40)
    log("Daily Health Check Started")

    checks = [
        ("Ollama", check_ollama),
        ("Toolbox", check_toolbox),
        ("Docker", check_docker),
        ("Plugins", check_plugins),
    ]

    all_ok = True
    for name, fn in checks:
        ok, detail = fn()
        status = "OK" if ok else "FAIL"
        if not ok:
            all_ok = False
        log(f"  {name}: {status} - {detail}")

    # Auto-restart toolbox if down
    if not check_toolbox()[0]:
        log("  Attempting toolbox restart...")
        if restart_toolbox():
            time.sleep(3)
            ok2, detail2 = check_toolbox()
            log(f"  Toolbox after restart: {'OK' if ok2 else 'FAIL'} - {detail2}")

    log(f"Health Check Complete: {'ALL OK' if all_ok else 'ISSUES FOUND'}")
