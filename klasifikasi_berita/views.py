from django.shortcuts import render

# Create your views here.
def klasifikasi_berita(request):
    context = {
        'nama' : 'Klasifikasi Berita',
    }
    return render(request, 'klasifikasi_berita/klasifikasi_berita.html', context)