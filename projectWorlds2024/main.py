import requests
import re
from bs4 import BeautifulSoup
 
url_lck = "https://gol.gg/tournament/tournament-ranking/LCK%20Spring%202024/"

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
    return wr

def joinWinRateName(arr1, arr2, html_page):

   print(2)
    

def main():
    html_page = getHtml(url_lck)
    joinWinRateName(getTeamNames(html_page), getTeamWinRate(html_page), html_page)


main()