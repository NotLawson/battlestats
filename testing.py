from flask import render_template, Flask

app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html", title="Title")

app.run(port=5000)