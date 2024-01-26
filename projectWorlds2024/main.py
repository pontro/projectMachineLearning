import requests
import re
from bs4 import BeautifulSoup
 
url_lck = "https://gol.gg/tournament/tournament-ranking/LCK%20Spring%202024/"

def getHtml(url):
    page = requests.get(url)
    html_page = BeautifulSoup(page.content, "html.parser")
    return html_page

def getTeamNames(html_page):
    nameSTR = re.compile(r'Hanwha Life eSports stats in LCK SPRING 2024')
    print (html_page.find_all('td', class_= "footable-visible footable-first-column"))

def main():
    html_page = getHtml(url_lck)
    getTeamNames(html_page)
   


main()