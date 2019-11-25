from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class NHLRegression(object):
    def __init__(self, player):
        self.pos = player.pos 
        year = []
        played = []
        if self.pos == 'G':
            wins = []
            losses = []
            gaa = []
            sv = []
            shutouts = []

            for season in player.stats:
                year.append(season.year)
                played.append(season.played)
                wins.append(season.wins)
                losses.append(season.losses)
                gaa.append(season.gaa)
                sv.append(season.sv)
                shutouts.append(season.shutouts)

            predictors = {'Year': year,
                          'Played': played,
                          'Wins': wins,
                          'Losses': losses,
                          'GAA': gaa,
                          'SV': sv,
                          'Shutouts': shutouts,
                         }
            self.df = pd.DataFrame(predictors,columns=['Year', 'Played','Wins','Losses','GAA','SV','Shutouts'])
        else:
            goals = []
            assists = []
            points = []
            plus_minus = []
            ppp = []
            shp = []
            gwg = []
            blocks = []

            for season in player.stats:
                year.append(season.year)
                played.append(season.played)
                goals.append(season.goals)
                assists.append(season.assists)
                points.append(season.goals+season.assists)
                plus_minus.append(season.plus_minus)
                ppp.append(season.ppp)
                shp.append(season.shp)
                gwg.append(season.gwg)
                blocks.append(season.blocks)

            predictors = {'Year': year,
                          'Played': played,
                          'Goals': goals,
                          'Assists': assists,
                          'Points': points,
                          '+/-': plus_minus,
                          'PPP': ppp,
                          'SHP': shp,
                          'GWG': gwg,
                          'Blocks': blocks,
                        }
            self.df = pd.DataFrame(predictors,columns=['Year', 'Played','Goals','Assists', 'Points','+/-','PPP','SHP','GWG','Blocks'])

    def print_stats(self):
        print(self.df)

    def run(self, year):
        X = self.df[['Year']]
        predicted_stats = []
        predicted_stats.append(year)
        if self.pos == 'G':
            for var in ['Played','Wins','Losses','GAA','SV','Shutouts']:
                Y = self.df[var]
                regression = linear_model.LinearRegression()
                regression.fit(X,Y)
                predicted_stats.append(round(regression.predict([[year]])[0],3))
        else:
            for var in ['Played','Goals','Assists', 'Points','+/-','PPP','SHP','GWG','Blocks']:
                Y = self.df[var]
                regression = linear_model.LinearRegression()
                regression.fit(X,Y)
                predicted_stats.append(round(regression.predict([[year]])[0],2))
        
        return predicted_stats
