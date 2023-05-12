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

