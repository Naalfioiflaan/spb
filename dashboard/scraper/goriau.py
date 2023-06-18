import requests
from datetime import datetime
import locale
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx
import time 
import sys
from . import classification as cl
from urllib.request import urlopen, Request

def scrap(tgl_awal, tgl_akhir):
    # mengatur waktu
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    print('Taking article file from GoRiau')

    count = 0

    # menyimpan ke database
    db = mysql.connector.connect(user = 'root', database = 'spb')
    cursor = db.cursor()

    with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
        default_browser = QueryValueEx(key, 'Progid')[0]
    match default_browser:
        case "FirefoxURL":
            firefox_options = FOptions()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument('log-level=2')
            browser = webdriver.Firefox(options=firefox_options)

        case "ChromeHTML":
            chrome_options = COptions()
            chrome_options.headless = True
            chrome_options.add_argument("--log-level=2")
            chromedriver_path = "./chromedriver.exe"
            service = Service(chromedriver_path)
            browser = webdriver.Chrome(options=chrome_options, service=service)

        # browser = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://www.goriau.com/indexberita.html'
    browser.get(url)
    

    time.sleep(15)

    pilih_tgl = tgl_awal.split('-')
    # start 
    select_tgl = Select(browser.find_element(By.NAME, 'indexDate'))
    if (int(pilih_tgl[2]) <10) :
        pilih_tanggal = pilih_tgl[2][1]
    else:
        pilih_tanggal = pilih_tgl[2]
    select_tgl.select_by_value(pilih_tanggal)
    time.sleep(5)

    select_bln = Select(browser.find_element(By.NAME, 'indexMonth'))
    if (int(pilih_tgl[1]) <10) :
        pilih_bln = pilih_tgl[1][1]
    else:
        pilih_bln = pilih_tgl[1]
    select_bln.select_by_value(pilih_bln)
    time.sleep(5)

    select_thn = Select(browser.find_element(By.NAME, 'indexYear'))
    select_thn.select_by_value(pilih_tgl[0])
    time.sleep(5)

    button = browser.find_element(By.XPATH, '//input[@value="Tampilkan Index"]')
    button.click()

    time.sleep(10)

    for i in range(0, 1095):
        print()
        print('==== PAGE ' + str(i) + ' ====')

        # Hasil request
        time.sleep(10)
        request = browser.page_source
        soup = BeautifulSoup(request, 'html5lib')
        all_cover_articles = soup.find_all('div', class_='index-title')
        
        tgl = soup.find('div', class_='index-section').text
        print(tgl)
        tgl = tgl.split(' ')
        tgl = tgl[1]+' '+tgl[2]+' '+tgl[3]
        tgl = datetime.strptime(tgl, '%d %B %Y').date()
        print(str(tgl))

        # menentukan tanggal yang akan diambil, mulai dr yang tinggi ke rendah
        start = datetime.strptime(tgl_awal, '%Y-%m-%d').date()
        print(str(start))
        end = datetime.strptime(tgl_akhir, '%Y-%m-%d').date()
        print(str(end))

        if(tgl > start):
            print('tgl lebih besar dari start == true')
            button = browser.find_element(By.XPATH, '//input[@value="Tampilkan Index"]')
            button.click()

        elif(tgl <= start and tgl >= end):
            for j in range(len(all_cover_articles)):
                print()
                
                # mengambil judul
                title = all_cover_articles[j].find('a').get_text()
                count += 1
                print("{0}. {1}".format(count, title))

                # mengambil link
                ragam = "https://www.goriau.com" in all_cover_articles[j].find('a')['href']
                if ragam  :
                    link = all_cover_articles[j].find('a')['href']
                else:
                    link = "https://goriau.com"+all_cover_articles[j].find('a')['href']
                print('link: '+link)

                # mengambil isi berita
                # memasuki detail tiap berita
                UserAgent = Request(link, headers={'User-Agent':'Mozilla/5.0'})
                html = urlopen(UserAgent)
                # artikel_content = BeautifulSoup(html, 'html.parser')
                # artikel = requests.get(link)
                # artikel_content = html.content
                # print(artikel_content)
                soup_artikel = BeautifulSoup(html, 'html5lib')
                isi_artikel = soup_artikel.find_all('div', class_= 'post-content tabs')
                if (len(isi_artikel) != 0):
                    x = isi_artikel[0].find_all('p')

                    # menyatukan paragraf
                    list_paragraf = []
                    for p in np.arange(0, len(x)):
                        prg = x[p].get_text().strip()
                        list_paragraf.append(prg)
                        final_artikel = " ".join(list_paragraf)
                    # mengambil topik
                    if ragam:
                        topik = 'Ragam'
                    else:
                        topik = soup_artikel.find('div', class_='breadcrumb').find_all('a')[2].get_text()
                    print('Topik: '+topik)

                else:
                    final_artikel = 'isi berita tidak ditemukan'
                    topik = 'isi berita tidak ditemukan'

                print('Tanggal:'+str(tgl))

                # classification step
                konten = title + ' '+ final_artikel
                kemiskinan = int(cl.classify_kemiskinan(konten))
                pengangguran = int(cl.classify_pengangguran(konten))
                demokrasi = int(cl.classify_demokrasi(konten))
                inflasi = int(cl.classify_inflasi(konten))
                ekonomi = int(cl.classify_ekonomi(konten))
                
                # memasukkan ke database
                add_berita = ('INSERT INTO klasifikasi_berita_berita'
                                '(judul, link, tanggal, isi_berita, sumber, kemiskinan, pengangguran, demokrasi, inflasi, pertumbuhan_ekonomi, status)'
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

                data_berita = (title, link, tgl, final_artikel, 'Go Riau', kemiskinan, pengangguran, demokrasi, inflasi, ekonomi, 'Belum diperiksa')

                # insertion
                cursor.execute(add_berita, data_berita)
                db.commit()
                
                berita_id = cursor.lastrowid
                if (kemiskinan == 1) :
                    add_kemiskinan = ('INSERT klasifikasi_berita_kemiskinan'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_kemiskinan = (berita_id, 0, 0, 0)
                    cursor.execute(add_kemiskinan, data_kemiskinan)
                    db.commit()
                if (pengangguran == 1) :
                    add_pengangguran = ('INSERT klasifikasi_berita_pengangguran'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_pengangguran = (berita_id, 0, 0, 0)
                    cursor.execute(add_pengangguran, data_pengangguran)
                    db.commit()
                if (demokrasi == 1) :
                    add_demokrasi = ('INSERT klasifikasi_berita_demokrasi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_demokrasi = (berita_id, 0, 0, 0)
                    cursor.execute(add_demokrasi, data_demokrasi)
                    db.commit()
                if (inflasi == 1) :
                    add_inflasi = ('INSERT klasifikasi_berita_inflasi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_inflasi = (berita_id, 0, 0, 0)
                    cursor.execute(add_inflasi, data_inflasi)
                    db.commit()
                if (ekonomi == 1) :
                    add_ekonomi = ('INSERT klasifikasi_berita_pertumbuhan_ekonomi'
                                        '(berita_id, naik, turun, tidak_ada)'
                                        'VALUES (%s, %s, %s, %s)')
                    data_ekonomi = (berita_id, 0, 0, 0)
                    cursor.execute(add_ekonomi, data_ekonomi)
                    db.commit()

            button = browser.find_element(By.XPATH, '//input[@value="Tampilkan Index"]')
            button.click()

        else:
            sys.exit()
            
    cursor.close()
    db.close()

