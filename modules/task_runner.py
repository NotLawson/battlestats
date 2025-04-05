## Task Runner for the Webserver
# This module is responsible for running tasks in the background.
# First, the task is passed to the Load Balancer, which runs in the main thread.
# The Load Balancer will then pass the task to the Task Runner, which will run the task in a separate thread.
# The Task Runner will then execute the task.
# The Load Balancer will also manange Task Runner scaling, and will create and destroy Task Runners as needed.

# A Task object will look something like this:
{
    "type": "<task_type>",
    "options": {
        "<option_name>": "<option_value>"
    }
}
# For example, lets say we wanted to run a task that updates a user's stats in the database.
# The task would look like this:
{
    "type": "update_stats_for_user",
    "options": {
        "user_id": "user_id"
    }
}
# This would pull all of the stats in the stats table for the user with the given user_id, and then update the stats for that user.

## Task Types:
# - update_stats_for_user: Update the stats for a user.
#   - user_id: The user id of the user to update the stats for.
#
# - update_fleets_for_user: Update the fleets for a user.
#   - user_id: The user id of the user to update the fleets for.
#
# - update_inventory_for_user: Update the inventory for a user.
#   - user_id: The user id of the user to update the inventory for.
#
# - process_battle: Process a battle.
#   - battle_id: The id of the battle to process.
#
# - recalculate_stats_for_fleet: Recalculate the stats for a fleet
#  - fleet_id: The id of the fleet to recalculate the stats for.




from threading import Thread
from db import Database
from battletabs import BattleTabsClient, UnAuthBattleTabsClient
from logging import Logger
import os, sys, json, time
from queue import Queue

## Load config
config = json.load(open("config.json"))

# Verify config
try:
    assert config["secret_key"] != ""
    assert config["port"] != ""
    assert config["port"].isdigit()
except:
    print("Invalid config.json file. Please check the file and try again.")
    exit(1)

## Arguments
DEBUG = False
if "--debug" in sys.argv:
    DEBUG = True 

logger = Logger("Main Thread")

if DEBUG:
    logger.setLevel("DEBUG")
    logger.debug("Debug mode enabled")
else:
    logger.setLevel("INFO")

# Exit Error
class Exit(Exception):
    pass

