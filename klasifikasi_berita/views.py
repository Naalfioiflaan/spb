from django.shortcuts import render
from django.http import HttpResponse
from .models import Berita
from .models import Kemiskinan
from .models import Pengangguran
from .models import Demokrasi
from .models import Inflasi
from .models import Pertumbuhan_Ekonomi
import xlwt
from django.db.models import Max
from django.db.models.functions import Coalesce
from datetime import datetime


# import pagination stuff
from django.core.paginator import Paginator

# Create your views here.
def klasifikasi_berita(request):
    auth_user = request.user
    context = {
        'nama' : 'Klasifikasi Berita',
        'user' : auth_user,
        'tgl_terakhir_diambil' : '4 Mei 2023',
    }
    return render(request, 'klasifikasi_berita/klasifikasi_berita.html', context)

def kemiskinan(request) :
    berita = Kemiskinan.objects.order_by('-berita__tanggal')
    total_berita = len(berita)
    first_row = Kemiskinan.objects.order_by('berita__tanggal').first()
    last_row = Kemiskinan.objects.order_by('berita__tanggal').last()

    list_pengaruh = ['Naik','Turun','Tidak ada']
    jlh_naik = int(Kemiskinan.objects.filter(naik = '1').count())
    jlh_turun = int(Kemiskinan.objects.filter(turun = '1').count())
    jlh_tidak_ada = int(Kemiskinan.objects.filter(tidak_ada = '1').count())
    jlh_pengaruh = [jlh_naik, jlh_turun, jlh_tidak_ada]

    naik_bulan = []
    for x in range (1,13):
        pengaruh = Kemiskinan.objects.filter(berita__tanggal__month = x).filter(naik = '1').count()
        naik_bulan.append(pengaruh)
    
    turun_bulan = []
    for x in range (1,13):
        pengaruh = Kemiskinan.objects.filter(berita__tanggal__month = x).filter(turun = '1').count()
        turun_bulan.append(pengaruh)
    
    tidak_ada_bulan = []
    for x in range (1,13):
        pengaruh = Kemiskinan.objects.filter(berita__tanggal__month = x).filter(tidak_ada = '1').count()
        tidak_ada_bulan.append(pengaruh)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : total_berita,
        'first_berita' : first_row,
        'last_berita' : last_row,
        'user' : request.user,
        'berita' : berita,
        'list' : list,
        'list_pengaruh' : list_pengaruh,
        'jlh_pengaruh' : jlh_pengaruh,
        'naik_bulan' : naik_bulan,
        'turun_bulan' : turun_bulan,
        'tidak_ada_bulan' : tidak_ada_bulan
    }
    return render(request, 'klasifikasi_berita/kemiskinan.html',context)

def export_kemiskinan(request):
    if request.method == 'POST':
        tgl = request.POST.get('tgl')
        tgls = tgl.split(' s/d ')
        tgl_awal = datetime.strptime(tgls[0], '%Y-%m-%d').date()
        if (len(tgls) == 2):
            tgl_akhir = datetime.strptime(tgls[1], '%Y-%m-%d').date()
        else:
            tgl_akhir = tgl_awal
        response = HttpResponse(content_type = "application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Berita Kemiskinan.xls'
        # kalau mau nambah waktu str(datetime.datetime.now())
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Kemiskinan')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns =  ['tanggal', 'judul', 'link','isi_berita', 'naik','turun','tidak_ada']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Kemiskinan.objects.all().values_list(
            'berita_id', 'naik', 'turun', 'tidak_ada')
        
        for row in rows:
            berita = Berita.objects.get(id = row[0])
            print(berita.tanggal)
            # tgl_berita = datetime.strptime(berita.tanggal, '%Y-%m-%d').date()
            if (berita.tanggal >= tgl_awal and berita.tanggal <= tgl_akhir):
                row_num += 1

                for col_num in range(len(columns)):
                    if (col_num > 3):
                        ws.write(row_num, col_num, str(row[col_num-3]), font_style)
                    else:
                        if col_num == 0:
                            ws.write(row_num, col_num, str(berita.tanggal), font_style)
                        if col_num == 1:
                            ws.write(row_num, col_num, berita.judul, font_style)
                        if col_num == 2:
                            ws.write(row_num, col_num, berita.link, font_style)
                        if col_num == 3:
                            ws.write(row_num, col_num, berita.isi_berita, font_style)

        wb.save(response)

        return response
    

