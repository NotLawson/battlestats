import random

def place(self, placement, board, layout):
        p = layout
        px = placement[0]
        py = placement[1]

        y = 0
        for row in layout:
            x = 0
            for tile in row:
                if tile == 1:
                    board[py+y][px+x] = self.index
                    p[y][x] = [px+x, py+y]
                x += 1
            y += 1
        return p, board, layout

class ShipSingle:
    id = "shipsingle"
    name = "Ship Single"
    health = 4
    last_use = 0

    rotations = [
            [
                [1,1,1,1],
            ],
            [
                [1],
                [1],
                [1],
                [1]
            ]
    ]
    ability_rotations = [
        # 0 = nothing, 1 = hit, 2 = reveal
        [
            [1,1,1]
        ],
        [
            [1],
            [1],
            [1]
        ]
    ]
    abiltity_info = {
            "type": "single", # single, combo, passive
            "cooldown": 3,
            "description": "Ability Description",
    }

    def __init__(self, owner, layout, rotation, fleetIndex, board, events):
        self.index = fleetIndex
        self.sunk = False
        self.event_queue = events
        self.owner = owner

        self.placement = layout
        self.layout = self.rotations[rotation]


    def hit(self, coords):
        y = 0
        for row in self.placement:
            x = 0
            for tile in row:
                if tile == coords:
                    self.layout[y][x] = 2
                    break
    
    def post_ability(self, last):
        pass

    def abiltity(self, coords, rotation):
        # this function will be called when the ship ability is used
        hits = self.ability_rotations[rotation]

        y = 0
        for row in hits:
            x = 0
            for tile in row:
                if tile == 1:
                    self.event_queue.put({
                        "type": "hit",
                        "coords": (coords[0]+x, coords[1]+y),
                        "board": "oppo",
                        "from": self.owner
                    })

                if tile == 2:
                    self.event_queue.put({
                        "type": "reveal",
                        "coords": (coords[0]+x, coords[1]+y),
                        "board": "oppo",
                        "from": self.owner
                    })

class ShipCombo:
    id = "shipcombo"
    name = "Ship Combo"
    health = 4
    last_use = 0
    rotations = [
            [
                [1,1,1,1],
            ],
            [
                [1],
                [1],
                [1],
                [1]
            ]
    ]
    abiltity_info = {
            "type": "combo", # single, combo, passive
            "cooldown": 3,
            "description": "Ability Description",
    }

    def __init__(self, owner, layout, rotation, fleetIndex, board, events):
        self.index = fleetIndex
        self.sunk = False
        self.event_queue = events
        self.owner = owner

        self.placement = layout
        self.layout = self.rotations[rotation]


    def hit(self, coords):
        y = 0
        for row in self.placement:
            x = 0
            for tile in row:
                if tile == coords:
                    self.layout[y][x] = 2
                    break

    # The runtime will call the ability functions in this order:
    #
    # ability()
    # process()
    # post_ability()

    def post_ability(self, last):
        iteration = last["iteration"]
        if last["hit"] == False:
            return True # ending combo
            
        if iteration >= 5:
            return True # ending combo
        
        return False
    def abiltity(self, coords):
        # this function will be called when the ship ability is used
        self.event_queue.put({
            "type": "hit",
            "coords": (coords[0], coords[1]),
            "board": "oppo",
            "from": self.owner
        })

        

# Ships
class BlunderBuster(ShipSingle):
    id = "blunderbuster"
    name = "Blunder Buster"
    health = 4

    rotations = [
        [
            [1,1],
            [1,1]
        ]
    ]

    abiltity_info = {
        "type": "single", # single, combo, passive
        "cooldown": 4,
        "description": "Randomly Attack 4 tiles in a 9 block square. When cooldown is less than zero, becomes 'Overcharged' and attacks 5 tiles",
    }
    ability_rotations = [
        [
            [1,1,1],
            [1,1,1]
            [1,1,1]
        ]
    ]

    def abiltity(self, coords, rotation):
        tiles = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        chosen = []
        layout = self.ability_rotations[rotation]
        i = 0
        if self.last_use > 4:
            for i in range(4):
                chosen.append(random.choice(tiles))
                i+=1
        else:
            for i in range(5):
                chosen.append(random.choice(tiles))
                i+=1

        for tile in chosen:
            layout[tile[1]][tile[0]] = 0


        for tile in chosen:
            self.event_queue.put({
                "type": "hit",
                "coords": tile,
                "board": "oppo",
                "from": self.owner
            })

        y = 0
        for row in layout:
            x = 0
            for tile in row:
                if tile == 1:
                    self.event_queue.put({
                        "type": "hit",
                        "coords": (coords[0]+x, coords[1]+y),
                        "board": "oppo",
                        "from": self.owner
                    })
