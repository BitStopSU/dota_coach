import requests
from starting_items import get_starting_items
import item_timings
import enemy_analyzer
import counter_predictor
import match_logger
import tts as _tts
import neutral_items
import hero_builds

_HERO_LOOKUP = {}

SUPPORT_HEROES = [
    "crystal_maiden", "lion", "witch_doctor", "shadow_shaman",
    "warlock", "dazzle", "oracle", "io", "chen", "bane",
    "earthshaker", "rubick", "disruptor", "keeper_of_the_light",
    "wisp", "undying", "grimstroke", "hoodwink", "dawnbreaker",
    "jakiro", "ogre_magi", "silencer", "skywrath_mage",
    "shadow_demon", "visage", "winter_wyvern", "techies",
    "snapfire", "marci", "muerta"
]

ITEM_NAME_MAP = {
    "Quelling Blade": "item_quelling_blade",
    "Tango": "item_tango",
    "Slippers of Agility": "item_slippers",
    "Circlet": "item_circlet",
    "Iron Branch": "item_branches",
    "Stout Shield": "item_stout_shield",
    "Blood Grenade": "item_blood_grenade",
    "Observer Ward": "item_ward_observer",
    "Sentry Ward": "item_ward_sentry",
    "Smoke of Deceit": "item_smoke_of_deceit",
    "Faerie Fire": "item_faerie_fire",
    "Magic Stick": "item_magic_stick",
    "Enchanted Mango": "item_enchanted_mango",
    "Healing Salve": "item_flask",
    "Clarity": "item_clarity",
}

EARLY_GAME_ITEMS = {
    "item_ward_observer": "Ward",
    "item_ward_sentry": "Sentry",
    "item_smoke_of_deceit": "Smoke",
    "item_tango": "Tango",
    "item_flask": "Salve",
    "item_clarity": "Clarity",
    "item_branches": "Branch",
    "item_circlet": "Circlet",
    "item_slippers": "Slippers",
    "item_gauntlets": "Gauntlets",
    "item_mantle": "Mantle",
    "item_quelling_blade": "Quelling",
    "item_stout_shield": "Stout",
    "item_blood_grenade": "Blood Grenade",
    "item_faerie_fire": "Faerie Fire",
    "item_magic_stick": "Magic Stick",
    "item_enchanted_mango": "Mango",
}


def load_hero_lookup():
    global _HERO_LOOKUP
    if _HERO_LOOKUP:
        return _HERO_LOOKUP
    try:
        resp = requests.get(
            "https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json",
            timeout=10
        )
        heroes = resp.json()
        for k, v in heroes.items():
            _HERO_LOOKUP[v["name"]] = v["localized_name"]
    except Exception as e:
        print(f"[heroes] ошибка загрузки: {e}")
    return _HERO_LOOKUP


def format_hero_name(raw):
    if not raw:
        return ""
    if not raw.startswith("npc_dota_hero_"):
        raw = "npc_dota_hero_" + raw
    lookup = load_hero_lookup()
    return lookup.get(raw, raw)


def get_inventory_names(items):
    names = set()
    for item in items.values():
        if isinstance(item, dict):
            n = item.get("name", "")
            if n:
                names.add(n)
    return names


def get_all_items(state):
    """Все предметы: инвентарь + стеш."""
    names = set()
    names |= get_inventory_names(state.get("items", {}))
    names |= get_inventory_names(state.get("stash", {}))
    return names


