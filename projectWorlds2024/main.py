import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import pandas as pd
 
url_lck = "https://gol.gg/tournament/tournament-ranking/LCK%20Spring%202023/"

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
        data_cells = row.find_all('td', class_='text-cenoter')
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
    

def main():
    html_page = getHtml(url_lck)
    data = {'Team': getTeamNames(html_page), 'WinRate': getTeamWinRate(html_page)}
    dataset = pd.DataFrame(data)
    x = dataset.iloc[:, -2:]
    print(x)
    
main()