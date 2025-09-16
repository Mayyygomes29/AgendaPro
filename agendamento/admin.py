from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    fields = ['nome','servico', 'date', 'time', 'status']
    list_display = [ 'servico', 'date', 'time', 'disponivel', 'status']
    search_fields = ['date'] 
    


    