def pengangguran(request) :
    berita = Pengangguran.objects.order_by('-berita__tanggal')
    total_berita = len(berita)
    first_row = Pengangguran.objects.order_by('berita__tanggal').first()
    last_row = Pengangguran.objects.order_by('berita__tanggal').last()

    list_pengaruh = ['Naik','Turun','Tidak ada']
    jlh_naik = int(Pengangguran.objects.filter(naik = '1').count())
    jlh_turun = int(Pengangguran.objects.filter(turun = '1').count())
    jlh_tidak_ada = int(Pengangguran.objects.filter(tidak_ada = '1').count())
    jlh_pengaruh = [jlh_naik, jlh_turun, jlh_tidak_ada]

    naik_bulan = []
    for x in range (1,13):
        pengaruh = Pengangguran.objects.filter(berita__tanggal__month = x).filter(naik = '1').count()
        naik_bulan.append(pengaruh)
    
    turun_bulan = []
    for x in range (1,13):
        pengaruh = Pengangguran.objects.filter(berita__tanggal__month = x).filter(turun = '1').count()
        turun_bulan.append(pengaruh)
    
    tidak_ada_bulan = []
    for x in range (1,13):
        pengaruh = Pengangguran.objects.filter(berita__tanggal__month = x).filter(tidak_ada = '1').count()
        tidak_ada_bulan.append(pengaruh)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : total_berita,
        'first_berita' : first_row,
        'last_berita' : last_row,
        'user' : request.user,
        'berita' : berita,
        'list' : list,
        'list_pengaruh' : list_pengaruh,
        'jlh_pengaruh' : jlh_pengaruh,
        'naik_bulan' : naik_bulan,
        'turun_bulan' : turun_bulan,
        'tidak_ada_bulan' : tidak_ada_bulan
    }
    return render(request, 'klasifikasi_berita/pengangguran.html', context)

def export_pengangguran(request):
   
    if request.method == 'POST' :
        tgl = request.POST.get('tgl')
        tgls = tgl.split(' s/d ')
        tgl_awal = datetime.strptime(tgls[0], '%Y-%m-%d').date()
        if (len(tgls) == 2):
            tgl_akhir = datetime.strptime(tgls[1], '%Y-%m-%d').date()
        else:
            tgl_akhir = tgl_awal
        response = HttpResponse(content_type = "application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Berita Pengangguran.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Pengangguran')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns =  ['tanggal', 'judul', 'link','isi_berita', 'naik','turun','tidak_ada']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Pengangguran.objects.all().values_list(
            'berita_id', 'naik', 'turun', 'tidak_ada')
        
        for row in rows:
            berita = Berita.objects.get(id = row[0])
            print(berita.tanggal)
            # tgl_berita = datetime.strptime(berita.tanggal, '%Y-%m-%d').date()
            if (berita.tanggal >= tgl_awal and berita.tanggal <= tgl_akhir):
                row_num += 1

                for col_num in range(len(columns)):
                    if (col_num > 3):
                        ws.write(row_num, col_num, str(row[col_num-3]), font_style)
                    else:
                        if col_num == 0:
                            ws.write(row_num, col_num, str(berita.tanggal), font_style)
                        if col_num == 1:
                            ws.write(row_num, col_num, berita.judul, font_style)
                        if col_num == 2:
                            ws.write(row_num, col_num, berita.link, font_style)
                        if col_num == 3:
                            ws.write(row_num, col_num, berita.isi_berita, font_style)

        wb.save(response)

        return response

def demokrasi(request) :
    berita = Demokrasi.objects.order_by('-berita__tanggal')
    total_berita = len(berita)
    first_row = Demokrasi.objects.order_by('berita__tanggal').first()
    last_row = Demokrasi.objects.order_by('berita__tanggal').last()

    list_pengaruh = ['Naik','Turun','Tidak ada']
    jlh_naik = int(Demokrasi.objects.filter(naik = '1').count())
    jlh_turun = int(Demokrasi.objects.filter(turun = '1').count())
    jlh_tidak_ada = int(Demokrasi.objects.filter(tidak_ada = '1').count())
    jlh_pengaruh = [jlh_naik, jlh_turun, jlh_tidak_ada]

    naik_bulan = []
    for x in range (1,13):
        pengaruh = Demokrasi.objects.filter(berita__tanggal__month = x).filter(naik = '1').count()
        naik_bulan.append(pengaruh)
    
    turun_bulan = []
    for x in range (1,13):
        pengaruh = Demokrasi.objects.filter(berita__tanggal__month = x).filter(turun = '1').count()
        turun_bulan.append(pengaruh)
    
    tidak_ada_bulan = []
    for x in range (1,13):
        pengaruh = Demokrasi.objects.filter(berita__tanggal__month = x).filter(tidak_ada = '1').count()
        tidak_ada_bulan.append(pengaruh)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : total_berita,
        'first_berita' : first_row,
        'last_berita' : last_row,
        'user' : request.user,
        'berita' : berita,
        'list' : list,
        'list_pengaruh' : list_pengaruh,
        'jlh_pengaruh' : jlh_pengaruh,
        'naik_bulan' : naik_bulan,
        'turun_bulan' : turun_bulan,
        'tidak_ada_bulan' : tidak_ada_bulan
    }
    return render(request, 'klasifikasi_berita/demokrasi.html',context)

