from rest_framework import serializers
from .models import Agendamento
from cliente.serializers import ClienteSerializer
from servico.serializers import ServicoSerializer

class AgendamentoSerializer(serializers.ModelSerializer):
    nome = ClienteSerializer()
    servico = ServicoSerializer()
    

    class Meta:
        model = Agendamento
        fields = ['id', 'nome', 'servico', 'date', 'time', 'status']


        

