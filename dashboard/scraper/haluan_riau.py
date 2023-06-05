import requests
from datetime import datetime
import locale
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
import sys
from . import classification as cl

def scrap(tgl_awal, tgl_akhir):

    # mengatur waktu
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # mengambil link halaman selanjutnya
    url = 'https://riau.harianhaluan.com/indeks-berita?daterange=&page=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    lp = 1000
    print('Taking article file from Haluan Riau'+str(lp)+' pages')

    count = 0

    # menyimpan ke database
    db = mysql.connector.connect(user = 'root', database = 'crawling')
    cursor = db.cursor()

    # mengambil data
    for i in range(1, 1001):
        print('==== PAGE ' + str(i) + ' ====')
        url = 'https://riau.harianhaluan.com/indeks-berita?daterange=&page='+str(i)
        
        # Membuat request
        r = requests.get(url)

        # Hasil request
        request = r.content
        soup = BeautifulSoup(request, 'html5lib')
        all_cover_articles = soup.find_all('div', class_='latest__item')

        for j in range(len(all_cover_articles)):
            print()
            
            # mengambil judul
            title = all_cover_articles[j].find('h2').find('a').get_text()

            # mengambil link
            link = all_cover_articles[j].find('h2').find('a')['href']

            # mengambil tanggal
            tgl = all_cover_articles[j].date.text
            tgl = tgl.split(',')[1].split('|')[0].strip()
            tgl = datetime.strptime(tgl, '%d %B %Y').date()

            # menentukan tanggal yang akan diambil
            start = datetime.strptime(tgl_awal, '%Y-%m-%d').date()
            end = datetime.strptime(tgl_akhir, '%Y-%m-%d').date()

            if (start < tgl and tgl <= end):
                count += 1
                print("{0}. {1}".format(count, title))
                print('link: '+link)
                print('Tanggal:'+str(tgl))

                # mengambil isi berita
                # memasuki detail tiap berita
                artikel = requests.get(link)
                sub_artikel = artikel.content
                soup_sub_artikel = BeautifulSoup(sub_artikel, 'html5lib')
                body = soup_sub_artikel.find_all('article', class_= 'read__content')
                if (len(body) != 0):
                    x = body[0].find_all('p')

                    # menyatukan paragraf
                    list_paragraf = []
                    for p in np.arange(0, len(x)):
                        prg = x[p].get_text().strip()
                        list_paragraf.append(prg)
                        final_artikel = " ".join(list_paragraf)
                    
                else:
                    final_artikel = 'isi berita tidak ditemukan'
                print(final_artikel)

                # # mengambil topik
                # topik = all_cover_articles[j].find('h4').get_text()
                # print('Topik:'+topik)

                # classification step
                konten = title + ' '+ final_artikel
                kemiskinan = int(cl.classify_kemiskinan(konten))
                pengangguran = int(cl.classify_pengangguran(konten))
                demokrasi = int(cl.classify_demokrasi(konten))
                inflasi = int(cl.classify_inflasi(konten))
                ekonomi = int(cl.classify_ekonomi(konten))

                # memasukkan ke database
                add_berita = ('INSERT INTO tes2'
                                '(judul, link, tanggal, isi_berita, sumber, kemiskinan, pengangguran, demokrasi, inflasi, pertumbuhan_ekonomi)'
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

                data_berita = (title, link, tgl, final_artikel, 'Haluan Riau', kemiskinan, pengangguran, demokrasi, inflasi, ekonomi)

                # insertion
                cursor.execute(add_berita, data_berita)
                db.commit()

                berita_id = cursor.lastrowid
                if (kemiskinan == 1) :
                    add_kemiskinan = ('INSERT INTO kemiskinan'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_kemiskinan = (berita_id, 0, 0, 0)
                    cursor.execute(add_kemiskinan, data_kemiskinan)
                    db.commit()
                if (pengangguran == 1) :
                    add_pengangguran = ('INSERT INTO pengangguran'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_pengangguran = (berita_id, 0, 0, 0)
                    cursor.execute(add_pengangguran, data_pengangguran)
                    db.commit()
                if (demokrasi == 1) :
                    add_demokrasi = ('INSERT INTO demokrasi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_demokrasi = (berita_id, 0, 0, 0)
                    cursor.execute(add_demokrasi, data_demokrasi)
                    db.commit()
                if (inflasi == 1) :
                    add_inflasi = ('INSERT INTO inflasi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_inflasi = (berita_id, 0, 0, 0)
                    cursor.execute(add_inflasi, data_inflasi)
                    db.commit()
                if (ekonomi == 1) :
                    add_ekonomi = ('INSERT INTO pertumbuhan_ekonomi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_ekonomi = (berita_id, 0, 0, 0)
                    cursor.execute(add_ekonomi, data_ekonomi)
                    db.commit()
            
            elif(start < tgl ):
                continue

            else:
                sys.exit()

    cursor.close()
    db.close()

    



