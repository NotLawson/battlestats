## Main File
## Contains the server
from flask import Flask, request, jsonify, render_template, send_file, redirect
import os, sys, json, time
from threading import Thread
from queue import Queue
from modules.battletabs import BattleTabsClient, UnAuthBattleTabsClient
from modules.db import Database


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

## Setup

# Setup Websever
app = Flask(__name__)
app.config['SECRET_KEY'] = config["secret_key"]

if DEBUG:
    app.config["DEBUG"] = True
    app.logger.setLevel("DEBUG")
    app.logger.debug("Debug mode enabled")
else:
    app.config["DEBUG"] = False
    app.logger.setLevel("INFO")

app.logger.info("Flask Setup Complete")

# BattleTabs API
battletabs = UnAuthBattleTabsClient()
app.logger.info("BattleTabs API Setup Complete")

# Postgres API
database = Database(config["postgres"]["host"], config["postgres"]["port"], config["postgres"]["user"], config["postgres"]["password"], app.logger)
app.logger.info("Postgres API Setup Complete")

