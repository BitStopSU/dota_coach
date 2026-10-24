from collections import defaultdict


_SCHEDULES = (
    ("Руна богатства", 0, 180),
    ("Руна силы", 360, 120),
    ("Руна мудрости", 420, 420),
    ("Нейтральные предметы — тир 1", 420, None),
    ("Нейтральные предметы — тир 2", 1020, None),
    ("Нейтральные предметы — тир 3", 1620, None),
    ("Нейтральные предметы — тир 4", 2220, None),
    ("Нейтральные предметы — тир 5", 3600, None),
)


def _events_between(start, end):
    events = defaultdict(list)
    if end <= start:
        return events

    for label, first_time, interval in _SCHEDULES:
        if interval is None:
            times = (first_time,) if start < first_time <= end else ()
        else:
            first_index = max(0, (start - first_time) // interval + 1)
            last_index = (end - first_time) // interval
            times = (
                first_time + index * interval
                for index in range(first_index, last_index + 1)
            )

        for event_time in times:
            events[event_time].append(label)

    return events


def upcoming_events(clock, horizon=60):
    """Return event groups occurring after clock within the given horizon."""
    events = _events_between(clock, clock + horizon)
    return [
        {
            "time": event_time,
            "seconds_until": event_time - clock,
            "labels": labels,
        }
        for event_time, labels in sorted(events.items())
    ]


class GameEventTracker:
    def __init__(self):
        self.last_clock = None

    def reset(self):
        self.last_clock = None

    def update(self, clock):
        """Return event groups crossed since the previous game-clock update."""
        previous_clock = self.last_clock
        self.last_clock = clock
        if previous_clock is None or clock < previous_clock:
            return []

        return [
            {"time": event_time, "labels": labels}
            for event_time, labels in sorted(
                _events_between(previous_clock, clock).items()
            )
        ]
