from criptomoneda import Criptomoneda


class Portafolio:
    __slots__ = ["totalInvested", "criptos"]
     # Constructor
    def __init__(self, totalInvested):
        self.criptos = {}
        self.totalInvested = float(totalInvested)

    # Método para añadir una criptomoneda al portafolio
    def add(self, cripto):
        criptoAux = Criptomoneda(cripto)
        self.criptos[criptoAux.getName()] = {'price' : float(criptoAux.getPrice()),
                                             'amount' : float(self.totalInvested)/criptoAux.getPrice(),
                                             'percent1h' : float(criptoAux.getPercentChange1h()),
                                             'percent24h' : float(criptoAux.getPercentChange24h()),
                                             'percent7d' : float(criptoAux.getPercentChange7d()),
                                             'percent30d' : float(criptoAux.getPercentChange30d())
                                             }

    # Método para aumentar la cantidad de inversión en el portafolio
    def incrementInvested(self, amount):
        self.totalInvested += float(amount)
        for x in self.criptos:
            self.criptos[x]['amount'] = float(self.totalInvested/self.criptos[x]['price'])

    # Método que devuelve todas las criptomonedas que están en el portafolio
    def getPortafolio(self):
        return self.criptos

    # Método que devuelve el total de inversión en el portafolio
    def getTotalInvested(self):
        return self.totalInvested