def analyze_grouped(state):
    """
    Вернуть подсказки, разделённые по категориям:
    {"timings": [...], "threats": [...], "general": [...], "pre_game": [...]}
    """
    result = {
        "timings": [],
        "threats": [],
        "general": [],
        "pre_game": [],
    }

    if not state:
        return result

    map_data = state.get("map", {})
    hero = state.get("hero", {})
    player = state.get("player", {})
    items = state.get("items", {})

    clock = map_data.get("clock_time", 0) or 0
    minutes = clock // 60

    inventory = get_inventory_names(items)
    all_items = get_all_items(state)

    # ── Aghanim's Scepter / Shard как флаги героя ──
    # Когда Scepter съедается через Aghanim's Blessing,
    # он становится флагом hero.aghanims_scepter = 1
    hero_block = state.get("hero", {})
    abilities = state.get("abilities", {})

    aghs_flag = (
        hero_block.get("aghanims_scepter")
        or abilities.get("aghanims_scepter")
    )
    shard_flag = (
        hero_block.get("aghanims_shard")
        or abilities.get("aghanims_shard")
    )

    if aghs_flag:
        inventory.add("item_ultimate_scepter")
    if shard_flag:
        inventory.add("item_aghanims_shard")

    # ── Проверка вардов: инвентарь + стеш + все формы ──
    ward_names = {
        "item_ward_observer",
        "item_ward_sentry",
        "item_ward_dispenser",
        "item_ward_observer_sentry",
    }
    has_ward = bool(ward_names & all_items)

    hero_raw = hero.get("name", "")
    is_support = any(s in hero_raw for s in SUPPORT_HEROES)

    # ═══════════════════════════════════════════════════
    #  ПРЕ-ГЕЙМ
    # ═══════════════════════════════════════════════════
    if clock < 0:
        hero_name = format_hero_name(hero_raw)
        recommended = get_starting_items(hero_name)
        seconds_to_start = abs(clock)
        result["pre_game"].append(f"До крипов: {seconds_to_start} сек")

        recommended_internal = set()
        for it in recommended[:6]:
            internal = ITEM_NAME_MAP.get(it, "")
            if internal:
                recommended_internal.add(internal)

            if internal and internal in inventory:
                result["pre_game"].append(f"<s>{it}</s>")
            else:
                result["pre_game"].append(it)

        extra = inventory - recommended_internal
        extra = {e for e in extra if e}
        if extra:
            extra_names = [
                EARLY_GAME_ITEMS.get(e, e.replace("item_", "").title())
                for e in extra
            ]
            result["pre_game"].append(
                f"⚠ Вне плана: {', '.join(extra_names[:4])}"
            )

        return result

    # ═══════════════════════════════════════════════════
    #  ТАЙМИНГИ ПРЕДМЕТОВ
    # ═══════════════════════════════════════════════════
    try:
        timing_tips = item_timings.get_timing_tips(
            hero_raw, clock, inventory=inventory
        )
        result["timings"].extend(timing_tips)
    except Exception as ex:
        print(f"[rules] ошибка таймингов: {ex}")

    # ═══════════════════════════════════════════════════
    #  НЕЙТРАЛЬНЫЕ ПРЕДМЕТЫ
    # ═══════════════════════════════════════════════════
    try:
        hero_role = hero_builds.get_role(hero_raw)
        neutral_tips = neutral_items.get_neutral_item_tips(state, hero_role)
        for n in neutral_tips:
            result["general"].append(n)
    except Exception as ex:
        print(f"[rules] ошибка нейтралок: {ex}")

    # ═══════════════════════════════════════════════════
    #  УГРОЗЫ ВРАГА
    # ═══════════════════════════════════════════════════
    if clock > 60:
        try:
            counter_tips = enemy_analyzer.get_counter_tips(state)
            result["threats"].extend(counter_tips)
        except Exception as ex:
            print(f"[rules] ошибка угроз: {ex}")

        if clock > 180:
            try:
                predict = counter_predictor.predict_counters(state)
                result["threats"].extend(predict)
            except Exception as ex:
                print(f"[rules] ошибка прогноза: {ex}")

            try:
                bkb_tip = counter_predictor.get_bkb_pierce_tips(state)
                if bkb_tip:
                    result["threats"].append(bkb_tip)
            except Exception as ex:
                print(f"[rules] ошибка bkb: {ex}")

    # ═══════════════════════════════════════════════════
    #  АНАЛИЗ КОМПОНЕНТОВ ВРАГА
    # ═══════════════════════════════════════════════════
    if clock > 120:
        try:
            comp_tips = enemy_analyzer.analyze_enemy_components(state)
            for c in comp_tips:
                result["threats"].append(f"📦 {c}")
        except Exception as ex:
            print(f"[rules] ошибка анализа компонентов: {ex}")

    # ═══════════════════════════════════════════════════
    #  ОБЩИЕ СОВЕТЫ
    # ═══════════════════════════════════════════════════
    hp = hero.get("health", 0) or 0
    max_hp = hero.get("max_health", 1) or 1
    hp_pct = (hp / max_hp * 100) if max_hp else 100

    if 0 <= minutes <= 1 and clock > 0:
        result["general"].append("Беги на руну")
        match_logger.log("EVENT", "Старт игры", cooldown=300)

    if minutes >= 10 and hp_pct < 30:
        result["general"].append("Мало HP, отойди")
        _tts.say("Мало здоровья", key="low_hp", cooldown=60)

    if is_support and not has_ward and 0 <= minutes < 10:
        result["general"].append("Купи варды")

    if 300 <= clock <= 360:
        result["general"].append("Рошан может появиться")
        _tts.say("Рошан", key="roshan", cooldown=120)

    for tip in result["timings"]:
        if isinstance(tip, dict) and "СЕЙЧАС" in tip.get("text", ""):
            _tts.say(
                tip["text"].replace("⚡ ", "").replace(": ТАЙМИНГ!", ""),
                key=f"timing_{tip.get('icon', '')}",
                cooldown=60,
            )
            break

    return result


def analyze(state):
    grouped = analyze_grouped(state)
    tips = []
    for key in ("pre_game", "timings", "threats", "general"):
        tips.extend(grouped.get(key, []))
    return tips