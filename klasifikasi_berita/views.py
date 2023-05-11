from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def klasifikasi_berita(request):
    context = {
        'nama' : 'Klasifikasi Berita',
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'tgl_terakhir_diambil' : '4 Mei 2023',
    }
    return render(request, 'klasifikasi_berita/klasifikasi_berita.html', context)

def kemiskinan(request) :
    context = {
        'total_berita' : 10.321,
    }
    return render(request, 'klasifikasi_berita/kemiskinan.html',context)

def pengangguran(request) :
    return render(request, 'klasifikasi_berita/pengangguran.html')

def demokrasi(request) :
    return render(request, 'klasifikasi_berita/demokrasi.html')

def inflasi(request) :
    return render(request, 'klasifikasi_berita/inflasi.html')

def ekonomi(request) :
    return render(request, 'klasifikasi_berita/pertumbuhan-ekonomi.html')