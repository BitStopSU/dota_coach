STARTING_ITEMS = {
    "carry_melee": [
        "Quelling Blade", "Tango", "Slippers of Agility",
        "Circlet", "Iron Branch"
    ],
    "carry_ranged": [
        "Tango", "Slippers of Agility", "Circlet",
        "Iron Branch", "Iron Branch"
    ],
    "mid": [
        "Tango", "Circlet", "Iron Branch", "Iron Branch",
        "Faerie Fire"
    ],
    "offlane": [
        "Tango", "Stout Shield", "Quelling Blade",
        "Iron Branch", "Iron Branch"
    ],
    "support": [
        "Tango", "Blood Grenade", "Observer Ward",
        "Sentry Ward", "Smoke of Deceit"
    ],
    "hard_support": [
        "Tango", "Blood Grenade", "Observer Ward",
        "Sentry Ward", "Smoke of Deceit"
    ],
}

HERO_ROLES = {
    # Carry melee
    "Anti-Mage": "carry_melee",
    "Juggernaut": "carry_melee",
    "Phantom Assassin": "carry_melee",
    "Faceless Void": "carry_melee",
    "Slark": "carry_melee",
    "Monkey King": "carry_melee",
    "Ursa": "carry_melee",
    "Wraith King": "carry_melee",
    "Lifestealer": "carry_melee",
    "Chaos Knight": "carry_melee",
    "Sven": "carry_melee",
    "Troll Warlord": "carry_melee",
    "Bloodseeker": "carry_melee",
    "Lycan": "carry_melee",

    # Carry ranged
    "Terrorblade": "carry_ranged",
    "Drow Ranger": "carry_ranged",
    "Medusa": "carry_ranged",
    "Sniper": "carry_ranged",
    "Luna": "carry_ranged",
    "Clinkz": "carry_ranged",
    "Morphling": "carry_ranged",
    "Gyrocopter": "carry_ranged",

    # Mid
    "Invoker": "mid",
    "Storm Spirit": "mid",
    "Queen of Pain": "mid",
    "Shadow Fiend": "mid",
    "Puck": "mid",
    "Ember Spirit": "mid",
    "Zeus": "mid",
    "Lina": "mid",
    "Tinker": "mid",
    "Void Spirit": "mid",
    "Outworld Destroyer": "mid",
    "Templar Assassin": "mid",
    "Death Prophet": "mid",

    # Offlane
    "Axe": "offlane",
    "Bristleback": "offlane",
    "Tidehunter": "offlane",
    "Mars": "offlane",
    "Underlord": "offlane",
    "Beastmaster": "offlane",
    "Centaur Warrunner": "offlane",
    "Timbersaw": "offlane",
    "Sand King": "offlane",
    "Dark Seer": "offlane",
    "Legion Commander": "offlane",
    "Doom": "offlane",
    "Night Stalker": "offlane",

    # Support
    "Crystal Maiden": "support",
    "Lion": "support",
    "Witch Doctor": "support",
    "Shadow Shaman": "support",
    "Warlock": "support",
    "Dazzle": "support",
    "Jakiro": "support",
    "Ogre Magi": "support",
    "Silencer": "support",
    "Skywrath Mage": "support",

    # Hard support
    "Oracle": "hard_support",
    "Io": "hard_support",
    "Chen": "hard_support",
    "Bane": "hard_support",
    "Shadow Demon": "hard_support",
    "Visage": "hard_support",
    "Winter Wyvern": "hard_support",
    "Snapfire": "hard_support",
    "Marci": "hard_support",
}


def get_starting_items(hero_name):
    role = HERO_ROLES.get(hero_name, "support")
    return STARTING_ITEMS.get(role, STARTING_ITEMS["support"])