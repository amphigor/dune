import random
from collections import deque
class Conflict:
    def __init__(self, title, escalation, rewards1, rewards2, rewards3):
        self.title = title
        self.escalation = escalation
        self.rewards1 = rewards1
        self.rewards2 = rewards2
        self.rewards3 = rewards3

def init_conflicts():
    conflict_Order = []
    #setup conflict 1, and choose 1/4
    conflict_Ones = [
        Conflict("Skirmish", 1, ["1Infl", "2Sol"], ["3Sol"], ["2Sol"]),
        Conflict("Skirmish", 1, ["1Infl", "1Spice"], ["2Spice"], ["1Spice"]),
        Conflict("Skirmish", 1, ["1VP"], ["1Water"], ["1Spice"]),
        Conflict("Skirmish", 1, ["1VP"], ["1Intrigue", "2Sol"],["2Sol"])
    ]
    chosen_One = conflict_Ones[random.randint(0,3)]
    conflict_Order.append(chosen_One)

    #setup conflict 2s, choose 5
    conflict_Twos = [
        Conflict("Sort Through The Chaos", 2, ["1Mentat", "1Intrigue", "2Sol"], ["1Intrigue", "2Sol"], ["2Sol"]),
        Conflict("Terrible Purpose", 2, ["1VP", "1Trash"], ["1Water", "1Spice"], ["1Spice"]),
        Conflict("Guild Bank Raid", 2, ["6Sol"], ["4Sol"], ["2Sol"]),
        Conflict("Machinations", 2, ["1Infl", "1SpecInfl"], ["1Water", "2Sol"], ["1Water"]),
        Conflict("Raid Stockpiles", 2, ["1Intrigue", "3Spice"], ["2Spice"], ["1Spice"]),
        Conflict("Secure Imperial Basin", 2, ["1VP", "1CF"], ["2Water"], ["1Water"]),
        Conflict("Siege of Arrakeen", 2, ["1VP", "1CF"], ["4Sol"], ["2Sol"]),
        Conflict("Siege of Carthag", 2, ["1VP", "1CF"], ["1Intrigue", "1Spice"], ["1Spice"]),
        Conflict("Desert Power", 2, ["1VP", "1Water"], ["1Water", "1Spice"], ["1Spice"]),
        Conflict("Cloak and Dagger", 2, ["1Infl", "2Intrigue"], ["1Intrigue", "1Spice"], ["1Choose", "1Intrigue", "1Spice"])
    ]
    for i in range(5):
        chosen_Two = conflict_Twos.pop(random.randint(0, len(conflict_Twos)-1))
        conflict_Order.append(chosen_Two)
    
    #setup conflict 3s, take all 4
    conflict_Threes = [
        Conflict("Grand Vision", 3, ["2Infl", "1Intrigue"], ["1Intrigue", "3Spice"], ["3Spice"]),
        Conflict("Battle For Imperial Basin", 3, ["2VP", "1CF"], ["5Spice"], ["3Spice"]),
        Conflict("Battle For Carthag", 3, ["2VP", "1CF"], ["1Intrigue", "3Spice"], ["3Spice"]),
        Conflict("Battle for Arrakeen", 3, ["2VP", "1CF"], ["2Choose", "1Intrigue", "2Spice", "3Sol"], ["1Intrigue", "2Sol"]),
    ]
    for i in range(4):
        chosen_Three = conflict_Threes.pop(random.randint(0, len(conflict_Threes)-1))
        conflict_Order.append(chosen_Three)

    listConflicts(conflict_Order)
    return conflict_Order

def listConflicts(conflict_order):
    #This should be hidden info beyond the first conflict anyway
    for conflict in conflict_order:
        print(conflict.title)
