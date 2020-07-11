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

def getAccumulation():
    dataAkumulasi = []
    contents = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TENGAH.json').json()
    caseAcm = str(contents['list_perkembangan'][-1]['AKUMULASI_KASUS'])
    deadAcm = str(contents['list_perkembangan'][-1]['AKUMULASI_MENINGGAL'])
    curedAcm = str(contents['list_perkembangan'][-1]['AKUMULASI_SEMBUH'])
    inTreatmentAcm = str(contents['list_perkembangan'][-1]['AKUMULASI_DIRAWAT_OR_ISOLASI'])
    deadPct = str("%.2f" % contents['meninggal_persen'])
    curedPct = str("%.2f" % contents['sembuh_persen'])
    dataAkumulasi.extend((caseAcm, deadAcm, curedAcm, inTreatmentAcm, deadPct, curedPct))
    return dataAkumulasi

def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Halo! Berikut daftar perintah untuk menggunakan bot ini.\n/terbaru untuk melihat informasi terbaru COVID-19 di Jawa Tengah\n/akumulasi untuk melihat akumulasi kasus COVID-19 di Jawa Tengah sampai saat ini')

def terbaru(bot, update):
    data = getLastUpdate()
    chat_id = update.message.chat_id
    isi_teks = '*Situasi COVID-19 di Jawa Tengah pada ' + data[0] + '*' + '\nKasus: *' + data[1] + '*\nMeninggal: *' + data[2] + '*\nSembuh: *' + data[3] + '*\nDirawat (isolasi): *' + data[4] + '*'
    bot.send_message(chat_id=chat_id, text=isi_teks, parse_mode="Markdown")

def akumulasi(bot, update):
    data = getAccumulation()
    chat_id = update.message.chat_id
    isi_teks = '*Akumulasi Kasus COVID-19 di Jawa Tengah*' + '\nKasus: *' + data[0] + '*\nMeninggal: *' + data[1] + '*\nSembuh: *' + data[2] + '*\nDirawat (isolasi): *' + data[3] + '*\nPersentase Meninggal: *' + data[4] +'%*\nPersentase Sembuh: *' + data[5] + '%*'
    bot.send_message(chat_id=chat_id, text=isi_teks, parse_mode="Markdown")

def main():
    updater = Updater('YOUR_TOKEN')
    dispatch = updater.dispatcher
    dispatch.add_handler(CommandHandler('start', start))
    dispatch.add_handler(CommandHandler('terbaru', terbaru))
    dispatch.add_handler(CommandHandler('akumulasi', akumulasi))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()