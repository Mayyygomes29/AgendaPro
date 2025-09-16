from django.contrib import admin
from .models import Profissional


@admin.register(Profissional)
class ClienteAdmin(admin.ModelAdmin):
    fields = ['user','cpf', 'celular']
    list_display =  ['user','cpf', 'celular']
    
 

