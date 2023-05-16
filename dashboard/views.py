from django.shortcuts import render
from .models import Berita

# import pagination stuff
from django.core.paginator import Paginator


# Create your views here.

def index(request) :
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'nama' : 'Selamat Datang',
        'user' : 'Nadira Alifia Ionendri',
        'tgl_terakhir_diambil' : '4 Mei 2023',
        'total_berita' : 10.321,
        'tgl_berita' : '2019-03-14',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'index.html', context)

def detail(request) :
    context = {
        'nama' : 'Detail Berita',
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'judul' : 'Menteri LHK Ingatkan Pentingnya Kolaborasi dan Jaga Kelola SDA Tanah Air',
        'teks' : 'PEKANBARU (RIAUPOS.CO) - Harga Tandan Buah Segar (TBS) kelapa sawit periode 15 sampai 21 Maret mengalami kenaikan pada setiap kelompok umur. Kenaikan terbesar terjadi pada kelompok umur 10 - 20 tahun sebesar Rp58,00/Kg dari harga pekan lalu. Sehingga harga pembelian TBS petani untuk periode satu minggu ke depan naik menjadi Rp2.947,12/Kg.',
        'teks2' : 'Kepala Dinas Perkebunan Riau Zulfadli mengatakan, faktor penyebab naiknya harga TBS periode ini karena terjadinya kenaikan harga jual CPO dan Kernel dari perusahaan yang menjadi sumber data. Indeks K yang dipakai adalah indeks K untuk 1 bulan kedepan yaitu 91,81%, harga penjualan CPO minggu ini naik sebesar Rp68,44 dan kernel minggu ini naik sebesar Rp954,53 dari minggu lalu. ',
        'teks3' : '"Untuk harga jual CPO, PT. Buana Wiralestari Mas menjual CPO dengan harga Rp 12.844,00/Kg dan mengalami kenaikkan harga sebesar Rp241,00/Kg dari harga minggu lalu. PT. Ramajaya Pramukti menjual CPO dengan harga Rp12.844,00/Kg dan mengalami kenaikkan harga sebesar Rp241,00/Kg dari harga minggu lalu," katanya. ',
        'teks4' : 'Sedangkan untuk harga jual Kernel, PT. Eka Dura Indonesia menjual Kernel dengan harga Rp6.459,46/Kg dan mengalami kenaikkan harga sebesar Rp198,20/Kg dari harga minggu lalu. PT. Sari Lembah Subur menjual Kernel dengan harga Rp6.486,49/Kg harga minggu ini. ',
        'teks5' : "\"PT. Musim Mas Batang Kulim Palm Oil Mill menjual Kernel dengan harga Rp8.330,00/Kg harga minggu ini. PTPN V Sei Buatan, PTPN V Sei Tapung, PT. Buana Wiralestari Mas, PT. Ramajaya Pramukti, tidak melakukan penjualan pada minggu ini,\" ujarnya. ",
        'teks6' : 'Sebagaimana diketahui bersama bahwa dari minggu lalu harga TBS yang ditetapkan oleh tim mengalami kenaikan. Kenaikan harga minggu ini lebih disebabkan karena faktor kenaikan harga CPO. Sedangkan sistem tata kelola penetapan harga TBS Provinsi Riau semakin membaik.',
        'teks7' : '"Membaiknya tata kelola penetapan harga merupakan upaya yang serius dari seluruh stake holder yang didukung oleh Pemerintah Provinsi Riau dan Kejaksaan Tinggi Riau. Komitmen bersama ini pada akhirnya tentu akan berimbas pada peningkatan pendapatan petani yang bermuara pada kesejahteraan masyarakat," ujarnya.',
    }
    return render(request, 'detail_berita.html', context)

def login(request) :
    return render(request, 'login.html')
