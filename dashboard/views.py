from django.shortcuts import render, redirect
from .models import Berita
from .models import BeritaKlasifikasi
from .models import Kemiskinan
from .models import Pengangguran
from .models import Demokrasi
from .models import Inflasi
from .models import Pertumbuhan_Ekonomi
from django.contrib.auth import authenticate, login, logout
from .forms import FormLogin
from django.contrib.auth.decorators import login_required
from django.conf import settings

# import pagination stuff
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url=settings.LOGIN_URL)
def index(request) :
    berita = BeritaKlasifikasi.objects.all()
    total_berita = len(berita)

    # mengatur pagination
    p = Paginator(BeritaKlasifikasi.objects.all(), 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'nama' : 'Selamat Datang',
        'user' : 'Nadira Alifia Ionendri',
        'tgl_terakhir_diambil' : '4 Mei 2023',
        'total_berita' : total_berita,
        'tgl_berita' : '2019-03-14',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'list' : list
    }
    return render(request, 'index.html', context)

def detail(request, id) :
    berita = BeritaKlasifikasi.objects.get(id = id)
    klasifikasi = {}
    
    # kemiskinan
    try:
        kemiskinan = Kemiskinan.objects.get(berita_id = id)
    except:
        pass
    else:
        klasifikasi['kemiskinan'] = kemiskinan
    # pengangguran
    try:
        pengangguran = Pengangguran.objects.get(berita_id = id)
    except:
        pass
    else:
        klasifikasi['pengangguran'] = pengangguran
    # demokrasi
    try:
        demokrasi = Demokrasi.objects.get(berita_id = id)
    except:
        pass
    else:
        klasifikasi['demokrasi'] = demokrasi
    # inflasi
    try:
        inflasi = Inflasi.objects.get(berita_id = id)
    except:
        pass
    else:
        klasifikasi['inflasi'] = inflasi
    # pertumbuhan_ekonomi
    try:
        pertumbuhan_ekonomi = Pertumbuhan_Ekonomi.objects.get(berita_id = id)
    except:
        pass
    else:
        klasifikasi['pertumbuhan_ekonomi'] = pertumbuhan_ekonomi

    context = {
        'nama' : 'Detail Berita',
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'berita' : berita,
        'klasifikasi' : klasifikasi,
    }
    return render(request, 'detail_berita.html', context)

def update_classification(request, id) :
    berita = BeritaKlasifikasi.objects.get(id = id)
    if (request.GET.get('kemiskinan')) :
        berita.kemiskinan = int(request.GET.get('kemiskinan'))
        try :
            kemiskinan = Kemiskinan.objects.get(berita_id = id)
        except :
            kemiskinan = Kemiskinan(berita_id=id, naik=0, turun=0, tidak_ada=0)
            kemiskinan.save()
        else :
            kemiskinan.delete()
    if (request.GET.get('pengangguran')) :
        berita.pengangguran = int(request.GET.get('pengangguran'))
        try :
            pengangguran = Pengangguran.objects.get(berita_id = id)
        except :
            pengangguran = Pengangguran(berita_id=id, naik=0, turun=0, tidak_ada=0)
            pengangguran.save()
        else :
            pengangguran.delete()
    if (request.GET.get('demokrasi')) :
        berita.demokrasi = int(request.GET.get('demokrasi'))
        try :
            demokrasi = Demokrasi.objects.get(berita_id = id)
        except :
            demokrasi = Demokrasi(berita_id=id, naik=0, turun=0, tidak_ada=0)
            demokrasi.save()
        else :
            demokrasi.delete()
    if (request.GET.get('inflasi')) :
        berita.inflasi = int(request.GET.get('inflasi'))
        try :
            inflasi = Inflasi.objects.get(berita_id = id)
        except :
            inflasi = Inflasi(berita_id=id, naik=0, turun=0, tidak_ada=0)
            inflasi.save()
        else :
            inflasi.delete()
    if (request.GET.get('pertumbuhan_ekonomi')) :
        berita.pertumbuhan_ekonomi = int(request.GET.get('pertumbuhan_ekonomi'))
        try :
            pertumbuhan_ekonomi = Pertumbuhan_Ekonomi.objects.get(berita_id = id)
        except :
            pertumbuhan_ekonomi = Pertumbuhan_Ekonomi(berita_id=id, naik=0, turun=0, tidak_ada=0)
            pertumbuhan_ekonomi.save()
        else : 
            pertumbuhan_ekonomi.delete()
    berita.save()
    return redirect('/detail_berita/'+id)

