import requests
from pathlib import Path

_hero_cache = {}
_item_cache = {}

IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

HERO_CDN = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/{}.png"
ITEM_CDN = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/{}_lg.png"
ITEM_CDN_FALLBACK = "https://media.steampowered.com/apps/dota2/images/items/{}_lg.png"


def hero_image_path(hero_name):
    if not hero_name:
        return None

    key = hero_name.replace("npc_dota_hero_", "")
    if key in _hero_cache:
        return _hero_cache[key]

    path = IMAGES_DIR / f"hero_{key}.png"
    if not path.exists():
        url = HERO_CDN.format(key)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and len(resp.content) > 500:
                path.write_bytes(resp.content)
            else:
                _hero_cache[key] = None
                return None
        except Exception as e:
            print(f"[images] ошибка загрузки героя {key}: {e}")
            _hero_cache[key] = None
            return None

    _hero_cache[key] = str(path)
    return str(path)


def item_image_path(item_name):
    if not item_name:
        return None

    key = item_name.replace("item_", "")
    if key in _item_cache:
        return _item_cache[key]

    path = IMAGES_DIR / f"item_{key}.png"
    if not path.exists():
        for url in (ITEM_CDN.format(key), ITEM_CDN_FALLBACK.format(key)):
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200 and len(resp.content) > 500:
                    path.write_bytes(resp.content)
                    break
            except Exception:
                continue
        else:
            _item_cache[key] = None
            return None

    _item_cache[key] = str(path)
    return str(path)