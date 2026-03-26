import random
class IntrigueCard:
    def __init__(self, title, type, cost, effect):
        self.title = title
        self.type = type
        self.cost = cost
        self.effect = effect
class Card:
    def __init__(self, title, persuasionCost, factionAffil, locationAccess, purchaseEffect, onPlay, onReveal): #holy terible
        self.title = title
        self.persuasionCost = persuasionCost
        self.factionAfill = factionAffil
        self.locationAccess = locationAccess
        self.purchaseEffect = purchaseEffect
        self.onPlay = onPlay
        self.onReveal = onReveal

numIntrigues = 40
allStartingCards = [ #Title, cost, faction affiliation, access, purchase effect, onPlay, on reveal
        Card("Signet Ring", 0, None, {"G", "B", "Y"}, None, {"Signet"}, {"1Pers"}),
        Card("Convincing Argument", 0, None, {}, None, {}, {"2Pers"}),
        Card("Dagger", 0, None, {"G"}, None, {}, {"1Sword"}),
        Card("Diplomacy", 0, None, {"FR", "BG", "SG", "EM"}, None, {}, {"1Pers"}),
        Card("Dune, The Desert Planet", 0, None, {"Y"}, None, {}, {"1Pers"}),
        Card("Reconnaisance", 0, None, {"B"}, None, {}, {"1Pers"}),
    ]


def init_imperium_deck():
    allImperiumCards = [
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"})
    ]
    random.shuffle(allImperiumCards)
    return allImperiumCards

    

def init_intrigues():
    allIntrigues = [
        IntrigueCard("Water Peddler's Union", "P", None, "1Water"),
        IntrigueCard("Windfall", "P", None, "2Sol"),
        IntrigueCard("Water of Life", "P", ["1Water", "1Spice"], "3Draw"),
        IntrigueCard("Ambush", "C", None, "4Swords")
    ]
    
    return random.shuffle(allIntrigues)
   