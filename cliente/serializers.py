from rest_framework import serializers
from .models import Cliente
from django.contrib.auth.models import User


class UserCliente(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email']


class ClienteSerializer(serializers.ModelSerializer):
    user = UserCliente()
    class Meta:
        model = Cliente
        fields = ['id','user','cpf', 'celular']
        extra_kwargs = {'password': {'write_only': True}}

 