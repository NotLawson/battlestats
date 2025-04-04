from __main__ import BTClient
from queue import Queue
from . import ships

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
    
class BattleFromServers:
    def __init__(self, id):
        self.id = id
        self.data = BTClient.query('{battle(id: "'+self.id+'") {id events players {id name} finishedAt winner {id name}}}')

        server_events = self.data["battle"]["events"]
        self.events = []
        self.players = {}

        i = 0
        event_kinds = ['battle-created', 'player-joined', 'maps-set', 'fleet-chosen-v2', 'ships-placed', 'battle-started', 'player-took-turn', 'player-responded-to-turn', 'battle-finished', 'battle-rewards-collected']
        # process events
        for i in range(len(self.events)):
            event = server_events[i]

            if event["kind"] == "battle-created":
                if event["battleKind"] == "friendly":
                    self.friendly = False
                else:
                    self.friendly = True
                
                self.created_at = event["createdAt"]

            elif event["kind"] == "player-joined":
                playerid = event["userId"]
                player = BTClient.query('{user(idOrShortId: "'+playerid+'") {name}}')
                self.players[playerid] = {
                    "id": event["player"]["id"],
                    "player": player["user"]["name"],
                    "fleet_name":"",
                    "fleet":[],
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
                }
                pass

            elif event["kind"] == "maps-set":
                # set maps
                pass

            elif event["kind"] == "fleet-chosen-v2":
                # chooses the fleet
                id = event["byUserId"]
                fleet = event["fleet"]
                if fleet["kind"] == "starting_fleet":
                    self.players[id]["fleet_name"] = fleet["definitionId"]
                else:
                    self.players[id]["fleet_name"] = fleet["name"]

            elif event["kind"] == "ships-placed":
                # places ships
                id = event["byUserId"]

                for id, placement in event["placements"]:
                    pass # finish ship classes first
                pass

            elif event["kind"] == "battle-started":
                pass # skip this

            elif event["kind"] == "player-took-turn":
                # player turn
                id = event["fromUserId"]

                players = list(self.players.keys())
                players.remove(id)
                opponent = players[0]


                pass
            elif event["kind"] == "player-responded-to-turn":
                pass # skip event as it is read by previous event
            
            elif event["kind"] == "battle-finished":
                pass
            elif event["kind"] == "battle-rewards-collected":
                pass
            else:
                self.events.append({
                    "kind": "unknown"
                })

