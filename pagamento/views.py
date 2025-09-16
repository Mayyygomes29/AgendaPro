
from .models import Receita, Despesa
from agendamento.models import Agendamento
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import ReceitaSerializer, DespesaSerializer
from agendamento.serializers import AgendamentoSerializer
from PRO.util import filtragem, somar_valores




#Lista serviços de um cliente e quanto ele pagou no total do mês
@api_view(['POST'])
def ValorMensalCliente(request):
    mes = request.data.get('mes')
    ano = request.data.get('ano')
    cpf = request.data.get('cpf')

    if not (mes and ano and cpf):
        return Response({'erro': 'Mês, ano e cpf são obrigatórios.'},status=400)

    try:
        mes = int(mes)
        ano= int(ano)
    except ValueError:
        return Response({'erro': 'Os parâmetros devem ser números inteiros.'}, status=400)
    
    agendamentos = Agendamento.objects.filter(nome__cpf=cpf, date__month=mes, date__year=ano, status='Concluído')
    
    filtro, ordenacao = filtragem(request)
    if filtro:
        agendamentos=agendamentos.filter(filtro)

    if ordenacao:
        agendamentos=agendamentos.order_by(ordenacao)

    if agendamentos.exists():
        serializer = AgendamentoSerializer(agendamentos, many= True)
        total = somar_valores(agendamentos,campo='servico__preco')
        
    else:
        return Response({'message': f'Nenhum serviço concluído encontrado para o CPF {cpf} em {mes}/{ano}.'},
                         status=404)
    
    return Response({'serviços':serializer.data,
                    'total pago': f'R${total:.2f}',
                    'período':f'{mes}/{ano}'}, status=200)

    


#Relatório final com despesas, receitas e calculo final
@api_view(['POST'])
def RelatorioFinalMes(request):
    mes = request.data.get('mes')
    ano = request.data.get('ano')
    
    if not(mes and ano):
        return Response({'erro':'Os parâmetros "mes" e "ano" são obrigatórios.'},status=400)
    
    try:
        mes = int(mes)
        ano=int(ano)
    except ValueError:
         return Response({'erro':'Os parâmetros "mes" e "ano" devem ser números inteiros.'}, status=400)   


    receita = Receita.objects.filter(data__month=mes, data__year=ano)
    despesa = Despesa.objects.filter(data__month=mes, data__year=ano) 
    
    serializer_receita = ReceitaSerializer(receita, many=True) 
    serializer_despesa = DespesaSerializer(despesa, many =True)

    receita_soma = somar_valores(receita)
    despesa_soma = somar_valores(despesa)
    total = receita_soma - despesa_soma
            
    return Response({'receitas':serializer_receita.data, 
                     'despesas':serializer_despesa.data,
                     'total': f'R$ {receita_soma:.2f} - R$ {despesa_soma:.2f} = R${total:.2f}',
                     'saldo positivo': total >= 0,
                     'periodo': f'{mes}/{ano}'}, status=200)



#Lista de Receita e o total do mes 
@api_view(['POST'])
def ReceitaMensalTotal(request):
    mes = request.data.get('mes')
    ano = request.data.get('ano')
    receita_mes = Receita.objects.filter(data__month = mes, data__year = ano)

    filtro, ordenacao = filtragem(request)
    if filtro:
        receita_mes=receita_mes.filter(filtro)

    if ordenacao:
        receita_mes=receita_mes.order_by(ordenacao)

    if receita_mes.exists():
        total = somar_valores(receita_mes)
        serializer = ReceitaSerializer(receita_mes, many =True)

        return Response({'dados':serializer.data,
                         'total receita':f'R${total:.2f}',
                         'periodo':f'{mes}/{ano}'},
                         status=200)       
    else:
         return Response({'erro':f'Não existe receita no mês {mes}/{ano}'},status=400)



#Salva os agendamento concluidos na receita
@api_view(['POST'])
def RegistrarReceitaAgendamento(request, mes, ano):
    agendamento = Agendamento.objects.filter(date__month=mes, date__year=ano, status ='Concluído')
   
    criado = 0
    for a in agendamento:
            data = a.date
            desc = f'{a.servico.nome} - {a.nome.cpf}'
            valor = a.servico.preco

            
            if not Receita.objects.filter(data=data,descricao=desc, valor=valor).exists():   
                try:    
                    Receita.objects.create(
                    data=data,
                    descricao=desc,
                    valor=valor,
                    categoria='Prestação de Serviço'
                )
                    criado += 1
                except Exception as e:
                    return Response({'erro':f'Erro ao criar receita: {e}'}, status=400)
    return Response({'message':f'{criado} receitas criadas com sucesso.'}, status=200)                    
  


#Detalha, exclui e atualiza receita
class ItemReceita(generics.RetrieveUpdateDestroyAPIView):
      queryset = Receita.objects.all()
      serializer_class = ReceitaSerializer


#Detalha, exclui e atualizar despesa
class ItemDespesa(generics.RetrieveUpdateDestroyAPIView):
     queryset =Despesa.objects.all()
     serializer_class= DespesaSerializer


#Cria despesa no banco de dados
@api_view(['POST'])
def CriarDespesa(request):
    data = request.data.get('data')
    descricao = request.data.get('descricao') 
    valor = request.data.get('valor')
    categoria = request.data.get('categoria')
    tipo = request.data.get('tipo')

    salvando_despesa = Despesa.objects.create(
         data=data,
         descricao=descricao,
         valor=valor,
         categoria = categoria, 
         tipo = tipo
    )

    serializer = DespesaSerializer(salvando_despesa)
    return Response({'message':'Despesa salva com sucesso.',
                     'dados':serializer.data}, status=201)



#lista com as depesas e o total
@api_view(['POST'])
def DespesaTotalMes(request):
    mes = request.data.get('mes')
    ano = request.data.get('ano')
    if not (mes and ano):
        return Response({'erro': 'Os parâmetros "mes" e "ano" são obrigatórios.'}, status=400)

    try:
        mes = int(mes)
        ano = int(ano)
    except ValueError:
        return Response({'erro': 'Os parâmetros "mes" e "ano" devem ser números inteiros.'}, status=400)
    
    despesa_mensal = Despesa.objects.filter(data__month=mes, data__year=ano)
    filtro, ordenacao = filtragem(request)
    if filtro:
       despesa_mensal=despesa_mensal.filter(filtro)

    if ordenacao:
        despesa_mensal=despesa_mensal.order_by(ordenacao)
    if despesa_mensal.exists():
        total_despesa = somar_valores(despesa_mensal)
        serializer = DespesaSerializer(despesa_mensal, many = True)
        return Response({'dados': serializer.data,
                         'total despesa':f'{total_despesa:.2f}',
                         'periodo':f'{mes}/{ano}'},
                         status=200)
    else:
        return Response({'erro': f'Nenhuma despesa encontrada na data {mes}/{ano}.'}, status=404)
    



