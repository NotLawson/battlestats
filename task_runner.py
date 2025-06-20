## Task Runner for the Webserver
## TODO: Implement a proper init order.
# This module is responsible for running tasks in the background.
# First, the task is passed to the Load Balancer, which runs in the main thread.
# This is done via a redis server, which also tracks system health
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
from modules.db import Database
from modules.battletabs import BattleTabsClient, UnAuthBattleTabsClient
from modules.config import Config
from logging import Logger
import os, sys, json, time
from queue import Queue
import redis

## Load config
config = Config("config.json")
if not config.check_config():
    print("Config file is missing or invalid. Please check config.json.")
    sys.exit(1)

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

# System Health
def health(state, scale = None):
    global redis_server
    if state == "ready":
        redis_server.set("health/manager", {
            "state":"running",
            "runners":scale,
            "since":time.time()
        })
    elif state == "exit":
        redis_server.set("health/manager", {
                "state":"exited",
                "since":time.time()
            })


# Runners
class Runner:
    def __init__(self,id: int, queue: Queue, database: Database, redis: redis.Redis):
        self.queue = queue
        self.database = database
        self.redis = redis
        self.logger = Logger(f"Runner-{str(id)}")
        self.id = id
        if DEBUG:
            self.logger.setLevel("DEBUG")
            self.logger.debug(f"Debug mode enabled for Runner-{str(id)}")
        else:
            self.logger.setLevel("INFO")

    def __call__(self):
        self.health("idle")
        while True:
            task = self.queue.get()
            if task is None:
                break
            try:
                self.health("running", task = task["type"])
                self.process_task(task)
            except Exit:
                self.logger.info("Exiting runner")
                self.health("exit")
            except Exception as e:
                type = task["type"]
                self.logger.error(f"Error processing task {type}: {e}")
            finally:
                self.health("idle")
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
        elif task["type"] == "exit":
            raise Exit
        else:
            self.logger.error(f"Unknown task type: {task['type']}")
    
    def health(self, state, task = None):
        if state == "running":
            self.redis.set("health/runner-"+str(self.id), {
                "state":"running",
                "task":task,
                "since":time.time()
            })
        elif state == "idle":
            self.redis.set("health/runner-"+str(self.id), {
                "state":"idle", 
                "since":time.time()
            })
        elif state == "exit":
            self.redis.set("health/runner-"+str(self.id), {
                    "state":"exited",
                    "since":time.time()
                })
class Manager:
    runners = []
    queues = []
    def __init__(self, init_scale, database: Database, redis: redis.Redis, runner_class = Runner):
        self.runner_class = runner_class
        self.database = database
        self.redis = redis
        self.current_scale = 0
    
    def scale(self, new_scale: int):
        if self.current_scale == new_scale:
            logger.warning(f"Can't scale from {str(self.current_scale)} to {str(new_scale)}")
        elif self.current_scale > new_scale:
            # decrease instances
            logger.info(f"Scaling from {str(self.current_scale)} to {str(new_scale)}...")
            instances_to_kill = self.current_scale - new_scale
            i = 0
            for i in range(instances_to_kill):
                logger.info(f"Killing instance {str(len(self.runners)-1)}")
                runner = self.runners.pop()
                queue = self.queues.pop()
                queue.put({
                    "type":"exit"
                })
                runner.join()
                del runner, queue
                i += 1
            logger.info("Done.")

        elif self.current_scale < new_scale:
            # increase instances
            logger.info(f"Scaling from {str(self.current_scale)} to {str(new_scale)}...")
            instances_to_create = new_scale - self.current_scale
            i = 0
            for i in range(instances_to_create):
                new_runner_id = len(self.runners)-1
                logger.info(f"Creating instance {str(new_runner_id)}")
                queue = Queue()
                runner = Thread(target=self.runner_class(new_runner_id, queue, self.database, self.redis))
                runner.start()
                self.runners.append(runner)
                self.queues.append(queue)
                i += 1

            logger.info("Done.")

        return new_scale
    
    def process_event(self, event):
        if event["type"] == "scale":
            new_scale = int(event["options"]["scale"])
            self.scale(new_scale)
        else:
            index, highest = 0, 0
            for i, queue in enumerate(self.queues):
                if len(queue) > highest:
                    highest = len(queue)
                    index = i
            self.queues[index].put(event)

# Load Balancer
redis_server = redis.Redis("systems")

# Redis Server Layout:
# /-
#  |- events: Events Queue. A redis subscription listens to this and updates the main event queue. Then, the load balancer sorts the events between runners
#  |- health: The health of the system runners. The runners update this themselves.

database = Database(config.get("postgres")["host"], config.get("postgres")["port"], config.get("postgres")["user"], config.get("postgres")["password"], logger)
pubsub = redis_server.pubsub()
pubsub.subscribe("event")
manager = Manager(config.get("init_runner_scale"), database, redis_server)

logger.info("Ready to process messages")
health("ready")
while True:
    event = pubsub.get_message()
    if event["type"]=="shutdown":
        break
    manager.process_event(event)
    time.sleep(0.5)
health("exit")
i = 0
logger.warning("Exiting...")
for i in range(len(manager.runners)):
    runner = manager.runners.pop()
    queue = manager.queue.pop()
    queue.put({"type":"exit"})
    runner.join()
    del runner, queue
    i += 1

logger.warning("Exited")