from django.urls import path
from .views import AgendarServico, AgendamentoView, AgendamentoMes, StatusAgendamento, AgendamentoDia,AgendamentoHoje, lembrete
from .views import atualizacaoAgendamento


urlpatterns = [
    path('listar-agendamento/', AgendamentoView, name="Listar todos os serviços agendados"),
    path('agendar-cliente/', AgendarServico, name='Agendar um serviço p/ o cliente'),
    path('listar-agendamento-mes/<int:m>/',AgendamentoMes, name='Lista todo o agendamento do mês passado' ),
    path('status/<int:pk>/', StatusAgendamento),
    path('agendamento-dia/', AgendamentoDia, name='todos os agendamentos do dia solicitado'),
    path('agendamento-hoje/',AgendamentoHoje, name='Agendamentos do dia' ),
    path('lembrete-agendamento/',lembrete, name='envia uma mensagem no dia para todos os agendamentos' ),
    path('detalhe-agendamento/<int:pk>/',atualizacaoAgendamento.as_view(), name= 'Detalhe de um único agendamento'), 
    path('excluir-agendamento/<int:pk>/',atualizacaoAgendamento.as_view(), name= 'Exclui um único agendamento'),
]    