def perbarui_pengaruh(request, id):
    if request.method == 'POST':
        
        # kemiskinan
        try:
            kemiskinan = Kemiskinan.objects.get(berita_id = id)
        except:
            pass
        else :
            match request.POST.get('kemiskinan'):
                case "naik":
                    kemiskinan.naik = 1
                    kemiskinan.turun = 0
                    kemiskinan.tidak_ada = 0
                case "turun":
                    kemiskinan.naik = 0 
                    kemiskinan.turun = 1
                    kemiskinan.tidak_ada = 0
                case "tidak_ada":
                    kemiskinan.naik = 0
                    kemiskinan.turun = 0
                    kemiskinan.tidak_ada = 1
            kemiskinan.save()
        
        # pengangguran
        try:
            pengangguran = Pengangguran.objects.get(berita_id = id)
        except:
            pass
        else :
            match request.POST.get('pengangguran'):
                case "naik":
                    pengangguran.naik = 1
                    pengangguran.turun = 0
                    pengangguran.tidak_ada = 0
                case "turun":
                    pengangguran.naik = 0 
                    pengangguran.turun = 1
                    pengangguran.tidak_ada = 0
                case "tidak_ada":
                    pengangguran.naik = 0
                    pengangguran.turun = 0
                    pengangguran.tidak_ada = 1
            pengangguran.save()

        # demokrasi
        try:
            demokrasi = Demokrasi.objects.get(berita_id = id)
        except:
            pass
        else :
            match request.POST.get('demokrasi'):
                case "naik":
                    demokrasi.naik = 1
                    demokrasi.turun = 0
                    demokrasi.tidak_ada = 0
                case "turun":
                    demokrasi.naik = 0 
                    demokrasi.turun = 1
                    demokrasi.tidak_ada = 0
                case "tidak_ada":
                    demokrasi.naik = 0
                    demokrasi.turun = 0
                    demokrasi.tidak_ada = 1
            demokrasi.save()

        # inflasi
        try:
            inflasi = Inflasi.objects.get(berita_id = id)
        except:
            pass
        else :
            match request.POST.get('inflasi'):
                case "naik":
                    inflasi.naik = 1
                    inflasi.turun = 0
                    inflasi.tidak_ada = 0
                case "turun":
                    inflasi.naik = 0 
                    inflasi.turun = 1
                    inflasi.tidak_ada = 0
                case "tidak_ada":
                    inflasi.naik = 0
                    inflasi.turun = 0
                    inflasi.tidak_ada = 1
            inflasi.save()
        
        # pertumbuhan_ekonomi
        try:
            pertumbuhan_ekonomi = Pertumbuhan_Ekonomi.objects.get(berita_id = id)
        except:
            pass
        else :
            match request.POST.get('pertumbuhan_ekonomi'):
                case "naik":
                    pertumbuhan_ekonomi.naik = 1
                    pertumbuhan_ekonomi.turun = 0
                    pertumbuhan_ekonomi.tidak_ada = 0
                case "turun":
                    pertumbuhan_ekonomi.naik = 0 
                    pertumbuhan_ekonomi.turun = 1
                    pertumbuhan_ekonomi.tidak_ada = 0
                case "tidak_ada":
                    pertumbuhan_ekonomi.naik = 0
                    pertumbuhan_ekonomi.turun = 0
                    pertumbuhan_ekonomi.tidak_ada = 1
            pertumbuhan_ekonomi.save()

    return redirect('/detail_berita/'+id)

def login_view(request) : 
    form = FormLogin()
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        
    return render(request, 'login.html',{'form':form})

def logout_views(request) :
    logout(request)
    request.session.flush()
    return redirect('/login')
