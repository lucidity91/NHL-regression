# Eric Mu
# CPSC 4660 Final Project
# File: initialize.py
# Purpose: Using extracted data from web, integrate into local database
from app import db, Player_Goalie, Player_Skater, SkaterStats, GoalieStats, Team
from extract import ExtractData
import timeit

# start program timer
start = timeit.default_timer()

db.create_all()

data = ExtractData()
teams = data.getTeams('https://www.hockey-reference.com/teams/')

record_count = 0

for team in teams:
    # create team table and add teams
    team_record = Team(team_name=team[0], division=team[1])
    db.session.add(team_record)
    
    players = data.getPlayers(team[2])
    # create skaters table and add skaters and their statistics
    for player in players[0]:
        stats = data.getStats(player, [2017, 2018, 2019])
        print('Adding data for player: ' + stats[0] + '...')
        skater_record = Player_Skater(full_name=stats[0], pos=stats[2], owner=team_record)
        db.session.add(skater_record)
        for season in stats[3]:
            skater_stats_record = SkaterStats(year=season[0], played=season[1], goals=season[2], assists=season[3], plus_minus=season[4], ppp=season[5], shp=season[6], gwg=season[7], blocks=season[8], owner=skater_record)
            db.session.add(skater_stats_record)
            record_count = record_count + 1
        record_count = record_count + 1

    # create goalies table and add skaters and their statistics
    for player in players[1]:
        stats = data.getStats(player, [2017, 2018, 2019])
        print('Adding data for player: ' + stats[0] + '...')
        goalie_record = Player_Goalie(full_name=stats[0], pos=stats[2], owner=team_record)
        db.session.add(goalie_record)
        for season in stats[3]:
            goalie_stats_record = GoalieStats(year=season[0], played=season[1], wins=season[2], losses=season[3], gaa=season[4], sv=season[5], shutouts=season[6], owner=goalie_record)
            db.session.add(goalie_stats_record)
            record_count = record_count + 1
        record_count = record_count + 1
    record_count = record_count + 1
    db.session.commit()

# stop timer
stop = timeit.default_timer()
time_taken = stop-start
print('Time taken:', time_taken)
print('Records created: ', record_count)
