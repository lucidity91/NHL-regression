from app import db, Player_Goalie, Player_Skater, SkaterStats, GoalieStats
from extract import ExtractData
import timeit

# name, team, pos
# year, played, goals, assists, plus_minus, ppp, shp, gwg

# start program timer
start = timeit.default_timer()

db.create_all()

data = ExtractData()
teams = data.getTeams('https://www.hockey-reference.com/teams/')

record_count = 0

for team in teams:
    players = data.getPlayers(team[1])
    # skaters
    for player in players[0]:
        stats = data.getStats(player, [2017, 2018, 2019])
        print('Adding data for player: ' + stats[0] + '...')
        skater_record = Player_Skater(full_name=stats[0], team=stats[1], pos=stats[2])
        db.session.add(skater_record)
        for season in stats[3]:
            skater_stats_record = SkaterStats(year=season[0], played=season[1], goals=season[2], assists=season[3], plus_minus=season[4], ppp=season[5], shp=season[6], gwg=season[7], blocks=season[8], owner=skater_record)
            db.session.add(skater_stats_record)
            record_count = record_count + 1
        record_count = record_count + 1

    # goalies
    for player in players[1]:
        stats = data.getStats(player, [2017, 2018, 2019])
        print('Adding data for player: ' + stats[0] + '...')
        goalie_record = Player_Goalie(full_name=stats[0], team=stats[1], pos=stats[2])
        db.session.add(goalie_record)
        for season in stats[3]:
            goalie_stats_record = GoalieStats(year=season[0], played=season[1], wins=season[2], losses=season[3], gaa=season[4], sv=season[5], shutouts=season[6], owner=goalie_record)
            db.session.add(goalie_stats_record)
            record_count = record_count + 1
        record_count = record_count + 1

    db.session.commit()

# stop timer
stop = timeit.default_timer()
time_taken = stop-start
print('Time taken:', time_taken)
print('Records created: ', record_count)