def export_demokrasi(request):
    if request.method == 'POST' :
        tgl = request.POST.get('tgl')
        tgls = tgl.split(' s/d ')
        tgl_awal = datetime.strptime(tgls[0], '%Y-%m-%d').date()
        if (len(tgls) == 2):
            tgl_akhir = datetime.strptime(tgls[1], '%Y-%m-%d').date()
        else:
            tgl_akhir = tgl_awal
        response = HttpResponse(content_type = "application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Berita Demokrasi.xls'
        # kalau mau nambah waktu str(datetime.datetime.now())
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Demokrasi')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns =  ['tanggal', 'judul', 'link','isi_berita', 'naik','turun','tidak_ada']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Demokrasi.objects.all().values_list(
            'berita_id', 'naik', 'turun', 'tidak_ada')
        
        for row in rows:
            berita = Berita.objects.get(id = row[0])
            print(berita.tanggal)
            # tgl_berita = datetime.strptime(berita.tanggal, '%Y-%m-%d').date()
            if (berita.tanggal >= tgl_awal and berita.tanggal <= tgl_akhir):
                row_num += 1

                for col_num in range(len(columns)):
                    if (col_num > 3):
                        ws.write(row_num, col_num, str(row[col_num-3]), font_style)
                    else:
                        if col_num == 0:
                            ws.write(row_num, col_num, str(berita.tanggal), font_style)
                        if col_num == 1:
                            ws.write(row_num, col_num, berita.judul, font_style)
                        if col_num == 2:
                            ws.write(row_num, col_num, berita.link, font_style)
                        if col_num == 3:
                            ws.write(row_num, col_num, berita.isi_berita, font_style)

    wb.save(response)

    return response

def inflasi(request) :
    berita = Inflasi.objects.order_by('-berita__tanggal')
    total_berita = len(berita)
    first_row = Inflasi.objects.order_by('berita__tanggal').first()
    last_row = Inflasi.objects.order_by('berita__tanggal').last()

    list_pengaruh = ['Naik','Turun','Tidak ada']
    jlh_naik = int(Inflasi.objects.filter(naik = '1').count())
    jlh_turun = int(Inflasi.objects.filter(turun = '1').count())
    jlh_tidak_ada = int(Inflasi.objects.filter(tidak_ada = '1').count())
    jlh_pengaruh = [jlh_naik, jlh_turun, jlh_tidak_ada]

    naik_bulan = []
    for x in range (1,13):
        pengaruh = Inflasi.objects.filter(berita__tanggal__month = x).filter(naik = '1').count()
        naik_bulan.append(pengaruh)
    
    turun_bulan = []
    for x in range (1,13):
        pengaruh = Inflasi.objects.filter(berita__tanggal__month = x).filter(turun = '1').count()
        turun_bulan.append(pengaruh)
    
    tidak_ada_bulan = []
    for x in range (1,13):
        pengaruh = Inflasi.objects.filter(berita__tanggal__month = x).filter(tidak_ada = '1').count()
        tidak_ada_bulan.append(pengaruh)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : total_berita,
        'first_berita' : first_row,
        'last_berita' : last_row,
        'user' : request.user,
        'berita' : berita,
        'list' : list,
        'list_pengaruh' : list_pengaruh,
        'jlh_pengaruh' : jlh_pengaruh,
        'naik_bulan' : naik_bulan,
        'turun_bulan' : turun_bulan,
        'tidak_ada_bulan' : tidak_ada_bulan
    }
    return render(request, 'klasifikasi_berita/inflasi.html', context)

def export_inflasi(request):
    if request.method == 'POST' :
        tgl = request.POST.get('tgl')
        tgls = tgl.split(' s/d ')
        tgl_awal = datetime.strptime(tgls[0], '%Y-%m-%d').date()
        if (len(tgls) == 2):
            tgl_akhir = datetime.strptime(tgls[1], '%Y-%m-%d').date()
        else:
            tgl_akhir = tgl_awal
        response = HttpResponse(content_type = "application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Berita Inflasi.xls'
        # kalau mau nambah waktu str(datetime.datetime.now())
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Inflasi')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns =  ['tanggal', 'judul', 'link','isi_berita', 'naik','turun','tidak_ada']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Inflasi.objects.all().values_list(
            'berita_id', 'naik', 'turun', 'tidak_ada')
        
        for row in rows:
            berita = Berita.objects.get(id = row[0])
            print(berita.tanggal)
            # tgl_berita = datetime.strptime(berita.tanggal, '%Y-%m-%d').date()
            if (berita.tanggal >= tgl_awal and berita.tanggal <= tgl_akhir):
                row_num += 1

                for col_num in range(len(columns)):
                    if (col_num > 3):
                        ws.write(row_num, col_num, str(row[col_num-3]), font_style)
                    else:
                        if col_num == 0:
                            ws.write(row_num, col_num, str(berita.tanggal), font_style)
                        if col_num == 1:
                            ws.write(row_num, col_num, berita.judul, font_style)
                        if col_num == 2:
                            ws.write(row_num, col_num, berita.link, font_style)
                        if col_num == 3:
                            ws.write(row_num, col_num, berita.isi_berita, font_style)

    wb.save(response)

    return response

