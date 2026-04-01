import requests
from bs4 import BeautifulSoup
import urllib.parse

my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

    
def get_winrate(name, tag):
    # Keeping your existing general winrate function
    encoded_name = urllib.parse.quote_plus(name)
    encoded_tag = urllib.parse.quote(tag)
    url_string = f"https://www.leagueofgraphs.com/summoner/br/{encoded_name}-{encoded_tag}"
    
    try:
        r = requests.get(url_string, headers=my_headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        wins = int(soup.find(class_="winsNumber").text)
        losses = int(soup.find(class_="lossesNumber").text)
        winRate = round((wins / (wins + losses)) * 100, 2)
        return encoded_name, encoded_tag, winRate
    except:
        return encoded_name, encoded_tag, "0"
