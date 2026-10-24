import json
import time
from pathlib import Path

import requests


API_URL = "https://api.opendota.com/api"
CACHE_PATH = Path.home() / ".dota_coach" / "draft_cache.json"
CACHE_TTL = 24 * 60 * 60

BUILTIN_COUNTERS = {
    "npc_dota_hero_phantom_assassin": {
        "npc_dota_hero_axe": "Контроль прыжка и защита от физического урона",
        "npc_dota_hero_oracle": "Защита союзника от физического бурста",
        "npc_dota_hero_razor": "Снижение урона и сильная линия",
    },
    "npc_dota_hero_bristleback": {
        "npc_dota_hero_ancient_apparition": "Блокирует лечение и регенерацию",
        "npc_dota_hero_viper": "Сильное давление на линии",
        "npc_dota_hero_necrolyte": "Снижает выживаемость и наказывает за низкое здоровье",
    },
    "npc_dota_hero_huskar": {
        "npc_dota_hero_ancient_apparition": "Блокирует лечение",
        "npc_dota_hero_viper": "Сильное давление на линии",
        "npc_dota_hero_axe": "Надежно контролирует героя с низким здоровьем",
    },
    "npc_dota_hero_meepo": {
        "npc_dota_hero_earthshaker": "Мощный урон по нескольким клонам",
        "npc_dota_hero_leshrac": "Массовый урон по клонам",
        "npc_dota_hero_winter_wyvern": "Контроль группы клонов",
    },
    "npc_dota_hero_broodmother": {
        "npc_dota_hero_earthshaker": "Эффективен против пауков и призывов",
        "npc_dota_hero_ember_spirit": "Быстро зачищает пауков",
        "npc_dota_hero_leshrac": "Массовый урон по призывам",
    },
    "npc_dota_hero_tinker": {
        "npc_dota_hero_nyx_assassin": "Наказывает за частое применение заклинаний",
        "npc_dota_hero_silencer": "Срывает применение заклинаний",
        "npc_dota_hero_night_stalker": "Ограничивает позиционную игру и применение заклинаний",
    },
    "npc_dota_hero_sniper": {
        "npc_dota_hero_spirit_breaker": "Может добраться до героя на дальней дистанции",
        "npc_dota_hero_spectre": "Находит и атакует из любой точки карты",
        "npc_dota_hero_clockwerk": "Надежно начинает бой с дальней дистанции",
    },
    "npc_dota_hero_antimage": {
        "npc_dota_hero_lion": "Длительный контроль и давление на ману",
        "npc_dota_hero_bane": "Надежный контроль мобильного героя",
        "npc_dota_hero_pugna": "Наказывает за низкий запас маны",
    },
    "npc_dota_hero_morphling": {
        "npc_dota_hero_ancient_apparition": "Блокирует лечение и восстановление здоровья",
        "npc_dota_hero_lion": "Мгновенный контроль и урон",
        "npc_dota_hero_axe": "Контроль, опасный для героя с низким здоровьем",
    },
    "npc_dota_hero_faceless_void": {
        "npc_dota_hero_disruptor": "Может вернуть мобильного героя после прыжка",
        "npc_dota_hero_winter_wyvern": "Способности могут сорвать атаку в Chronosphere",
        "npc_dota_hero_shadow_demon": "Может спасти союзников из Chronosphere",
    },
    "npc_dota_hero_enigma": {
        "npc_dota_hero_silencer": "Может прервать применение Black Hole",
        "npc_dota_hero_rubick": "Может украсть Black Hole",
        "npc_dota_hero_winter_wyvern": "Может сорвать командную драку",
    },
    "npc_dota_hero_puck": {
        "npc_dota_hero_silencer": "Сайленс мешает использовать мобильность",
        "npc_dota_hero_night_stalker": "Ограничивает применение заклинаний",
        "npc_dota_hero_disruptor": "Наказывает за попытку отступить",
    },
    "npc_dota_hero_storm_spirit": {
        "npc_dota_hero_silencer": "Сайленс мешает использовать мобильность",
        "npc_dota_hero_nyx_assassin": "Наказывает за частое применение заклинаний",
        "npc_dota_hero_disruptor": "Может вернуть героя после прыжка",
    },
    "npc_dota_hero_slark": {
        "npc_dota_hero_bloodseeker": "Раскрывает героя и мешает отступить",
        "npc_dota_hero_zuus": "Может обнаружить героя под Shadow Dance",
        "npc_dota_hero_ursa": "Силен в затяжной дуэли",
    },
    "npc_dota_hero_medusa": {
        "npc_dota_hero_antimage": "Сжигает ману, от которой зависит выживаемость",
        "npc_dota_hero_invoker": "Сильные заклинания против героя с большим запасом маны",
        "npc_dota_hero_lion": "Может быстро истощить ману",
    },
    "npc_dota_hero_terrorblade": {
        "npc_dota_hero_earthshaker": "Массовый урон по иллюзиям",
        "npc_dota_hero_leshrac": "Быстро зачищает иллюзии",
        "npc_dota_hero_winter_wyvern": "Контролирует иллюзии и срывает атаку",
    },
    "npc_dota_hero_naga_siren": {
        "npc_dota_hero_earthshaker": "Массовый урон по иллюзиям",
        "npc_dota_hero_leshrac": "Быстро зачищает иллюзии",
        "npc_dota_hero_ember_spirit": "Эффективно зачищает иллюзии",
    },
    "npc_dota_hero_phantom_lancer": {
        "npc_dota_hero_earthshaker": "Массовый урон по иллюзиям",
        "npc_dota_hero_leshrac": "Быстро зачищает иллюзии",
        "npc_dota_hero_ember_spirit": "Эффективно зачищает иллюзии",
    },
    "npc_dota_hero_ursa": {
        "npc_dota_hero_shadow_demon": "Может вывести героя из драки",
        "npc_dota_hero_vengefulspirit": "Может спасти цель от прыжка",
        "npc_dota_hero_troll_warlord": "Силен в продолжительном бою",
    },
    "npc_dota_hero_wraith_king": {
        "npc_dota_hero_ancient_apparition": "Блокирует восстановление здоровья",
        "npc_dota_hero_necrolyte": "Наказывает за низкое здоровье",
        "npc_dota_hero_ursa": "Высокий урон по одиночной цели",
    },
    "npc_dota_hero_dazzle": {
        "npc_dota_hero_ancient_apparition": "Блокирует лечение",
        "npc_dota_hero_silencer": "Мешает применить спасительные заклинания",
        "npc_dota_hero_doom_bringer": "Мешает использовать заклинания и предметы",
    },
    "npc_dota_hero_oracle": {
        "npc_dota_hero_silencer": "Мешает применить спасительные заклинания",
        "npc_dota_hero_doom_bringer": "Мешает использовать заклинания и предметы",
        "npc_dota_hero_ancient_apparition": "Блокирует лечение",
    },
    "npc_dota_hero_chen": {
        "npc_dota_hero_earthshaker": "Силен против группы призывов",
        "npc_dota_hero_leshrac": "Массовый урон по призывам",
        "npc_dota_hero_axe": "Может быстро зачистить группу крипов",
    },
}

