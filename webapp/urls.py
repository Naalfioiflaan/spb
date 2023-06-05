"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard import views
from klasifikasi_berita import views as kb
from kelola_pengguna import views as kp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ambil_riau_pos', views.ambil_riaupos, name='ambil-riau-pos'),
    # path('detail_berita', views.detail, name='detail-berita'),
    path('detail_berita/<id>/', views.detail, name='detail-berita'),
    path('update_klasifikasi_berita/<id>/', views.update_classification, name='update-class'),
    path('update_pengaruh_berita/<id>/', views.perbarui_pengaruh, name='update-pengaruh'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_views, name='logout'),
    path('klasifikasi_berita', kb.klasifikasi_berita, name='klasifikasi_berita'),
    path('kelola_pengguna', kp.kelola_pengguna, name='kelola_pengguna'),
    path('kemiskinan', kb.kemiskinan, name="kemiskinan"),
    path('pengangguran', kb.pengangguran, name="pengangguran"),
    path('demokrasi', kb.demokrasi, name="demokrasi"),
    path('inflasi', kb.inflasi, name="inflasi"),
    path('pertumbuhan-ekonomi', kb.ekonomi, name="pertumbuhan-ekonomi"),

]
