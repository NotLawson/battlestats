import psycopg2, json

## DATABASE SETUP ##
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
register_adapter(dict, Json)


class Database:
    def __init__(self, host, port, user, password, logger):
        self.logger = logger

        self.logger.info("Connecting to database...")
        self.conn = psycopg2.connect(
            host=host,
            database="battlestats",
            user=user,
            password=password,
            port=port
        )
        self.logger.info("Connected to database")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        self.setup()

    def setup(self):
        self.logger.info("Setting up database...")

        ## TABLE CREATION ##
        ## Users table
        # - id: User id
        # - username: Username
        # - password: hash of password. the password is never given to the server, the hash is generated by the client side and 
        #   then sent to the server. This protects the user's password in the event of a database breach
        # - email: email used for communication with the user
        # - token: The battletabs user token. The user will generate the token client side (again, no credentials going to the server) and
        #   then send it to the server. This allows us to support Discord, Google and Apple login ontop of user/password (hopefully, I will
        #   investigate this later)
        # - battletabs_id: The battletabs user id. This is used to identify the user in the battletabs API
        # - battletabs_username: The battletabs username. This is used to identify the user and find thier id.
        # - fleets: The fleets the user has. This is an array of fleet ids.
        # - flags: specifies the account type, as well as warnings, bans, moderation and admin:
        #   - standard: Standard user account. has an email, has a valid token
        #   - system: System account. Does not have an email or a valid token. This is used for stuff like admin accounts etc
        #   - banned: The user is banned from the platform. They will not be able to login or use the API.
        #   - warning: The user has a warning. This is used for moderation purposes. The user can still login and use the API.
        #   - moderator: The user is a moderator. This is used for moderation purposes.
        #   - admin: The user is an admin. This is used for moderation purposes.
        #   - fleetmod: The user is a fleet moderator. This is used for moderation purposes.
        # - last_login: The last time the user logged in. This is used for moderation purposes.
        # - account_created: The time the account was created. This is used for moderation purposes.
        self.logger.info("Setting up users table...")
    
        try: 
            self.cursor.execute('''
            CREATE TABLE users(
                        id serial primary key,
                        username varchar(50) not null,
                        password varchar(255) not null,
                        email varchar(50),
                        token text,
                        battletabs_id text,
                        battletabs_username text,
                        fleets array(text),
                        flags array(text),
                        last_login timestamp,
                        account_created timestamp
                        )
            ''')
            self.logger.info("Users table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Users table already exists, moving on...")

        ## Stats Table
        # When updating this table, the task runner will create another row with a different timestamp. This allows us to keep track of historical data.
        # - user_id: the user id that the stats belong to
        # - wins: amount of wins;
        # - losses: amount of losses;
        # - winrate: winrate
        # - games_played: amount of games played
        # - league: the amount of trophies the user currently has. this can be used to calculate the current rank of a user
        # - diamonds: the amount of diamonds the user has.
        # - gold: the amount of gold the user has.
        # - gems: the amount of gems the user has.
        # - from: the time the stats were taken. This is used to determine if the stats are up to date, or if it's been long enough since the last stats update.
        self.logger.info("Setting up stats table...")
        try:
            self.cursor.execute('''
            CREATE TABLE stats(
                        user_id integer references users(id),
                        wins integer,
                        losses integer,
                        winrate float,
                        games_played integer,
                        league integer,
                        diamonds integer,
                        gold integer,
                        gems integer,
                        from timestamp
                        )
            ''')
            self.logger.info("Stats table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Stats table already exists, moving on...")

        ## Ships Table
        # This is a static table used to store ships metadata.
        # - definition_id: The id of the ship in the battletabs API.
        # - name: The name of the ship.
        # - type: The type of the ship.
        #   - attacker: Attacker ship
        #   - sonar: Sonar ship
        #   - revealer: Revealer ship
        #   - special: Special ship
        # - cd: The cooldown of the ship.
        # - ability: The description of the ship's ability from the game.
        # - dpt: The damage per turn of the ship as defined by HeavenlySome's BattleTabs damage table.
        # - skins: An array of skin ids that the ship has.
        # - health: The amount of tiles the ship owns.
        # - tags: The tags of the ship. This can be used to filter ships by skills.
        #   - big: The ship is big.
        #   - small: The ship is small.
        # - last_updated: The last time the ship was updated. This is used to determine if the ship is up to date.
        self.logger.info("Setting up ships table...")
        try:
            self.cursor.execute('''
            CREATE TABLE ships(
                        definition_id text primary key unique,
                        name text,
                        type text,
                        cd integer,
                        ability text,
                        dpt float,
                        skins array(text),
                        health integer,
                        tags array(text)
                        )
            ''')
            self.logger.info("Ships table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Ships table already exists, moving on...")
        
        ## Fleets Table
        # - id: The id of the fleet.
        # - name: The name of the fleet.
        # - owner_id: The id of the user that owns the fleet.
        # - description: The description of the fleet.
        # - ships: The ships in the fleet. This is an array of ship ids.
        # - tags: The tags of the fleet. This is an array of tags that can be used to filter fleets by skills.
        #   - big: The fleet is big.
        #   - small: The fleet is small.
        #   - fast: The fleet is fast.
        #   - slow: The fleet is slow.
        # - type: The type of the fleet (2a2r etc)
        # - dpt: The damage per turn of the fleet as defined by HeavenlySome's BattleTabs damage table.
        # - wins: The amount of wins the fleet has.
        # - losses: The amount of losses the fleet has.
        # - winrate: The winrate of the fleet.
        # - games_played: The amount of games played with the fleet.
        # - health: The amount of tiles the fleet owns.
        # - last_updated: The last time the fleet was updated.
        self.logger.info("Setting up fleets table...")
        try:
            self.cursor.execute('''
            CREATE TABLE fleets(
                        id serial primary key,
                        name text,
                        owner_id integer references users(id),
                        description text,
                        ships array(text),
                        tags array(text),
                        type text,
                        dpt float,
                        wins integer,
                        losses integer,
                        winrate float,
                        games_played integer,
                        last_updated timestamp,
                        health integer
                        )
            ''')
            self.logger.info("Fleets table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Fleets table already exists, moving on...")
        
        ## Inventory Table
        # - user_id: The id of the user that owns the inventory.
        # - ships: The ships in the inventory. This is an array of ship ids.
        # - skins: The skins in the inventory. This is an array of skin ids.
        # - cosmetics: The cosmetics in the inventory. This is an array of cosmetic ids.
        # - medals: The medals in the inventory. This is an array of medal ids.
        # - last_updated: The last time the inventory was updated.
        self.logger.info("Setting up inventory table...")
        try:
            self.cursor.execute('''
            CREATE TABLE inventory(
                        user_id integer references users(id),
                        ships array(text),
                        skins array(text),
                        cosmetics array(text),
                        medals array(text),
                        last_updated timestamp
                        )
            ''')
            self.logger.info("Inventory table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Inventory table already exists, moving on...")

        ## Battles Table
        # - id: The id of the battle. This is set by the BattleTabs API.
        # - first_player_id: The id of the first player. This is thier battletabs id.
        # - second_player_id: The id of the second player. This is thier battletabs id.
        # - winner_id: The id of the winner. This is thier battletabs id.
        # - first_player_fleet: The fleet of the first player. This is an array of ship ids.
        # - first_player_fleet_id: The fleet id of the first player.
        # - second_player_fleet: The fleet of the second player. This is an array of ship ids.
        # - second_player_fleet_id: The fleet id of the first player.
        # - map: The map of the battle. This is a map_id from the BattleTabs API.
        # - type: The type of the battle. This is a string that can be used to filter battles by type
        #   - short: The battle was short.
        #   - long: The battle was long.
        # - ranked: The battle was a ranked battle. This is a boolean value.
        # - start_time: The time the battle started.
        # - end_time: The time the battle ended.
        # - turns: The amount of turns the battle lasted.
        self.logger.info("Setting up battles table...")
        try:
            self.cursor.execute('''
            CREATE TABLE battles(
                        id text primary key,
                        first_player_id text,
                        second_player_id text,
                        winner_id text,
                        first_player_fleet array(text),
                        first_player_fleet_id integer references fleets(id),
                        second_player_fleet array(text),
                        second_player_fleet_id integer references fleets(id),
                        map text,
                        type text,
                        ranked boolean,
                        start_time timestamp,
                        end_time timestamp,
                        turns integer
                        )
            ''')
            self.logger.info("Battles table created")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Battles table already exists, moving on...")
        

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    def execute_many(self, query, params=None):
        self.cursor.executemany(query, params)
        return self.cursor.fetchall()

