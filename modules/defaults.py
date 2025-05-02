from db import Database
import time

def import_ships(database: Database):
    # This script adds the normal ships to the database. It should only run when creating the database, as so not to overwrite changes or new ships
    ships = [
        {
            "definitionid":"skullcove",
            "name":"Skull Cove",
            "type":"special",
            "cd":-1, # passive
            "ability":"The Skull Cove has a passive ability, attacking 4 random tiles on your opponent's board every time it takes non-fatal damage from your opponent, once per turn, However the ability is disabled if skull cove is the last ship alive.",
            "dpt":{
                "avgDPT": -100, # null
                "maxDPT": -100,
                "minDPT": -100,
                "avgRVT": -100,
                "maxRVT": -100, 
                "minRVT": -100,
                "avgSPT": -100,
                "maxSPT": -100,
                "minSPT": -100
            },
            "skins":["beachHoliday"],
            "health":5,
            "tags":[]
        },
        {
            "definitionid":"piratethief",
            "name":"Pirate Thief",
            "type":"special",
            "cd":1,
            "ability":"The pirate thief attacks one tile on the opponent's board with a cooldown of 1. If it hits a ship, the cooldown of the ship that gets hit increases by 1.",
            "dpt":{
                "avgDPT": -100, # null
                "maxDPT": -100,
                "minDPT": -100,
                "avgRVT": -100,
                "maxRVT": -100, 
                "minRVT": -100,
                "avgSPT": -100,
                "maxSPT": -100,
                "minSPT": -100
            },
            "skins":[],
            "health":3,
            "tags":[]
        },
        {
            "definitionid":"chaosSlug",
            "name":"Chaos Slug",
            "type":"revealer",
            "cd":1,
            "ability":"The Chaos Slug has the ability to reveal 3 random tiles on the opponent's grid and reveal 1 of your own tiles.",
            "dpt":{
                "avgDPT": 0,
                "maxDPT": 0,
                "minDPT": 0,
                "avgRVT": 3,
                "maxRVT": 3, 
                "minRVT": 3,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":4,
            "tags":[]
        },
        {
            "definitionid":"valkyrie",
            "name":"Valkyrie",
            "type":"attacker",
            "cd":5,
            "ability":"The Valkyrie, by default, attacks 2 tiles with a 5 turn cooldown, However the Valkyrie attacks one more tile for each sunken ship on your side of the board.",
            "dpt":{
                "avgDPT": 0.5,
                "maxDPT": 0.8,
                "minDPT": 0.2,
                "avgRVT": 0,
                "maxRVT": 0, 
                "minRVT": 0,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":4,
            "tags":[]
        },
        {
            "definitionid":"chaossub",
            "name":"Chaos Sub",
            "type":"sonar",
            "cd":1,
            "ability":"The Chaos Sub has the ability to Sonar 1 tile with a cooldown of 1. However, the maximum ability cooldown increases by 1 each use.",
            "dpt":{
                "avgDPT": -100,
                "maxDPT": -100,
                "minDPT": -100,
                "avgRVT": -100,
                "maxRVT": -100, 
                "minRVT": -100,
                "avgSPT": -100,
                "maxSPT": -100,
                "minSPT": -100
            },
            "skins":[],
            "health":5,
            "tags":[]
        },
        {
            "definitionid":"electriceel",
            "name":"Electric Eels",
            "type":"revealer",
            "cd":3,
            "ability":"The Electric Eels targets 1 tile. If the tile contains a ship, the ship will be fully revealed.",
            "dpt":{
                "avgDPT": 0,
                "maxDPT": 0,
                "minDPT": 0,
                "avgRVT": 1.5,
                "maxRVT": 2.67, 
                "minRVT": 0.33,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":4,
            "tags":[]
        },
        {
            "definitionid":"coracle",
            "name":"Coracle",
            "type":"attacker",
            "cd":6,
            "ability":"The Coracle can only attack revealed squares, and once it attacks, it will destroy the ships in 1 shot. Coracle also has the passive ability where one unoccupied (meaning no ships are on it) tile will be revealed on your own side when attacking without an ability.",
            "dpt":{
                "avgDPT": 0.58,
                "maxDPT": 1.17,
                "minDPT": 0,
                "avgRVT": 0,
                "maxRVT": 0, 
                "minRVT": 0,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":["jackoracle", "beachcoracle"],
            "health":1,
            "tags":[]
        },
        {
            "definitionid":"longboat",
            "name":"Longboat",
            "type":"attacker",
            "cd":6,
            "ability":"The Longboat can attack up to 5 times. If you miss a ship, or destroy a ship, the ability will stop early.",
            "dpt":{
                "avgDPT": 0.33,
                "maxDPT": 0.67,
                "minDPT": 0,
                "avgRVT": 0,
                "maxRVT": 0, 
                "minRVT": 0,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":4,
            "tags":[]
        },
        {
            "definitionid":"squid",
            "name":"Killer Squid",
            "type":"revealer",
            "cd":2,
            "ability":"The Killer Squid can only attack a revealed tile and reveals all 4 surrounding tiles",
            "dpt":{
                "avgDPT": 0,
                "maxDPT": 0,
                "minDPT": 0,
                "avgRVT": 1.5,
                "maxRVT": 2, 
                "minRVT": 0.5,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":3,
            "tags":[]
        },
        {
            "definitionid":"cartographer",
            "name":"Cartographer",
            "type":"revealer",
            "cd":5,
            "ability":"The Cartographer have the ability to choose a revealed tile and expand the revealed area by 1 tile.",
            "dpt":{
                "avgDPT": 0,
                "maxDPT": 0,
                "minDPT": 0,
                "avgRVT": 1.6,
                "maxRVT": 2.4, 
                "minRVT": 0.4,
                "avgSPT": 0,
                "maxSPT": 0,
                "minSPT": 0
            },
            "skins":[],
            "health":4,
            "tags":[]
        },
    ]

    for ship in ships:
        database.execute("INSERT INTO ships (definition_id, name, type, cd, ability, dpt, skins, health, tags, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ship["definitionid"], ship["name"], ship["type"], ship["cd"], ship["ability"], ship["dpt"], ship["skins"], ship["health"], ship["tags"]))