from django import forms

class UploadForm(forms.Form):
    docfile=forms.FileField(label='Selecione su archivo')
