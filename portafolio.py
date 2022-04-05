from criptomoneda import Criptomoneda


class Portafolio:
    __slots__ = ["totalInvested", "criptos"]

    def __init__(self, totalInvested):
        self.criptos = {}
        self.totalInvested = float(totalInvested)

    def add(self, cripto):
        criptoAux = Criptomoneda(cripto)
        self.criptos[criptoAux.getName()] = {'price' : float(criptoAux.getPrice()),
                                             'amount' : float(self.totalInvested)/criptoAux.getPrice(),
                                             'percent1h' : float(criptoAux.getPercentChange1h()),
                                             'percent24h' : float(criptoAux.getPercentChange24h()),
                                             'percent7d' : float(criptoAux.getPercentChange7d()),
                                             'percent30d' : float(criptoAux.getPercentChange30d())
                                             }

    def incrementInvested(self, amount):
        self.totalInvested += float(amount)
        for x in self.criptos:
            self.criptos[x]['amount'] = float(self.totalInvested/self.criptos[x]['price'])

    def getPortafolio(self):
        return self.criptos

    def getTotalInvested(self):
        return self.totalInvested

    def __str__(self):
        return str(self.criptos) + " " + str(self.totalInvested)
