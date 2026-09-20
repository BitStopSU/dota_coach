# ─────────────────────────────────────────────────────────
#  Нейтральные предметы Dota 2
#  tier 1: 5–14 мин   (5 мадстонов)
#  tier 2: 15–24 мин  (10 мадстонов)
#  tier 3: 25–34 мин  (15 мадстонов)
#  tier 4: 35+ мин    (20 мадстонов)
# ─────────────────────────────────────────────────────────

ARTIFACTS_BY_TIER = {
    1: [
        {"name": "Chipped Vest", "internal": "item_chipped_vest",
         "roles": ["carry", "offlane", "mid"],
         "reason": "Возврат урона"},
        {"name": "Occult Bracelet", "internal": "item_occult_bracelet",
         "roles": ["offlane", "support"],
         "reason": "Реген маны при уроне"},
        {"name": "Pollywog Charm", "internal": "item_pollywog_charm",
         "roles": ["support", "carry"],
         "reason": "Хилл в линии"},
        {"name": "Mana Draught", "internal": "item_mana_draught",
         "roles": ["mid", "support"],
         "reason": "Восстановление маны"},
        {"name": "Duelist Gloves", "internal": "item_duelist_gloves",
         "roles": ["carry", "mid"],
         "reason": "Скорость атаки"},
        {"name": "Ash Legion Shield", "internal": "item_ash_legion_shield",
         "roles": ["offlane", "support"],
         "reason": "Физический барьер"},
        {"name": "Pig Pole", "internal": "item_pig_pole",
         "roles": ["support", "offlane"],
         "reason": "Аура скорости атаки"},
        {"name": "Trusty Shovel", "internal": "item_trusty_shovel",
         "roles": ["support"],
         "reason": "Копает руны"},
        {"name": "Broom Handle", "internal": "item_broom_handle",
         "roles": ["carry", "mid"],
         "reason": "Урон и скорость атаки"},
        {"name": "Seeds of Serenity", "internal": "item_seeds_of_serenity",
         "roles": ["support"],
         "reason": "Хилл союзникам"},
        {"name": "Tumbler's Toy", "internal": "item_tumblers_toy",
         "roles": ["support", "offlane"],
         "reason": "Мини-блинк"},
        {"name": "Ocean Heart", "internal": "item_ocean_heart",
         "roles": ["support", "mid"],
         "reason": "Реген HP/маны"},
        {"name": "Ripper's Lash", "internal": "item_rippers_lash",
         "roles": ["offlane", "support"],
         "reason": "Замедление"},
        {"name": "Keen Optic", "internal": "item_keen_optic",
         "roles": ["support", "mid"],
         "reason": "Дальность и мана"},
        {"name": "Faded Broach", "internal": "item_faded_broach",
         "roles": ["mid", "carry"],
         "reason": "Мана и HP"},
        {"name": "Lance of Pursuit", "internal": "item_lance_of_pursuit",
         "roles": ["carry", "offlane"],
         "reason": "Замедление атакой"},
        {"name": "Blast Rig", "internal": "item_blast_rig",
         "roles": ["offlane"],
         "reason": "Урон и уклонение"},
    ],
    2: [
        {"name": "Searing Signet", "internal": "item_searing_signet",
         "roles": ["mid", "support"],
         "reason": "Магический урон от спеллов"},
        {"name": "Brigand's Blade", "internal": "item_brigands_blade",
         "roles": ["carry"],
         "reason": "Дополнительный урон"},
        {"name": "Essence Ring", "internal": "item_essence_ring",
         "roles": ["support", "offlane"],
         "reason": "Хилл"},
        {"name": "Poor Man's Shield", "internal": "item_poor_mans_shield",
         "roles": ["carry", "offlane"],
         "reason": "Блок физ. урона"},
        {"name": "Gossamer Cape", "internal": "item_gossamer_cape",
         "roles": ["carry", "mid"],
         "reason": "Уклонение"},
        {"name": "Vambrace", "internal": "item_vambrace",
         "roles": ["carry", "offlane"],
         "reason": "Статы по атрибуту"},
        {"name": "Pupil's Gift", "internal": "item_pupils_gift",
         "roles": ["mid", "support"],
         "reason": "Мана и урон"},
        {"name": "Grove Bow", "internal": "item_grove_bow",
         "roles": ["carry", "mid"],
         "reason": "Урон и дальность"},
        {"name": "Quickening Charm", "internal": "item_quickening_charm",
         "roles": ["support", "offlane"],
         "reason": "Снижение кулдаунов"},
        {"name": "Dragon Scale", "internal": "item_dragon_scale",
         "roles": ["offlane", "support"],
         "reason": "Броня и реген"},
        {"name": "Elven Tunic", "internal": "item_elven_tunic",
         "roles": ["carry", "mid"],
         "reason": "Уклонение и скорость"},
        {"name": "Bullwhip", "internal": "item_bullwhip",
         "roles": ["support"],
         "reason": "Ускорение союзников"},
        {"name": "Ring of Aquila", "internal": "item_ring_of_aquila",
         "roles": ["carry", "mid"],
         "reason": "Мана и статы"},
        {"name": "Philosopher's Stone", "internal": "item_philosophers_stone",
         "roles": ["support"],
         "reason": "Больше золота"},
        {"name": "Nether Shawl", "internal": "item_nether_shawl",
         "roles": ["mid", "offlane"],
         "reason": "Маг. сопротивление"},
    ],
    3: [
        {"name": "Serrated Shiv", "internal": "item_serrated_shiv",
         "roles": ["carry", "mid"],
         "reason": "Урон по одиночной цели"},
        {"name": "Cloak of Flames", "internal": "item_cloak_of_flames",
         "roles": ["offlane", "support"],
         "reason": "Аура урона"},
        {"name": "Stormcrafter", "internal": "item_stormcrafter",
         "roles": ["mid", "support"],
         "reason": "Урон и мобильность"},
        {"name": "Gunpowder Gauntlet", "internal": "item_gunpowder_gauntlet",
         "roles": ["carry", "mid"],
         "reason": "AoE-урон"},
        {"name": "Psychic Headband", "internal": "item_psychic_headband",
         "roles": ["support", "mid"],
         "reason": "Дальность"},
        {"name": "Titan Sliver", "internal": "item_titan_sliver",
         "roles": ["carry", "mid"],
         "reason": "Урон и статы"},
        {"name": "Ceremonial Robe", "internal": "item_ceremonial_robe",
         "roles": ["support", "offlane"],
         "reason": "Снижение урона"},
        {"name": "Spider Legs", "internal": "item_spider_legs",
         "roles": ["carry", "offlane"],
         "reason": "Скорость"},
        {"name": "Dandelion Amulet", "internal": "item_dandelion_amulet",
         "roles": ["support"],
         "reason": "Маг. блок"},
        {"name": "Paladin Sword", "internal": "item_paladin_sword",
         "roles": ["carry", "offlane"],
         "reason": "Лайфстил и урон"},
        {"name": "Orb of Destruction", "internal": "item_orb_of_destruction",
         "roles": ["carry", "mid"],
         "reason": "Урон и замедление"},
        {"name": "Telescope", "internal": "item_telescope",
         "roles": ["support"],
         "reason": "Обзор"},
        {"name": "Witchbane", "internal": "item_witchbane",
         "roles": ["support"],
         "reason": "Урон по магам"},
        {"name": "Enchanted Quiver", "internal": "item_enchanted_quiver",
         "roles": ["carry", "mid"],
         "reason": "Усиление атаки"},
        {"name": "Greater Faerie Fire", "internal": "item_greater_faerie_fire",
         "roles": ["carry", "mid"],
         "reason": "Хилл и урон"},
    ],
    4: [
        {"name": "Apex", "internal": "item_apex",
         "roles": ["carry", "offlane", "mid"],
         "reason": "Буст атрибутов (топ для драки)"},
        {"name": "Pyrrhic Cloak", "internal": "item_pyrrhic_cloak",
         "roles": ["offlane"],
         "reason": "Урон и выживаемость"},
        {"name": "Fallen Sky", "internal": "item_fallen_sky",
         "roles": ["mid", "support"],
         "reason": "AoE-урон + стан"},
        {"name": "Dezun Bloodrite", "internal": "item_dezun_bloodrite",
         "roles": ["mid", "support"],
         "reason": "Усиление AoE"},
        {"name": "Magnifying Monocle", "internal": "item_magnifying_monocle",
         "roles": ["carry", "mid"],
         "reason": "Ускорение фарма"},
        {"name": "Crippling Crossbow", "internal": "item_crippling_crossbow",
         "roles": ["support"],
         "reason": "Замедление"},
        {"name": "Flicker", "internal": "item_flicker",
         "roles": ["carry", "mid"],
         "reason": "Уклонение"},
        {"name": "Force Boots", "internal": "item_force_boots",
         "roles": ["support"],
         "reason": "Мобильность"},
        {"name": "Stygian Desolator", "internal": "item_stygian_desolator",
         "roles": ["carry"],
         "reason": "Минус броня"},
        {"name": "Mirror Shield", "internal": "item_mirror_shield",
         "roles": ["offlane"],
         "reason": "Отражение заклинаний"},
        {"name": "Unwavering Condition", "internal": "item_unwavering_condition",
         "roles": ["carry", "mid"],
         "reason": "Стабильный урон"},
        {"name": "Book of the Dead", "internal": "item_book_of_the_dead",
         "roles": ["support"],
         "reason": "Скелеты-помощники"},
    ],
}


