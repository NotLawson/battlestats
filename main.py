## Main File
## Contains the server
import os, sys, json, time
from flask import Flask, request, jsonify, render_template, send_file, redirect


# Setup
## Load config
config = json.load(open("config.json"))
### Verify config
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

## Setup Websever
app = Flask(__name__)
app.config['SECRET_KEY'] = config["secret_key"]

## Configure logger
if DEBUG:
    app.config["DEBUG"] = True
    app.logger.setLevel("DEBUG")
    app.logger.debug("Debug mode enabled")
else:
    app.config["DEBUG"] = False
    app.logger.setLevel("INFO")
app.logger.info("Flask Setup Complete")

## BattleTabs API
from modules.battletabs import BattleTabsClient, UnAuthBattleTabsClient
battletabs = UnAuthBattleTabsClient()
app.logger.info("BattleTabs API Setup Complete")

## Postgres API
from modules.db import Database
database = Database(config["postgres"]["host"], config["postgres"]["port"], config["postgres"]["user"], config["postgres"]["password"], app.logger)
app.logger.info("Postgres API Setup Complete")

## Get auth module (depends on database)
from modules import auth
app.logger.info("Auth Module Setup Complete")

# Routes
## Admin
@app.route("/admin")
def admin_home():
    """ 
    Admin home page. This is the main page for the admin panel. This will act as a dashboard for the admin section.
    """
    #return render_template("admin_home.html")
    return render_template("not_built.html")
@app.route("/admin/users")
def admin_users():
    """
    Admin users page. This will show a list of all users and their information.
    """
    #return render_template("admin_users.html")
    return render_template("not_built.html")
@app.route("/admin/users/<user_id>")
def admin_user(user_id):
    """
    Admin user page. This will show a specific user and their information.
    """
    #return render_template("admin_user.html")
    return render_template("not_built.html")
@app.route("/admin/users/<user_id>/edit", methods=["GET", "POST", "DELETE"])
def admin_user_edit(user_id):
    """
    Admin user edit page. This will show a form to edit a specific user.
    This will handle GET for the form, POST for the form submission and DELETE for deleting the user.
    """
    #return render_template("admin_user_edit.html")
    return render_template("not_built.html")
@app.route("/admin/fleets")
def admin_fleets():
    """
    Admin fleets page. This will show a list of all fleets and their information.
    """
    #return render_template("admin_fleets.html")
    return render_template("not_built.html")
@app.route("/admin/fleets/<fleet_id>")
def admin_fleet(fleet_id):
    """
    Admin fleet page. This will show a specific fleet and their information.
    """
    #return render_template("admin_fleet.html")
    return render_template("not_built.html")
@app.route("/admin/fleets/<fleet_id>/edit", methods=["GET", "POST", "DELETE"])
def admin_fleet_edit(fleet_id):
    """
    Admin fleet edit page. This will show a form to edit a specific fleet.
    This will handle GET for the form, POST for the form submission and DELETE for deleting the fleet.
    """
    #return render_template("admin_fleet_edit.html")
    return render_template("not_built.html")
@app.route("/admin/clans")
def admin_clans():
    """
    Admin clans page. This will show a list of all clans and their information.
    """
    #return render_template("admin_clans.html")
    return render_template("not_built.html")
@app.route("/admin/clans/<clan_id>")
def admin_clan(clan_id):
    """
    Admin clan page. This will show a specific clan and their information.
    """
    #return render_template("admin_clan.html")
    return render_template("not_built.html")
@app.route("/admin/clans/<clan_id>/edit", methods=["GET", "POST", "DELETE"])
def admin_clan_edit(clan_id):
    """
    Admin clan edit page. This will show a form to edit a specific clan.
    This will handle GET for the form, POST for the form submission and DELETE for deleting the clan.
    """
    #return render_template("admin_clan_edit.html")
    return render_template("not_built.html")
@app.route("/admin/settings")
def admin_settings():
    """
    Admin settings page. This will show a form to edit the settings of the server.
    """
    #return render_template("admin_settings.html")
    return render_template("not_built.html")
