from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from datetime import datetime
import requests
import re

def getLastUpdate():
    data = []
    contents = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TENGAH.json').json()
    last_update = datetime.strptime(contents['last_date'], "%Y-%m-%d")
    converted = last_update.strftime("%d-%m-%Y")
    data.append(converted)
    case = str(contents['list_perkembangan'][-1]['KASUS'])
    dead = str(contents['list_perkembangan'][-1]['MENINGGAL'])
    cured = str(contents['list_perkembangan'][-1]['SEMBUH'])
    inTreatment = str(contents['list_perkembangan'][-1]['DIRAWAT_OR_ISOLASI'])
    data.extend((case, dead, cured, inTreatment))
    return data

def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Halo! Masukkan perintah /terbaru untuk melihat data terbaru COVID-19 di Jawa Tengah')

def terbaru(bot, update):
    data = getLastUpdate()
    chat_id = update.message.chat_id
    isi_teks = '*Situasi COVID-19 di Jawa Tengah pada ' + data[0] + '*' + '\nKasus: *' + data[1] + '*\nMeninggal: *' + data[2] + '*\nSembuh: *' + data[3] + '*\nDirawat (isolasi): *' + data[4] + '*'
    bot.send_message(chat_id=chat_id, text=isi_teks, parse_mode="Markdown")

def main():
    updater = Updater('YOUR_TOKEN')
    dispatch = updater.dispatcher
    dispatch.add_handler(CommandHandler('start', start))
    dispatch.add_handler(CommandHandler('terbaru', terbaru))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()