# Threads
class Runner:
    def __init__(self,id: int, queue: Queue, battletabs: BattleTabsClient, database: Database):
        self.queue = queue
        self.battletabs = battletabs
        self.database = database
        self.logger = Logger(f"Runner-{str(id)}")
        if DEBUG:
            self.logger.setLevel("DEBUG")
            self.logger.debug(f"Debug mode enabled for Runner-{str(id)}")
        else:
            self.logger.setLevel("INFO")

    def run(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            try:
                self.process_task(task)
            except Exception as e:
                self.logger.error(f"Error processing task {task["type"]}: {e}")
            except Exit:
                self.logger.info("Exit signal received, stopping thread.")
                break
            finally:
                self.queue.task_done()
                time.sleep(0.5) # sleep to prevent overloading the battletabs servers.

    def process_task(self, task):
        # Process the task here
        # For example, you can call the battletabs API or database API here
        if task["type"] == "update_stats_for_user":
            user_id = task["options"]["user_id"]
            
            # Get the user's authToken and battletabs id from the database
            user_obj = self.database.execute("SELECT token, battletabs_id FROM users WHERE id = %s", (user_id,))
            authToken = user_obj[0][0]
            battletabs_id = user_obj[0][1]
            
            # Create a new BattleTabsClient object with the user's authToken
            client = BattleTabsClient(authToken)

            # Get the user's stats from the BattleTabs API
            stats = client.raw_query("me {stats {wins losses} currencies} myLeagueProgress {id	trophies highestTrophies diamonds}")

            # Extract stats from the response
            wins = stats["me"]["stats"]["wins"]
            losses = stats["me"]["stats"]["losses"]
            trophies = stats["myLeagueProgress"]["trophies"]
            diamonds = stats["myLeagueProgress"]["diamonds"]
            gold = stats["currencies"]["gold"]
            gems = stats["currencies"]["gems"]

            games_played = wins + losses
            winrate = wins / games_played if games_played > 0 else 0

            # get the current time
            now = time.time()

            # Update the user's stats in the database
            self.database.execute("INSERT INTO users (user_id, wins, losses, winrate, games_played, league, diamonds, gold, gems, from) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (battletabs_id, wins, losses, winrate, games_played, trophies, diamonds, gold, gems, now))
 
        elif task["type"] == "update_fleets_for_user":
            user_id = task["options"]["user_id"]

            # Get the user's authToken and battletabs id from the database
            user_obj = self.database.execute("SELECT token, battletabs_id FROM users WHERE id = %s", (user_id,))
            authToken = user_obj[0][0]
            battletabs_id = user_obj[0][1]

            # Create a new BattleTabsClient object with the user's authToken
            client = BattleTabsClient(authToken)

            # Get the user's fleets from the BattleTabs API
            fleets_raw = client.raw_query("query {customFleets {name ships {definitionId}}}")["customFleets"]
            fleets = []

            # Extract fleets from the response
            for fleet in fleets_raw:
                name = fleet["name"]
                ships = []
                for ship in fleet["ships"]:
                    ships.append(ship["definitionId"])
                
                fleets.append({"name": name, "ships": ships})
            
            fleets_for_database = []
            # match fleets from user with ones in the database
            for fleet in fleets:
                db_fleet_obj = self.database.execute("SELECT id, name FROM fleets WHERE %s in ANY(ships) AND %s in ANY(ships) AND %s in ANY(ships) AND %s in ANY(ships)", (fleet["ships"][0], fleet["ships"][1], fleet["ships"][2], fleet["ships"][3]))
                if len(db_fleet_obj) == 0:
                    # This fleet doesn't exist in the database, so we need to create it
                    # get stats for the fleet
                    dpt = 0
                    health = 0
                    for ship in fleet["ships"]:
                        ship_obj = self.database.execute("SELECT dpt, health FROM ships WHERE id = %s", (ship,))
                        dpt += ship_obj[0][0]
                        health += ship_obj[0][1]
                    
                    now = time.time()

                    # Create the fleet in the database
                    self.database.execute("INSERT INTO fleets (name, ships, dpt, health, owner_id, last_updated) VALUES (%s, %s)", (fleet["name"], fleet["ships"], dpt, health, user_id, now))
                    db_fleet_obj = self.database.execute("SELECT id, name FROM fleets WHERE %s in ANY(ships) AND %s in ANY(ships) AND %s in ANY(ships) AND %s in ANY(ships)", (fleet["ships"][0], fleet["ships"][1], fleet["ships"][2], fleet["ships"][3]))
                    db_fleet_obj = db_fleet_obj[0]
                else:
                    db_fleet_obj = db_fleet_obj[0]
                
                # add fleet to user's fleet list
                fleets_for_database.append(db_fleet_obj[0])

            now = time.time()
            
            # update the user's fleets in the database
            self.database.execute("UPDATE users SET fleets = %s WHERE id = %s", (fleets_for_database, user_id))

        elif task["type"] == "update_inventory_for_user":
            user_id = task["options"]["user_id"]
            
            # Get the user's authToken and battletabs id from the database
            user_obj = self.database.execute("SELECT token, battletabs_id FROM users WHERE id = %s", (user_id,))
            authToken = user_obj[0][0]
            battletabs_id = user_obj[0][1]

            # Create a new BattleTabsClient object with the user's authToken
            client = BattleTabsClient(authToken)

            # Get the user's inventory from the BattleTabs API
            inventory_raw = client.raw_query("blueprints {shipDefinitionId status} avatarParts {definitionId} avatarPartVariants {definitionId kind}myShipSkins {skins {definitionId}}")

            # Extract inventory from the response
            items = []

            for part in inventory_raw["avatarParts"]:
                items.append(part["definitionId"])
            for part in inventory_raw["avatarPartVariants"]:
                items.append(part["definitionId"])
            
            skins = []

            for skin in inventory_raw["myShipSkins"]["skins"]:
                skins.append(skin["definitionId"])
            
            ships = []
            for ship in inventory_raw["blueprints"]:
                ships.append(ship["shipDefinitionId"])

            now = time.time()

            # Update the user's inventory in the database
            self.database.execute("UPDATE users SET inventory = %s, skins = %s, ships = %s WHERE id = %s", (items, skins, ships, user_id))
            
        elif task["type"] == "process_battle":
            pass
        elif task["type"] == "recalculate_stats_for_fleet":
            pass
        else:
            self.logger.error(f"Unknown task type: {task['type']}")