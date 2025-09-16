from django.contrib import admin
from .models import Servico

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    fields = ['nome', 'preco', 'profissional']
    list_display = ['nome', 'preco']
    
# Register your models here.
