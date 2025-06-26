## Main File
## Contains the server
print("BattleStats!")
## The webserver has to load the following components:
## 0. System imports
## 1. Configuration
## 2. Webserver
## 3. Logger
## 4. Database
## 5. BattleTabs API
## 6. Auth module
## 7. Non-system imports
## 8. Routes
## 9. Task Runner

## 0. System imports
import os, sys, json, time, requests

## 1. Configuration
from modules.config import Config
config = Config("config.json")

DEBUG = False
if "--debug" in sys.argv:
    DEBUG = True


## 2. Webserver
from flask import Flask, request, jsonify, render_template, send_file, redirect, make_response, Response
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("secret_key", "super_secret_secret_key")

## 3. Logger
if DEBUG:
    app.config["DEBUG"] = True
    app.logger.setLevel("DEBUG")
    app.logger.debug("Debug mode enabled")
else:
    app.config["DEBUG"] = False
    app.logger.setLevel("INFO")
app.logger.info("Flask Setup Complete")

## 4. Database
from modules.db import Database
while True:
    try:
        database = Database(config.get("postgres")["host"], config.get("postgres")["port"], config.get("postgres")["user"], config.get("postgres")["password"], app.logger)
        app.logger.info("Postgres API Setup Complete")
        break
    except Exception as e:
        app.logger.error("Failed to connect to Postgres database: %s", e)
        app.logger.info("Retrying in 5 seconds...")
        time.sleep(5)

## 5. BattleTabs API
from modules.battletabs import BattleTabsClient, UnAuthBattleTabsClient
battletabs = UnAuthBattleTabsClient()
app.logger.info("BattleTabs API Setup Complete")

## 6. Auth systems
## (depends on database)
from modules import auth
app.logger.info("Auth Module Setup Complete")

## 7. Non-system imports
from datetime import datetime
from modules import runner
runner = runner.RunnerClient()
app.logger.info("Non-system imports Setup Complete")

## 8. Routes
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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("account_login.html", error="Username and password are required.")
        token = auth.login(username, password)
        if not token:
            return render_template("account_login.html", error="Invalid username or password.")
        resp = make_response(redirect("/"))
        resp.set_cookie("session_token", token)
        app.logger.info("User %s logged in successfully with token %s", username, token)
        return resp

    return render_template("account_login.html")

@app.route("/account/register", methods=["GET", "POST"])
def account_register():
    """
    Account register page. This will show a form to register a new account.
    This will handle GET for the form, POST for the form submission.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        battletabs_token = request.form.get("battletabs_token")
        battletabs_id = request.form.get("battletabs_id")
        battletabs_username = request.form.get("battletabs_username")
        fleets = []
        if not username or not password or not email or not battletabs_token or not battletabs_id or not battletabs_username:
            return render_template("account_register.html", error="All fields are required. Please ensure you have logged into a BattleTabs Account before submitting.")
        if not auth.signup(username, password, email, battletabs_token, battletabs_id, battletabs_username, fleets):
            app.logger.info("Failed to create account for user %s with email %s", username, email)
            return render_template("account_register.html", error="Failed to create account. This is most likely due to a username or email already being in use. Please try again with a different username or email.")
        session_token = auth.login(username, password)
        resp = make_response(redirect("/"))
        resp.set_cookie("session_token", session_token)
        app.logger.info("Successfully created account for user %s with email %s", username, email)
        runner.event({"type":"update_stats_for_user", "options": {"user_id": database.get_user_by_username(username)[0]}})
        return resp
    return render_template("account_register.html")
@app.route("/account/register/battletabs")
def account_register_battletabs():
    """
    BattleTabs Account linking popup page. This endpoint just returns the template.
    """
    return render_template("account_register_battletabs.html")
    
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
    app.logger.info("User is accessing the home page")
    id = auth.auth(request)
    if not id:
        return render_template("misc_index.html")
    else:
        user = database.get_user_by_id(id)
        if not user:
            return render_template("misc_index.html")
        stats = database.execute("SELECT * FROM stats WHERE user_id = %s ORDER BY time DESC", (id,))
        runner.event({"type": "update_stats_for_user", "options": {"user_id": id}})
        return render_template("misc_home.html", user=user, round=round, stats=stats if stats else None)

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

## API
### GraphQL Proxy
@app.route("/api/graphql", methods = ["POST"])
def api_graphql():
    """
    GraphQL Proxy endpoint. This will proxy the request to the BattleTabs API.
    This will handle POST requests with a JSON body containing the query and variables.
    """
    query = request.get_data().decode("utf-8")
    auth_token = request.headers.get("Authorization", False)
    if not auth_token:
        try:
            return jsonify(battletabs.raw(query))
        except Exception as e:
            app.logger.error("Error in GraphQL query: %s", e)
            return jsonify({"error": "Invalid query"}), 400
    else:
        try:
            client = BattleTabsClient(auth_token.split(" ")[1])
            return jsonify(client.raw(query))
        except Exception as e:
            app.logger.error("Error in GraphQL query with auth: %s", e)
            return jsonify({"error": "Invalid query"}), 400


@app.route("/api/ping", methods=["GET"])
def api_ping():
    """
    Ping the runners
    """
    runner.event({"type": "ping"})
    return jsonify({"status": "pong"}), 200

## Starting the webserver
if __name__ == "__main__":
    app.logger.info("Starting server on port %s", config.get("port", 5000))
    app.run(host="0.0.0.0", port=config.get("port", 5000), debug=True)
    