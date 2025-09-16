from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profissional
from .serializers import ProfissionalSerializer
from rest_framework import generics
from django.contrib.auth.models import User

#Cadastra um novo profissional
@api_view(['POST'])
def CadastrarProfissional(request):
    nome = request.data.get('first_name')
    celular = request.data.get('celular')
    email = request.data.get('email')
    cpf = request.data.get('cpf')
    username = request.data.get('username')
    senha = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'erro':'Username já existe.'}, status=409)

    if not Profissional.objects.filter(cpf=cpf).exists(): #Se CPF não existir, irá criar um novo usuário
            dadosProfissional = User.objects.create_user(
                username=username,
                first_name = nome,
                email = email,
                password= senha
            )
            dados = Profissional.objects.create(user=dadosProfissional, cpf=cpf, celular = celular)
            dadosSerializer = ProfissionalSerializer(dados)
            return Response ({'message':'Profissional salvo com sucesso.',
                            'dados': dadosSerializer.data}, status=201)
    else: #Senão, irá enviar uma mensagem de erro 
            return Response({'erro':'Profissional já existe'},status=409)


#Lista todos os profissionais
class ListaDeFuncionarios(generics.ListAPIView):
    queryset =Profissional.objects.all()
    serializer_class = ProfissionalSerializer


#Exclui e Atualiza o profissional
class ExcluirAtualizarProfissional(generics.RetrieveUpdateDestroyAPIView):
    queryset=Profissional.objects.all()
    serializer_class=ProfissionalSerializer




