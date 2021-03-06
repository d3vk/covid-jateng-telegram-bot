from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

def getData():
    data = []
    contents = requests.get('https://corona.jatengprov.go.id/data/chart_harian_akumulatif').json()
    last_update = datetime.strptime(contents[-1]['tanggal'], "%Y-%m-%d")
    converted_date = last_update.strftime("%d-%m-%Y")
    positif = contents[-1]['covid']
    sembuh = contents[-1]['sembuh']
    meninggal = contents[-1]['dead']
    total_covid = contents[-1]['covid_sum']
    total_sembuh = contents[-1]['sembuh_sum']
    total_meninggal = contents[-1]['dead_sum']
    total_positif = int(total_covid) - int(total_meninggal) - int(total_sembuh)
    data.extend((converted_date, positif, sembuh, meninggal, total_covid, str(total_positif), total_meninggal, total_sembuh))
    return data

def getPdpOdp():
    URL = 'https://corona.jatengprov.go.id/data'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    total_pdp = soup.find('h3', class_='font-counter fc-orange').get_text()
    total_odp = soup.find('h3', class_='font-counter fc-ungu').get_text()
    data.extend((total_pdp, total_odp))
    data_baru = [i.replace(".","") for i in data]
    return data_baru

def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Halo! Berikut daftar perintah untuk menggunakan bot ini.\n/terbaru untuk melihat informasi terbaru COVID-19 di Jawa Tengah\n/akumulasi untuk melihat akumulasi kasus COVID-19 di Jawa Tengah sampai saat ini')

def terbaru(bot, update):
    data = getData()
    chat_id = update.message.chat_id
    isi_teks = '*Situasi Kasus Positif COVID-19 di Jawa Tengah pada ' + data[0] + '*' + '\nDirawat: *' + data[1] + '*\nSembuh: *' + data[2] + '*\nMeninggal: *' + data[3] + '*'
    bot.send_message(chat_id=chat_id, text=isi_teks, parse_mode="Markdown")

def akumulasi(bot, update):
    data = getData()
    data_PdpOdp = getPdpOdp()
    chat_id = update.message.chat_id
    isi_teks = '*Akumulasi Kasus COVID-19 di Jawa Tengah*' + '\nKasus Positif: *' + data[4] + '*\nDirawat: *' + data[5] + '*\nSembuh: *' + data[6] + '*\nMeninggal: *' + data[7] + '*\nJumlah PDP: *' + data_PdpOdp[0] + '*\nJumlah ODP: *' + data_PdpOdp[1] + '*'
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