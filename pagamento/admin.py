from django.contrib import admin
from .models import Despesa, Receita


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    fields = ['data','descricao', 'tipo', 'valor']
    search_fields = ['data', 'descricao','categoria'] 
    list_display =['data','descricao', 'tipo', 'valor']

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    fields = ['data','descricao', 'tipo', 'valor']
    list_display =['data','descricao', 'tipo', 'valor']
    search_fields = ['data', 'descricao','categoria']     
    
