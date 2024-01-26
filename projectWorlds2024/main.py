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

    for element in teams:
        print(element.string)

    return teams

def main():
    html_page = getHtml(url_lck)
    getTeamNames(html_page)
   


main()