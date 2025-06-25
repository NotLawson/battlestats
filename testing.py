from flask import render_template, Flask

app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html", title="Title")

app.run(port=5000)

stats = {
    'myLeagueProgress': {
        'trophies': 0,
        'highestTrophies': 0, 
        'diamonds': 0
    }, 
    'me': {
        'stats': {
            'wins': 760,
            'losses': 575
        }, 
        'currencies': {
            'gold': 34657, 
            'gems': 92, 
            'research_points': 255
        }
    }
}