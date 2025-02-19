from flask import Flask, render_template, request, redirect
import db as db_lib
import redis

app = Flask(__name__)
#leaguedb = db_lib.League()
userdb = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


# Import submodules in order
from modules import battletabs
from modules import auth
#from modules import player, battles

@app.route('/')
def index():
    username = auth.auth(request.cookies.get('token'))
    return render_template('index.html', username=username)

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
            return redirect('/', 302).set_cookie('token', token)
        return render_template('login.html', message=message)
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authtoken = request.form['authtoken']
        if userdb.get(username)!=None:
            message = "Username already exists"
        else:
            #try:
                userdb.set(username, auth.User(username, password, authtoken))
                token = auth.login(username, password)
            #except Exception as e:
            #    print(e)
            #    return render_template('signup.html', message="Invalid BattleTabs token")
            
            return redirect('/', 302).set_cookie('token', token)
        return render_template('signup.html', message=message)
    return render_template('signup.html')


app.run("0.0.0.0", 3000, debug=True)