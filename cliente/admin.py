from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    fields = ['user','cpf','celular']
    list_display = ['user','cpf', 'celular']
    search_fields =['user','cpf','celular']
    
# Register your models here.
