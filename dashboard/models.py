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

class BeritaKlasifikasi(models.Model):
    judul = models.CharField(
       db_column='judul', max_length=200, blank=True, null=True)
    link = models.CharField(
        db_column='link', max_length=500, blank=True, null=True)
    tanggal = models.DateField(
        db_column='tanggal', blank=True, null=True)
    isi_berita = models.TextField(
        db_column='isi_berita', blank=True, null=True)
    sumber = models.CharField(
        db_column='sumber', max_length=255, blank=True, null=True)
    kemiskinan = models.IntegerField(
        db_column='kemiskinan', blank=True, null=True)
    pengangguran = models.IntegerField(
        db_column='pengangguran', blank=True, null=True)
    demokrasi = models.IntegerField(
        db_column='demokrasi', blank=True, null=True)
    inflasi = models.IntegerField(
        db_column='inflasi', blank=True, null=True)
    pertumbuhan_ekonomi = models.IntegerField(
        db_column='pertumbuhan_ekonomi', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tes2'

class Kemiskinan(models.Model) :
    berita = models.OneToOneField(BeritaKlasifikasi, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'kemiskinan'
        
class Pengangguran(models.Model) :
    berita = models.OneToOneField(BeritaKlasifikasi, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'pengangguran'

class Demokrasi(models.Model) :
    berita = models.OneToOneField(BeritaKlasifikasi, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'demokrasi'

class Inflasi(models.Model) :
    berita = models.OneToOneField(BeritaKlasifikasi, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'inflasi'

class Pertumbuhan_Ekonomi(models.Model) :
    berita = models.OneToOneField(BeritaKlasifikasi, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'pertumbuhan_ekonomi'