import requests
import json
from pathlib import Path

CACHE = Path("current_patch.json")

def get_latest_patch():
    url = "https://www.dota2.com/datafeed/patchnoteslist?language=english"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        patches = resp.json().get("patches", [])
        if patches:
            return patches[0].get("patch_number")
    except Exception as e:
        print(f"[patch] ошибка: {e}")
    return None

def check_patch():
    cached = {}
    if CACHE.exists():
        cached = json.loads(CACHE.read_text(encoding="utf-8"))

    latest = get_latest_patch()
    if latest and latest != cached.get("version"):
        print(f"[patch] новый патч: {latest}")
        cached["version"] = latest
        CACHE.write_text(json.dumps(cached, ensure_ascii=False), encoding="utf-8")
        return latest
    return cached.get("version")