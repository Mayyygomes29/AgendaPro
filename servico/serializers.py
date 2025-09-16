from rest_framework import serializers
from .models import Servico
from profissional.models import Profissional
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']


class profissionalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # ou writeable se quiser permitir edição neste serializer
    class Meta:
        model = Profissional
        fields = ['user', 'funcao'] 
        

class ServicoSerializer(serializers.ModelSerializer):
    profissional = profissionalSerializer()
    class Meta:
       model = Servico
       fields = ['id','nome', 'preco','profissional']