import unittest

import game_events


class GameEventTests(unittest.TestCase):
    def test_groups_wisdom_and_neutral_tier_at_seven_minutes(self):
        due = game_events.GameEventTracker()
        due.update(419)

        events = due.update(420)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["time"], 420)
        self.assertEqual(
            events[0]["labels"],
            ["Руна мудрости", "Нейтральные предметы — тир 1"],
        )

    def test_upcoming_event_has_countdown(self):
        events = game_events.upcoming_events(360)

        self.assertEqual(events[0]["seconds_until"], 60)
        self.assertEqual(
            events[0]["labels"],
            ["Руна мудрости", "Нейтральные предметы — тир 1"],
        )

    def test_bounty_and_power_runes_share_six_minute_event(self):
        tracker = game_events.GameEventTracker()
        tracker.update(359)

        events = tracker.update(360)

        self.assertEqual(
            events[0]["labels"],
            ["Руна богатства", "Руна силы"],
        )

    def test_tracker_does_not_repeat_or_fire_after_clock_reset(self):
        tracker = game_events.GameEventTracker()
        tracker.update(179)
        self.assertEqual(len(tracker.update(180)), 1)
        self.assertEqual(tracker.update(181), [])
        self.assertEqual(tracker.update(-60), [])
        self.assertEqual(tracker.update(-59), [])


if __name__ == "__main__":
    unittest.main()
