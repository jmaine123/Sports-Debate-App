
import requests
import sqlite3
from bs4 import BeautifulSoup
import csv

# g = input("Enter first letter of last name : ")

def scrapePlayers():
    global players
    players=[]  # a list to store players
    for i in range(ord('a'), ord('z')+1):
        # print (chr(i))

        URL = 'https://www.basketball-reference.com/players/%s/'%(chr(i))
        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'html.parser')

        table = soup.find('tbody')

        for row in table.findAll('tr'):
            player = {}
            player['Name'] = row.th.a.text
            player['Position'] = row.find('td', {'data-stat':'pos'}).text
            player['Height'] = row.find('td', {'data-stat':'height'}).text
            player['Birth Date'] = row.find('td', {'data-stat':'birth_date'}).text
            player['College'] = row.find('td', {'data-stat':'colleges'}).text
            player['Player_id'] = row.th['data-append-csv']
            player['Url'] = row.th.a['href']
            player['Year_Start'] = row.find('td', {'data-stat':'year_min'}).text
            player['Year_End'] = row.find('td', {'data-stat':'year_max'}).text
            players.append(player)

    # for player in players:
    #     print(player['Name'])

def dailygames():
    global games
    games = []
    URL = 'https://www.basketball-reference.com/boxscores/?month=10&day=26&year=2019'
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('div',{'class':'game_summaries'})
    for row in table.findAll('div'):
        game = {}
        game['topScorer'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[1].a.text
        game['topScorerPoints'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[2].text
        for trow in row.findAll('table', {'class':'teams'}):
            game['loser'] = trow.tbody.find('tr', {'class', 'loser'}).td.a.text
            game['loserScore'] = trow.tbody.find('tr', {'class', 'loser'}).find('td',{'class':'right'}).text
            game['winner'] = trow.tbody.find('tr', {'class', 'winner'}).td.a.text
            game['winnerScore'] = trow.tbody.find('tr', {'class', 'winner'}).find('td',{'class':'right'}).text
            games.append(game)
    # print (games)


# for x in quotes:
#     print (x['lines'])

###for scraping into a csv####
# filename = 'nba.csv'
# with open(filename, 'w') as f:
#     w = csv.DictWriter(f,['Name','Position','Height','Birth Date','College','ID','Url'])
#     w.writeheader()
#     for player in players:
#         w.writerow(player)
######


# def first_overall_draft():
#     global draft_players
#     draft_players = []
#     URL = 'https://www.basketball-reference.com/draft'
#     r = requests.get(URL)
#
#     soup = BeautifulSoup(r.content, 'html.parser')
#
#     table = soup.find('tbody')
#
#     for row in table.findAll('tr'):
#         first_draft = {}
#         first_draft['Year'] = row.find('th',{'data-stat','year_id'}).text,
#         first_draft['League'] = row.find('td',{'data-stat','lg_id'}).text,
#         first_draft['TeamName'] = row.find('td',{'data-stat','team_name'}).text,
#         first_draft['Player'] = row.find('td',{'data-stat','player'}).text,
#         first_draft['College'] = row.find('td',{'data-stat','college_name'}).text,
#         first_draft['URL'] = row.find('td',{'data-stat','player'}).,





####creating table#####


conn = sqlite3.connect('nbastats.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS playersInfo(ID INTEGER PRIMARY KEY AUTOINCREMENT, Player_id TEXT, Name TEXT, Position TEXT, Height REAL, Birthdate TEXT, College TEXT, Url TEXT)')

def create_boxscore():
    c.execute('CREATE TABLE IF NOT EXISTS boxScore(Loser TEXT, LoserScore INT, Winner TEXT, WinnerScore INT, TopScorer TEXT, TopScorerPoints INT)')

def top_draft_table():
    c.execute('CREATE TABLE IF NOT EXISTS topDraftTable(Loser TEXT, LoserScore INT, Winner TEXT, WinnerScore INT, TopScorer TEXT, TopScorerPoints INT)')

def boxscore_entry():
    for game in games:
        c.execute("INSERT INTO boxScore(Loser, LoserScore, Winner, WinnerScore, TopScorer, TopScorerPoints) VALUES (?, ?, ?, ?, ?, ?) ",
            (game['loser'], game['loserScore'], game['winner'], game['winnerScore'], game['topScorer'], game['topScorerPoints']))
        conn.commit()

def data_entry():
    for player in players:
        c.execute("INSERT INTO playersInfo(ID, Player_id, Name, Position, Height, Birthdate, College, Url) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?) ",
            (player['Player_id'], player['Name'], player['Position'], player['Height'], player['Birth Date'], player['College'], player['Url']))
        conn.commit()




dailygames()
create_boxscore()
boxscore_entry()
scrapePlayers()
create_table()
data_entry()
c.close()
conn.close()
