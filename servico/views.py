from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from profissional.models import Profissional
from .models import Servico
from .serializers import ServicoSerializer
from rest_framework import generics

#Registra serviço
@api_view(['POST'])
def RegistrarServico(request):
        try:
            nome = request.data.get('nome') #Verifica se já existe um serviço c/ esse nome

            if not Servico.objects.filter(nome=nome).exists(): #Se não existir nome, ele irár pegar os dados passado na url
                nome = request.data.get('nome')                #E vai criar um novo cadastro 
                preco = request.data.get('preco')
                profissional = request.data.get('profissional')

                prof = get_object_or_404(Profissional, pk=profissional)
            
                dados = Servico.objects.create(
                    nome=nome,
                    preco=preco,
                    profissional=prof
                )
                dadosSerializer = ServicoSerializer(dados)
                return Response({'message': 'Serviço cadastrado com sucesso.',
                                'serviço':dadosSerializer.data},
                                status=201)
            
            else:
                return Response({'message':'Serviço já existe.'}, status=400)
                
        except Exception as e:
            return Response({'erro': str(e)}, status=500)

            

#Lista todos os serviços
class ListaDeServico(generics.ListAPIView):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer


#Atualiza e exclui os serviço com id
class ExcluirAtualizarServico(generics.RetrieveUpdateDestroyAPIView):
    queryset=Servico.objects.all()
    serializer_class= ServicoSerializer    