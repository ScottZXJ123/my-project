import json
from typing import List, Dict, Any, Optional

###############################################################################
#                        STRATEGY LIBRARY CLASS
###############################################################################

class StrategyLibrary:
    def __init__(self):
        self.rules = {
            "POSITION_BONUS": {"points": 5},
            "FAST_ATTACK_BONUS": {"points": 3},
            "CRITICAL_HIT_BONUS": {"points": 2},
            "ABILITY_USAGE_BONUS": {"points": 4},
            "ITEM_USAGE_BONUS": {"points": 3},
            "FIRST_STRIKE_BONUS": {"points": 2},
            "LAST_STAND_BONUS": {"points": 3},
            "HEALING_EFFICIENCY_BONUS": {"points": 4},
            "DEFENSE_SURVIVAL_BONUS": {"points": 2},
            "TEAMWORK_BONUS": {"points": 5},
            "MULTI_HIT_BONUS": {"points": 3},
            "DODGE_BONUS": {"points": 2},
            "COUNTER_ATTACK_BONUS": {"points": 3},
            "FLEXIBLE_POSITION_BONUS": {"points": 2},
            "CRITICAL_DEFENSE_BONUS": {"points": 2},
            "SPEED_ADVANTAGE_BONUS": {"points": 3},
            "LUCKY_HIT_BONUS": {"points": 1},
            "POWER_SURGE_BONUS": {"points": 4},
            "ELEMENTAL_ADVANTAGE_BONUS": {"points": 3},
            "SKILL_COMBO_BONUS": {"points": 4},
            "PENETRATION_BONUS": {"points": 2},
            "ARMOR_BREAK_BONUS": {"points": 2},
            "SURPRISE_ATTACK_BONUS": {"points": 3},
            "EVADE_BONUS": {"points": 2},
            "COUNTER_MOVE_BONUS": {"points": 2},
            "FLOOR_ADVANTAGE_BONUS": {"points": 1},
            "AMBIENT_EFFECT_BONUS": {"points": 1},
            "POSITIONING_ADVANTAGE_BONUS": {"points": 3},
            "MORALE_BOOST_BONUS": {"points": 2},
            "TACTICAL_RETREAT_BONUS": {"points": 2},
            "RESOURCE_MANAGEMENT_BONUS": {"points": 3},
            "TIME_CRITICAL_BONUS": {"points": 2},
            "STRATEGIC_OVERTAKE_BONUS": {"points": 4},
            "ULTIMATE_MOVE_BONUS": {"points": 5},
            "ADAPTIVE_STRATEGY_BONUS": {"points": 3}
        }

    def get_rules(self) -> dict:
        return self.rules

###############################################################################
#                       SCORING ENGINE CLASS
###############################################################################

