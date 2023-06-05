from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import mysql.connector
import sys
import classification as cl

url = 'https://pekanbaru.tribunnews.com/'
UserAgent = Request(url, headers={'User-Agent':'Mozilla/5.0'})
html = urlopen(UserAgent)
data = BeautifulSoup(html, 'html.parser')

all_cover_articles = data.find_all('div', class_='mr140')

# menyimpan ke database
db = mysql.connector.connect(user = 'root', database = 'crawling')
cursor = db.cursor()

count = 1
for n in range(len(all_cover_articles)):
    print()
    # getting the title
    title = all_cover_articles[n].find('h3').find('a').get_text().strip()   

    # getting the link
    links = all_cover_articles[n].find('h3').find('a')['href']+"?page=all"

    # mengambil tanggal
    tgl = all_cover_articles[n].time['title']
    tgl = tgl.split(' ')[0].strip()
    tgl = datetime.strptime(tgl, '%Y-%m-%d').date()

    # menentukan tanggal yang akan diambil
    start = datetime.strptime('2023-05-30', '%Y-%m-%d').date()
    end = datetime.strptime('2023-05-31', '%Y-%m-%d').date()

    if (start < tgl and tgl <= end):
            count += 1
            print("{0}. {1}".format(count, title))
            print('link: '+links)
            print('Tanggal:'+str(tgl))

            # go to inside the detail view of news
            user_agent_artikel = Request(links, headers={'User-Agent':'Mozilla/5.0'})
            artikel = urlopen(user_agent_artikel)
            artikel_content = BeautifulSoup(artikel, 'html.parser')
            body = artikel_content.find_all('div', class_='multi-fontsize')
            if (len(body) != 0):
                    x = body[0].find_all('p')

                    # menyatukan paragraf
                    list_paragraf = []
                    for p in np.arange(0, len(x)):
                        prg = x[p].get_text().strip()
                        list_paragraf.append(prg)
                        final_artikel = "\n".join(list_paragraf)
                    
            else:
                    final_artikel = 'isi berita tidak ditemukan'

            # classification step
            konten = title + ' '+ final_artikel
            kemiskinan = cl.classify_kemiskinan(konten)
            pengangguran = cl.classify_pengangguran(konten)
            demokrasi = cl.classify_demokrasi(konten)
            inflasi = cl.classify_inflasi(konten)
            ekonomi = cl.classify_ekonomi(konten)
            
            # memasukkan ke database
            add_berita = ('INSERT INTO tes2'
                            '(judul, link, tanggal, isi_berita, sumber, kemiskinan, pengangguran, demokrasi, inflasi, pertumbuhan_ekonomi)'
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

            data_berita = (title, links, tgl, final_artikel, 'Tribun Pekanbaru', int(kemiskinan), int(pengangguran), int(demokrasi), int(inflasi), int(ekonomi))

            # insertion
            cursor.execute(add_berita, data_berita)
            db.commit()
        
    elif(start < tgl ):
        continue

    else:
        sys.exit()
           
cursor.close()
db.close()

