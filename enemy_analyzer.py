from collections import defaultdict

_enemy_inventories = defaultdict(set)
_enemy_picks = set()

# ─────────────────────────────────────────────────────────
#  Таблица угроз → контр-предметы
# ─────────────────────────────────────────────────────────
THREAT_COUNTERS = {
    "physical": {
        "name": "Физический урон",
        "items": ["Assault Cuirass", "Crimson Guard", "Ghost Scepter", "Heaven's Halberd"],
    },
    "magic": {
        "name": "Магический урон",
        "items": ["Pipe of Insight", "Glimmer Cape", "Black King Bar"],
    },
    "cc": {
        "name": "Контроль (станы/руты)",
        "items": ["Black King Bar", "Linken's Sphere", "Force Staff", "Scythe of Vyse"],
    },
    "silence": {
        "name": "Сайленс",
        "items": ["Manta Style", "Eul's Scepter", "Guardian Greaves", "Lotus Orb"],
    },
    "evasion": {
        "name": "Уклонение",
        "items": ["Monkey King Bar", "Bloodthorn", "Nullifier"],
    },
    "bkb_pierce": {
        "name": "Угрозы через BKB",
        "items": ["Scythe of Vyse", "Orchid Malevolence", "Bloodthorn", "Ethereal Blade"],
    },
    "armor": {
        "name": "Высокая броня",
        "items": ["Desolator", "Assault Cuirass", "Monkey King Bar"],
    },
    "heal": {
        "name": "Лечение/Регенерация",
        "items": ["Spirit Vessel", "Eye of Skadi", "Shiva's Guard"],
    },
    "illusions": {
        "name": "Иллюзии",
        "items": ["Maelstrom", "Mjollnir", "Battle Fury", "Radiance"],
    },
    "invis": {
        "name": "Невидимость",
        "items": ["Dust of Appearance", "Sentry Ward", "Gem of True Sight"],
    },
    "burst": {
        "name": "Магический бурст",
        "items": ["Black King Bar", "Glimmer Cape", "Pipe of Insight", "Hood of Defiance"],
    },
    "summons": {
        "name": "Саммоны/Призывы",
        "items": ["Maelstrom", "Mjollnir", "Battle Fury", "Crimson Guard"],
    },
    "mobility": {
        "name": "Мобильность/Прыжки",
        "items": ["Rod of Atos", "Scythe of Vyse", "Orchid Malevolence", "Nullifier"],
    },
    "sustain": {
        "name": "Устойчивость/Лайфстил",
        "items": ["Spirit Vessel", "Eye of Skadi", "Shiva's Guard", "Skull Basher"],
    },
}

