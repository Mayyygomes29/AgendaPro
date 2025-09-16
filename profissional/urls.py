from django.urls import path
from .views import CadastrarProfissional, ListaDeFuncionarios, ExcluirAtualizarProfissional
urlpatterns = [
   path('cadastrar/funcionario/', CadastrarProfissional, name='Cadastra profissional'),
   path('listar/funcionarios/', ListaDeFuncionarios.as_view(), name = 'Lista de funcionarios'),
   path('excluir-profissional/<int:pk>/', ExcluirAtualizarProfissional.as_view(), name='Exclui profissional'),
   path('atualiza-profissional/<int:pk>/', ExcluirAtualizarProfissional.as_view(), name='Atualiza dados do Profissional')

]
