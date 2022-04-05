import json

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from criptomoneda import Criptomoneda
from portafolio import Portafolio


# API Key

class Bot:
    __slots__ = "portafolios"

    def __init__(self):

        with open("api.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            updater = Updater(jsonObject['Telegram_API'])
            jsonFile.close()

        self.portafolios = {}
        self.listeners(updater)
        updater.start_polling()
        updater.idle()

    def listeners(self, updater):
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('cripto', self.cripto))
        updater.dispatcher.add_handler(CommandHandler('portafolio', self.comandoPortafolio))

    # Comando start
    def start(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        update.message.reply_text(
            'Bienvenido {} \nPara buscar alguna criptomoneda en especifico tienes que colocar /cripto <SIGLA CRIPTO>'.format(
                user['username']))

    # Comando cripto
    def cripto(self, update: Update, context: CallbackContext) -> None:
        try:
            cripto = Criptomoneda(context.args.pop())
            update.message.reply_text(f'Nombre de la criptomoneda: {cripto.getFullName()} '
                                      f'\nPrecio actual: {(round(cripto.getPrice(), 4)):,.2f} USD'
                                      f'\nMarket Cap: {cripto.getMarketCap():,.2f} USD'
                                      f'\nCambio en la última hora: {cripto.getPercentChange1h()} %'
                                      f'\nCambio en el último dia: {cripto.getPercentChange24h()} %'
                                      f'\nCambio en la última semana: {cripto.getPercentChange7d()} %'
                                      f'\nCambio en el último mes: {cripto.getPercentChange30d()} %')
        except IndexError:
            update.message.reply_text('Debes escribir las siglas de la criptomoneda de la que quieras saber')
        except KeyError:
            update.message.reply_text('No existe esa cripto')

    def comandoPortafolio(self, update: Update, context: CallbackContext):
        try:
            if context.args[0] == 'create':
                self.createPortafolio(context, update)
            elif context.args[0] == 'addInvest':
                self.addInvest(context, update)
            elif context.args[0] == 'addCripto':
                self.addCripto(context, update)
            elif context.args[0] == 'show':
                self.showPortafolio(update)
        except AttributeError:
            update.message.reply_text('Primero debes crear el portafolio: /portafolio create <amount>')
        except IndexError:
            update.message.reply_text('El uso correcto del comando es /portafolio <create|addInvest> <amount>')
        # except KeyError:
          #  update.message.reply_text('La criptomoneda que has pasado no existe')

    def showPortafolio(self, update):
        msg = ""
        gainLoss1h = 0
        gainLoss24h = 0
        gainLoss7d = 0
        gainLoss30d = 0
        user = self.portafolios[update.message.from_user['username']]
        for x in user.getPortafolio():
            userPortafolio = user.getPortafolio()
            msg += x + " : " + str(userPortafolio[x]['price']) + '\n'
            gainLoss1h += userPortafolio[x]['price'] * userPortafolio[x]['amount'] - ((userPortafolio[x]['price'] - (userPortafolio[x]['percent1h'] / 100 * userPortafolio[x]['price'])) * userPortafolio[x]['amount'])
            gainLoss24h += userPortafolio[x]['price'] * userPortafolio[x]['amount'] - ((userPortafolio[x]['price'] - (userPortafolio[x]['percent24h'] / 100 * userPortafolio[x]['price'])) * userPortafolio[x]['amount'])
            gainLoss7d += userPortafolio[x]['price'] * userPortafolio[x]['amount'] - ((userPortafolio[x]['price'] - (userPortafolio[x]['percent7d'] / 100 * userPortafolio[x]['price'])) * userPortafolio[x]['amount'])
            gainLoss30d += userPortafolio[x]['price'] * userPortafolio[x]['amount'] - ((userPortafolio[x]['price'] - (userPortafolio[x]['percent30d'] / 100 * userPortafolio[x]['price'])) * userPortafolio[x]['amount'])
        msg += 'Total invertido : ' + str(
            user.getTotalInvested()) + '\nTotal ganado/perdido respecto la última hora : ' + str(
            gainLoss1h) + '\nTotal ganado/perdido respecto las últimas 24 horas : ' + str(
            gainLoss24h) + '\nTotal ganado/perdido respecto los últimos 7 dias : ' + str(
            gainLoss7d) + '\nTotal ganado/perdido respecto los últimos 30 dias : ' + str(gainLoss30d)
        update.message.reply_text(msg)

    def createPortafolio(self, context, update):
        invested = context.args[1]
        self.portafolios[update.message.from_user['username']] = Portafolio(invested)
        update.message.reply_text('Funciona')

    def addInvest(self, context, update):
        self.portafolios[update.message.from_user['username']].incrementInvested(context.args[1])
        update.message.reply_text('Funciona')

    def addCripto(self, context, update):
        self.portafolios[update.message.from_user['username']].add(context.args[1])
        update.message.reply_text('Funciona')


a = Bot()
