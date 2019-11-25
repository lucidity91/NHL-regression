from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from regression import NHLRegression

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost/nhlstats'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB definitions
class Player(db.Model):
    __abstract__ = True
    pid = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(25))
    team = db.Column(db.String(25))
    pos = db.Column(db.String(5))

class Player_Skater(Player):
    __tablename__ = 'skater'
    stats = db.relationship('SkaterStats', backref='owner')

class Player_Goalie(Player):
    __tablename__ = 'goalie'
    stats = db.relationship('GoalieStats', backref='owner')

class SkaterStats(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    played = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    ppp = db.Column(db.Integer)
    shp = db.Column(db.Integer)
    gwg = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    pid = db.Column(db.Integer, db.ForeignKey('skater.pid'))

class GoalieStats(db.Model):
    gid = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    gaa = db.Column(db.Float)
    sv = db.Column(db.Float)
    shutouts = db.Column(db.Integer)
    pid = db.Column(db.Integer, db.ForeignKey('goalie.pid'))

# Page definitions
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/regression")
def regression():
    return render_template("regression.html")

@app.route("/query", methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        skater = Player_Skater.query.filter_by(full_name=request.form['name']).first()
        goalie = Player_Goalie.query.filter_by(full_name=request.form['name']).first()
        if skater:
            regress = NHLRegression(skater)
            predictions = regress.run(2020)
            return render_template("show_query.html", player=skater, predictions=predictions)
        if goalie:
            regress = NHLRegression(goalie)
            predictions = regress.run(2020)
            return render_template("show_query.html", player=goalie, predictions=predictions)
    return render_template("query.html")

if __name__ == "__main__":
    app.run(debug=True)
