from django.urls import path 
from .views import ValorMensalCliente,RelatorioFinalMes, ReceitaMensalTotal,RegistrarReceitaAgendamento,CriarDespesa,DespesaTotalMes
from .views import ItemDespesa, ItemReceita

urlpatterns = [
    
    path('valor-mensal-cliente/', ValorMensalCliente, name='Todos os serviços feito pelo cliente e o valor do mes'),
    path('relatorio-final/', RelatorioFinalMes, name='Relatório do mes'),
    path('total-receita/', ReceitaMensalTotal, name='Total da receita de tal mes'),
    path('registrar-receita/', RegistrarReceitaAgendamento, name='Registar agendamento na receita'),
    path('registrar-despesa/', CriarDespesa, name='Registra despesa'),
    path('total-despesa/', DespesaTotalMes, name='Total de despesa no mes'),
    path('editar-depesa/', ItemDespesa.as_view(), name='atualiza despesa'),
    path('detalhe-depesa/', ItemDespesa.as_view(), name='detalhe de despesa'),
    path('deletar-depesa/', ItemDespesa.as_view(), name='deleta despesa'),
    path('editar-receita/', ItemReceita.as_view(), name='atualiza receita'),
    path('detalhe-receita/', ItemReceita.as_view(), name='detalhe de receita'),
    path('deletar-receita/', ItemReceita.as_view(), name='deletar receita'),

]
