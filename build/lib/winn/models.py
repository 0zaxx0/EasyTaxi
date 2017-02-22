from django.db import models

# Create your models here.

class Conductor(models.Model):
    d_id=models.CharField(max_length=24,primary_key=True)
    d_cityc=models.CharField(max_length=10)
    d_name=models.CharField(max_length=50)
    d_fone=models.IntegerField()
    d_email=models.EmailField(max_length=50)
    d_active=models.CharField(max_length=8)
    d_date=models.DateField()

    def __str__(self):
        return self.d_id

class Referido(models.Model):
    r_id=models.ForeignKey(Conductor)
    r_name=models.CharField(max_length=50)
    r_fone=models.IntegerField()
    r_email=models.EmailField(max_length=50)
    r_active=models.CharField(max_length=8)
    r_rut=models.IntegerField()

    def __str__(self):
        return self.r_id
    
