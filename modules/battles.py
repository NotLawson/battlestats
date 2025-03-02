from __main__ import BTClient


class Battle:
    def __init__(self, id):
        self.id = id
        self.data = BTClient.query('{battle(id: "'+self.id+'") {id events players {id name} finishedAt winner {id name}}}')
        self.players = self.data["battle"]["players"]
        self.winner = self.data["battle"]["winner"]
        self.finishedAt = self.data["battle"]["finishedAt"]
        self.events = self.data["battle"]["events"]