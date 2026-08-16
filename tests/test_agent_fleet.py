import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AgentFleetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "agents/registry.json").read_text(encoding="utf-8"))

    def test_validator(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "bin/validate-agent-fleet.py")],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_claude_agents_are_ported(self):
        legacy = {p.stem for p in (ROOT / ".claude/agents").glob("*.md")}
        self.assertTrue(legacy <= set(self.registry["agents"]))

    def test_cycle_order_and_parallel_research(self):
        morning = self.registry["cycles"]["morning"]
        self.assertGreater(len(morning[0]), 1)
        self.assertEqual(morning[-3:], [["logistics"], ["planner"], ["critic"]])
        self.assertEqual(self.registry["cycles"]["evening"], [["logistics"], ["planner"], ["critic"]])

    def test_critical_ownership(self):
        owners = {}
        for name, cfg in self.registry["agents"].items():
            for path in cfg["writes"]: owners.setdefault(path, []).append(name)
        self.assertEqual(owners["trip/itinerary.md"], ["planner"])
        self.assertNotIn("trip/itinerary.md", self.registry["agents"]["critic"]["writes"])
        self.assertFalse(set(self.registry["human_only"]) & set().union(
            *(set(a["writes"]) for a in self.registry["agents"].values())
        ))

    def test_food_and_map_agents(self):
        self.assertEqual(self.registry["agents"]["scout-food"]["writes"][0], "research/food.md")
        self.assertIn("scout-food", self.registry["cycles"]["morning"][0])
        self.assertEqual(self.registry["agents"]["mapmaker"]["modes"], [])
        self.assertIn("state/map.html", self.registry["agents"]["mapmaker"]["writes"])
        self.assertTrue((ROOT / "bin/mapkit/build_map.py").is_file())

if __name__ == "__main__":
    unittest.main()
