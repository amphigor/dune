class BoardSpace: #simulates a board space
    def __init__(self, name, access, isCombat, cost, reward, isMaker, flagReward, specialReq = None):
        self.name = name
        self.access = access
        self.isCombat = isCombat
        self.cost = cost
        self.reward = reward
        self.isMaker = isMaker
        self.flag = None
        self.flagReward = flagReward
        self.isOccupied = False
        self.specialReq = specialReq
        if isMaker:
            self.currentMaker = 0
        
class Board: #simulates one board for a game
    def __init__(self):
        self.boardSpaces = set() #set or list
        self.yellowSpaces = set()
        self.occupiedSpaces = set()
        self.boardSpaceRefs = {
            "Arrakeen": BoardSpace("Arrakeen", "B", True, None, ["1Troop", "1Draw"], False, ["1Sol"]),
            "Carthag": BoardSpace("Carthag", "B", True, None, ["1Troop", "1Intrigue"], False, ["1Sol"]),
            "Research Station": BoardSpace("Research Station", "B", True, ["2Water"], ["3Draw"], False, None),
            "Sietch Tabr": BoardSpace("Sietch Tabr", "B", True, None, ["1Troop", "1Water"], False, None, ["2InflF"]),

            "Imperial Basin": BoardSpace("Imperial Basin", "Y", True, None, ["1Spice"], True, ["1Spice"]),
            "Hagga Basin": BoardSpace("Hagga Basin", "Y", True, ["1Water"], ["2Spice"], True, None),
            "The Great Flat": BoardSpace("The Great Flat", "Y", True, ["2Water"], ["3Spice"], True, None),

            "Secure Contract": BoardSpace("Secure Contract", "Y", False, None, ["3Sol"], False, None),
            "Sell Melange": BoardSpace("Sell Melange", "Y", False, ["1Choose", "2Spice", "3Spice", "4Spice", "5Spice"],
                                         ["6Sol", "8Sol", "10Sol", "12Sol"], False, None), #needs special implm.

            "High Council": BoardSpace("High Council", "G", False, ["5Sol"], ["1HighCouncil"], False, None),
            "Mentat": BoardSpace("Mentat", "G", False, ["2Sol"], ["1Mentat"], False, None),
            "Rally Troops": BoardSpace("Rally Troops", "G", False, ["4Sol"], ["4Troop"], False, None),
            "Swordmaster": BoardSpace("Swordmaster", "G", False, ["8Sol"], ["1Swordmaster"], False, None),
            "Hall of Oratory": BoardSpace("Hall of Oratory", "G", False, None, ["1Pers", "1Troop"], False, None),

            "Wealth": BoardSpace("Wealth", "EM", False, None, ["1InflE", "2Sol"], False, None),
            "Conspire": BoardSpace("Conspire", "EM", False, ["4Spice"], ["1InflE", "5Sol", "2Troop", "1Intrigue"],
                                         False, None),

            "Foldspace": BoardSpace("Foldspace", "SG", False, None, ["1InflS", "1Foldspace"], False, None),
            "Heighliner": BoardSpace("Heighliner", "SG", True, ["6Spice"], ["1InflS", "5Troop", "2Water"], False, None),

            "Secrets": BoardSpace("Secrets", "BG", False, None, ["1InflB", "1Intrigue", "1IntrigueSteal"], False, None),
            "Selective Breeding": BoardSpace("Selective Breeding", "BG", False, ["2Spice", "1Trash"], ["1InflB", "2Draw"], False, None),

            "Stillsuits": BoardSpace("Stillsuits", "FR", True, None, ["1InflF", "1Water"], False, None),
            "Hardy Warriors": BoardSpace("Hardy Warriors", "FR", True, ["1Water"], ["1InflF", "2Troop"], False, None)
        }

        for value in self.boardSpaceRefs.values():
            self.boardSpaces.add(value)
            if value.access == "Y":
                self.yellowSpaces.add(value)

    def availableSpaces(self):
        return self.boardSpaces.difference(self.occupiedSpaces)
    
