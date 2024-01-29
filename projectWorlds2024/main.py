import requests
import re
import pandas as pd
import numpy as np 
from bs4 import BeautifulSoup
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC 

#2023 urls
lck2023url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202023/"
lck23results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202023/"
emea2023url = "https://gol.gg/tournament/tournament-ranking/EMEA%20Masters%20Summer%202023/"
emea2023results = "https://gol.gg/tournament/tournament-matchlist/EMEA%20Masters%20Summer%202023/"

#2022 urls
lck2022url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202022/"
lck22results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202022/"

#2021 urls
lck2021url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202021/"
lck21results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202021/"

#2020 urls
lck2020url = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202020/"
lck20results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202020/"

def getHtml(url):
    page = requests.get(url)
    html_page = BeautifulSoup(page.content, "html.parser")
    return html_page

def getTeamNames(html_page):
    nameSTR = re.compile(r'Hanwha Life eSports stats in LCK SPRING 2024')
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

def getWinners(html_page, lck2022):
    team_rows = html_page.find_all('tr')[1:]
    teams_stats = []
    for row in team_rows:
        data_cells = row.find_all('td', class_='text_victory')
        for data_cell in data_cells:
            stats = data_cell.text.strip()
            teams_stats.append(stats)

    
    winner = teams_stats[0]

    wins = [0 for i in range(len(getTeamNames(lck2022)))]
    for i in range (len(getTeamNames(lck2022))):
        if getTeamNames(lck2022)[i] == winner:
            wins[i] = 1

    return wins
    
def main():

    # training data
    # 2020 
    lck2020 = getHtml(lck2020url)
    lckResults20 = getHtml(lck20results)
    dataLCK20 = {'Team': getTeamNames(lck2020), 'WinRate': getTeamWinRate(lck2020), 'GDM': getTeamGDM(lck2020), 'Wins': getWinners(lckResults20, lck2020)}
    dfLCK20 = pd.DataFrame(dataLCK20)

    # 2021 
    lck2021 = getHtml(lck2021url)
    lckResults21 = getHtml(lck21results)
    dataLCK21 = {'Team': getTeamNames(lck2021), 'WinRate': getTeamWinRate(lck2021), 'GDM': getTeamGDM(lck2021), 'Wins': getWinners(lckResults21, lck2021)}
    dfLCK21 = pd.DataFrame(dataLCK21)

    # 2022 
    lck2022 = getHtml(lck2022url)
    lckResults22 = getHtml(lck22results)
    dataLCK22 = {'Team': getTeamNames(lck2022), 'WinRate': getTeamWinRate(lck2022), 'GDM': getTeamGDM(lck2022), 'Wins': getWinners(lckResults22, lck2022)}
    dfLCK22 = pd.DataFrame(dataLCK22)
    
    # concat dataFrames
    trainingDataFrame = pd.concat([dfLCK22, dfLCK21, dfLCK20])

    # x_train and y_train def
    x_train = trainingDataFrame.iloc[:, -3:-1].values
    y_train = trainingDataFrame.iloc[:, -1:].values
    y_train = y_train.ravel()

    # test data
    # 2023
    lck2023 = getHtml(lck2023url)
    lckResults23 = getHtml(lck23results)
    dataLCK23 = {'Team': getTeamNames(lck2023), 'WinRate': getTeamWinRate(lck2023), 'GDM': getTeamGDM(lck2023), 'Wins': getWinners(lckResults23, lck2023)}
    dfLCK23 = pd.DataFrame(dataLCK23)
    testingDataFrame = dfLCK23

    x_test = testingDataFrame.iloc[:, -3:-1].values
    y_test = testingDataFrame.iloc[:, -1:].values

    x_test_original = x_test.copy()

    # standarize xtrain and xtest so we can use them for inputs for training or evaluating
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    # train model
    classifier = SVC(kernel = 'linear', random_state=0)
    classifier.fit(x_train, y_train)

    # make the predictions
    y_pred = classifier.predict(x_test)
    predictions = y_pred.reshape(len(y_pred),1)
    predictions = predictions.ravel()

    # show results
    results = {'Team': getTeamNames(lck2023), 'WinRate': getTeamWinRate(lck2023), 'GDM': getTeamGDM(lck2023), 'Wins': getWinners(lckResults23, lck2023), 'WinsPred': predictions}
    results_df = pd.DataFrame(results)
    results_df['Check'] = np.where(results_df['WinsPred'] == results_df['Wins'], '✔', '✘')

    print(results_df)

main()