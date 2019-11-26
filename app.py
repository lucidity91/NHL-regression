# Eric Mu
# CPSC 4660 Final Project
# File: app.py
# Purpose: main file for driving web app, contains DB and Page definitions
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from regression import NHLRegression

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost/nhlstats'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB definitions
class Team(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(25))
    division = db.Column(db.String(25))
    skaters = db.relationship('Player_Skater', backref='owner')
    goalies = db.relationship('Player_Goalie', backref='owner')

class Player(db.Model):
    __abstract__ = True
    pid = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(25))
    pos = db.Column(db.String(5))

class Player_Skater(Player):
    __tablename__ = 'skater'
    stats = db.relationship('SkaterStats', backref='owner')
    tid = db.Column(db.Integer, db.ForeignKey('team.tid'))

class Player_Goalie(Player):
    __tablename__ = 'goalie'
    stats = db.relationship('GoalieStats', backref='owner')
    tid = db.Column(db.Integer, db.ForeignKey('team.tid'))

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
# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Page for regression analysis and player comparisons
@app.route("/regression", methods=['GET', 'POST'])
def regression():
    skaters = Player_Skater.query.all()
    goalies = Player_Goalie.query.all()

    # On form submit, do comparison
    if request.method == 'POST':
        skater1 = Player_Skater.query.filter_by(full_name=request.form['name1']).first()
        goalie1 = Player_Goalie.query.filter_by(full_name=request.form['name1']).first()
        skater2 = Player_Skater.query.filter_by(full_name=request.form['name2']).first()
        goalie2 = Player_Goalie.query.filter_by(full_name=request.form['name2']).first()
        if skater1:
            regress = NHLRegression(skater1)
            predictions1 = regress.run(2020)
            if skater2:
                regress2 = NHLRegression(skater2)
                predictions2 = regress2.run(2020)
                diff = []
                for i in range(1,len(predictions1)):
                    diff.append(round(predictions1[i]-predictions2[i],2))
                return render_template("show_regression.html", player1=skater1, player2=skater2, predictions1=predictions1, predictions2=predictions2, diff=diff)
            if goalie2:
                regress2 = NHLRegression(goalie2)
                predictions2 = regress2.run(2020)
                return render_template("show_regression.html", player1=skater1, player2=goalie2, predictions1=predictions1, predictions2=predictions2)
        if goalie1:
            regress = NHLRegression(goalie1)
            predictions1 = regress.run(2020)
            if skater2:
                regress2 = NHLRegression(skater2)
                predictions2 = regress2.run(2020)
                return render_template("show_regression.html", player1=goalie1, player2=skater2, predictions1=predictions1, predictions2=predictions2)
            if goalie2:
                regress2 = NHLRegression(goalie2)
                predictions2 = regress2.run(2020)
                diff = []
                for i in range(1,len(predictions1)):
                    diff.append(round(predictions1[i]-predictions2[i],3))
                return render_template("show_regression.html", player1=goalie1, player2=goalie2, predictions1=predictions1, predictions2=predictions2, diff=diff)
    return render_template("regression.html", skaters=skaters, goalies=goalies)

# Page for referencing players by team
@app.route("/view", methods=['GET', 'POST'])
def view():
    teams = Team.query.all()
    if request.method == 'POST':
        team_selected = Team.query.filter_by(team_name=request.form['team']).first()
        return render_template("show_team.html", skaters=team_selected.skaters, goalies=team_selected.goalies)
    return render_template("view.html", teams=teams)

if __name__ == "__main__":
    app.run(debug=True)
