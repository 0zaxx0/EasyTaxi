from django.db import models
from django_pandas.managers import DataFrameManager
from datetime import datetime
# Create your models here.

class Conductor(models.Model):
    d_id=models.CharField(max_length=26,primary_key=True)
    d_cityc=models.CharField(max_length=10)
    d_name=models.CharField(max_length=50)
    d_fone=models.IntegerField()
    d_email=models.EmailField(max_length=50)
    d_active=models.CharField(max_length=8)
    d_date=models.DateField()
    total_c=models.IntegerField()
    objects=DataFrameManager()

    def __str__(self):
        return self.d_id

class Referido(models.Model):
    r_id=models.ForeignKey(Conductor)
    r_name=models.CharField(max_length=50)
    r_fone=models.IntegerField()
    r_email=models.EmailField(max_length=50)
    r_active=models.CharField(max_length=8)
    r_rut=models.IntegerField()
    objects=DataFrameManager()
    
    def __str__(self):
        return self.r_id
    
class Condiciones(models.Model):
    Ciudad=models.CharField(max_length=10)
    NumCarreras=models.IntegerField()
    ReferidoEspecial=models.CharField(max_length=100,default='')
    NumCarrerasEspecial=models.IntegerField(default=0)
    Plazo=models.IntegerField()
    Modalidad=models.CharField(max_length=20)
    Premio=models.IntegerField()
    PeriodoCarga=models.CharField(max_length=50)

    def __str__(self):
        return self.Ciudad
class CondicionesRef(models.Model):
    Ciudad=models.CharField(max_length=10)
    NumCarreras=models.IntegerField()
    ReferidoEspecial=models.CharField(max_length=100,default='')
    NumCarrerasEspecial=models.IntegerField(default=0)
    Plazo=models.IntegerField()
    Modalidad=models.CharField(max_length=20)
    Premio=models.IntegerField()
    PeriodoCarga=models.CharField(max_length=80)

    def __str__(self):
        return self.Ciudad

class HistoricoBienvenida(models.Model):
    driver_id=models.CharField(max_length=30,primary_key=True)
    date = models.DateTimeField(default=datetime.now,blank=True)
    monto_pago=models.IntegerField()

    def __str__(self):
        return self.driver_id
