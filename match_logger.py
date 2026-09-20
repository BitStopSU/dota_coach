from datetime import datetime
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

_session_file = None
_last_event = {}


def _get_session_file():
    global _session_file
    if _session_file is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        _session_file = LOGS_DIR / f"match_{ts}.log"
        _session_file.write_text(
            f"=== Dota Coach — сессия {ts} ===\n",
            encoding="utf-8"
        )
    return _session_file


def log(event_type, message, cooldown=0):
    """
    Записать событие в лог.
    cooldown: если > 0, одинаковые события чаще чем раз в N секунд не пишутся.
    """
    global _last_event
    now = datetime.now()

    if cooldown > 0:
        key = f"{event_type}:{message}"
        last = _last_event.get(key)
        if last and (now - last).total_seconds() < cooldown:
            return
        _last_event[key] = now

    try:
        path = _get_session_file()
        with path.open("a", encoding="utf-8") as f:
            f.write(
                f"[{now.strftime('%H:%M:%S')}] [{event_type}] {message}\n"
            )
    except Exception as e:
        print(f"[logger] ошибка: {e}")


def log_purchase(player, hero, item):
    hero_display = (
        hero.replace("npc_dota_hero_", "").replace("_", " ").title()
    )
    item_display = (
        item.replace("item_", "").replace("_", " ").title()
    )
    log(
        "PURCHASE",
        f"{player} ({hero_display}) купил {item_display}",
        cooldown=0
    )


def log_event(event_type, text):
    log(event_type, text)


def get_log_path():
    return str(_get_session_file()) if _session_file else None