# ─────────────────────────────────────────────────────────
#  Угрозы по героям (все 120+)
# ─────────────────────────────────────────────────────────
HERO_THREATS = {
    # ── Strength ──────────────────────────────────
    "npc_dota_hero_alchemist":          ["physical", "heal", "sustain"],
    "npc_dota_hero_axe":                ["physical", "cc"],
    "npc_dota_hero_bristleback":        ["physical", "armor", "sustain"],
    "npc_dota_hero_centaur":            ["physical", "cc", "burst"],
    "npc_dota_hero_chaos_knight":       ["physical", "cc", "illusions"],
    "npc_dota_hero_dawnbreaker":        ["physical", "heal", "cc"],
    "npc_dota_hero_doom_bringer":       ["cc", "silence", "sustain"],
    "npc_dota_hero_dragon_knight":      ["physical", "cc", "armor"],
    "npc_dota_hero_earth_spirit":       ["magic", "cc", "mobility"],
    "npc_dota_hero_earthshaker":        ["magic", "cc", "burst"],
    "npc_dota_hero_elder_titan":        ["magic", "cc", "summons"],
    "npc_dota_hero_huskar":             ["physical", "heal", "sustain"],
    "npc_dota_hero_kunkka":             ["physical", "cc", "burst"],
    "npc_dota_hero_legion_commander":   ["physical", "cc", "heal"],
    "npc_dota_hero_life_stealer":       ["physical", "sustain", "cc"],
    "npc_dota_hero_mars":               ["physical", "cc", "armor"],
    "npc_dota_hero_night_stalker":      ["physical", "silence", "cc"],
    "npc_dota_hero_ogre_magi":          ["magic", "cc", "burst"],
    "npc_dota_hero_omniknight":         ["heal", "cc"],
    "npc_dota_hero_primal_beast":       ["physical", "cc", "mobility"],
    "npc_dota_hero_pudge":              ["magic", "cc", "burst"],
    "npc_dota_hero_slardar":            ["physical", "cc", "armor"],
    "npc_dota_hero_spirit_breaker":     ["physical", "cc", "mobility"],
    "npc_dota_hero_sven":               ["physical", "cc", "burst"],
    "npc_dota_hero_tidehunter":         ["physical", "cc", "armor"],
    "npc_dota_hero_timbersaw":          ["magic", "armor", "mobility"],
    "npc_dota_hero_tiny":               ["physical", "burst", "cc"],
    "npc_dota_hero_treant":             ["heal", "cc", "invis"],
    "npc_dota_hero_tusk":               ["physical", "cc", "burst"],
    "npc_dota_hero_underlord":          ["magic", "cc", "armor"],
    "npc_dota_hero_undying":            ["heal", "summons", "sustain"],
    "npc_dota_hero_wraith_king":        ["physical", "cc", "sustain"],

    # ── Agility ───────────────────────────────────
    "npc_dota_hero_anti_mage":          ["physical", "mobility", "armor"],
    "npc_dota_hero_arc_warden":         ["physical", "illusions", "burst"],
    "npc_dota_hero_bloodseeker":        ["physical", "silence", "sustain"],
    "npc_dota_hero_bounty_hunter":      ["physical", "invis", "burst"],
    "npc_dota_hero_clinkz":             ["physical", "invis", "mobility"],
    "npc_dota_hero_drow_ranger":        ["physical", "silence"],
    "npc_dota_hero_ember_spirit":       ["magic", "mobility", "burst"],
    "npc_dota_hero_faceless_void":      ["physical", "cc", "evasion"],
    "npc_dota_hero_gyrocopter":         ["physical", "burst"],
    "npc_dota_hero_hoodwink":           ["magic", "cc", "burst"],
    "npc_dota_hero_juggernaut":         ["physical", "heal", "mobility"],
    "npc_dota_hero_luna":               ["physical", "burst", "mobility"],
    "npc_dota_hero_medusa":             ["physical", "armor", "sustain"],
    "npc_dota_hero_meepo":              ["physical", "summons", "burst"],
    "npc_dota_hero_monkey_king":        ["physical", "invis", "mobility"],
    "npc_dota_hero_morphling":          ["physical", "mobility", "sustain"],
    "npc_dota_hero_naga_siren":         ["physical", "illusions", "cc"],
    "npc_dota_hero_nevermore":          ["magic", "physical", "burst"],
    "npc_dota_hero_nyx_assassin":       ["magic", "invis", "cc", "burst"],
    "npc_dota_hero_pangolier":          ["physical", "cc", "mobility", "evasion"],
    "npc_dota_hero_phantom_assassin":   ["physical", "evasion", "burst"],
    "npc_dota_hero_phantom_lancer":     ["physical", "illusions", "mobility"],
    "npc_dota_hero_razor":              ["physical", "armor", "sustain"],
    "npc_dota_hero_riki":               ["physical", "invis", "silence"],
    "npc_dota_hero_slark":              ["physical", "heal", "invis", "cc"],
    "npc_dota_hero_sniper":             ["physical", "burst"],
    "npc_dota_hero_spectre":            ["physical", "illusions", "sustain"],
    "npc_dota_hero_terrorblade":        ["physical", "illusions", "burst"],
    "npc_dota_hero_troll_warlord":      ["physical", "evasion", "sustain"],
    "npc_dota_hero_ursa":               ["physical", "burst", "sustain"],
    "npc_dota_hero_viper":              ["physical", "magic", "armor"],
    "npc_dota_hero_weaver":             ["physical", "invis", "mobility"],

    # ── Intelligence ──────────────────────────────
    "npc_dota_hero_ancient_apparition": ["magic", "burst", "heal"],
    "npc_dota_hero_bane":               ["magic", "cc", "burst"],
    "npc_dota_hero_batrider":           ["magic", "cc", "mobility"],
    "npc_dota_hero_chen":               ["summons", "heal", "burst"],
    "npc_dota_hero_crystal_maiden":     ["magic", "cc", "burst"],
    "npc_dota_hero_dark_seer":          ["magic", "illusions", "cc"],
    "npc_dota_hero_dark_willow":        ["magic", "cc", "burst"],
    "npc_dota_hero_dazzle":             ["heal", "magic", "sustain"],
    "npc_dota_hero_death_prophet":      ["magic", "silence", "summons"],
    "npc_dota_hero_disruptor":          ["magic", "cc", "silence"],
    "npc_dota_hero_enchantress":        ["physical", "heal", "summons"],
    "npc_dota_hero_enigma":             ["magic", "cc", "summons"],
    "npc_dota_hero_grimstroke":         ["magic", "cc", "silence"],
    "npc_dota_hero_invoker":            ["magic", "cc", "burst", "summons"],
    "npc_dota_hero_jakiro":             ["magic", "cc", "burst"],
    "npc_dota_hero_keeper_of_the_light":["magic", "heal", "cc"],
    "npc_dota_hero_leshrac":            ["magic", "burst", "mobility"],
    "npc_dota_hero_lich":               ["magic", "burst", "heal"],
    "npc_dota_hero_lina":               ["magic", "burst"],
    "npc_dota_hero_lion":               ["magic", "cc", "burst"],
    "npc_dota_hero_muerta":             ["magic", "physical", "burst"],
    "npc_dota_hero_necrolyte":          ["magic", "heal", "sustain", "armor"],
    "npc_dota_hero_obsidian_destroyer": ["magic", "burst", "silence"],
    "npc_dota_hero_oracle":             ["heal", "magic", "cc"],
    "npc_dota_hero_outworld_destroyer": ["magic", "burst", "silence"],
    "npc_dota_hero_puck":               ["magic", "cc", "silence", "mobility"],
    "npc_dota_hero_pugna":              ["magic", "burst", "heal"],
    "npc_dota_hero_queenofpain":        ["magic", "burst", "mobility"],
    "npc_dota_hero_rubick":             ["magic", "cc", "burst"],
    "npc_dota_hero_shadow_demon":       ["magic", "cc", "silence"],
    "npc_dota_hero_shadow_shaman":      ["magic", "cc", "summons"],
    "npc_dota_hero_silencer":           ["magic", "silence", "burst"],
    "npc_dota_hero_skywrath_mage":      ["magic", "silence", "burst"],
    "npc_dota_hero_snapfire":           ["magic", "cc", "burst"],
    "npc_dota_hero_storm_spirit":       ["magic", "cc", "mobility", "burst"],
    "npc_dota_hero_techies":            ["magic", "burst", "silence"],
    "npc_dota_hero_tinker":             ["magic", "silence", "burst"],
    "npc_dota_hero_visage":             ["physical", "summons", "burst"],
    "npc_dota_hero_warlock":            ["magic", "heal", "cc", "summons"],
    "npc_dota_hero_winter_wyvern":      ["magic", "heal", "cc"],
    "npc_dota_hero_wisp":               ["heal", "sustain", "mobility"],
    "npc_dota_hero_witch_doctor":       ["magic", "cc", "burst"],
    "npc_dota_hero_zuus":               ["magic", "burst"],

    # ── Universal ─────────────────────────────────
    "npc_dota_hero_abaddon":            ["heal", "sustain", "cc"],
    "npc_dota_hero_broodmother":        ["physical", "summons", "invis"],
    "npc_dota_hero_lycan":              ["physical", "summons", "mobility"],
    "npc_dota_hero_marci":              ["physical", "heal", "cc", "mobility"],
    "npc_dota_hero_mirana":             ["magic", "cc", "mobility"],
    "npc_dota_hero_vengefulspirit":     ["physical", "cc", "mobility"],
    "npc_dota_hero_void_spirit":        ["magic", "mobility", "burst"],
    "npc_dota_hero_windrunner":         ["physical", "cc", "evasion"],
}


