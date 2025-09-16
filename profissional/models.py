from django.db import models
from django.contrib.auth.models import User

class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.BigIntegerField()
    cpf = models.BigIntegerField(unique=True)
    funcao = models.CharField(max_length=150)
    
    def __str__(self):
        return {self.funcao}