from django.db import models

class Post (models.Model):
    title=models.CharField(max_length = 130)
    body=models.TextField()
    date=models.DateTimeField()

    def __str__(self):
        return self.title
class Fichero_dim (models.Model):
    fecha=models.DateField()
    descripcion=models.CharField(max_length = 100)
    fichero=models.FileField(upload_to='ficheros')
    def __str__(self):
        return self.descripcion
