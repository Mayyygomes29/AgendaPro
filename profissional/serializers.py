from rest_framework import serializers
from .models import Profissional
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class UserProfissional(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']



class ProfissionalSerializer(serializers.ModelSerializer):
    user = UserProfissional()
    class Meta:
        model = Profissional
        fields = ['id','user','celular','cpf', 'funcao' ]
    

          



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        email = attrs.get('email')
        try:
            profissional = Profissional.objects.get(email=email)
        except Profissional.DoesNotExist():
            raise AuthenticationFailed('Usuário não encontrado!')
        
        senha = attrs.get('senha')
      
        profissional = Profissional.objects.get(senha=senha)
        if not profissional == senha:
            raise AuthenticationFailed('Senha Incorreta!')
       
        return super().validate(attrs)