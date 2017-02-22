from django.conf.urls import url
from . import views
from django.views.generic import ListView, DetailView
from winn.models import HistoricoBienvenida

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^uploads/', views.upload_file, name='uploads'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^tablas', views.mostrar, name='tablas'),
    #url(r'^$', ListView.as_view(queryset=HistoricoBienvenida.objects.all().order_by("-date")[:25], template_name="winn/gan.html")),
    url(r'^(?P<pk>.+)$', DetailView.as_view(model = HistoricoBienvenida, template_name="winn/gan.html")),
]
