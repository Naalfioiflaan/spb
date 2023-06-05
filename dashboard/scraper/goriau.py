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
import classification as cl

# mengatur waktu
locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

print('Taking article file from GoRiau')

count = 0

# menyimpan ke database
db = mysql.connector.connect(user = 'root', database = 'crawling')
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
        # chrome_options.headless = True
        chrome_options.add_argument("--log-level=2")
        chromedriver_path = "./chromedriver.exe"
        service = Service(chromedriver_path)
        browser = webdriver.Chrome(options=chrome_options, service=service)

    # browser = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.goriau.com/indexberita.html'
browser.get(url)

time.sleep(15)

# start kayanya
select_tgl = Select(browser.find_element(By.NAME, 'indexDate'))
select_tgl.select_by_value('31')
time.sleep(5)

select_bln = Select(browser.find_element(By.NAME, 'indexMonth'))
select_bln.select_by_value('5')
time.sleep(5)

select_thn = Select(browser.find_element(By.NAME, 'indexYear'))
select_thn.select_by_value('2023')
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
    start = datetime.strptime('2023-05-31', '%Y-%m-%d').date()
    print(str(start))
    end = datetime.strptime('2023-05-30', '%Y-%m-%d').date()
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
            artikel = requests.get(link)
            artikel_content = artikel.content
            soup_artikel = BeautifulSoup(artikel_content, 'html5lib')
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
            kemiskinan = cl.classify_kemiskinan(konten)
            pengangguran = cl.classify_pengangguran(konten)
            demokrasi = cl.classify_demokrasi(konten)
            inflasi = cl.classify_inflasi(konten)
            ekonomi = cl.classify_ekonomi(konten)
            
            # memasukkan ke database
            add_berita = ('INSERT INTO tes2'
                            '(judul, link, tanggal, isi_berita, sumber, kemiskinan, pengangguran, demokrasi, inflasi, pertumbuhan_ekonomi)'
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

            data_berita = (title, link, tgl, final_artikel, 'Go Riau', int(kemiskinan), int(pengangguran), int(demokrasi), int(inflasi), int(ekonomi))

            # insertion
            cursor.execute(add_berita, data_berita)
            db.commit()
            
        button = browser.find_element(By.XPATH, '//input[@value="Tampilkan Index"]')
        button.click()

    else:
        sys.exit()
        
cursor.close()
db.close()

