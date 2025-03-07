#from __main__ import BTClient
from queue import Queue
from . import ships

class BattleFromServers:
    def __init__(self, id):
        self.id = id
        self.data = BTClient.query('{battle(id: "'+self.id+'") {id events players {id name} finishedAt winner {id name}}}')
        self.players = self.data["battle"]["players"]
        self.winner = self.data["battle"]["winner"]
        self.finishedAt = self.data["battle"]["finishedAt"]
        self.events = self.data["battle"]["events"]

        i = len(self.events)



class Battle:
    def __init__(self, players):
        self.event_queue = Queue()
        self.players = [
            {
                "name":players[0],
                "fleet":["ship1", "ship2", "ship3", "ship4"],
                "revealed_board":[
                    # 0 = unrevealed, 1 = rock, 2 = empty, 3 = revealed, 4 = hit, 5 = sunk
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]
                ],
                "board":[
                    # E = empty, R = rock, <id> = ship
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                ]
            },
            {
                "name":players[1],
                "fleet":["ship1","ship2","ship3","ship4"],
                "revealed_board":[
                    # 0 = unrevealed, 1 = rock, 2 = empty, 3 = revealed, 4 = hit, 5 = sunk
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]
                ],
                "board":[
                    # E = empty, R = rock, <id> = ship
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                    ["E","E","E","E","E","E","E","E"],
                ]
            },
        ]
        self.events = []
        

    def move(self, player, x, y):

        if player == 0:
            # attacking player 2 (index 1)

            # 0 = unrevealed, 1 = rock, 2 = empty, 3 = revealed, 4 = hit, 5 = sunk
            if self.players[1]["revealed_board"][y][x] == 0:

                # if unrevealed
                hidden_tile = self.players[1]["board"][y][x]

                # E = empty, R = rock, <id> = ship
                if hidden_tile == "E":
                    self.players[1]["revealed_board"][y][x] = 2
                    outcome = "miss"
                elif hidden_tile == "R":
                    self.players[1]["revealed_board"][y][x] = 1
                    outcome = "miss"
                else:
                    self.players[1]["revealed_board"][y][x] = 4
                    ship = player[1]["fleet"][hidden_tile]



