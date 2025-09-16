from datetime import date, datetime
from django.db import models
from django.forms import ValidationError
from cliente.models import Cliente
from servico.models import Servico
from datetime import time
import holidays


class Agendamento(models.Model):
    hr_choice = (
        (time(9, 0), "09:00"),
        (time(10, 0), "10:00"),
        (time(11, 0), "11:00"),
        (time(12, 0), "12:00"),
        (time(14, 0), "14:00"),
        (time(15, 0), "15:00"),
        (time(16, 0), "16:00"),
        (time(17, 0), "17:00"),
        (time(18, 0), "18:00"),
        (time(19, 0), "19:00"),
        (time(20, 0), "20:00"),
    )
    st = (
          ('Concluído', 'Concluído'),
          ('Cancelado', 'Cancelado')
    ) 
    nome = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None, null=False)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, default=None, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(choices=hr_choice, null=False)
    disponivel = models.BooleanField(default=True, null=True)
    status = models.CharField(max_length=15, choices=st, default = 'Pendente')

    
   

    def __str__(self):
         return f'{self.nome} - {self.servico} - {self.date} às {self.time}'

#Esse método é o próprio "save()" que vem disponivel com o model, porém ele vai fazer uma verificação antes de salvar
    def save(self, *args, **kwargs): 
        conflito = Agendamento.objects.filter(
            date= self.date,
            time = self.time,
            servico = self.servico,
         ).exclude(pk=self.pk).exists()
            
        if conflito: #VER SE DATA/HR EXISTE, SE SIM RETORNA UM ERRO.
            raise ValidationError("Horário indisponível para esse serviço.")
        
        self.disponivel=False #senão, salvará os dados e colocará o disponivel como false
        super().save(*args, **kwargs) #salva junto com o admin 


    @classmethod
    def CriarData(cls):
            #pega o Ano e Mês atual
            anoAtual = date.today().year
            mesAtual = date.today().month
            feriado = holidays.Brazil()

            if mesAtual in [1,3,5,7,8,10,12]:  #Se o mês for um desses listado, sera com 31 dias
                dias = 31
             
            elif mesAtual == 2: #Se o mês for 2, sera 29 ou 28 dias   
                if (anoAtual % 4 == 0 and anoAtual % 100 != 0) or (anoAtual % 400 == 0):
                    dias = 29
                else:
                    dias = 28
                            
            else: #Senão, será de 30 dias
                dias = 30

            if dias:    
                for dia in range(1, dias + 1): #Lista do 1 até o total de cada dia representado pelo if
                    for hora in dict(cls.hr_choice).keys(): #E em cada dia, irá listar a hora que foi determinada por 'hr_choice'
                        data_completa = datetime(anoAtual, mesAtual, dia)
                        data= data_completa.weekday() #coloca de segunda(0) até domingo (6)
                        
                        if data == 6:
                            print(f'{data} Não funcionamos domingo.')
                            continue
                        if data_completa.date() in feriado:
                            print(f'É feriado! Não abriremos. Bom feriado de {feriado.get(data)}')
                            continue

                        if not cls.objects.filter(date=data_completa, time=hora).exists(): #Se a data e a hr nao existir, ele criara uma data e uma hora no banco, disponivel =TRUE 
                            cls.objects.create(date=data_completa, time=hora, disponivel = True)
                    
                        print( data_completa, hora)


        

    
                

