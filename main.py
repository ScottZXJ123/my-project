#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Simulation Code
--------------------
This file pre-configures two team lineups and then runs an automated, turn‑based
battle simulation. The game engine logs each action and event into a confrontation
log. Once the battle is complete, the engine writes the battle log and basic team
information into JSON files. The engine has no knowledge of any hidden strategy
library (which is only used later during scoring).

The file includes extended dummy code sections to simulate a codebase of ~1000 lines.
"""

import random
import uuid
import math
import json
from typing import List, Dict, Any, Optional

###############################################################################
#                           STATUS EFFECTS CLASS
###############################################################################

class StatusEffect:
    def __init__(self, name: str, duration: int, effect_value: int, effect_type: str):
        self.name = name
        self.duration = duration
        self.effect_value = effect_value
        self.effect_type = effect_type

    def apply_effect(self, character: 'Character') -> None:
        if self.effect_type == "poison":
            character.take_damage(self.effect_value)
        elif self.effect_type == "heal":
            character.heal(self.effect_value)
        elif self.effect_type == "buff":
            character.attack += self.effect_value
        elif self.effect_type == "debuff":
            character.defense = max(0, character.defense - self.effect_value)

    def tick(self) -> None:
        self.duration -= 1

    def is_expired(self) -> bool:
        return self.duration <= 0

    def __repr__(self) -> str:
        return f"<StatusEffect {self.name}, Duration: {self.duration}, Value: {self.effect_value}>"

###############################################################################
#                           ABILITY CLASS
###############################################################################

class Ability:
    def __init__(self, name: str, power: int, cooldown: int, effect: Optional[StatusEffect] = None):
        self.name = name
        self.power = power
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.effect = effect

    def is_available(self) -> bool:
        return self.current_cooldown == 0

    def use(self) -> None:
        self.current_cooldown = self.cooldown

    def tick_cooldown(self) -> None:
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def __repr__(self) -> str:
        return f"<Ability {self.name}, Power: {self.power}, Cooldown: {self.cooldown}>"

###############################################################################
#                             ITEM CLASS
###############################################################################

class Item:
    def __init__(self, name: str, effect: str, effect_value: int, quantity: int = 1):
        self.name = name
        self.effect = effect
        self.effect_value = effect_value
        self.quantity = quantity

    def use_item(self, character: 'Character') -> None:
        if self.effect == "heal":
            character.heal(self.effect_value)
        elif self.effect == "damage":
            character.take_damage(self.effect_value)
        elif self.effect == "buff":
            character.attack += self.effect_value
        self.quantity -= 1

    def __repr__(self) -> str:
        return f"<Item {self.name}, Effect: {self.effect}, Value: {self.effect_value}, Qty: {self.quantity}>"

###############################################################################
#                          CHARACTER CLASS
###############################################################################

class Character:
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int,
                 team_id: str, position: int, abilities: Optional[List[Ability]] = None,
                 inventory: Optional[List[Item]] = None):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team_id = team_id
        self.position = position
        self.alive = True
        self.abilities = abilities if abilities is not None else []
        self.inventory = inventory if inventory is not None else []
        self.status_effects: List[StatusEffect] = []

    def is_alive(self) -> bool:
        return self.alive

    def take_damage(self, amount: int) -> None:
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0
            self.alive = False

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.current_hp + amount, self.max_hp)
        if self.current_hp > 0:
            self.alive = True

    def add_status_effect(self, effect: StatusEffect) -> None:
        self.status_effects.append(effect)

    def process_status_effects(self) -> List[str]:
        logs = []
        for effect in self.status_effects:
            effect.apply_effect(self)
            logs.append(f"{self.name} is affected by {effect.name} ({effect.effect_value})")
            effect.tick()
        self.status_effects = [e for e in self.status_effects if not e.is_expired()]
        return logs

    def tick_abilities(self) -> None:
        for ability in self.abilities:
            ability.tick_cooldown()

    def __repr__(self) -> str:
        return f"<Character {self.name}, HP: {self.current_hp}/{self.max_hp}, Team: {self.team_id}, Pos: {self.position}>"

###############################################################################
#                           TEAM CLASS
###############################################################################

class Team:
    def __init__(self, team_id: str):
        self.team_id = team_id
        self.characters: List[Character] = []
        self.formation: List[int] = []

    def add_character(self, character: Character) -> None:
        self.characters.append(character)
        self.formation.append(character.position)

    def get_alive_characters(self) -> List[Character]:
        return [c for c in self.characters if c.is_alive()]

    def is_defeated(self) -> bool:
        return all(not c.is_alive() for c in self.characters)

    def rearrange_formation(self, new_order: List[int]) -> None:
        if len(new_order) != len(self.characters):
            return
        for character, new_pos in zip(self.characters, new_order):
            character.position = new_pos
        self.formation = new_order

    def __repr__(self) -> str:
        return f"<Team {self.team_id}, Formation: {self.formation}>"

###############################################################################
#                         EVENT SYSTEM CLASSES
###############################################################################

class Event:
    def __init__(self, description: str):
        self.event_id = uuid.uuid4().hex
        self.description = description

    def process(self, game_engine: 'GameEngine') -> None:
        pass

    def __repr__(self) -> str:
        return f"<Event {self.event_id}: {self.description}>"

class CriticalHitEvent(Event):
    def __init__(self, attacker: Character, target: Character, extra_damage: int):
        super().__init__(f"Critical hit by {attacker.name} on {target.name} for extra {extra_damage}")
        self.attacker = attacker
        self.target = target
        self.extra_damage = extra_damage

    def process(self, game_engine: 'GameEngine') -> None:
        self.target.take_damage(self.extra_damage)

class MissEvent(Event):
    def __init__(self, attacker: Character, target: Character):
        super().__init__(f"{attacker.name}'s attack missed {target.name}")
        self.attacker = attacker
        self.target = target

    def process(self, game_engine: 'GameEngine') -> None:
        pass

class AbilityUsedEvent(Event):
    def __init__(self, user: Character, ability: Ability, target: Optional[Character]):
        super().__init__(f"{user.name} used ability {ability.name} on {target.name if target else 'None'}")
        self.user = user
        self.ability = ability
        self.target = target

    def process(self, game_engine: 'GameEngine') -> None:
        if self.ability.effect and self.target:
            self.target.add_status_effect(self.ability.effect)

###############################################################################
#                        GAME ENGINE CLASS
###############################################################################

class GameEngine:
    def __init__(self, team_a: Team, team_b: Team, random_seed: Optional[int] = None):
        self.team_a = team_a
        self.team_b = team_b
        self.turn_log: List[Dict[str, Any]] = []
        self.event_log: List[Event] = []
        self.battle_over = False
        self.turn_count = 0
        if random_seed is not None:
            random.seed(random_seed)

    def run_battle(self) -> None:
        max_turns = 100
        while not self.battle_over and self.turn_count < max_turns:
            self.turn_count += 1
            turn_details = {"turn_number": self.turn_count, "actions": []}
            status_logs = self._process_status_effects()
            if status_logs:
                turn_details["status_effects"] = status_logs
            all_fighters = self._get_all_alive_characters()
            if not all_fighters:
                self.battle_over = True
                break
            all_fighters.sort(key=lambda c: (-c.speed, c.position))
            for fighter in all_fighters:
                if not fighter.is_alive():
                    continue
                fighter.tick_abilities()
                action_detail = self._perform_action(fighter)
                turn_details["actions"].append(action_detail)
                if self.team_a.is_defeated() or self.team_b.is_defeated():
                    self.battle_over = True
                    break
            self.turn_log.append(turn_details)
            self._process_events()
        self._log_battle_result()

    def _get_all_alive_characters(self) -> List[Character]:
        return self.team_a.get_alive_characters() + self.team_b.get_alive_characters()

    def _process_status_effects(self) -> List[str]:
        logs = []
        for character in self._get_all_alive_characters():
            logs.extend(character.process_status_effects())
        return logs

    def _perform_action(self, fighter: Character) -> Dict[str, Any]:
        action_detail = {"actor": fighter.name, "action": None, "target": None, "damage": 0, "extra": []}
        available_abilities = [ab for ab in fighter.abilities if ab.is_available()]
        if available_abilities and random.random() < 0.3:
            ability = random.choice(available_abilities)
            target = self._choose_target(fighter)
            if target:
                ability.use()
                self.event_log.append(AbilityUsedEvent(fighter, ability, target))
                damage = max(1, fighter.attack + ability.power - target.defense)
                target.take_damage(damage)
                action_detail["action"] = f"use ability {ability.name}"
                action_detail["target"] = target.name
                action_detail["damage"] = damage
                action_detail["extra"].append("ability event logged")
            else:
                action_detail["action"] = "idle"
        else:
            target = self._choose_target(fighter)
            if target:
                if random.random() < 0.1:
                    self.event_log.append(MissEvent(fighter, target))
                    action_detail["action"] = "attack (missed)"
                    action_detail["target"] = target.name
                    action_detail["damage"] = 0
                else:
                    extra_damage = 0
                    if random.random() < 0.2:
                        extra_damage = int(fighter.attack * 0.5)
                        self.event_log.append(CriticalHitEvent(fighter, target, extra_damage))
                    base_damage = max(1, fighter.attack - target.defense)
                    total_damage = base_damage + extra_damage
                    target.take_damage(total_damage)
                    action_detail["action"] = "attack"
                    action_detail["target"] = target.name
                    action_detail["damage"] = total_damage
            else:
                action_detail["action"] = "idle"
        return action_detail

    def _choose_target(self, fighter: Character) -> Optional[Character]:
        target_team = self.team_b if fighter.team_id == self.team_a.team_id else self.team_a
        living_enemies = target_team.get_alive_characters()
        return random.choice(living_enemies) if living_enemies else None

    def _process_events(self) -> None:
        while self.event_log:
            event = self.event_log.pop(0)
            event.process(self)
            self.turn_log[-1].setdefault("events", []).append(str(event))

    def _log_battle_result(self) -> None:
        if self.team_a.is_defeated() and self.team_b.is_defeated():
            result = "Draw: Both teams defeated."
        elif self.team_a.is_defeated():
            result = f"Team {self.team_b.team_id} wins!"
        elif self.team_b.is_defeated():
            result = f"Team {self.team_a.team_id} wins!"
        else:
            result = "Turn limit reached. Possibly a draw."
        self.turn_log.append({"battle_result": result, "final_turn": self.turn_count})

    def get_confrontation_log(self) -> List[Dict[str, Any]]:
        return self.turn_log

###############################################################################
#                        BATTLE REPLAY SYSTEM
###############################################################################

class BattleReplay:
    def __init__(self, log: List[Dict[str, Any]]):
        self.log = log

    def display_replay(self) -> None:
        for entry in self.log:
            if "turn_number" in entry:
                print(f"--- Turn {entry['turn_number']} ---")
                if "status_effects" in entry:
                    for effect in entry["status_effects"]:
                        print(effect)
                for action in entry.get("actions", []):
                    print(f"{action['actor']} performed {action['action']} on {action.get('target', 'N/A')} causing {action['damage']} damage")
                if "events" in entry:
                    for ev in entry["events"]:
                        print(f"Event: {ev}")
            elif "battle_result" in entry:
                print(f"Battle Result: {entry['battle_result']} after {entry.get('final_turn', 'unknown')} turns")
            print("\n")

###############################################################################
#                           MAIN GAME EXAMPLE
###############################################################################

def main_example() -> None:
    # Create teams and set up lineups
    # Create teams
    team_a = Team("Team_A")
    team_b = Team("Team_B")

# Define common status effects and items
    poison = StatusEffect("Poison", duration=3, effect_value=2, effect_type="poison")
    heal_effect = StatusEffect("Heal", duration=1, effect_value=4, effect_type="heal")
    potion = Item("Health Potion", effect="heal", effect_value=10, quantity=2)
    elixir = Item("Elixir", effect="buff", effect_value=2, quantity=1)

# Define a pool of 12 abilities (you can adjust parameters as needed)
    ability_fireball      = Ability("Fireball", power=5, cooldown=3, effect=poison)
    ability_heal          = Ability("Heal", power=-3, cooldown=2, effect=heal_effect)
    ability_quick_strike  = Ability("Quick Strike", power=3, cooldown=1)
    ability_shield_bash   = Ability("Shield Bash", power=4, cooldown=2)
    ability_lightning     = Ability("Lightning", power=6, cooldown=3)
    ability_frost         = Ability("Frost", power=4, cooldown=2, effect=StatusEffect("Freeze", duration=1, effect_value=0, effect_type="debuff"))
    ability_windslash     = Ability("Wind Slash", power=5, cooldown=2)
    ability_earthquake    = Ability("Earthquake", power=7, cooldown=4)
    ability_magic_missile = Ability("Magic Missile", power=4, cooldown=1)
    ability_poison_dart   = Ability("Poison Dart", power=3, cooldown=2, effect=poison)
    ability_rejuvenate    = Ability("Rejuvenate", power=-4, cooldown=3, effect=heal_effect)
    ability_berserk       = Ability("Berserk", power=8, cooldown=5)

# Create a list containing all 12 abilities
    abilities_pool = [
        ability_fireball, ability_heal, ability_quick_strike, ability_shield_bash,
        ability_lightning, ability_frost, ability_windslash, ability_earthquake,
        ability_magic_missile, ability_poison_dart, ability_rejuvenate, ability_berserk
    ]

# For demonstration, each champion will be given the full pool of 12 abilities.
# In a real game you might allow players to choose a subset from this pool.
# Add characters to Team A
    char_a = Character("A", hp=40, attack=12, defense=4, speed=14, team_id="Team_A", position=0, 
                      abilities=[ability_quick_strike, ability_lightning, ability_magic_missile, ability_frost], 
                      inventory=[potion])
    char_b = Character("B", hp=35, attack=10, defense=5, speed=12, team_id="Team_A", position=1, 
                      abilities=[ability_shield_bash, ability_heal, ability_earthquake, ability_poison_dart], 
                      inventory=[elixir])
    char_c = Character("C", hp=30, attack=30, defense=30, speed=20, team_id="Team_A", position=2, 
                      abilities=[ability_berserk, ability_earthquake, ability_fireball, ability_quick_strike])
    char_d = Character("D", hp=50, attack=11, defense=20, speed=13, team_id="Team_A", position=3, 
                      abilities=[ability_rejuvenate, ability_magic_missile, ability_frost, ability_shield_bash])
    team_a.add_character(char_a)
    team_a.add_character(char_b)
    team_a.add_character(char_c)
    team_a.add_character(char_d)

# Add characters to Team B
    char_x = Character("X", hp=42, attack=13, defense=30, speed=11, team_id="Team_B", position=0, 
                      abilities=[ability_fireball, ability_shield_bash, ability_rejuvenate, ability_magic_missile])
    char_y = Character("Y", hp=38, attack=40, defense=5, speed=15, team_id="Team_B", position=1, 
                      abilities=[ability_berserk, ability_lightning, ability_earthquake, ability_quick_strike])
    char_z = Character("Z", hp=33, attack=10, defense=6, speed=18, team_id="Team_B", position=2, 
                      abilities=[ability_quick_strike, ability_poison_dart, ability_frost, ability_rejuvenate])
    char_w = Character("W", hp=36, attack=11, defense=20, speed=20, team_id="Team_B", position=3, 
                      abilities=[ability_shield_bash, ability_heal, ability_rejuvenate, ability_magic_missile])
    team_b.add_character(char_x)
    team_b.add_character(char_y) 
    team_b.add_character(char_z)
    team_b.add_character(char_w)   

# Optionally rearrange formations
    team_a.rearrange_formation([0, 1, 2, 3])
    team_b.rearrange_formation([0, 1, 2, 3])

    # Run the battle simulation
    engine = GameEngine(team_a, team_b, random_seed=12345)
    engine.run_battle()
    confrontation_log = engine.get_confrontation_log()

    # Replay battle on console
    print("===== BATTLE REPLAY =====")
    replay = BattleReplay(confrontation_log)
    replay.display_replay()

    # Save battle log and team info to JSON files for scoring
    with open("battle_log.json", "w") as f:
        json.dump(confrontation_log, f, indent=4)
    
    # Save simple team info (only team IDs and formations)
    teams_info = {
        "Team_A": {"formation": team_a.formation},
        "Team_B": {"formation": team_b.formation}
    }
    with open("teams.json", "w") as f:
        json.dump(teams_info, f, indent=4)
    
    print("Battle simulation complete. Logs saved to 'battle_log.json' and 'teams.json'.")

###############################################################################
#                                ENTRY POINT
###############################################################################

if __name__ == "__main__":
    main_example()