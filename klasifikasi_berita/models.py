from django.db import models

class Berita(models.Model):
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
    status = models.CharField(
       db_column='status', max_length=30, blank=True, null=True)
    
class Kemiskinan(models.Model) :
    berita = models.OneToOneField(Berita, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    @property
    def tanggal(self):
        return self.berita.tanggal
    
    @property
    def judul(self):
        return self.berita.judul
    
    @property
    def link(self):
        return self.berita.link

class Pengangguran(models.Model) :
    berita = models.OneToOneField(Berita, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    @property
    def tanggal(self):
        return self.berita.tanggal
    
    @property
    def judul(self):
        return self.berita.judul
    
    @property
    def link(self):
        return self.berita.link

class Demokrasi(models.Model) :
    berita = models.OneToOneField(Berita, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    @property
    def tanggal(self):
        return self.berita.tanggal
    
    @property
    def judul(self):
        return self.berita.judul
    
    @property
    def link(self):
        return self.berita.link

class Inflasi(models.Model) :
    berita = models.OneToOneField(Berita, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    @property
    def tanggal(self):
        return self.berita.tanggal
    
    @property
    def judul(self):
        return self.berita.judul
    
    @property
    def link(self):
        return self.berita.link

class Pertumbuhan_Ekonomi(models.Model) :
    berita = models.OneToOneField(Berita, on_delete=models.CASCADE, db_column='berita_id', related_name='+')
    naik = models.IntegerField(
        db_column='naik', blank=True, null=True)
    turun = models.IntegerField(
        db_column='turun', blank=True, null=True)
    tidak_ada = models.IntegerField(
        db_column='tidak_ada', blank=True, null=True)
    @property
    def tanggal(self):
        return self.berita.tanggal
    
    @property
    def judul(self):
        return self.berita.judul
    
    @property
    def link(self):
        return self.berita.link