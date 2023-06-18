from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import mysql.connector
import sys
import locale
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.chrome.service import Service as CService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.firefox.service import Service as FService
from webdriver_manager.firefox import GeckoDriverManager
from . import classification as cl

def scrap(tgl_awal, tgl_akhir):
	# mengatur waktu
	locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

	print('Taking article file from Tribun Pekanbaru')

	with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
			default_browser = QueryValueEx(key, 'Progid')[0]
	match default_browser:
		case "FirefoxURL":
			firefox_options = FOptions()
			firefox_options.add_argument("--headless")
			firefox_options.add_argument('log-level=2')
			service = FService(GeckoDriverManager().install())
			browser = webdriver.Firefox(options=firefox_options, service=service)

		case "ChromeHTML":
			chrome_options = COptions()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--log-level=2")
			service = CService(ChromeDriverManager().install())
			browser = webdriver.Chrome(options=chrome_options, service=service)
				
	url = 'https://pekanbaru.tribunnews.com/'
	browser.get(url)

	browser.execute_script("""function loadmore() {
		if ($("#ltldmr").length > 0) $("#ltldmr").remove();
		var getLast = parseInt($("#latestul li").last().attr("data-sort"));
		$("#latestul").append("<li class='loading'><i class='fa fa-refresh fa-spin fa-2x blue'></i></li>");
		$(".loading").show();
		var newlast = getLast;
		if (newLast <= 1000) {
			$.getJSON("https://pekanbaru.tribunnews.com/ajax/latest?callback=?", { start: newlast, img: 'thumb2', icon: '1' }, function (data) {
				$.each(data.posts, function (key, val) {
					newlast = newlast + 1;
					if (val.video) {
						var vthumb = "<i class='fa fa-play playoverlay'></i>";
						var vtitle = " <i class='fa fa-play-circle-o'></i>";
					}
					else {
						var vthumb = "";
						var vtitle = "";
					}
					if (val.thumb) {
						var img = "<div class='fr mt5 ml15 pos_rel'><a href='" + val.url + "' title='" + val.title + "'><img src='" + val.thumb + "' width='120' height='90' loading='lazy' class='shou2 bgwhite' alt='" + val.title + "'/></a>" + vthumb + "</div>";
						var milatest = "mr140";
					}
					else {
						var img = "";
						var milatest = "";
					}
					if (val.subtitle) subtitle = "<h4 class='fbo2 f14 red'><a href='" + val.subtitle_url + "' title='" + val.subtitle + "' >" + val.subtitle + "</a></h4>";
					else subtitle = '';

					$("#latestul").append("<li class='p1520 art-list pos_rel' data-sort='" + newlast + "'>" + img + "<div class='" + milatest + "'>" + subtitle + "<h3><a href='" + val.url + "' title='" + val.title + "' class='f20 ln24 fbo txt-oev-2'>" + val.title + vtitle + "</a></h3><div class='grey2 pt5 f13 txt-oev-2'>" + val.introtext + "</div><div class='pt5 grey'><span><a href='" + val.s_url + "' class='fbo2 tsa-2' title='" + val.s_title + "'>" + val.s_title + "</a></span><span class='fa fa-clock-o mr5 ml7'></span><time class='foot timeago' title='" + val.date + "'>" + val.times_ago + "</time></div></div><div class='sharecot pos_abs nw' data-href='" + val.url + "' data-title='" + val.title + "' data-via='tribunpekanbaru'></div><div class='cl2'></div></li>");
				});
				$(".loading").remove();
			});
		}
	}""")

	browser.execute_script("setInterval(loadmore, 2000);")
	time.sleep(60)

	request = browser.page_source
	soup = BeautifulSoup(request, 'html5lib')

	all_cover_articles = soup.find_all('div', class_='mr140')

	# # menyimpan ke database
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
		tgl = tgl.split('T')[0].strip()
		tgl = datetime.strptime(tgl, '%Y-%m-%d').date()

		# menentukan tanggal yang ingin diambil
		start = datetime.strptime(tgl_awal, '%Y-%m-%d').date()
		end = datetime.strptime(tgl_akhir, '%Y-%m-%d').date()

		if (tgl >= start and tgl <= end):
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
					print(final_artikel)
			else:
					final_artikel = 'isi berita tidak ditemukan'

			# classification step
			konten = title + ' '+ final_artikel
			kemiskinan = int(cl.classify_kemiskinan(konten))
			pengangguran = int(cl.classify_pengangguran(konten))
			demokrasi = int(cl.classify_demokrasi(konten))
			inflasi = int(cl.classify_inflasi(konten))
			ekonomi = int(cl.classify_ekonomi(konten))
			
			# memasukkan ke database
			add_berita = ('INSERT INTO tes2'
							'(judul, link, tanggal, isi_berita, sumber, kemiskinan, pengangguran, demokrasi, inflasi, pertumbuhan_ekonomi, status)'
							'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

			data_berita = (title, links, tgl, final_artikel, 'Tribun Pekanbaru', kemiskinan, pengangguran, demokrasi, inflasi, ekonomi, 'Belum diperiksa')

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

		elif(tgl < start or tgl > end):
			continue

		else:
			sys.exit()
				
	cursor.close()
	db.close()

