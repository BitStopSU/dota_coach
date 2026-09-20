import requests
import hero_builds
import purchase_log

_timings_cache = {}
_hero_id_cache = {}


# ─────────────────────────────────────────────────────────
#  Апгрейды: если базовый предмет превратился в один из этих —
#  считаем, что базовый тоже собран.
# ─────────────────────────────────────────────────────────
UPGRADES = {
    "item_rod_of_atos": [
        "item_octarine_core", "item_gleipnir",
    ],
    "item_arcane_boots": [
        "item_guardian_greaves",
    ],
    "item_null_talisman": [
        "item_nullifier", "item_veil_of_discord",
    ],
    "item_boots": [
        "item_arcane_boots", "item_power_treads", "item_phase_boots",
        "item_tranquil_boots", "item_guardian_greaves",
    ],
    "item_maelstrom": [
        "item_mjollnir", "item_gleipnir",
    ],
    "item_yasha": [
        "item_manta", "item_sange_and_yasha",
    ],
    "item_sange": [
        "item_heavens_halberd", "item_sange_and_yasha",
    ],
    "item_oblivion_staff": [
        "item_orchid", "item_bloodthorn",
    ],
    "item_hyperstone": [
        "item_assault", "item_monkey_king_bar", "item_moon_shard",
        "item_bloodthorn",
    ],
    "item_vanguard": [
        "item_crimson_guard", "item_abyssal_blade",
    ],
    "item_hood_of_defiance": [
        "item_pipe", "item_eternal_shroud",
    ],
    "item_headdress": [
        "item_mekansm", "item_pipe", "item_guardian_greaves",
    ],
    "item_buckler": [
        "item_mekansm", "item_crimson_guard", "item_guardian_greaves",
    ],
    "item_blitz_knuckles": [
        "item_orchid", "item_bloodthorn",
    ],
    "item_shadow_amulet": [
        "item_glimmer_cape",
    ],
    "item_ghost": [
        "item_ethereal_blade",
    ],
    "item_ogre_axe": [
        "item_black_king_bar", "item_sange", "item_echo_sabre",
        "item_ultimate_scepter",
    ],
    "item_blade_of_alacrity": [
        "item_yasha", "item_ultimate_scepter", "item_diffusal_blade",
    ],
    "item_staff_of_wizardry": [
        "item_rod_of_atos", "item_ultimate_scepter",
        "item_cyclone", "item_force_staff",
    ],
    "item_reaver": [
        "item_satanic", "item_heart",
    ],
    "item_eaglesong": [
        "item_butterfly",
    ],
    "item_relic": [
        "item_radiance",
    ],
    "item_mystic_staff": [
        "item_shivas_guard", "item_octarine_core", "item_lotus_orb",
    ],
    "item_ultimate_orb": [
        "item_skadi", "item_sheepstick", "item_satanic", "item_refresher",
    ],
    "item_ultimate_scepter": [
        "item_ultimate_scepter_2",
    ],
}


def load_hero_ids():
    global _hero_id_cache
    if _hero_id_cache:
        return _hero_id_cache
    try:
        resp = requests.get(
            "https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json",
            timeout=10
        )
        heroes = resp.json()
        for hid, data in heroes.items():
            _hero_id_cache[data["name"]] = int(hid)
    except Exception as e:
        print(f"[timings] ошибка загрузки ID героев: {e}")
    return _hero_id_cache


def get_item_timing_remote(hero_name, item_name):
    cache_key = (hero_name, item_name, "remote")
    if cache_key in _timings_cache:
        return _timings_cache[cache_key]

    hero_ids = load_hero_ids()
    hero_id = hero_ids.get(hero_name)
    if not hero_id:
        _timings_cache[cache_key] = None
        return None

    item_key = item_name.replace("item_", "")
    url = "https://api.opendota.com/api/scenarios/itemTimings"
    params = {"hero_id": hero_id, "item": item_key}

    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                total_time = sum(d.get("time", 0) for d in data)
                total_games = sum(d.get("games", 0) for d in data)
                total_wins = sum(d.get("wins", 0) for d in data)
                if total_games == 0:
                    _timings_cache[cache_key] = None
                    return None
                result = {
                    "avg_time": total_time / total_games,
                    "winrate": total_wins / total_games * 100,
                    "games": total_games,
                }
                _timings_cache[cache_key] = result
                return result
    except Exception as e:
        print(f"[timings] ошибка OpenDota: {e}")

    _timings_cache[cache_key] = None
    return None


def format_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def _was_purchased(item_name):
    """Покупался ли предмет в текущей сессии."""
    try:
        recent = purchase_log.get_recent_purchases(200)
        for entry in recent:
            if entry.get("item") == item_name:
                return True
    except Exception:
        pass
    return False


