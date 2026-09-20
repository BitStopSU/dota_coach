from collections import defaultdict

_previous_inventories = defaultdict(set)
purchase_events = []

_spectator_mode = False


def get_current_inventory(state):
    result = []
    if not state:
        return result

    players = state.get("players")
    if players:
        for p in players:
            hero = p.get("hero_name") or p.get("hero", {}).get("name", "")
            name = p.get("name", f"Игрок {p.get('player_slot', '?')}")
            for item_data in p.get("items", {}).values():
                if isinstance(item_data, dict):
                    n = item_data.get("name", "")
                    if n and n.startswith("item_"):
                        result.append((name, hero, n))
    else:
        hero = state.get("hero", {}).get("name", "")
        name = state.get("player", {}).get("name") or _hero_display(hero)
        for item_data in state.get("items", {}).values():
            if isinstance(item_data, dict):
                n = item_data.get("name", "")
                if n and n.startswith("item_"):
                    result.append((name, hero, n))

    return result


def detect_purchases(state):
    global purchase_events, _spectator_mode
    if not state:
        return []

    new_purchases = []
    players = state.get("players")

    if players:
        _spectator_mode = True
        for player in players:
            slot = player.get("player_slot")
            if slot is None:
                continue
            hero_name = player.get("hero_name") or player.get("hero", {}).get("name", "")
            player_name = player.get("name", f"Игрок {slot}")
            current_items = _extract_items(player.get("items", {}))
            _process_slot(slot, current_items, hero_name, player_name, new_purchases)
    else:
        _spectator_mode = False
        hero_name = state.get("hero", {}).get("name", "")
        player_block = state.get("player", {})
        slot = player_block.get("player_slot", 0)
        player_name = state.get("player", {}).get("name") or _hero_display(hero_name)
        current_items = _extract_items(state.get("items", {}))
        _process_slot(slot, current_items, hero_name, player_name, new_purchases)

    if new_purchases:
        purchase_events.extend(new_purchases)
        purchase_events = purchase_events[-100:]

    return new_purchases


def _extract_items(items_dict):
    names = set()
    if not isinstance(items_dict, dict):
        return names
    for item_data in items_dict.values():
        if isinstance(item_data, dict):
            name = item_data.get("name", "")
            if name and name.startswith("item_"):
                names.add(name)
    return names


def _process_slot(slot, current_items, hero_name, player_name, out_list):
    if slot not in _previous_inventories:
        _previous_inventories[slot] = current_items
        return

    prev = _previous_inventories[slot]
    added = current_items - prev

    for item in added:
        out_list.append({
            "player": player_name,
            "hero": hero_name,
            "item": item,
            "slot": slot,
        })

    _previous_inventories[slot] = current_items


def _hero_display(hero_name):
    if not hero_name:
        return "?"
    return hero_name.replace("npc_dota_hero_", "").replace("_", " ").title()


def get_recent_purchases(n=20):
    return purchase_events[-n:]


def is_spectator():
    return _spectator_mode


def reset():
    global purchase_events
    _previous_inventories.clear()
    purchase_events = []