def ekonomi(request) :
    berita = Pertumbuhan_Ekonomi.objects.order_by('-berita__tanggal')
    total_berita = len(berita)
    first_row = Pertumbuhan_Ekonomi.objects.order_by('berita__tanggal').first()
    last_row = Pertumbuhan_Ekonomi.objects.order_by('berita__tanggal').last()

    list_pengaruh = ['Naik','Turun','Tidak ada']
    jlh_naik = int(Pertumbuhan_Ekonomi.objects.filter(naik = '1').count())
    jlh_turun = int(Pertumbuhan_Ekonomi.objects.filter(turun = '1').count())
    jlh_tidak_ada = int(Pertumbuhan_Ekonomi.objects.filter(tidak_ada = '1').count())
    jlh_pengaruh = [jlh_naik, jlh_turun, jlh_tidak_ada]

    naik_bulan = []
    for x in range (1,13):
        pengaruh = Pertumbuhan_Ekonomi.objects.filter(berita__tanggal__month = x).filter(naik = '1').count()
        naik_bulan.append(pengaruh)
    
    turun_bulan = []
    for x in range (1,13):
        pengaruh = Pertumbuhan_Ekonomi.objects.filter(berita__tanggal__month = x).filter(turun = '1').count()
        turun_bulan.append(pengaruh)
    
    tidak_ada_bulan = []
    for x in range (1,13):
        pengaruh = Pertumbuhan_Ekonomi.objects.filter(berita__tanggal__month = x).filter(tidak_ada = '1').count()
        tidak_ada_bulan.append(pengaruh)

    # mengatur pagination
    p = Paginator(berita, 20)
    page = request.GET.get('page')
    list = p.get_page(page)

    context = {
        'total_berita' : total_berita,
        'first_berita' : first_row,
        'last_berita' : last_row,
        'user' : request.user,
        'berita' : berita,
        'list' : list,
        'list_pengaruh' : list_pengaruh,
        'jlh_pengaruh' : jlh_pengaruh,
        'naik_bulan' : naik_bulan,
        'turun_bulan' : turun_bulan,
        'tidak_ada_bulan' : tidak_ada_bulan
    }
    return render(request, 'klasifikasi_berita/pertumbuhan-ekonomi.html',context)

def export_pertumbuhan_ekonomi(request):
    if request.method == 'POST':
        tgl = request.POST.get('tgl')
        tgls = tgl.split(' s/d ')
        tgl_awal = datetime.strptime(tgls[0], '%Y-%m-%d').date()
        if (len(tgls) == 2):
            tgl_akhir = datetime.strptime(tgls[1], '%Y-%m-%d').date()
        else:
            tgl_akhir = tgl_awal
        response = HttpResponse(content_type = "application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Berita Pertumbuhan Ekonomi.xls'
        # kalau mau nambah waktu str(datetime.datetime.now())
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Pertumbuhan Ekonomi')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns =  ['tanggal', 'judul', 'link','isi_berita', 'naik','turun','tidak_ada']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        font_style = xlwt.XFStyle()

        rows = Pertumbuhan_Ekonomi.objects.all().values_list(
            'berita_id', 'naik', 'turun', 'tidak_ada')
        
        for row in rows:
            berita = Berita.objects.get(id = row[0])
            print(berita.tanggal)
            # tgl_berita = datetime.strptime(berita.tanggal, '%Y-%m-%d').date()
            if (berita.tanggal >= tgl_awal and berita.tanggal <= tgl_akhir):
                row_num += 1

                for col_num in range(len(columns)):
                    if (col_num > 3):
                        ws.write(row_num, col_num, str(row[col_num-3]), font_style)
                    else:
                        if col_num == 0:
                            ws.write(row_num, col_num, str(berita.tanggal), font_style)
                        if col_num == 1:
                            ws.write(row_num, col_num, berita.judul, font_style)
                        if col_num == 2:
                            ws.write(row_num, col_num, berita.link, font_style)
                        if col_num == 3:
                            ws.write(row_num, col_num, berita.isi_berita, font_style)

    wb.save(response)

    return response