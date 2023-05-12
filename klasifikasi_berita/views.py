from django.shortcuts import render
from django.http import HttpResponse
from .models import Berita

# import pagination stuff
from django.core.paginator import Paginator

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
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : 5.321,
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'klasifikasi_berita/kemiskinan.html',context)

def pengangguran(request) :
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : 5.321,
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'klasifikasi_berita/pengangguran.html', context)

def demokrasi(request) :
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : 5.321,
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'klasifikasi_berita/demokrasi.html',context)

def inflasi(request) :
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : 5.321,
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'klasifikasi_berita/inflasi.html', context)

def ekonomi(request) :
    berita = Berita.objects.all()

    # mengatur pagination
    p = Paginator(Berita.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : 5.321,
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'klasifikasi_berita/pertumbuhan-ekonomi.html',context)