from django.db import models

# Create your models here.

class Berita(models.Model):
    judul = models.CharField(
       db_column='judul', max_length=200, blank=True, null=True)
    link = models.CharField(
        db_column='link', max_length=500, blank=True, null=True)
    topik = models.CharField(
        db_column='topik', max_length=255, blank=True, null=True)
    tanggal = models.DateField(
        db_column='tanggal', blank=True, null=True)
    isi_berita = models.TextField(
        db_column='isi_berita', blank=True, null=True)
    sumber = models.CharField(
        db_column='sumber', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'berita'