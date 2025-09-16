from django.forms import ValidationError
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from PRO.services import messageCadastro, messageLembrete
from .models import Agendamento
from rest_framework.response import Response
from .serializers import AgendamentoSerializer
from cliente.models import Cliente
from servico.models import Servico
from datetime import date, datetime
from rest_framework import generics
from PRO.util import filtragem
from django.views.decorators.cache import cache_page


#Lista com todos os agendamentos 
@cache_page(60 * 10)
@api_view(['GET'])
def AgendamentoView(request):
    filtros, ordenacao = filtragem(request)
    dados = Agendamento.objects.all()
    if filtros:
        dados = dados.filter(filtros)
    if ordenacao:
        dados = dados.order_by(ordenacao)

    serializer = AgendamentoSerializer(dados, many=True)
    return Response(serializer.data, status=200)


#Lista todos os agendamentos de um mês especifico
@cache_page(60 * 10)
@api_view(['POST'])
def AgendamentoMes(request, m):
    m=int(m)
    agendamento = Agendamento.objects.filter(date__month=m)
    filtros, ordenacao=filtragem(request)
    if filtros:
        agendamento = agendamento.filter(filtros)
    if ordenacao:
        agendamento = agendamento.order_by(ordenacao)
    if agendamento.exists():        
        serializer = AgendamentoSerializer(agendamento, many=True)
        return Response({f'Agendamento do mês {m}': serializer.data}, status=200)

    else:
        return Response({'erro':f'Não há agendamento para o mês {m}'}, status=404)
    



#Lista os agendamentos de um dia especifico
@cache_page(60 * 10)
@api_view(['POST'])    
def AgendamentoDia(request):
    hoje = request.data.get('date')
    if not hoje:
        return Response({'erro': 'O campo "date" é obrigatório.'}, status=400)
    try:
        data= datetime.strptime(hoje,'%Y-%m-%d').date()
    except ValueError:
        return Response({'erro': 'Formato de data inválido. Use o formato YYYY-MM-DD.'}, status=400)    
    

    agendamento = Agendamento.objects.filter(date=data)
    filtros, ordenacao=filtragem(request)
    if filtros:
        agendamento = agendamento.filter(filtros)
    if ordenacao:
        agendamento = agendamento.order_by(ordenacao)

    if agendamento.exists():
        serializer= AgendamentoSerializer(agendamento, many=True)
        return Response({'message':serializer.data}, status=200)
    else:
        return Response({'erro': 'Não existe agendamentos nesse dia'}, status=404)



#Lista o Agendamento do dia
@cache_page(60 * 10)
@api_view(['GET'])
def AgendamentoHoje(request):
    hoje = date.today()
    agendamento = Agendamento.objects.filter(date=hoje)
    filtros, ordenacao=filtragem(request)
    if filtros:
        agendamento = agendamento.filter(filtros)
    if ordenacao:
        agendamento = agendamento.order_by(ordenacao)

    if agendamento.exists():
        serializer = AgendamentoSerializer(agendamento, many = True)
        return Response({'message': serializer.data}, status=200)
    
    else: 
        return Response({'erro':'Não tem agendamento marcando para hoje.'}, status=404)
    


#Envia msg para todos os clientes agendados no dia  
@api_view(['GET'])
def lembrete(request):
    hoje = date.today()
    dia = hoje.weekday()

    agendamentos = Agendamento.objects.filter(date=hoje)
    if dia == 6:
        return Response({'erro':'Não trabalhamos aos domingos.'}, status=400)
    
    if agendamentos.exists():
        for pessoa in agendamentos:
                messageLembrete(nome=pessoa.nome.user.first_name,
                                servico=pessoa.servico, 
                                data=hoje, 
                                hora=pessoa.time, 
                                telefone=pessoa.nome.celular)
        return Response({'message': 'Mensagens enviadas com sucesso.'}, status=200)
    else:
        return Response({'erro': 'Nenhum agendamento para hoje.'}, status=404) 
 

#Agenda um servico 
@api_view(['POST'])
def AgendarServico(request):
    id_nome = request.data.get('cliente')
    id_servico = request.data.get('servico')
    date = request.data.get('date')  
    time = request.data.get('time')

    cliente = get_object_or_404(Cliente, id=id_nome)  # Pega o id do cliente
    servico = get_object_or_404(Servico, id=id_servico)  # Pega o id do serviço

    existe = Agendamento.objects.filter(  # Verifica se já existe esse serviço nesse horário
        servico=servico,
        date=date,
        time=time
    ).exists()

    if existe:
        return Response({'erro': 'Já existe um agendamento para este horário.'}, status=409)

    agendamento = Agendamento(nome=cliente, servico=servico, date=date, time=time)  # Cria um agendamento

    try:
        agendamento.disponivel = False  # Coloca o agendamento como indisponível
        agendamento.save()  # Tenta salvar no banco
        messageCadastro(
            servico=servico,
            nome=cliente.user.first_name,
            data=date,
            hora=time,
            telefone=cliente.celular
        )
    except ValidationError as e:  # Caso não consiga agendar, retorna erro
        return Response({'erro': str(e)}, status=400)

    dadosSerializer = AgendamentoSerializer(agendamento)
    return Response({'Agendamento Concluído': dadosSerializer.data}, status=201)



#Somente o profissional consegue alterar o status do agendamento
@api_view(['PATCH'])        
def StatusAgendamento(request, pk):
   ag= get_object_or_404(Agendamento, pk=pk)      #pega o id do agendamento que quero alterar o status
   status = request.data.get('status')            #pego o status que está sendo passado pelo profissional
   if not status:                                 #verifica se é um usuario tem a permissao 
        return Response({'erro': 'O campo "status" é obrigatório.'}, status=400)          
   if request.user.is_staff:                        
        ag.status = status
        ag.save() 
        return Response({'message':f'Status atualizado para {ag.status}.'}, status=200)
   else:
       return Response({'erro':'Somente usuários com permissão.'}, status=403) 



class atualizacaoAgendamento(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer 

