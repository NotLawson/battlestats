from flask import Flask, render_template, request, redirect, make_response
import modules.db as db
import json
from queue import Queue


app = Flask(__name__)

import modules.auth as auth
from modules.auth import UserDB
userdb = UserDB()

battledb = db.DB("battles")
#fleetdb = db.DB("fleets") # not implemented

from modules import battletabs
BTClient = battletabs.BattleTabsClientUnAuth()


# Import submodules in order
from modules import battles

from modules import service
main_queue = Queue()
service.start(main_queue, 2)

@app.route('/')
def index():
    username = auth.auth(request.cookies.get('token'))
    if username==None:
        return render_template('index.html', title="BattleStats")
    user = userdb.get(username)
    main_queue.put({"type":"sync", "username":username})
    return render_template('home.html', user=user, title="BS: Home", round=round, int=int, json=json)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = auth.login(username, password)
        if token=="invalidusername":
            message = "Invalid username"
        elif token=="invalidpassword":
            message = "Invalid password"
        else:
            resp = make_response(redirect('/', 302))
            resp.set_cookie('token', token)
            return resp
        return render_template('login.html', message=message, title="BS: Login")
    return render_template('login.html', title="BS: Login")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if userdb.get(username)!=None:
            message = "Username already exists"
        else:
                bt_email = request.form['email']
                bt_password = request.form['bt']

                authtoken = BTClient.mutate('mutation {loginWithCredentials(email: "'+bt_email+'", password: "'+bt_password+'")}')["loginWithCredentials"]
            #try:
                userdb.set(username, auth.User(username, password, authtoken))
                userdb.redis.set("_idtousername", json.dumps({**json.loads(userdb.redis.get("_idtousername")), userdb.get(username).id:username}))
                token = auth.login(username, password)
            #except Exception as e:
            #    print(e)
            #    return render_template('signup.html', message="Invalid BattleTabs token")
                resp = make_response(redirect('/', 302))
                resp.set_cookie('token', token)
                return resp
        return render_template('signup.html', message=message, title="BS: Signup")
    return render_template('signup.html', title="BS: Signup")

@app.route('/players', methods=['GET','POST'])
def players_search():
    if request.method == 'POST':
        username = userdb.find_username(request.form['id'])
        return redirect('/players/'+username)
    return render_template('players.html', title="BS: Players")

@app.route('/players/<username>')
def player_info(username):
    if username=="unknown":
        return render_template('player_notfound.html', title="BS: Player Not Found")
    user = userdb.get(username)
    if user==None:
        return render_template('player_notfound.html', title="BS: Player Not Found")
    main_queue.put({"type":"sync", "username":username})
    return render_template('player.html', user=user, title="BS: Player", int=int, json=json)



app.run("0.0.0.0", 3000, debug=True)