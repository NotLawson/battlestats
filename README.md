# BattleStats
## A Stat Tracker for [BattleTabs](https://battletabs.com)

> WIP: This app is a work in progress. Many feature haven't been implemented/don't work

> **Due to the API we are using being an internal one, I will not put this project into production until the BattleTabs devs are ready to support other developers, as per request.**

## Idea
What exactly do we want to track in a tracking app for BattleTabs?

- League Trophies and Level. Trophies are the MMR for BattleTabs, and determine levels.
- Win Rate and Win Streaks. Other Skill metrics
- Map rotations. Collect a list of maps and show the current map to the user
- Item Shop. Collate the item shop and send notifications based on the user's inventory
- Clan Leaderboards and points. Show leaderboards for these, etc
- Fleet performance (+ a fleet designer). Allow user a more indepth evaluation of their fleets
- The meta. Most common ships, fleets, etc

## Development
How can we do this?

Battletabs does not have an official API as of yet, so I will have to use the unofficial API (aka the internal API).

The Battletabs client (your browser on battletabs.io) comunicates to the Battlestabs servers (fly.io servers on battletabs.fly.io) via GraphQL, and more specifically, Websocket GraphQL on battletabs.fly.io/graphql.

The great thing about GraphQL is that, even though there isn't any documentation, the GraphQL Server sends all the available endpoints and schemas and related documentation to the client on request. This means that, using an API browser like Insomnia, I can get all the available commands without having to manaually search throught the code. Yay!

Some of these endpoints don't require use to be authenticated, but most relating to "me-" or "my-" do, so we will need to find some way to cheese the GraphQL server into thinking we are a legitimate client.

~~This took me a long time, mostly just searching all of the .js files I could find for anything relating to the authentication process, but since every single variable was a random combination of either 1, 2 or 3 letters, I never found the part that retrieves an auth token. For now however, I can just copy the config (which includes the auth token) that the legitimate client sends to log into its GraphQL session, which can be found in the Network section of Chrome's developer tools, when you inspect the /graplhql websocket and scroll to the top of the messages.~~

> I figured it out. There's a mutation on the server called loginWithCredentials. This takes the arguemnts email and password, and returns the authToken we need! This means I can create my own login page instead of needing to pull of something nefarious or complicated.

So let's look at our first item to track:

### League and Trophies, WR and WS
What we need to be able to do is to take a userid and return with trophies, WR, WS and other stats, as well as record those stats somewhere for graphs and history.

The storing bit is easy. We can use InfluxDB to just log the stats at the right times. However, getting the stats is a little bit trickier.

#### League/Trophies
There aren't any endpoints according to the schema that allow me to lookup league levels and trophies by user. I tried one called "leaguePlayers" that takes the arguements minTrophies, maxTropies and take. min and max are pretty self explanitory, but take is quite an unusual argument name that I couldn't figure out.

I tried running this with minTrophies set to 0 and maxTrophies set to something like 100000000, but it only returned about 5 or 6 players. I'm pretty sure there are more than 6 people who play Battletabs, so I'm going to label this command as unusable.

There is another command, "adminListLeaguePlayers", which only takes the arguement take, no min/max arguements, so I'm fairly sure that command would be the best option, if only my account had admin privledges. Ahh well.

There is a command to get players near a trophy amount, "nearbyLeaguePlayers" that takes a trophies arguemnt, but I didn't try that one as it still won't allow me to get either a list of all players to filter through, or a command that does it for me.

The command "league", which just returns a League object, also doesn't help too much. It just contains some meta data around the diamond dash and when the league finishes.

If you use the command "userById" (or "userByShortId"), it will return their lifetime trophies as well as other stats (We'll look at this command later), but not thier current League level.

So far, the only command that returns a player's current trophy amount is "myLeagueProgress", which, you guessed it, only returns the trophys for the currently authed player. This is workable, but not ideal, as it will require the player to give us thier auth token to track thier stats, but having their token also means we can track other useful things like their battles, fleets etc, so it's not all bad.

#### WR and WS

Thank god for the "userById" command, because it returns a bunch of player data and stats, like wins, losses, shots (which is really broken for some reason), and, you guessed it, win rate and winstreaks without having to be authed as the user. So, uh, yeah, not much else to say here.

### Map rotation

More good news here, we can both query the current map with "currentMap" AND subscibe to "currentMapChanged", which will both return the map id. Yey!

### Item shop

MORE GOOD NEWS?!?! There are 4 different commands to check the daily shop, "dailyBlueprint", "dailyEmotes", "dailyShipSkin" and "dailyAvatarPart", which all return both prices and meta data. So, yeah easy again.

### Fleets and ships

While we can't just query for a user's custom fleets, we are able to find our own custom fleets. This will be similar to getting league rankings, as we will periodically log into a user account to grab current fleets. These fleets can be then uploaded and discussed.

It should also be able to indentify different fleet types (such as 2a2r) and suggest different strategies based on it, aswell as calculating the damage per turn using the [BattleTabs Damage](https://discord.com/channels/770955477215084554/770955477215084556/1360054020613472438) Table by originally by HeavenlySome (fixed up by me). 

I also want to be able to associate fleets with replays. This way we can include a win rate as well as average reveal and shot stats from different matches. This allows us to get to my ulitmate goal: The fleet creator.

#### Fleet Creator

The fleet creator is probabaly one of my favourite (and high priority) features for this stats tracker. Basically, I want to have a list of all Battletabs ships, grouped into catergories (also in the damage table, thanks Heavenly!). This allows us to more easily pick different ability types. It also should be able to autocomplete different ships based on the ships you've already picked, e.g. if you picked cartographer, raft and coracle, it might pick longboat or valkryie.

It should also show the stats I mentioned before, like winrate, average reveals, average shots etc to give users a better view of what their fleets are capable of.`

## Contributing 

I would love help making this project. Look in issues for things that need to be done.

To get setup for development with this project, there are a couple of thing you need to install/config:

- The latest version of Python, but anything 3.9 onwards should work.
- The latest version of all the packages in requirements.txt, unless specified.
- [Just](https://just.systems/man/en/quick-start.html) is also quite useful, so I'd install that
- A Postgres database with a default database of postgres. This app will sort out setting up the tables. If you run this inside of a docker stack (e.g. the compose.yml file in the root of this repository), please make sure you set the config.json file's database variables to the same as the variables for the postgres container. Likewise, please match the database variable to the ones needed to contact a bare metal postgres installation.
- A Redis instance. This allows the main.py server and the task runner to communicate.

Then just run the main Python file (main.py). It'll start a webserver on the port specified in the config file.

You also need to run task_runner.py, which will start a task runner for the main server

## Todo

- Finish entering ship details into the modules/defaults.py file. Use the BattleTabs wiki to get the ability description, and the BattleTabs Damage Table to get the DPT values.
- Finish fleshing out the website
- Finish making the website pretty
- Create the backend functions for all of this
- Finish creating the tasks for the task runner
- Create some documentation for the BattleTabs API at https://battletabs.fly.io/graphql (you should be able to get the schema from it, just create some docs)
- Display Stat history using Chart.js
- Get the frontend working
- Auto upload replays (hows that gonna work?)
- Fleet designer/Manager (shipyard)
- Leaderboard
- View other player's historical stats

