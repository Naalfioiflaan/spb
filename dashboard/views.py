from django.shortcuts import render, redirect
from klasifikasi_berita.models import Berita
from klasifikasi_berita.models import Kemiskinan
from klasifikasi_berita.models import Pengangguran
from klasifikasi_berita.models import Demokrasi
from klasifikasi_berita.models import Inflasi
from klasifikasi_berita.models import Pertumbuhan_Ekonomi
from .scraper import riaupos as rp
from .scraper import haluan_riau as hr
from .scraper import goriau as gr
from .scraper import tribun as tp
from django.contrib.auth import authenticate, login, logout
from .forms import FormLogin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime

# import pagination stuff
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url=settings.LOGIN_URL)
def index(request) :
  if request.user.is_staff == True:
    berita = Berita.objects.order_by('-tanggal')
    rp_first_row = Berita.objects.filter(sumber="Riau Pos").order_by('-tanggal').first()
    hr_first_row = Berita.objects.filter(sumber="Haluan Riau").order_by('-tanggal').first()
    gr_first_row = Berita.objects.filter(sumber="Go Riau").order_by('-tanggal').first()
    tp_first_row = Berita.objects.filter(sumber="Tribun Pekanbaru").order_by('-tanggal').first()

    if rp_first_row:
        rp_tgl = rp_first_row.tanggal
    else:
        rp_tgl = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
    if hr_first_row:
        hr_tgl = hr_first_row.tanggal
    else:
        hr_tgl = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
    if gr_first_row:
        gr_tgl = gr_first_row.tanggal
    else:
        gr_tgl = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
    if tp_first_row:
        tp_tgl = tp_first_row.tanggal
    else:
        tp_tgl = (datetime.datetime.now() - datetime.timedelta(days=7)).date()

    search = request.GET.get('q')
    if search:
        berita = Berita.objects.filter(judul__icontains=search)
    else:
        berita = Berita.objects.order_by('-tanggal')

    total_berita = len(berita)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page', 1)
    list = p.get_page(page)
    
    context = {
        'user' : request.user,
        'rp_tgl_terakhir_diambil' : rp_tgl,
        'hr_tgl_terakhir_diambil' : hr_tgl,
        'gr_tgl_terakhir_diambil' : gr_tgl,
        'tp_tgl_terakhir_diambil' : tp_tgl,
        'total_berita' : total_berita,
        'berita' : berita,
        'list' : list
    }
    return render(request, 'index.html', context)
  else:
    return redirect('/403')

def unauthorized(request):
    if request.user.is_staff == False:
        return render(request, 'unauthorized.html')
    else:
        return redirect('/')

def ambil_riaupos(request):
    if request.method == 'POST':
        tgl_awal = request.POST.get('tgl_awal')
        print(tgl_awal)
        tgl_akhir = request.POST.get('tgl_akhir')
        print(tgl_akhir)
        rp.scrap(tgl_awal, tgl_akhir)
    return redirect('/')

def ambil_haluanriau(request):
    if request.method == 'POST':
        tgl_awal = request.POST.get('tgl_awal')
        print(tgl_awal)
        tgl_akhir = request.POST.get('tgl_akhir')
        print(tgl_akhir)
        hr.scrap(tgl_awal, tgl_akhir)
    return redirect('/')

def ambil_goriau(request):
    if request.method == 'POST':
        tgl_awal = request.POST.get('tgl_awal')
        print(tgl_awal)
        tgl_akhir = request.POST.get('tgl_akhir')
        print(tgl_akhir)
        gr.scrap(tgl_awal, tgl_akhir)
    return redirect('/')

def ambil_tribun_pekanbaru(request):
    if request.method == 'POST':
        tgl_awal = request.POST.get('tgl_awal')
        print(tgl_awal)
        tgl_akhir = request.POST.get('tgl_akhir')
        print(tgl_akhir)
        tp.scrap(tgl_awal, tgl_akhir)
    return redirect('/')

def detail(request, id) :
    berita = Berita.objects.get(id = id)
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
        'user' : request.user,
        'berita' : berita,
        'klasifikasi' : klasifikasi,
    }
    return render(request, 'detail_berita.html', context)

def update_classification(request, id) :
    berita = Berita.objects.get(id = id)
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
    
        #status
        if request.POST.get('diperiksa'):
            berita = Berita.objects.get(id = id)
            berita.status = "Diperiksa"
            berita.save()
        
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

        # status
        

    return redirect('/detail_berita/'+id)

def login_view(request) : 
    form = FormLogin()
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff == False:
                return redirect('/klasifikasi_berita')
            return redirect('/')
        
    return render(request, 'login.html',{'form':form})

def logout_views(request) :
    logout(request)
    request.session.flush()
    return redirect('/login')
