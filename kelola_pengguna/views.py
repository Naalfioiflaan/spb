from django.shortcuts import render

# Create your views here.
def kelola_pengguna(request):
    context = {
        'nama' : 'Kelola Pengguna',
        'user' : 'Nadira Alifia Ionendri',
        'email_user' : 'alifianadira11@gmail.com'
    }
    return render(request, 'kelola_pengguna/kelola_pengguna.html', context)