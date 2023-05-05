from django.shortcuts import render

# Create your views here.
def index(request) :
    context = {
        'nama' : 'Selamat Datang',
        'user' : 'Nadira Alifia Ionendri',
        'tgl_terakhir_diambil' : '4 Mei 2023',
        'total_berita' : 10.321,
        'tgl_berita' : '2019-03-14',
        'judul_berita' : 'Naik Terus, Harga TBS kelapa sawit dekati RP 3000 per KG',
        'link_berita': 'https://riaupos.jawapos.com/eko',
        'email_user' : 'alifianadira11@gmail.com'
    }
    return render(request, 'index.html', context)