class Leader:
    def __init__(self, title, passive, signet):
        self.title = title
        self.passive = passive
        self.signet = signet

def init_leaders():
    leaderList = [
        Leader("Paul Atreides", "", ""),
        Leader("Ilban Richese", "", ""),
        Leader("Earl Memmon Thorvald", "", ""),
        Leader("The Beast", "", "") #start with easy implementations to simulate
    ]
    return leaderList