@app.route("/admin/settings/edit", methods=["GET", "POST"])
def admin_settings_edit():
    """
    Admin settings edit page. This will show a form to edit the settings of the server.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("admin_settings_edit.html")
    return render_template("not_built.html")
@app.route("/admin/logs")
def admin_logs():
    """
    Admin logs page. This will show a list of all logs and their information.
    """
    #return render_template("admin_logs.html")
    return render_template("not_built.html")
@app.route("/admin/logs/<log_id>")
def admin_log(log_id):
    """
    Admin log page. This will show a specific log and its information.
    """
    #return render_template("admin_log.html")
    return render_template("not_built.html")
@app.route("/admin/vitals")
def admin_vitals():
    """
    Admin vitals page. This will show a list of all vitals on the server.
    """
    #return render_template("admin_vitals.html")
    return render_template("not_built.html")
@app.route("/admin/news")
def admin_news():
    """
    Admin news page. This will show a list of all news and their information.
    """
    #return render_template("admin_news.html")
    return render_template("not_built.html")
@app.route("/admin/news/<news_id>")
def admin_news_item(news_id):
    """
    Admin news item page. This will show a specific news item and its information.
    """
    #return render_template("admin_news_item.html")
    return render_template("not_built.html")
@app.route("/admin/news/<news_id>/edit", methods=["GET", "POST", "DELETE"])
def admin_news_edit(news_id):
    """
    Admin news item edit page. This will show a form to edit a specific news item.
    This will handle GET for the form, POST for the form submission and DELETE for deleting the news item.
    """
    #return render_template("admin_news_edit.html")
    return render_template("not_built.html")
@app.route("/admin/news/create", methods=["GET", "POST"])
def admin_news_create():
    """
    Admin news item create page. This will show a form to create a new news item.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("admin_news_create.html")
    return render_template("not_built.html")
## Accounts
@app.route("/account")
def account_home():
    """
    Account home page. This will show the account information of the user.
    """
    #return render_template("account_home.html")
    return render_template("not_built.html")
@app.route("/account/edit", methods=["GET", "POST", "DELETE"])
def account_edit():
    """
    Account edit page. This will show a form to edit the account information of the user.
    This will handle GET for the form, POST for the form submission and DELETE for deleting the account.
    Upon deleting the account, the user will be logged out and redirected to the home page.
    The database entry will be updated to remove the username, password, email, battletabs token and any other information.
    Existing user stats will not be removed from the database, and the account will recieve ghost status. This allows for the user to remove their account
    without disrupting the database or losing their stats.
    """
    #return render_template("account_edit.html")
    return render_template("not_built.html")
@app.route("/account/logout")
def account_logout():
    """
    Account logout page. This will log the user out and redirect to the home page.
    """
    #return render_template("account_logout.html")
    return render_template("not_built.html")
@app.route("/account/login", methods=["GET", "POST"])
def account_login():
    """
    Account login page. This will show a form to log in to the account.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("account_login.html")
    return render_template("not_built.html")
@app.route("/account/register", methods=["GET", "POST"])
def account_register():
    """
    Account register page. This will show a form to register a new account.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("account_register.html")
    return render_template("not_built.html")
@app.route("/account/forgot_password", methods=["GET", "POST"])
def account_forgot_password():
    """
    Account forgot password page. This will show a form to reset the password of the account.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("account_forgot_password.html")
    return render_template("not_built.html")
@app.route("/account/verify_email", methods=["GET", "POST"])
def account_verify_email():
    """
    Account verify email page. This will show a form to verify the email of the account.
    This will handle GET for the form, POST for the form submission.
    """
    #return render_template("account_verify_email.html")
    return render_template("not_built.html")

## Misc
@app.route("/")
def misc_home():
    """
    Home page. This will show the home page of the application.
    This will switch between the home page when logged in and the index page when not logged in.
    This will show the latest news, updates and stats.
    """
    #return render_template("misc_home.html")
    return render_template("not_built.html")
@app.route("/news")
def misc_news():
    """
    News page. This will show the latest news and updates from the application. This will mirror ingame news and updates but also
    include news from BattleStats about development and updates to the application.
    """
    #return render_template("misc_news.html")
    return render_template("not_built.html")
@app.route("/news/<news_id>")
def misc_news_item(news_id):
    """
    News item page. This will show a specific news item and its information.
    """
    #return render_template("misc_news_item.html")
    return render_template("not_built.html")
@app.route("/shop")
def misc_shop():
    """
    Shop page. This will show the shop page from BattleTabs. This will show the items available for purchase and the prices.
    """
    #return render_template("misc_shop.html")
    return render_template("not_built.html")
@app.route("/items")
def misc_items():
    """
    Items page. This will show a list of all items and their information. This includes ships, skins and cosmetics.
    """
    #return render_template("misc_items.html")
    return render_template("not_built.html")
@app.route("/items/<item_id>")
def item(item_id):
    """
    Item page. This will show a specific item and its information.
    """
    #return render_template("item.html")
    return render_template("not_built.html")
@app.route("/maps")
def maps():
    """
    Maps page. This will show a list of all maps and their information, along with the current daily map.
    """
    #return render_template("maps.html")
    return render_template("not_built.html")

## Stats

## Fleets

## Clans