import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class ExtractData(object):
    def getTeams(self, link):
        url = requests.get(link)
        parsed_uri = urlparse(link)
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        self.soup = BeautifulSoup(url.text, 'html.parser')

        teams = []
        menu = self.soup.find('div', {'id': 'site_menu'})
        divisions = menu.find_all('div', {'class': 'division'})

        for division in divisions:
            urls = division.find_all('a', href=True)
            for url in urls:
                full_url = urljoin(self.base, url.get('href'))
                teams.append([url.text,full_url])

        return teams

    def getPlayers(self, link):
        url = requests.get(link)
        parsed_uri = urlparse(link)
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        self.soup = BeautifulSoup(url.text, 'html.parser')

        skaters = []
        goalies = []
        team_stats_table = self.soup.find('table', {'id': 'team_stats'})
        team_stats = team_stats_table.find_all('tr')
        team_name = team_stats[1].find('th', {'data-stat':'team_name'}).text

        all_skaters = self.soup.find('div', {'id': 'all_skaters'})
        player_table = all_skaters.find('tbody')
        players = player_table.find_all('tr')
        for player in players:
            name = player.find('a', href=True).text
            full_url = urljoin(self.base, player.find('a', href=True).get('href'))
            pos = player.find('td', {'data-stat':'pos'}).text
            if pos == 'G':
                goalies.append([name,team_name, pos, full_url])
            else:
                skaters.append([name,team_name, pos, full_url])

        return [skaters, goalies]
    
    def getStats(self, player, years):
        url = requests.get(player[3])
        parsed_uri = urlparse(player[3])
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        self.soup = BeautifulSoup(url.text, 'html.parser') 

        name = self.soup.find('h1', {'itemprop': 'name'}).text
        team = player[1]
        pos = player[2]
        stats = []

        stats_table = self.soup.find('table', {'id': 'stats_basic_plus_nhl'}) 
        for year in years:
            season_stats = stats_table.find_all('tr', {'id': 'stats_basic_plus_nhl.'+str(year)})
            for season in season_stats:
                if (pos == 'G'):
                    played = season.find('td', {'data-stat': 'games_goalie'}).text
                    wins = season.find('td', {'data-stat': 'wins_goalie'}).text
                    losses = season.find('td', {'data-stat': 'losses_goalie'}).text
                    gaa = season.find('td', {'data-stat': 'goals_against_avg'}).text
                    sv = season.find('td', {'data-stat': 'save_pct'}).text
                    shutouts = season.find('td', {'data-stat': 'shutouts'}).text
                    stats.append([year, played, wins, losses, gaa, sv, shutouts])
                else:
                    played = season.find('td', {'data-stat': 'games_played'}).text
                    goals = season.find('td', {'data-stat': 'goals'}).text
                    assists = season.find('td', {'data-stat': 'assists'}).text
                    plus_minus = season.find('td', {'data-stat': 'plus_minus'}).text
                    ppp = int(season.find('td', {'data-stat': 'goals_pp'}).text)+int(season.find('td', {'data-stat': 'assists_pp'}).text) 
                    shp = int(season.find('td', {'data-stat': 'goals_sh'}).text)+int(season.find('td', {'data-stat': 'assists_sh'}).text) 
                    gwg = int(season.find('td', {'data-stat': 'goals_gw'}).text)
                    blocks = season.find('td', {'data-stat': 'blocks'}).text
                    stats.append([year, played, goals, assists, plus_minus, ppp, shp, gwg, blocks])

        return [name, team, pos, stats]
