from django.shortcuts import render

# Create your views here.
def klasifikasi_berita(request):
    context = {
        'nama' : 'Klasifikasi Berita',
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com',
        'tgl_terakhir_diambil' : '4 Mei 2023',
    }
    return render(request, 'klasifikasi_berita/klasifikasi_berita.html', context)