_previous_kda = {}


def calculate_score(kills, deaths, assists):
    """
    Ценность игрока по KDA.
    Формула: K*1.0 + A*0.6 - D*1.2
    """
    weighted = kills * 1.0 + assists * 0.6
    penalty = deaths * 1.2
    score = weighted - penalty
    return round(score, 1)


def get_kda_table(state, my_team_slot=None):
    global _previous_kda

    players = state.get("players", [])
    if not players:
        # Обычная игра — только свой KDA
        player = state.get("player", {})
        hero = state.get("hero", {})
        if not player or not hero:
            return []

        k = player.get("kills", 0) or 0
        d = player.get("deaths", 0) or 0
        a = player.get("assists", 0) or 0
        score = calculate_score(k, d, a)

        hero_name = hero.get("name", "")
        name = player.get("name") or _hero_display(hero_name)

        return [{
            "name": name,
            "hero": hero_name,
            "kills": k,
            "deaths": d,
            "assists": a,
            "score": score,
            "trend": "flat",
            "team": "my",
            "slot": 0,
        }]

    result = []
    for p in players:
        hero_name = p.get("hero_name") or p.get("hero", {}).get("name", "")
        if not hero_name:
            continue

        slot = p.get("player_slot", 0)
        team = "radiant" if slot < 128 else "dire"

        k = p.get("kills", 0) or 0
        d = p.get("deaths", 0) or 0
        a = p.get("assists", 0) or 0
        score = calculate_score(k, d, a)

        prev = _previous_kda.get(slot)
        trend = "flat"
        if prev is not None:
            if score > prev + 0.05:
                trend = "up"
            elif score < prev - 0.05:
                trend = "down"
        _previous_kda[slot] = score

        result.append({
            "name": p.get("name", f"Игрок {slot}"),
            "hero": hero_name,
            "kills": k,
            "deaths": d,
            "assists": a,
            "score": score,
            "trend": trend,
            "team": team,
            "slot": slot,
        })

    result.sort(key=lambda x: x["score"], reverse=True)
    return result


def _hero_display(hero_name):
    if not hero_name:
        return "?"
    return (
        hero_name
        .replace("npc_dota_hero_", "")
        .replace("_", " ")
        .title()
    )


def reset():
    global _previous_kda
    _previous_kda.clear()