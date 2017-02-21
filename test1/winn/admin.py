from django.contrib import admin
from winn.models import Conductor, Referido,Condiciones,CondicionesRef,HistoricoBienvenida

admin.site.register(Condiciones)
admin.site.register(CondicionesRef)
admin.site.register(HistoricoBienvenida)
# Register your models here.
