

from requests import Session
import json


class Criptomoneda:
    __slots__ = ("name", "price", "fullName", "market_cap", "percentChange1h", "percentChange24h", "percentChange7d",
                 "percentChange30d")

    def __init__(self, name):
        self.name = name.upper()
        self.price = self.setPrice()
        self.fullName = self.setFullName()
        self.market_cap = self.setMarket_Cap()
        self.percentChange1h = self.setPercentChange1h()
        self.percentChange24h = self.setPercentChange24h()
        self.percentChange7d = self.setPercentChange7d()
        self.percentChange30d = self.setPercentChange30d()

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getFullName(self):
        return self.fullName

    def getMarketCap(self):
        return self.market_cap

    def getPercentChange1h(self):
        return self.percentChange1h

    def getPercentChange24h(self):
        return self.percentChange24h

    def getPercentChange7d(self):
        return self.percentChange7d

    def getPercentChange30d(self):
        return self.percentChange30d

    def setFullName(self):
        return self.loadJson()['data'][self.name]['name']

    def setPrice(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['price']

    def setMarket_Cap(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['market_cap']

    def setPercentChange1h(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['percent_change_1h']

    def setPercentChange24h(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['percent_change_24h']

    def setPercentChange7d(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['percent_change_7d']

    def setPercentChange30d(self):
        return self.loadJson()['data'][self.name]['quote']['USD']['percent_change_30d']

    def loadJson(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # Coinmarketcap API url
        parameters = {'symbol': self.name,
                      'convert': 'USD'}  # API parameters to pass in for retrieving specific cryptocurrency data
        with open("api.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': jsonObject['CMC_API']
        }  # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        info = json.loads(response.text)
        return info

    def setName(self, name):
        self.name = name

    def __str__(self):
        return self.name + " " + str(self.price)