# ─────────────────────────────────────────────────────────
#  Чары (энчантменты) — дают пассивные статы
# ─────────────────────────────────────────────────────────
ENCHANTMENTS = [
    {"name": "Quickened", "roles": ["support", "mid"],
     "reason": "−кулдауны, +уклонение"},
    {"name": "Mystical", "roles": ["mid", "support"],
     "reason": "+мана реген, +маг. сопр."},
    {"name": "Timeless", "roles": ["support", "mid"],
     "reason": "+длительность, +урон заклинаний"},
    {"name": "Tough", "roles": ["offlane", "carry"],
     "reason": "+урон, +броня, +сопр. отталкиванию"},
    {"name": "Keen-eyed", "roles": ["support", "mid"],
     "reason": "+дальность, +восст. маны"},
    {"name": "Manic", "roles": ["carry", "mid"],
     "reason": "+скорость атаки, +урон"},
    {"name": "Elusive", "roles": ["carry", "mid"],
     "reason": "+уклонение, +скорость"},
    {"name": "Ferocious", "roles": ["carry", "offlane"],
     "reason": "+урон с руки, лайфстил"},
    {"name": "Brute", "roles": ["offlane", "carry"],
     "reason": "+сила, +HP"},
    {"name": "Alert", "roles": ["support", "mid"],
     "reason": "+дальность атаки, +маг. сопр."},
    {"name": "Cruel", "roles": ["mid", "support"],
     "reason": "+усиление закл., −расход маны"},
    {"name": "Fierce", "roles": ["carry", "mid"],
     "reason": "+урон, +скорость атаки"},
]