_FALLBACK_ALIASES = {
    "npc_dota_hero_anti_mage": "npc_dota_hero_antimage",
}


def _read_cache():
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _write_cache(cache):
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(
            json.dumps(cache, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"[draft] не удалось сохранить кэш: {exc}")


def _fallback_catalog():
    from enemy_analyzer import HERO_THREATS
    from hero_builds import get_role

    heroes = {}
    for raw_name in HERO_THREATS:
        name = _FALLBACK_ALIASES.get(raw_name, raw_name)
        short_name = name.removeprefix("npc_dota_hero_")
        heroes[name] = {
            "id": name,
            "name": name,
            "localized_name": short_name.replace("_", " ").title(),
            "roles": [get_role(name)],
        }
    return sorted(heroes.values(), key=lambda hero: hero["localized_name"])


def load_hero_catalog():
    cache = _read_cache()
    cached = cache.get("heroes")
    if cached and time.time() - cache.get("heroes_updated", 0) < CACHE_TTL:
        return cached, "OpenDota (кэш)"

    try:
        response = requests.get(f"{API_URL}/heroes", timeout=8)
        response.raise_for_status()
        heroes = response.json()
        if not isinstance(heroes, list) or not heroes:
            raise ValueError("OpenDota вернул пустой список героев")
        heroes.sort(key=lambda hero: hero["localized_name"])
        cache["heroes"] = heroes
        cache["heroes_updated"] = time.time()
        _write_cache(cache)
        return heroes, "OpenDota"
    except (requests.RequestException, ValueError, KeyError) as exc:
        if cached:
            return cached, f"кэш OpenDota; сеть недоступна: {exc}"
        return _fallback_catalog(), f"локальная база; OpenDota недоступен: {exc}"


def load_matchups(enemy_ids):
    cache = _read_cache()
    matchups_cache = cache.setdefault("matchups", {})
    results = {}
    warnings = []
    changed = False

    for enemy_id in enemy_ids:
        cached = matchups_cache.get(str(enemy_id), {})
        is_fresh = (
            cached.get("updated", 0) > time.time() - CACHE_TTL
            and isinstance(cached.get("data"), list)
        )
        if is_fresh:
            results[enemy_id] = cached["data"]
            continue

        try:
            response = requests.get(
                f"{API_URL}/heroes/{enemy_id}/matchups",
                timeout=6,
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("OpenDota вернул неверный формат матчапов")
            matchups_cache[str(enemy_id)] = {
                "updated": time.time(),
                "data": data,
            }
            results[enemy_id] = data
            changed = True
        except (requests.RequestException, ValueError) as exc:
            warnings.append(f"Не загрузился матчап для {enemy_id}: {exc}")
            if isinstance(cached.get("data"), list):
                results[enemy_id] = cached["data"]

    if changed:
        _write_cache(cache)
    return results, warnings


def recommend_picks(heroes, ally_ids, enemy_ids, matchups, limit=10):
    if not enemy_ids:
        return []

    heroes_by_id = {hero["name"]: hero for hero in heroes}
    unavailable = set(ally_ids) | set(enemy_ids)
    counters = {}
    for enemy_id in enemy_ids:
        for hero_id, reason in BUILTIN_COUNTERS.get(enemy_id, {}).items():
            counters.setdefault(hero_id, []).append((enemy_id, reason))

    matchup_rows = {}
    for enemy_id in enemy_ids:
        for row in matchups.get(enemy_id, []):
            candidate_id = next(
                (
                    hero["name"]
                    for hero in heroes
                    if hero["id"] == row.get("hero_id")
                ),
                None,
            )
            if candidate_id is None:
                continue
            games = row.get("games_played", 0)
            wins = row.get("wins", 0)
            if not isinstance(games, int) or not isinstance(wins, int) or games <= 0:
                continue
            matchup_rows.setdefault(candidate_id, []).append(
                (enemy_id, games, wins)
            )

    recommendations = []
    candidates = (set(matchup_rows) | set(counters)) - unavailable
    for candidate_id in candidates:
        hero = heroes_by_id.get(candidate_id)
        if hero is None:
            continue

        rows = matchup_rows.get(candidate_id, [])
        total_games = sum(games for _, games, _ in rows)
        stats_rate = (
            sum(games - wins for _, games, wins in rows) / total_games
            if total_games else None
        )
        # Shrink small samples toward an even matchup; this is a ranking, not a win prediction.
        stat_score = (
            (stats_rate - 0.5) * 100 * total_games / (total_games + 250)
            if stats_rate is not None else 0
        )
        counter_details = counters.get(candidate_id, [])
        score = 50 + stat_score + min(6, 2.5 * len(counter_details))

        reasons = [
            f"{heroes_by_id.get(enemy_id, {}).get('localized_name', enemy_id)}: {reason}"
            for enemy_id, reason in counter_details
        ]
        if stats_rate is not None:
            reasons.insert(
                0,
                f"Матчапы OpenDota: {stats_rate * 100:.1f}% побед, "
                f"{total_games} игр",
            )

        recommendations.append({
            "hero": hero,
            "score": score,
            "stats_rate": stats_rate,
            "games": total_games,
            "reasons": reasons,
        })

    recommendations.sort(
        key=lambda item: (
            item["score"],
            item["games"],
            item["hero"]["localized_name"],
        ),
        reverse=True,
    )
    return recommendations[:limit]
