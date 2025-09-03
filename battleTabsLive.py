# BattleTabs Live Bot
# Keeps track of finished battles from the BattleTabs live discord channel

from modules import config
config = config.Config("config.json")

import discord
"""intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True"""

client = discord.Client(activity=discord.Streaming(name="BattleTabs Battles", url="https://battlestats.thatrandompi.xyz", game="BattleTabs"))

from modules import runner
rc = runner.RunnerClient(host="systems")

@client.event
async def on_message(message):
    if message.channel.id != 779285528259330078: # #battletabs-live channel
        return
    # Process the message
    embed = message.embeds[0]
    if embed.title != "Battle Finished!":
        return
    for field in embed.fields:
        if field.name != "Replay":
            continue
        # Process the replay field
        print("replay:", field.value)
        replay_id = field.value[37:].split("/")[0]
        rc.event({ # send battle id off to the runner
            "type": "process_battle",
            "options": {
            "replay_id": replay_id
            }
        })
        print("Battle ID:", replay_id)
        return
    return

@client.event
async def on_ready():
    print("ready")

client.run(config.get("discord_token"))