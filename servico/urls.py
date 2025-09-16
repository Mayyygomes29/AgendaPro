from django.urls import path
from .views import RegistrarServico,ListaDeServico, ExcluirAtualizarServico


urlpatterns = [
    path('cadastrar-servico/', RegistrarServico, name= 'Registrar Serviço' ),
    path('listar-servico/', ListaDeServico.as_view(),name='Lista de Serviço' ),
     path('atualizar-excluir/servico/<int:pk>/', ExcluirAtualizarServico.as_view(), name='excluir_servico'),
]
    