def _is_upgraded(item_name, inventory):
    """Апгрейднут ли предмет в один из предметов в инвентаре."""
    upgrades = UPGRADES.get(item_name, [])
    for up in upgrades:
        if up in inventory:
            return True
    return False


def _is_aghs_consumed(item_name, inventory):
    """
    Если item_name = ultimate_scepter, а инвентарь содержит
    flags — caller уже сам добавил 'item_ultimate_scepter' в inventory.
    Эта проверка нужна для случая, когда caller не добавил.
    """
    if item_name == "item_ultimate_scepter":
        return "item_ultimate_scepter" in inventory
    return False


def get_timing_tips(hero_name, clock, inventory=None):
    """
    Тайминги с учётом уже купленных предметов.
    Предмет считается «готовым», если:
      - есть в инвентаре
      - был куплен ранее (лог)
      - превратился в апгрейд (Atos → Octarine)
      - съеден как Aghanim's (флаг в hero/abilities)
    """
    tips = []
    inventory = inventory or set()

    build = hero_builds.get_build(hero_name)

    if build:
        for item_name, display, avg, wr in build["build"]:
            in_inv = item_name in inventory
            was_bought = _was_purchased(item_name)
            upgraded = _is_upgraded(item_name, inventory)
            done = in_inv or was_bought or upgraded

            if done:
                tips.append({
                    "text": f"✔ {display}",
                    "icon": item_name,
                    "done": True,
                    "html": f'<span style="color: #7DCEA0;">✔ {display}</span>',
                })
                continue

            if clock < avg - 120:
                tips.append({
                    "text": f"🎯 {display}: ~{format_time(avg)}",
                    "icon": item_name,
                    "done": False,
                    "html": (
                        f'<span style="color: #AED6F1;">'
                        f'🎯 {display}: цель ~{format_time(avg)}'
                        f'</span>'
                    ),
                })
            elif avg - 120 <= clock <= avg + 180:
                tips.append({
                    "text": f"⚡ {display}: СЕЙЧАС!",
                    "icon": item_name,
                    "done": False,
                    "html": (
                        f'<span style="color: #F7DC6F; font-weight: bold;">'
                        f'⚡ {display}: ТАЙМИНГ!'
                        f'</span>'
                    ),
                })
            elif clock > avg + 300:
                tips.append({
                    "text": f"⚠ {display}: опоздание ({format_time(avg)})",
                    "icon": item_name,
                    "done": False,
                    "html": (
                        f'<span style="color: #EC7063;">'
                        f'⚠ {display}: опоздание (цель {format_time(avg)})'
                        f'</span>'
                    ),
                })
    else:
        role_items = {
            "mid": [
                ("item_arcane_boots", "Arcane Boots"),
                ("item_blink", "Blink Dagger"),
            ],
            "carry": [
                ("item_power_treads", "Power Treads"),
                ("item_black_king_bar", "BKB"),
            ],
            "offlane": [
                ("item_vanguard", "Vanguard"),
                ("item_blink", "Blink Dagger"),
            ],
            "support": [
                ("item_arcane_boots", "Arcane Boots"),
                ("item_glimmer_cape", "Glimmer Cape"),
            ],
        }
        role = hero_builds.get_role(hero_name)
        items = role_items.get(role, role_items["support"])

        for item_name, display in items:
            in_inv = item_name in inventory
            was_bought = _was_purchased(item_name)
            upgraded = _is_upgraded(item_name, inventory)
            if in_inv or was_bought or upgraded:
                tips.append({
                    "text": f"✔ {display}",
                    "icon": item_name,
                    "done": True,
                    "html": f'<span style="color: #7DCEA0;">✔ {display}</span>',
                })
                continue

            timing = get_item_timing_remote(hero_name, item_name)
            if not timing:
                continue
            avg = timing["avg_time"]
            wr = timing["winrate"]
            if clock < avg - 120:
                tips.append({
                    "text": f"🎯 {display}: ~{format_time(avg)}",
                    "icon": item_name,
                    "done": False,
                    "html": (
                        f'<span style="color: #AED6F1;">'
                        f'🎯 {display}: цель ~{format_time(avg)} (WR {wr:.0f}%)'
                        f'</span>'
                    ),
                })
            elif avg - 120 <= clock <= avg + 180:
                tips.append({
                    "text": f"⚡ {display}: СЕЙЧАС!",
                    "icon": item_name,
                    "done": False,
                    "html": (
                        f'<span style="color: #F7DC6F; font-weight: bold;">'
                        f'⚡ {display}: ТАЙМИНГ!'
                        f'</span>'
                    ),
                })

    return tips