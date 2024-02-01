from datetime import datetime, date, time, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Empresa(models.Model):
    razao_social = models.CharField(max_length=50)
    nome_fantasia = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)
    ramo = models.CharField(max_length=20)

    def __str__(self):
        return self.razao_social


class Representante(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome_representante = models.CharField(max_length=25)
    sobrenome_representante = models.CharField(max_length=25)
    cpf_representante = models.CharField(max_length=14, unique=True)
    cargo_representante = models.CharField(max_length=20)
    data_nascimento_representante = models.DateField()
    telefone_representante = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.TextField()
    username = models.CharField(max_length=150, default='')
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Setores(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome_setor = models.CharField(max_length=50)
    descricao_setor = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return self.nome_setor


class Expediente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    DIAS_DA_SEMANA = (
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo')
    )
    descricao_expediente = models.CharField(max_length=100)
    dia_da_semana = models.CharField(max_length=253)
    entrada_1 = models.TimeField()
    saida_1 = models.TimeField()
    entrada_2 = models.TimeField()
    saida_2 = models.TimeField()
    horario_total = models.TimeField()

    def save(self, *args, **kwargs):
        self.entrada_1 = self.entrada_1.replace(microsecond=0)
        self.saida_1 = self.saida_1.replace(microsecond=0)
        self.entrada_2 = self.entrada_2.replace(microsecond=0)
        self.saida_2 = self.saida_2.replace(microsecond=0)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.dia_da_semana

    def get_dias_da_semana(self):
        return self.dia_da_semana.split(',')

    def set_dias_da_semana(self, dias):
        self.dia_da_semana = ','.join(dias)


class Funcionario(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setores, on_delete=models.SET_NULL, null=True)
    horario = models.ForeignKey(Expediente, on_delete=models.SET_NULL, null=True)
    matricula_funcionario = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$'
            ),
        ],
    )
    nome_funcionario = models.CharField(max_length=25)
    sobrenome_funcionario = models.CharField(max_length=25)
    cpf_funcionario = models.CharField(max_length=14, unique=True)
    cargo_funcionario = models.CharField(max_length=14)
    data_nascimento_funcionario = models.DateField()
    email_funcionario = models.EmailField(unique=True)
    senha_funcionario = models.TextField()
    telefone_funcionario = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    online = models.BooleanField(default=False)
    ferias = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_funcionario


class BlackListSite(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    nome_site = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_site
    
class BlackListApp(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    nome_app = models.CharField(max_length=50)
    executavel = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome_site
    

class Atividades(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    nome_atividade = models.CharField(max_length=100)
    descricao_atividade = models.CharField(max_length=200)
    STATUS_ATIVIDADE_CHOICES = (
        ('Não iniciado', 'Não iniciado'), # Atividade não iniciada
        ('Em progresso', 'Em progresso'), # Atividade iniciada
        ('Concluído', 'Concluído'), # Atividade concluida
        ('Em espera', 'Em espera'), # Atividade pausada
    )
    status_atividade = models.CharField(max_length=200, choices=STATUS_ATIVIDADE_CHOICES, default='Não iniciado')
    data_atividade = models.DateField()
    tempo_entrega = models.TimeField()
    def save(self, *args, **kwargs):
        self.tempo_entrega = self.tempo_entrega.replace(microsecond=0)

        super().save(*args, **kwargs)