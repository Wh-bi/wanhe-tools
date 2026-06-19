"""
Watchdog for AI Toolbox - monitors health and auto-restarts
"""
import requests, subprocess, time, os

API = "http://localhost:8888/health"
LOG = r"D:\Lobster_Workspace\sandbox\watchdog.log"
BACKEND = r"D:\Lobster_Workspace\projects\ai_toolbox\toolbox_backend.py"
PYTHON = r"C:\Users\鹈垣\AppData\Local\Programs\Python\Python313\python.exe"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def check_health():
    try:
        r = requests.get(API, timeout=5)
        return r.status_code == 200
    except:
        return False

def restart_backend():
    log("Restarting toolbox_backend.py...")
    subprocess.Popen([PYTHON, BACKEND], creationflags=subprocess.CREATE_NO_WINDOW)
    time.sleep(5)

log("Watchdog started")
fail_count = 0

while True:
    if check_health():
        if fail_count > 0:
            log(f"Health restored after {fail_count} failures")
        fail_count = 0
    else:
        fail_count += 1
        log(f"Health check failed ({fail_count}/2)")
        if fail_count >= 2:
            restart_backend()
            fail_count = 0
    time.sleep(30)
