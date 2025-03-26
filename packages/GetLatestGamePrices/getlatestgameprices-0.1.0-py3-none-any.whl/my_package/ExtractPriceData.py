import requests
from bs4 import BeautifulSoup
import re

def GetGamePrices(game):
    game = game.lower().replace(' ', '-').replace(':', '').replace('.', '')
    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                    'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                    'Chrome/90.0.4430.93 Safari/537.36'
                } 
        response = requests.get(f'https://gg.deals/game/{game}/',headers)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            Prices = soup.find('div', class_='d-flex header-game-prices-content active')
            if Prices:
                Official_And_Keyshop_Prices = ExtractPrices(Prices.text)
                if Official_And_Keyshop_Prices == {"official stores": None, "keyshops": None}:
                    return 'Free'
                return Official_And_Keyshop_Prices
            else:
                print("Error Occured while getting the prices")
        else:
            print("Failed to get a response. Status code:", response.status_code)
    except Exception as e:
        print("Something went wrong:", e)
    
def ExtractPrices(data):
    pattern_standard = r"(official[-\s]*stores|keyshops)[-:\s]*[~]?\$(\d+\.\d+)"
    matches = re.findall(pattern_standard, data, flags=re.IGNORECASE)
    prices = {"official stores": None, "keyshops": None}
    for label, price in matches:
        if "official" in label.lower():
            prices["official stores"] = price
        elif "keyshops" in label.lower():
            prices["keyshops"] = price
    
    return prices
