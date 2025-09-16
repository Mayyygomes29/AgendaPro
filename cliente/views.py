from rest_framework.response import Response
from .models import Cliente
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import ClienteSerializer
from agendamento.models import Agendamento
from agendamento.serializers import AgendamentoSerializer
from datetime import date
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from PRO.util import filtragem
from django.db import IntegrityError

#Cadastrar um cliente
@api_view(['POST'])
@permission_classes([AllowAny])
def CadastrarCliente(request): 
    nome = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')
    cpf= request.data.get('cpf')
    celular = request.data.get('celular')
    email = request.data.get('email') 
            
    if Cliente.objects.filter(cpf=cpf).exists(): #Verifica se existe cpf
        return Response({'erro':'cpf já existe.'}, status=409)
    if User.objects.filter(username=username).exists(): #Verifica se existe username
        return Response({'erro': 'Username já existe.'}, status=409) 
    
    try:
        dadosCliente = User(
            username = username,
            email=email,
            first_name = nome,
            )
        dadosCliente.set_password(password)
        dadosCliente.save()
        dados = Cliente.objects.create(user=dadosCliente, cpf=cpf, celular=celular)   
    except IntegrityError:
        return Response({'erro': 'Erro ao cadastrar cliente. Verifique os dados e tente novamente.'}, status=400)      


    dadosClienteSerializer = ClienteSerializer(dados)
    return Response({'message':'Cliente cadastrado com sucesso.', 
                        'dados':dadosClienteSerializer.data}, status=201)
        


#Lista todos os serviços q o cliente agendou
@api_view(['POST'])
def ListarTodosOsServico(request, pk):
    try:
        user = Cliente.objects.get(id=pk)
    except Cliente.DoesNotExist:
        return Response({'erro': 'Usuário não existe.'}, status=404)
    
    agendamentos = Agendamento.objects.filter(nome=user)
    filtros, ordenacao = filtragem(request)
    if filtros:
        agendamentos= agendamentos.filter(filtros)
    if ordenacao:
        agendamentos= agendamentos.order_by(ordenacao)    
            
    if agendamentos.exists():
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response({'message': serializer.data },status = 200)
    else:
        return Response({'erro':'Não existe nenhum agendamento pelo cliente.'}, status=400)

        


#Lista agendamentos futuros do cliente específico
@api_view(['POST'])
def ListarAgendamentosFuturos(request, pk):
    hoje = date.today() #pega a data de hoje 
    agendamentos_futuros = Agendamento.objects.filter(nome__id=pk, date__gte=hoje) #filtra se há algum id desse cliente c/ agendamentos futuros
                                                                      #usando o 'gt', para pegar data maior q hoje
    if agendamentos_futuros.exists():   
        serializer = AgendamentoSerializer(agendamentos_futuros, many=True)
        return Response({'Agendamentos futuros': serializer.data}, status=200)
    else:
        return Response({'erro':'Não existe agendamentos futuros.'}, status=400)
       
            
#Exclui e Atualiza cliente
class ExcluirEAtualizarCliente(RetrieveUpdateDestroyAPIView):
     queryset =Cliente.objects.all()
     serializer_class= ClienteSerializer


#Lista todos os clientes                            
class ListarCliente(ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class =ClienteSerializer     