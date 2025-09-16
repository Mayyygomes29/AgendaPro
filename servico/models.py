from django.db import models
from profissional.models import Profissional


class Servico(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.FloatField()
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE,null=False, default=None)
    
    

    def __str__(self):
        return self.nome 