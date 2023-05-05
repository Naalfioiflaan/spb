from django.shortcuts import render

# Create your views here.
def kelola_pengguna(request):
    context = {
        'nama' : 'Kelola Pengguna'
    }
    return render(request, 'kelola_pengguna/kelola_pengguna.html', context)