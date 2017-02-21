from django.db import models

def nombre(instance, filename):
    return 'user_/{0}'.format(filename)
class Document(models.Model):
    docfile=models.FileField(upload_to=nombre)
# Create your models here.
