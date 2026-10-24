import unittest

from draft_advisor import recommend_picks


class DraftAdvisorTests(unittest.TestCase):
    def setUp(self):
        self.heroes = [
            {
                "id": 1,
                "name": "npc_dota_hero_phantom_assassin",
                "localized_name": "Phantom Assassin",
                "roles": ["Carry"],
            },
            {
                "id": 2,
                "name": "npc_dota_hero_axe",
                "localized_name": "Axe",
                "roles": ["Offlane"],
            },
            {
                "id": 3,
                "name": "npc_dota_hero_oracle",
                "localized_name": "Oracle",
                "roles": ["Support"],
            },
        ]

    def test_recommends_available_builtin_counters(self):
        recommendations = recommend_picks(
            self.heroes,
            ally_ids=[],
            enemy_ids=["npc_dota_hero_phantom_assassin"],
            matchups={},
        )

        names = [item["hero"]["name"] for item in recommendations]
        self.assertIn("npc_dota_hero_axe", names)
        self.assertIn("npc_dota_hero_oracle", names)

    def test_open_dota_matchup_stats_affect_rank_and_explanation(self):
        recommendations = recommend_picks(
            self.heroes,
            ally_ids=[],
            enemy_ids=["npc_dota_hero_phantom_assassin"],
            matchups={
                "npc_dota_hero_phantom_assassin": [
                    {"hero_id": 2, "games_played": 100, "wins": 40}
                ]
            },
        )

        axe = next(
            item for item in recommendations
            if item["hero"]["name"] == "npc_dota_hero_axe"
        )
        self.assertEqual(axe["stats_rate"], 0.6)
        self.assertEqual(axe["games"], 100)
        self.assertTrue(any("OpenDota" in reason for reason in axe["reasons"]))
        self.assertEqual(
            recommendations[0]["hero"]["name"],
            "npc_dota_hero_axe",
        )

    def test_excludes_heroes_already_picked(self):
        recommendations = recommend_picks(
            self.heroes,
            ally_ids=["npc_dota_hero_axe"],
            enemy_ids=["npc_dota_hero_phantom_assassin"],
            matchups={},
        )

        self.assertNotIn(
            "npc_dota_hero_axe",
            [item["hero"]["name"] for item in recommendations],
        )

    def test_needs_at_least_one_enemy_pick(self):
        self.assertEqual(
            recommend_picks(self.heroes, [], [], {}),
            [],
        )


if __name__ == "__main__":
    unittest.main()
