from django.contrib.auth.models import User
from django.db import models

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    cpf = models.CharField(max_length=11, unique=True, default=None)
    celular = models.CharField(max_length=15, null= False)

    def __str__(self):
        return (f'{self.cpf}, {self.celular}')
