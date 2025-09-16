from django.db import models


class MovimentoFinanceiro(models.Model):
    TIPOS = [
        ('fixa', 'Fixa'),
        ('variavel', 'Variável'),
        ('outro', 'Outro'),
    ]
    CATEGORIA = [
        ('Receita', 'Receita'),
        ('Despesa', 'Despesa'),
    ]
    categoria = models.CharField(max_length=30, choices=CATEGORIA, verbose_name='Categoria', default='Outro')
    data = models.DateField(auto_now_add=True, verbose_name='Data')
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='Variavel')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')

    class Meta:
        abstract = True  # Não cria tabela

    def __str__(self):
        return f'{self.descricao} ---> {self.valor}'
    



class Receita(MovimentoFinanceiro):
    pass
    

class Despesa(MovimentoFinanceiro):
    pass