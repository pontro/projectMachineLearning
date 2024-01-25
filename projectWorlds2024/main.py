import requests

from bs4 import BeautifulSoup

url_lck = "https://gol.gg/tournament/tournament-stats/LCK%20Spring%202024/"

def getHtml(url):
    page = requests.get(url)
    html_page = BeautifulSoup(page.content, "html.parser")
    return html_page



def main():
    html_page = getHtml(url_lck)
    print(html_page)


main()