# Формат:
# hero_name: {
#     "role": "mid" | "carry" | "offlane" | "support" | "hard_support",
#     "build": [
#         (item_name, display_name, avg_time_seconds, winrate_percent),
#         ...
#     ]
# }

HERO_BUILDS = {
    # ── Mid ──────────────────────────────────────────
    "npc_dota_hero_skywrath_mage": {
        "role": "mid",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   330,  56.0),
            ("item_null_talisman", "Null Talisman",  420,  55.0),
            ("item_rod_of_atos",   "Rod of Atos",    870,  58.0),
            ("item_ultimate_scepter", "Aghanim's",  1200,  60.0),
        ],
    },
    "npc_dota_hero_zuus": {
        "role": "mid",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   330,  55.0),
            ("item_aether_lens",   "Aether Lens",    780,  57.0),
            ("item_ultimate_scepter", "Aghanim's",  1200,  59.0),
            ("item_octarine_core", "Octarine",      1500,  58.0),
        ],
    },
    "npc_dota_hero_queenofpain": {
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  54.0),
            ("item_power_treads",  "Power Treads",   420,  55.0),
            ("item_orchid",        "Orchid",         900,  57.0),
            ("item_black_king_bar","BKB",           1320,  58.0),
        ],
    },
    "npc_dota_hero_storm_spirit": {
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  55.0),
            ("item_arcane_boots",  "Arcane Boots",   360,  55.0),
            ("item_orchid",        "Orchid",         900,  57.0),
            ("item_bloodstone",    "Bloodstone",    1200,  56.0),
        ],
    },
    "npc_dota_hero_lina": {
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  54.0),
            ("item_arcane_boots",  "Arcane Boots",   360,  55.0),
            ("item_aether_lens",   "Aether Lens",    780,  57.0),
            ("item_ultimate_scepter", "Aghanim's",  1200,  60.0),
        ],
    },
    "npc_dota_hero_puck": {
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  54.0),
            ("item_arcane_boots",  "Arcane Boots",   360,  55.0),
            ("item_blink",         "Blink Dagger",   720,  58.0),
            ("item_ultimate_scepter", "Aghanim's",  1200,  58.0),
        ],
    },
    "npc_dota_hero_tinker": {
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  55.0),
            ("item_soul_ring",     "Soul Ring",      360,  56.0),
            ("item_blink",         "Blink Dagger",   720,  58.0),
            ("item_ultimate_scepter", "Aghanim's",  1140,  60.0),
        ],
    },
    "npc_dota_hero_sniper": {
        "role": "mid",
        "build": [
            ("item_power_treads",  "Power Treads",   420,  55.0),
            ("item_dragon_lance",  "Dragon Lance",   720,  56.0),
            ("item_maelstrom",     "Maelstrom",      780,  57.0),
            ("item_black_king_bar","BKB",           1320,  58.0),
        ],
    },
    "npc_dota_hero_nevermore": {  # Shadow Fiend
        "role": "mid",
        "build": [
            ("item_bottle",        "Bottle",          90,  55.0),
            ("item_power_treads",  "Power Treads",   420,  55.0),
            ("item_black_king_bar","BKB",           1200,  58.0),
            ("item_butterfly",     "Butterfly",     1500,  60.0),
        ],
    },

    # ── Carry ────────────────────────────────────────
    "npc_dota_hero_phantom_assassin": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   480,  55.0),
            ("item_battle_fury",   "Battle Fury",   1020,  56.0),
            ("item_desolator",     "Desolator",     1200,  58.0),
            ("item_black_king_bar","BKB",           1500,  58.0),
        ],
    },
    "npc_dota_hero_juggernaut": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   480,  56.0),
            ("item_battle_fury",   "Battle Fury",   1020,  55.0),
            ("item_manta",         "Manta Style",   1200,  58.0),
            ("item_butterfly",     "Butterfly",     1500,  60.0),
        ],
    },
    "npc_dota_hero_antimage": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   540,  54.0),
            ("item_battle_fury",   "Battle Fury",   1080,  55.0),
            ("item_manta",         "Manta Style",   1260,  57.0),
            ("item_abyssal_blade","Abyssal Blade",  1740,  58.0),
        ],
    },
    "npc_dota_hero_faceless_void": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   480,  55.0),
            ("item_mask_of_madness","MoM",           780,  56.0),
            ("item_maelstrom",     "Maelstrom",      900,  56.0),
            ("item_black_king_bar","BKB",           1320,  58.0),
        ],
    },
    "npc_dota_hero_spectre": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   540,  54.0),
            ("item_radiance",      "Radiance",      1320,  56.0),
            ("item_manta",         "Manta Style",   1500,  57.0),
            ("item_heart",         "Heart",         1800,  58.0),
        ],
    },
    "npc_dota_hero_terrorblade": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   480,  55.0),
            ("item_dragon_lance",  "Dragon Lance",   720,  56.0),
            ("item_manta",         "Manta Style",   1260,  58.0),
            ("item_skadi",         "Eye of Skadi",  1620,  59.0),
        ],
    },
    "npc_dota_hero_slark": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   480,  55.0),
            ("item_echo_sabre",    "Echo Sabre",     960,  56.0),
            ("item_silver_edge",   "Silver Edge",   1320,  57.0),
            ("item_skadi",         "Eye of Skadi",  1620,  58.0),
        ],
    },
    "npc_dota_hero_medusa": {
        "role": "carry",
        "build": [
            ("item_power_treads",  "Power Treads",   540,  54.0),
            ("item_manta",         "Manta Style",   1200,  55.0),
            ("item_skadi",         "Eye of Skadi",  1500,  57.0),
            ("item_butterfly",     "Butterfly",     1740,  58.0),
        ],
    },

    # ── Offlane ──────────────────────────────────────
    "npc_dota_hero_axe": {
        "role": "offlane",
        "build": [
            ("item_vanguard",      "Vanguard",       780,  55.0),
            ("item_blink",         "Blink Dagger",  1020,  58.0),
            ("item_blade_mail",    "Blade Mail",    1200,  56.0),
            ("item_heart",         "Heart",         1800,  58.0),
        ],
    },
    "npc_dota_hero_bristleback": {
        "role": "offlane",
        "build": [
            ("item_vanguard",      "Vanguard",       780,  55.0),
            ("item_pipe",          "Pipe of Insight",1140,  56.0),
            ("item_heart",         "Heart",         1740,  57.0),
            ("item_ultimate_scepter","Aghanim's",   1500,  58.0),
        ],
    },
    "npc_dota_hero_tidehunter": {
        "role": "offlane",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   420,  55.0),
            ("item_blink",         "Blink Dagger",   900,  60.0),
            ("item_pipe",          "Pipe of Insight",1260,  57.0),
            ("item_refresher",     "Refresher",     1500,  58.0),
        ],
    },
    "npc_dota_hero_mars": {
        "role": "offlane",
        "build": [
            ("item_phase_boots",   "Phase Boots",    480,  55.0),
            ("item_blink",         "Blink Dagger",   900,  58.0),
            ("item_black_king_bar","BKB",           1260,  57.0),
            ("item_assault",       "Assault Cuirass",1740, 58.0),
        ],
    },
    "npc_dota_hero_underlord": {
        "role": "offlane",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   420,  55.0),
            ("item_pipe",          "Pipe of Insight",1200,  56.0),
            ("item_crimson_guard","Crimson Guard",  1320,  57.0),
            ("item_greaves",       "Guardian Greaves",1800, 58.0),
        ],
    },
    "npc_dota_hero_timbersaw": {
        "role": "offlane",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   420,  55.0),
            ("item_hood_of_defiance","Hood",         900,  56.0),
            ("item_kaya_and_sange","Kaya & Sange",  1320,  57.0),
            ("item_shivas_guard",  "Shiva's Guard", 1620,  58.0),
        ],
    },
    "npc_dota_hero_legion_commander": {
        "role": "offlane",
        "build": [
            ("item_phase_boots",   "Phase Boots",    480,  55.0),
            ("item_blink",         "Blink Dagger",   900,  58.0),
            ("item_blade_mail",    "Blade Mail",    1140,  56.0),
            ("item_black_king_bar","BKB",           1320,  57.0),
        ],
    },

    # ── Support ──────────────────────────────────────
    "npc_dota_hero_crystal_maiden": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_glimmer_cape",  "Glimmer Cape",  1020,  56.0),
            ("item_blink",         "Blink Dagger",  1320,  58.0),
            ("item_black_king_bar","BKB",           1680,  57.0),
        ],
    },
    "npc_dota_hero_lion": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  55.0),
            ("item_blink",         "Blink Dagger",  1080,  58.0),
            ("item_aether_lens",   "Aether Lens",   1200,  56.0),
            ("item_ultimate_scepter","Aghanim's",   1620,  58.0),
        ],
    },
    "npc_dota_hero_witch_doctor": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_glimmer_cape",  "Glimmer Cape",  1020,  55.0),
            ("item_aether_lens",   "Aether Lens",   1200,  56.0),
            ("item_ultimate_scepter","Aghanim's",   1620,  57.0),
        ],
    },
    "npc_dota_hero_shadow_shaman": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_blink",         "Blink Dagger",  1080,  58.0),
            ("item_aether_lens",   "Aether Lens",   1200,  56.0),
            ("item_ultimate_scepter","Aghanim's",   1620,  58.0),
        ],
    },
    "npc_dota_hero_dazzle": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_glimmer_cape",  "Glimmer Cape",   960,  55.0),
            ("item_aether_lens",   "Aether Lens",   1140,  56.0),
            ("item_ultimate_scepter","Aghanim's",   1560,  57.0),
        ],
    },
    "npc_dota_hero_warlock": {
        "role": "support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_glimmer_cape",  "Glimmer Cape",   960,  55.0),
            ("item_aether_lens",   "Aether Lens",   1140,  56.0),
            ("item_refresher",     "Refresher",     1680,  58.0),
        ],
    },
    "npc_dota_hero_oracle": {
        "role": "hard_support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  55.0),
            ("item_glimmer_cape",  "Glimmer Cape",   960,  57.0),
            ("item_aether_lens",   "Aether Lens",   1140,  56.0),
            ("item_force_staff",   "Force Staff",   1260,  56.0),
        ],
    },
    "npc_dota_hero_io": {
        "role": "hard_support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  56.0),
            ("item_mekansm",       "Mekansm",       1020,  57.0),
            ("item_greaves",       "Guardian Greaves",1560,58.0),
            ("item_holy_locket",   "Holy Locket",   1200,  56.0),
        ],
    },
    "npc_dota_hero_chen": {
        "role": "hard_support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   480,  56.0),
            ("item_mekansm",       "Mekansm",        900,  58.0),
            ("item_greaves",       "Guardian Greaves",1440,58.0),
            ("item_vladmir",       "Vladmir's",     1020,  56.0),
        ],
    },
    "npc_dota_hero_bane": {
        "role": "hard_support",
        "build": [
            ("item_arcane_boots",  "Arcane Boots",   540,  54.0),
            ("item_glimmer_cape",  "Glimmer Cape",   960,  56.0),
            ("item_aether_lens",   "Aether Lens",   1140,  56.0),
            ("item_black_king_bar","BKB",           1620,  57.0),
        ],
    },
}


def get_build(hero_name):
    """Вернуть билд героя или None."""
    return HERO_BUILDS.get(hero_name)


def get_role(hero_name):
    """Вернуть роль героя или 'support' по умолчанию."""
    build = HERO_BUILDS.get(hero_name)
    if build:
        return build["role"]
    return "support"


def get_all_builds():
    return HERO_BUILDS