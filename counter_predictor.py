# Ключ — что собрано у врага (item_name)
# Значение — что покупать против этого

ITEM_COUNTERS = {
    # ── Физический урон ──
    "item_butterfly": {
        "counter": ["Monkey King Bar", "Bloodthorn", "Nullifier"],
        "reason": "Уклонение",
    },
    "item_monkey_king_bar": {
        "counter": ["Heaven's Halberd", "Ghost Scepter"],
        "reason": "Точные удары",
    },
    "item_desolator": {
        "counter": ["Assault Cuirass", "Crimson Guard"],
        "reason": "Минус броня",
    },
    "item_radiance": {
        "counter": ["Black King Bar", "Pipe of Insight"],
        "reason": "Аура урона",
    },
    "item_basher": {
        "counter": ["Black King Bar", "Linken's Sphere"],
        "reason": "Стан",
    },
    "item_abyssal_blade": {
        "counter": ["Black King Bar", "Linken's Sphere", "Aeon Disk"],
        "reason": "Стан через BKB",
    },
    "item_bloodthorn": {
        "counter": ["Black King Bar", "Manta Style", "Eul's Scepter"],
        "reason": "Сайленс и криты",
    },
    "item_nullifier": {
        "counter": ["Black King Bar", "Linken's Sphere"],
        "reason": "Снимает баффы",
    },
    "item_skadi": {
        "counter": ["Black King Bar", "Hurricane Pike"],
        "reason": "Замедление атаки",
    },

    # ── Магический урон и бурст ──
    "item_ultimate_scepter": {
        "counter": ["Black King Bar", "Pipe of Insight", "Glimmer Cape"],
        "reason": "Усиленные способности",
    },
    "item_octarine_core": {
        "counter": ["Black King Bar", "Pipe of Insight"],
        "reason": "Частые способности",
    },
    "item_shivas_guard": {
        "counter": ["Black King Bar", "Pipe of Insight", "Glimmer Cape"],
        "reason": "Аура холода",
    },
    "item_bloodstone": {
        "counter": ["Spirit Vessel", "Eye of Skadi"],
        "reason": "Регенерация",
    },
    "item_dagon_5": {
        "counter": ["Black King Bar", "Glimmer Cape", "Pipe of Insight"],
        "reason": "Магический бурст",
    },
    "item_ethereal_blade": {
        "counter": ["Black King Bar", "Manta Style"],
        "reason": "Магический бурст",
    },

    # ── Контроль ──
    "item_scythe_of_vyse": {
        "counter": ["Black King Bar", "Linken's Sphere", "Aeon Disk"],
        "reason": "Хекс",
    },
    "item_orchid": {
        "counter": ["Manta Style", "Eul's Scepter", "Black King Bar"],
        "reason": "Сайленс",
    },
    "item_sheepstick": {
        "counter": ["Black King Bar", "Linken's Sphere"],
        "reason": "Хекс",
    },
    "item_diffusal_blade": {
        "counter": ["Black King Bar", "Manta Style"],
        "reason": "Сжигание маны",
    },
    "item_rod_of_atos": {
        "counter": ["Black King Bar", "Manta Style", "Force Staff"],
        "reason": "Рут",
    },

    # ── Танки ──
    "item_heart": {
        "counter": ["Spirit Vessel", "Eye of Skadi", "Desolator"],
        "reason": "Много HP",
    },
    "item_satanic": {
        "counter": ["Spirit Vessel", "Eye of Skadi"],
        "reason": "Лайфстил",
    },
    "item_assault": {
        "counter": ["Desolator", "Monkey King Bar"],
        "reason": "Броня и аура скорости",
    },
    "item_crimson_guard": {
        "counter": ["Desolator", "Monkey King Bar"],
        "reason": "Блок урона",
    },
    "item_pipe": {
        "counter": ["Desolator", "Diffusal Blade"],
        "reason": "Магический блок",
    },
    "item_black_king_bar": {
        "counter": ["Scythe of Vyse", "Beastmaster's Roar", "Ethereal Blade"],
        "reason": "Иммунитет к магии",
    },

    # ── Утилити ──
    "item_blink": {
        "counter": ["Rod of Atos", "Nullifier", "Bloodthorn"],
        "reason": "Инициация",
    },
    "item_shadow_blade": {
        "counter": ["Dust of Appearance", "Sentry Ward", "Gem of True Sight"],
        "reason": "Невидимость",
    },
    "item_silver_edge": {
        "counter": ["Dust of Appearance", "Sentry Ward", "Gem of True Sight"],
        "reason": "Невидимость",
    },
    "item_invis_sword": {
        "counter": ["Dust of Appearance", "Sentry Ward"],
        "reason": "Невидимость",
    },
    "item_force_staff": {
        "counter": ["Nullifier", "Skull Basher"],
        "reason": "Спасение союзников",
    },
    "item_glimmer_cape": {
        "counter": ["Dust of Appearance", "Nullifier", "Sentry Ward"],
        "reason": "Магический щит",
    },
    "item_aeon_disk": {
        "counter": ["Nullifier", "Scythe of Vyse"],
        "reason": "Авто-спасение",
    },
}


def predict_counters(state, my_team="team2"):
    """
    Возвращает список советов: что купить против собранных предметов врага.
    """
    from enemy_analyzer import get_enemy_heroes

    tips = []
    enemies = get_enemy_heroes(state, my_team)

    # Собираем все предметы врагов
    enemy_items = {}
    for e in enemies:
        hero = e["hero"]
        hero_display = hero.replace("npc_dota_hero_", "").replace("_", " ").title()
        for item_data in e["items"].values():
            if not isinstance(item_data, dict):
                continue
            name = item_data.get("name", "")
            if name and name.startswith("item_"):
                enemy_items.setdefault(name, []).append(hero_display)

    # Ищем советы
    seen_counters = set()
    for item_name, heroes in enemy_items.items():
        if item_name not in ITEM_COUNTERS:
            continue

        counter_info = ITEM_COUNTERS[item_name]
        counter_items = counter_info["counter"]
        reason = counter_info["reason"]

        # Не дублируем советы
        counter_key = tuple(counter_items[:2])
        if counter_key in seen_counters:
            continue
        seen_counters.add(counter_key)

        item_display = item_name.replace("item_", "").replace("_", " ").title()
        hero_str = ", ".join(set(heroes))
        tips.append(
            f"{hero_str}: {item_display} ({reason}) → {counter_items[0]}"
        )

    return tips[:5]


def get_bkb_pierce_tips(state, my_team="team2"):
    """
    Если у врага много BKB-пробивающих угроз — предупредить.
    """
    from enemy_analyzer import get_enemy_heroes

    enemies = get_enemy_heroes(state, my_team)
    bkb_pierce_heroes = []

    # Герои, чьи способности работают через BKB
    for e in enemies:
        hero = e["hero"]
        # Doom, Bane, Beastmaster, Enigma, Magnus, Legion
        if any(x in hero for x in [
            "doom_bringer", "bane", "beastmaster", "enigma",
            "magnus", "legion_commander", "batrider", "pudge"
        ]):
            hero_display = hero.replace("npc_dota_hero_", "").replace("_", " ").title()
            bkb_pierce_heroes.append(hero_display)

    if len(bkb_pierce_heroes) >= 2:
        return f"⚠ Через BKB: {', '.join(bkb_pierce_heroes)} → Aeon Disk, Linken's"
    return None