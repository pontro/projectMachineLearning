import requests
import re
from bs4 import BeautifulSoup

import pandas as pd
 
lck2023url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202023/"
lck2022url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202022/"
lck2021url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202021/"
lck22results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202022/"

def getHtml(url):
    page = requests.get(url)
    html_page = BeautifulSoup(page.content, "html.parser")
    return html_page

def getTeamNames(html_page):
    teams = html_page.find_all('a', title = re.compile("stats in LCK"))
    names = []
    for element in teams:
        names.append(element.string)
    return names

def getTeamWinRate(html_page):
    winRate=html_page.find_all('div', class_= "col-auto pl-1 position-absolute")
    wr = []
    for element in winRate:
        wr.append(element.string)
    for i in range(len(wr)):
        wr[i] = int (wr[i].strip("%"))
    return wr

def getTeamGDM(html_page):
    team_rows = html_page.find_all('tr')[1:]
    teams_stats = []
    for row in team_rows:
        data_cells = row.find_all('td', class_='text-center')
        for data_cell in data_cells:
            stats = data_cell.text.strip()
            teams_stats.append(stats)

    teams_GDM = []
    counter = 0
    for team_stat in teams_stats:
        counter += 1
        if counter % 5 == 0:
            teams_GDM.append(team_stat)
            counter = 0


    for i in range(len(teams_GDM)):
         teams_GDM[i] = int (teams_GDM[i])
    return teams_GDM

def getWinners(html_page):
    team_rows = html_page.find_all('tr')[1:]
    teams_stats = []
    for row in team_rows:
        data_cells = row.find_all('td', class_='text_victory')
        for data_cell in data_cells:
            stats = data_cell.text.strip()
            teams_stats.append(stats)

    print("Teams Stats:", teams_stats)

    teams_Winner = []
    counter = 0
    for team_stat in teams_stats:
        counter += 1
        if counter % 2 == 0:
            teams_Winner.append(team_stat)
            counter = 0 

    print("Teams Winners:", teams_Winner)


def main():
    #training data
    

    lck2022 = getHtml(lck2022url)
    lck22 = getHtml(lck22results)
    dataLCK22 = {'Team': getTeamNames(lck2022), 'WinRate': getTeamWinRate(lck2022), 'GDM': getTeamGDM(lck2022)}
    dfLCK22 = pd.DataFrame(dataLCK22)
    
    winner = getWinners(lck22)
    dfLCK22['Winners'] = winner


    trainingData = dfLCK22.iloc[:, -3:].values
    


    #test data
    lck2023 = getHtml(lck2023url)
    dataLCK23 = {'Team': getTeamNames(lck2023), 'WinRate': getTeamWinRate(lck2023), 'GDM': getTeamGDM(lck2023)}
    dfLCK23 = pd.DataFrame(dataLCK23)
    
    testData = dfLCK23.iloc[:, -2:].values

    teamNames = pd.concat([dfLCK22, dfLCK23])
    
    print(teamNames)

main()

