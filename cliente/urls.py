from django.urls import path
from .views import CadastrarCliente,ListarCliente, ListarTodosOsServico, ExcluirEAtualizarCliente, ListarAgendamentosFuturos
 
urlpatterns = [
     path('cadastrar/cliente/', CadastrarCliente, name='cadastrar-cliente' ),
     path('listar-cliente/',ListarCliente.as_view(), name ='Lista usuários'),
     path('listar-servico-usuario/<int:pk>/',ListarTodosOsServico, name='Lista todos os serviços' ),
     path('excluir-cliente/<int:pk>/', ExcluirEAtualizarCliente.as_view(), name='Exclui cliente'),
     path('atualizar-cliente/<int:pk>/', ExcluirEAtualizarCliente.as_view(), name='atualiza os dados do cliente'),
     path('agendamentos-futuros-cliente/<int:pk>/', ListarAgendamentosFuturos, name='Lista todos os agendamentos futuros do cliente')

 ]
 