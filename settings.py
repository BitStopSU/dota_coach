import json
from pathlib import Path

CONFIG_PATH = Path("config.json")

DEFAULTS = {
    "overlay": {
        "x": 1500,
        "y": 350,
        "width": 420,
        "height": 600,
        "opacity": 0.85,
        "font_size": 10,
        "enabled": True,
    },
    "purchase_window": {
        "x": 50,
        "y": 400,
        "width": 440,
        "height": 600,
        "opacity": 0.85,
        "enabled": True,
    },
    "kda_window": {
        "x": 1000,
        "y": 400,
        "width": 500,
        "height": 460,
        "opacity": 0.9,
        "enabled": True,
    },
    "blocks": {
        "timings": True,
        "threats": True,
        "general": True,
    },
    "tts": {
        "enabled": True,
        "volume": 0.9,
        "rate": 180,
    },
    "hotkeys": {
        "menu_key": "delete",
        "overlay_key": "f5",
        "purchase_key": "f6",
        "kda_key": "f7",
        "analysis_key": "f8",
    },
    "ai": {
        "provider": "deepseek",
        "deepseek_api_key": "sk-aef10865c1e54bb8b6f54cba1aca27b2",
        "deepseek_model": "deepseek-chat",
        "deepseek_base_url": "https://api.deepseek.com",
        "gemini_api_key": "",
        "gemini_model": "gemini-2.0-flash",
        "language": "ru",
        "auto_analyze_on_match_end": False,
    },
}


def load():
    if not CONFIG_PATH.exists():
        save(DEFAULTS)
        return DEFAULTS.copy()
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        for section, values in DEFAULTS.items():
            if section not in data:
                data[section] = values.copy()
            else:
                for k, v in values.items():
                    data[section].setdefault(k, v)
        return data
    except Exception as e:
        print(f"[settings] ошибка чтения: {e}")
        return DEFAULTS.copy()


def save(data):
    try:
        CONFIG_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        print(f"[settings] ошибка записи: {e}")


def get(section, key=None):
    data = load()
    if key:
        return data.get(section, {}).get(key)
    return data.get(section, {})


def set_value(section, key, value):
    data = load()
    data.setdefault(section, {})[key] = value
    save(data)