MADSTONE_THRESHOLD = {
    1: 5,
    2: 10,
    3: 15,
    4: 20,
}


def get_current_tier(minutes):
    if 5 <= minutes < 15:
        return 1
    if 15 <= minutes < 25:
        return 2
    if 25 <= minutes < 35:
        return 3
    if minutes >= 35:
        return 4
    return None


def _all_neutral_internal_names():
    names = set()
    for tier in ARTIFACTS_BY_TIER.values():
        for a in tier:
            names.add(a["internal"])
    return names


def _neutral_inventory_tiers(state):
    """Вернуть множество тиров нейтралок, которые уже в инвентаре."""
    all_map = {}
    for tier, items in ARTIFACTS_BY_TIER.items():
        for a in items:
            all_map[a["internal"]] = tier

    tiers_in_inv = set()
    items = state.get("items", {})
    for slot_data in items.values():
        if isinstance(slot_data, dict):
            n = slot_data.get("name", "")
            if n in all_map:
                tiers_in_inv.add(all_map[n])
    return tiers_in_inv


def _get_madstones(state):
    player = state.get("player", {})
    ms = player.get("madstones")
    if ms is not None:
        return int(ms)

    items = state.get("items", {})
    count = 0
    for slot_data in items.values():
        if isinstance(slot_data, dict):
            n = slot_data.get("name", "")
            if n == "item_madstone_bundle":
                count += slot_data.get("count", 1) or 1
    return count if count > 0 else None


def get_neutral_item_tips(state, hero_role="support"):
    """
    Нумерованные советы по нейтралкам.
    Не блокируем, если уже есть нейтралка другого тира.
    """
    tips = []

    map_data = state.get("map", {})
    clock = map_data.get("clock_time", 0) or 0
    minutes = clock // 60

    tier = get_current_tier(minutes)
    if tier is None:
        return tips

    # Если у тебя уже есть нейтралка ЭТОГО тира — молчим,
    # иначе показываем советы (у тебя могут быть нейтралки более низких тиров)
    tiers_in_inv = _neutral_inventory_tiers(state)
    if tier in tiers_in_inv:
        return tips

    threshold = MADSTONE_THRESHOLD.get(tier, 10)
    madstones = _get_madstones(state)

    # ── Прогресс мадстонов ──
    if madstones is not None:
        if madstones >= threshold:
            tips.append(
                f"🎁 Мадстоны {madstones}/{threshold} — выбирай T{tier}!"
            )
        elif madstones >= threshold - 1:
            tips.append(
                f"🎁 Мадстоны {madstones}/{threshold} — ещё 1 и берёшь T{tier}"
            )

    # ── Топ-3 артефакта для роли ──
    artifacts = ARTIFACTS_BY_TIER.get(tier, [])
    role_artifacts = [a for a in artifacts if hero_role in a.get("roles", [])]
    if not role_artifacts:
        role_artifacts = artifacts

    if role_artifacts:
        tips.append(f"⚔ Артефакт T{tier} (топ по роли):")
        for i, a in enumerate(role_artifacts[:3], 1):
            tips.append(f"  {i}. {a['name']} — {a['reason']}")

    # ── Топ-3 чар для роли ──
    role_ench = [e for e in ENCHANTMENTS if hero_role in e.get("roles", [])]
    if not role_ench:
        role_ench = ENCHANTMENTS

    if role_ench:
        tips.append(f"✨ Чары (топ по роли):")
        for i, e in enumerate(role_ench[:3], 1):
            tips.append(f"  {i}. {e['name']} — {e['reason']}")

    return tips