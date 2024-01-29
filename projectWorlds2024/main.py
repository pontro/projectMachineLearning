import requests, re, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC 

url_lck = "https://gol.gg/tournament/tournament-ranking/LCK%20Spring%202024/"
#2023 urls
url_lck_2023_ranking = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202023/"
url_lck_2023_results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202023/"

#2022 urls
url_lck_2022_ranking = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202022/"
url_lck_2022_results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202022/"

#2021 urls
url_lck_2021_ranking = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202021/"
url_lck_2021_results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202021/"

#2020 urls
url_lck_2020_ranking = "https://gol.gg/tournament/tournament-ranking/LCK%20Summer%20Playoffs%202020/"
url_lck_2020_results = "https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%20Playoffs%202020/"

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

def get_Team_Data(url_ranking, url_results):
    html_ranking = getHtml(url_ranking)
    html_results = getHtml(url_results)
    team_Data = {'Team': getTeamNames(html_ranking), 'WinRate': getTeamWinRate(html_ranking), 'GDM': getTeamGDM(html_ranking), 'Wins': getWinners(html_results, html_ranking)}
    return team_Data

def main():

    # training data
    # 2020 
    data_lck_2020 = get_Team_Data(url_lck_2020_ranking, url_lck_2020_results)
    df_lck_2020 = pd.DataFrame(data_lck_2020)

    # 2021 
    data_lck_2021 = get_Team_Data(url_lck_2021_ranking, url_lck_2021_results)
    df_lck_2021 = pd.DataFrame(data_lck_2021)

    # 2022 
    data_lck_2022 = get_Team_Data(url_lck_2022_ranking, url_lck_2022_results)
    df_lck_2022 = pd.DataFrame(data_lck_2022)
    
    # concat training dataFrames
    trainingDataFrame = pd.concat([df_lck_2022, df_lck_2021, df_lck_2020])

    # x_train and y_train def
    x_train = trainingDataFrame.iloc[:, -3:-1].values
    y_train = trainingDataFrame.iloc[:, -1:].values
    y_train = y_train.ravel()

    #test data
    #2023
    lck2023 = getHtml(lck2023url)
    lckResults23 = getHtml(lck23results)
    dataLCK23 = {'Team': getTeamNames(lck2023), 'WinRate': getTeamWinRate(lck2023), 'GDM': getTeamGDM(lck2023), 'Wins': getWinners(lckResults23, lck2023)}
    dfLCK23 = pd.DataFrame(dataLCK23)
    testingDataFrame = dfLCK23

    x_test = testingDataFrame.iloc[:, -3:-1].values
    y_test = testingDataFrame.iloc[:, -1:].values

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

    tests = y_test.reshape(len(y_test), 1)

    print(predictions)

    #results = {'Team': getTeamNames(lck2023), 'WinRate': getTeamWinRate(lck2023), 'GDM': getTeamGDM(lck2023), 'Wins': getWinners(lckResults23, lck2023), 'Wins Pred': predictions}
    #results = pd.DataFrame(results)



main()