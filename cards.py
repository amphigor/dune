import random
class IntrigueCard:
    def __init__(self, title, type, cost, effect):
        self.title = title
        self.type = type
        self.cost = cost
        self.effect = effect
class Card:
    def __init__(self, title, persuasionCost, factionAffil, locationAccess, purchaseEffect, onPlay, onReveal, onTrash = None, id = 0): #holy terible
        self.title = title
        self.persuasionCost = persuasionCost
        self.factionAffil = factionAffil
        self.locationAccess = locationAccess
        self.purchaseEffect = purchaseEffect
        self.onPlay = onPlay
        self.onReveal = onReveal
        self.onTrash = onTrash

        self.revealed = False

        self.id = id

    def __repr__(self):
        return self.title

numIntrigues = 40
allStartingCards = [ #Title, cost, faction affiliation, access, purchase effect, onPlay, on reveal
        Card("Signet Ring", 0, None, {"G", "B", "Y"}, None, {"1Signet"}, {"1Pers"}, id=0),
        Card("Convincing Argument", 0, None, {}, None, {}, {"2Pers"}, id = 1),
        Card("Dagger", 0, None, {"G"}, None, {}, {"1Sword"}, id = 2),
        Card("Diplomacy", 0, None, {"FR", "BG", "SG", "EM"}, None, {}, {"1Pers"}, id = 3),
        Card("Dune, The Desert Planet", 0, None, {"Y"}, None, {}, {"1Pers"}, id=4),
        Card("Reconnaissance", 0, None, {"B"}, None, {}, {"1Pers"}, id=5),
    ]


def init_imperium_deck():
    allImperiumCards = [
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}),
        Card("Nuclear Bomb", 7, None, {"B", "Y"}, None, {"1Trash"}, {"9Sword"}),
        Card("super Worm riders", 7, {"FR"}, {"Y", "FR"}, {"1InflF"}, {"4Spice"}, {"7Sword"}),
        Card("lisan al gaib!!!", 8, {"FR", "BG"}, {"G", "B", "Y", "FR", "BG"}, {"4InflF"}, {"9Troop"}, {"9Pers"})
    ]
    for i in range(63):
        allImperiumCards.append(Card("Arrakis Recruiter", 2, None, {"B"}, None, {"1Troop"}, {"1Pers", "1Sword"}))
    random.shuffle(allImperiumCards)
    return allImperiumCards

def init_reserve_AL():
    arrakis_Liaisons = []
    for i in range(8):
        arrakis_Liaisons.append(Card("Arrakis Liaison", 2, {"FR"}, {"G", "B"}, None, None, {"2Pers"}))
    return arrakis_Liaisons

def init_reserve_TSMF():
    spice_must_flows = []
    for i in range(8):
        spice_must_flows.append(Card("The Spice Must Flow", 9, None, None, {"1VP"}, None, {"1Spice"}))
    return spice_must_flows

def init_intrigues():
    allIntrigues = [
        IntrigueCard("Water Peddler's Union", "P", None, "1Water"),
        IntrigueCard("Windfall", "P", None, "2Sol"),
        IntrigueCard("Water of Life", "P", ["1Water", "1Spice"], "3Draw"),
        IntrigueCard("Ambush", "C", None, "4Swords")
    ]
    for i in range(49):
        allIntrigues.append(IntrigueCard("Windfall", "P", None, "2Sol"))
    random.shuffle(allIntrigues)
    return allIntrigues
   