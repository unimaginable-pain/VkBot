import requests
import json

def getglovecasecost():
    return json.loads(requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=5&market_hash_name=Glove%20Case").text)["lowest_price"]
