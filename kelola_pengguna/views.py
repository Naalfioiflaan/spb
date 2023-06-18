from django.shortcuts import render, redirect
# import pagination stuff
from django.core.paginator import Paginator
from .models import AuthUser
from django.contrib.auth.models import User

# Create your views here.
def kelola_pengguna(request):
  pengguna = AuthUser.objects.all()
  # mengatur pagination
  search = request.GET.get('q')
  if search:
      pengguna = AuthUser.objects.filter(username__icontains=search)
  else:
      pengguna = AuthUser.objects.all()
  total_pengguna = len(pengguna)
  p = Paginator(pengguna, 20)
  page = request.GET.get('page')
  list = p.get_page(page)

  if request.user.is_staff == True:
    context = {
        'nama' : 'Kelola Pengguna',
        'user' : request.user,
        'list' : list,
        'pengguna' : pengguna,
        'total_pengguna' : total_pengguna
    }
    return render(request, 'kelola_pengguna/kelola_pengguna.html', context)
  else:
    return redirect('/403')
  
def add_user(request):
  if request.user.is_staff == True:
    if request.method == 'POST':
      username = request.POST['username']
      email = request.POST['email']
      password1 = request.POST['password1']
      password2 = request.POST['password2']

      if password1 == password2:
        user = User.objects.create_user(username=username, email=email, password=password1)
            # Perform any additional tasks if needed
        return redirect('/kelola_pengguna')
  else:
    return redirect('/403')

def update_status(request, id):
  if request.user.is_staff == True:
    pengguna = AuthUser.objects.get(id = id)
    if (request.GET.get('is_staff')) :
      pengguna.is_staff = bool(int(request.GET.get('is_staff')))
      pengguna.save()
    return redirect('/kelola_pengguna')
  else:
    return redirect('/403')
  
def remove_pengguna(request, id) :
  if request.user.is_staff == True :
    pengguna = AuthUser.objects.get(id = id)
    pengguna.delete()
    return redirect('/kelola_pengguna')
  else:
    return redirect('403')