class ScoringEngine:
    def __init__(self, strategy_library: StrategyLibrary):
        self.strategy_library = strategy_library
        self.rules = strategy_library.get_rules()

    def score_battle(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> Dict[str, int]:
        score_a = 0
        score_b = 0
        # List of strategy functions to apply:
        strategies = [
            self._apply_position_bonus,
            self._apply_fast_attack_bonus,
            self._apply_critical_hit_bonus,
            self._apply_ability_usage_bonus,
            self._apply_item_usage_bonus,
            self._apply_first_strike_bonus,
            self._apply_last_stand_bonus,
            self._apply_healing_efficiency_bonus,
            self._apply_defense_survival_bonus,
            self._apply_teamwork_bonus,
            self._apply_multi_hit_bonus,
            self._apply_dodge_bonus,
            self._apply_counter_attack_bonus,
            self._apply_flexible_position_bonus,
            self._apply_critical_defense_bonus,
            self._apply_speed_advantage_bonus,
            self._apply_lucky_hit_bonus,
            self._apply_power_surge_bonus,
            self._apply_elemental_advantage_bonus,
            self._apply_skill_combo_bonus,
            self._apply_penetration_bonus,
            self._apply_armor_break_bonus,
            self._apply_surprise_attack_bonus,
            self._apply_evade_bonus,
            self._apply_counter_move_bonus,
            self._apply_floor_advantage_bonus,
            self._apply_ambient_effect_bonus,
            self._apply_positioning_advantage_bonus,
            self._apply_morale_boost_bonus,
            self._apply_tactical_retreat_bonus,
            self._apply_resource_management_bonus,
            self._apply_time_critical_bonus,
            self._apply_strategic_overtake_bonus,
            self._apply_ultimate_move_bonus,
            self._apply_adaptive_strategy_bonus
        ]
        for func in strategies:
            a, b = func(log, team_info)
            score_a += a
            score_b += b
        return {"Team_A": score_a, "Team_B": score_b}

    # Each strategy function examines the battle log and/or team info.
    def _apply_position_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("POSITION_BONUS")
        bonus_a = rule["points"] if team_info["Team_A"]["formation"] == sorted(team_info["Team_A"]["formation"]) else 0
        bonus_b = rule["points"] if team_info["Team_B"]["formation"] == sorted(team_info["Team_B"]["formation"]) else 0
        return bonus_a, bonus_b

    def _apply_fast_attack_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("FAST_ATTACK_BONUS")
        bonus_a = 0
        bonus_b = 0
        if log and "actions" in log[0]:
            first_action = log[0]["actions"][0]
            actor = first_action["actor"]
            # Assume Team_A if actor starts with A, else Team_B (for demonstration)
            if actor in ["A", "B", "C", "D"]:
                bonus_a += rule["points"]
            else:
                bonus_b += rule["points"]
        return bonus_a, bonus_b

    def _apply_critical_hit_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("CRITICAL_HIT_BONUS")
        bonus_a = sum(rule["points"] for turn in log for ev in turn.get("events", []) if "Critical hit" in ev and "Team_A" in ev)
        bonus_b = sum(rule["points"] for turn in log for ev in turn.get("events", []) if "Critical hit" in ev and "Team_B" in ev)
        return bonus_a, bonus_b

    def _apply_ability_usage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ABILITY_USAGE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "use ability" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "use ability" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_item_usage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ITEM_USAGE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "use item" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "use item" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_first_strike_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("FIRST_STRIKE_BONUS")
        bonus_a = bonus_b = 0
        if log and log[0].get("actions", []):
            actor = log[0]["actions"][0]["actor"]
            if actor in ["A", "B", "C", "D"]:
                bonus_a += rule["points"]
            else:
                bonus_b += rule["points"]
        return bonus_a, bonus_b

    def _apply_last_stand_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("LAST_STAND_BONUS")
        # If a team has exactly one champion remaining (simulated here via formation length of 1)
        bonus_a = rule["points"] if len(team_info["Team_A"]["formation"]) == 1 else 0
        bonus_b = rule["points"] if len(team_info["Team_B"]["formation"]) == 1 else 0
        return bonus_a, bonus_b

    def _apply_healing_efficiency_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("HEALING_EFFICIENCY_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Heal" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Heal" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_defense_survival_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("DEFENSE_SURVIVAL_BONUS")
        bonus_a = rule["points"]  # Dummy value for demonstration
        bonus_b = rule["points"]
        return bonus_a, bonus_b

    def _apply_teamwork_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("TEAMWORK_BONUS")
        bonus_a = rule["points"]
        bonus_b = rule["points"]
        return bonus_a, bonus_b

    def _apply_multi_hit_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("MULTI_HIT_BONUS")
        bonus_a = bonus_b = 0
        for turn in log:
            counts = {}
            for action in turn.get("actions", []):
                actor = action["actor"]
                counts[actor] = counts.get(actor, 0) + 1
            for actor, count in counts.items():
                if count > 1:
                    if actor in ["A", "B", "C", "D"]:
                        bonus_a += rule["points"]
                    else:
                        bonus_b += rule["points"]
        return bonus_a, bonus_b

    def _apply_dodge_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("DODGE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "missed" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "missed" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_counter_attack_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        # For simplicity, no counter attack bonus implemented.
        return 0, 0

    def _apply_flexible_position_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("FLEXIBLE_POSITION_BONUS")
        bonus_a = rule["points"] if team_info["Team_A"]["formation"] != sorted(team_info["Team_A"]["formation"]) else 0
        bonus_b = rule["points"] if team_info["Team_B"]["formation"] != sorted(team_info["Team_B"]["formation"]) else 0
        return bonus_a, bonus_b

    def _apply_critical_defense_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("CRITICAL_DEFENSE_BONUS")
        bonus_a = bonus_b = 0
        for turn in log:
            for ev in turn.get("events", []):
                if "Critical hit" in ev and "Team_A" in ev:
                    bonus_a += rule["points"]
                elif "Critical hit" in ev and "Team_B" in ev:
                    bonus_b += rule["points"]
        return bonus_a, bonus_b

    def _apply_speed_advantage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("SPEED_ADVANTAGE_BONUS")
        # Dummy: assign bonus based on formation sum (lower sum means higher speed)
        bonus_a = rule["points"] if sum(team_info["Team_A"]["formation"]) < sum(team_info["Team_B"]["formation"]) else 0
        bonus_b = rule["points"] if sum(team_info["Team_B"]["formation"]) < sum(team_info["Team_A"]["formation"]) else 0
        return bonus_a, bonus_b

    def _apply_lucky_hit_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("LUCKY_HIT_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] == 1 and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] == 1 and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_power_surge_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("POWER_SURGE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 15 and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 15 and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_elemental_advantage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ELEMENTAL_ADVANTAGE_BONUS")
        # Dummy: check if "Fireball" is used
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Fireball" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Fireball" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_skill_combo_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("SKILL_COMBO_BONUS")
        bonus_a = bonus_b = 0
        last_turn = {}
        for turn in log:
            for action in turn.get("actions", []):
                actor = action["actor"]
                if actor in last_turn and turn["turn_number"] - last_turn[actor] == 1:
                    if actor in ["A", "B", "C", "D"]:
                        bonus_a += rule["points"]
                    else:
                        bonus_b += rule["points"]
                last_turn[actor] = turn["turn_number"]
        return bonus_a, bonus_b

    def _apply_penetration_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("PENETRATION_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 10 and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 10 and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_armor_break_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ARMOR_BREAK_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 20 and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "attack" in action["action"] and action["damage"] >= 20 and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_surprise_attack_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("SURPRISE_ATTACK_BONUS")
        bonus_a = bonus_b = 0
        last_actor = None
        for turn in log:
            if turn.get("actions", []):
                first_actor = turn["actions"][0]["actor"]
                if last_actor and first_actor != last_actor:
                    if first_actor in ["A", "B", "C", "D"]:
                        bonus_a += rule["points"]
                    else:
                        bonus_b += rule["points"]
                last_actor = turn["actions"][-1]["actor"]
        return bonus_a, bonus_b

    def _apply_evade_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("EVADE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "missed" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "missed" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_counter_move_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        return 0, 0

    def _apply_floor_advantage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("FLOOR_ADVANTAGE_BONUS")
        sum_a = sum(team_info["Team_A"]["formation"])
        sum_b = sum(team_info["Team_B"]["formation"])
        bonus_a = rule["points"] if sum_a < sum_b else 0
        bonus_b = rule["points"] if sum_b < sum_a else 0
        return bonus_a, bonus_b

    def _apply_ambient_effect_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("AMBIENT_EFFECT_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if action["action"] == "idle" and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if action["action"] == "idle" and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_positioning_advantage_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("POSITIONING_ADVANTAGE_BONUS")
        bonus_a = rule["points"] if team_info["Team_A"]["formation"] == sorted(team_info["Team_A"]["formation"]) else 0
        bonus_b = rule["points"] if team_info["Team_B"]["formation"] == sorted(team_info["Team_B"]["formation"]) else 0
        return bonus_a, bonus_b

    def _apply_morale_boost_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("MORALE_BOOST_BONUS")
        # Dummy: difference in formation sum as a proxy for morale
        diff = abs(sum(team_info["Team_A"]["formation"]) - sum(team_info["Team_B"]["formation"]))
        bonus_a = rule["points"] * diff
        bonus_b = rule["points"] * diff
        return bonus_a, bonus_b

    def _apply_tactical_retreat_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("TACTICAL_RETREAT_BONUS")
        bonus_a = rule["points"] if len(team_info["Team_A"]["formation"]) == len(team_info["Team_A"]["formation"]) else 0
        bonus_b = rule["points"] if len(team_info["Team_B"]["formation"]) == len(team_info["Team_B"]["formation"]) else 0
        return bonus_a, bonus_b

    def _apply_resource_management_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("RESOURCE_MANAGEMENT_BONUS")
        # Dummy: always award bonus if formation exists
        bonus_a = rule["points"]
        bonus_b = rule["points"]
        return bonus_a, bonus_b

    def _apply_time_critical_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("TIME_CRITICAL_BONUS")
        if log and log[-1].get("final_turn", 100) < 10:
            return rule["points"], rule["points"]
        return 0, 0

    def _apply_strategic_overtake_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("STRATEGIC_OVERTAKE_BONUS")
        bonus_a = bonus_b = 0
        if log and "battle_result" in log[-1]:
            result = log[-1]["battle_result"]
            if "Team_A" in result:
                bonus_a += rule["points"]
            elif "Team_B" in result:
                bonus_b += rule["points"]
        return bonus_a, bonus_b

    def _apply_ultimate_move_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ULTIMATE_MOVE_BONUS")
        bonus_a = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Ultimate" in action["action"] and action["actor"] in ["A", "B", "C", "D"])
        bonus_b = sum(rule["points"] for turn in log for action in turn.get("actions", []) if "Ultimate" in action["action"] and action["actor"] not in ["A", "B", "C", "D"])
        return bonus_a, bonus_b

    def _apply_adaptive_strategy_bonus(self, log: List[Dict[str, Any]], team_info: Dict[str, Any]) -> (int, int):
        rule = self.rules.get("ADAPTIVE_STRATEGY_BONUS")
        bonus_a = rule["points"] if team_info["Team_A"]["formation"] != sorted(team_info["Team_A"]["formation"]) else 0
        bonus_b = rule["points"] if team_info["Team_B"]["formation"] != sorted(team_info["Team_B"]["formation"]) else 0
        return bonus_a, bonus_b

###############################################################################
#                           MAIN SCORING FUNCTION
###############################################################################

def main():
    # Load battle log and team configuration produced by game.py
    with open("battle_log.json", "r") as f:
        battle_log = json.load(f)
    with open("teams.json", "r") as f:
        teams_info = json.load(f)

    # Initialize strategy library and scoring engine
    strategy_lib = StrategyLibrary()
    scoring_engine = ScoringEngine(strategy_lib)
    scores = scoring_engine.score_battle(battle_log, teams_info)

    print("===== FINAL STRATEGY SCORES =====")
    print(f"Team Alpha (Team_A): {scores.get('Team_A', 0)}")
    print(f"Team Beta (Team_B): {scores.get('Team_B', 0)}")

if __name__ == "__main__":
    main()