# ─────────────────────────────────────────────────────────
#  Определение врагов и угроз
# ─────────────────────────────────────────────────────────

def get_enemy_heroes(state, my_team="team2"):
    players = state.get("players", [])
    enemies = []

    for p in players:
        team = p.get("team", "")
        if not team:
            slot = p.get("player_slot", 0)
            team = "team2" if slot < 128 else "team3"

        if team != my_team:
            hero = p.get("hero_name") or p.get("hero", {}).get("name", "")
            if hero:
                enemies.append({
                    "hero": hero,
                    "name": p.get("name", ""),
                    "slot": p.get("player_slot"),
                    "items": p.get("items", {}),
                })

    return enemies


def analyze_threats(state, my_team="team2"):
    enemies = get_enemy_heroes(state, my_team)
    threats = set()
    for e in enemies:
        hero_threats = HERO_THREATS.get(e["hero"], [])
        threats.update(hero_threats)
    return threats, enemies


def get_counter_tips(state, my_team="team2"):
    tips = []
    threats, enemies = analyze_threats(state, my_team)

    if not threats:
        return tips

    # Ограничиваем до 4 самых важных угроз, чтобы не забивать экран
    priority_order = [
        "cc", "silence", "magic", "physical", "burst",
        "evasion", "armor", "heal", "invis", "illusions",
        "summons", "mobility", "sustain", "bkb_pierce"
    ]
    sorted_threats = [t for t in priority_order if t in threats][:4]

    for threat_key in sorted_threats:
        if threat_key not in THREAT_COUNTERS:
            continue
        threat = THREAT_COUNTERS[threat_key]
        items_str = ", ".join(threat["items"][:2])
        tips.append(f"{threat['name']} → {items_str}")

    return tips


def get_enemy_build_analysis(state, my_team="team2"):
    global _enemy_inventories

    tips = []
    enemies = get_enemy_heroes(state, my_team)

    for e in enemies:
        slot = e["slot"]
        if slot is None:
            continue

        current_items = set()
        for item_data in e["items"].values():
            if isinstance(item_data, dict):
                name = item_data.get("name", "")
                if name and name.startswith("item_"):
                    current_items.add(name)

        if slot not in _enemy_inventories:
            _enemy_inventories[slot] = current_items
            continue

        added = current_items - _enemy_inventories[slot]
        _enemy_inventories[slot] = current_items

        if added:
            hero_display = e["hero"].replace("npc_dota_hero_", "").replace("_", " ").title()
            for item in added:
                item_display = item.replace("item_", "").replace("_", " ").title()
                tips.append(f"{hero_display}: {item_display}")

    return tips


def reset():
    global _enemy_inventories, _enemy_picks
    _enemy_inventories.clear()
    _enemy_picks.clear()