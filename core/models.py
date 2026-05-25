from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# 1. Usuário Customizado
class UsuarioNexus(AbstractUser):
    telefone = models.CharField("Telefone", max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "Usuário Nexus"
        verbose_name_plural = "Usuários Nexus"

    def __str__(self):
        return self.username

# 2. Modelo de Projeto
class Project(models.Model):
    STATUS_PLANEJAMENTO = 'PLANEJAMENTO'
    STATUS_DESENVOLVIMENTO = 'DESENVOLVIMENTO'
    STATUS_TESTES = 'TESTES'
    STATUS_ENTREGUE = 'ENTREGUE'
    STATUS_PAUSADO = 'PAUSADO'

    STATUS_CHOICES = [
        (STATUS_PLANEJAMENTO, 'Em Planejamento'),
        (STATUS_DESENVOLVIMENTO, 'Em Desenvolvimento'),
        (STATUS_TESTES, 'Em Testes'),
        (STATUS_ENTREGUE, 'Entregue'),
        (STATUS_PAUSADO, 'Pausado'),
    ]

    PRIORITY_CHOICES = [
        ('Alta', 'Alta'),
        ('Média', 'Média'),
        ('Baixa', 'Baixa'),
    ]

    title = models.CharField("Título", max_length=200)
    client = models.CharField("Cliente", max_length=200, blank=True, null=True)
    desc = models.TextField("Descrição", blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANEJAMENTO, db_index=True)
    priority = models.CharField("Prioridade", max_length=10, choices=PRIORITY_CHOICES, default='Alta', db_index=True)
    progress = models.IntegerField("Progresso (%)", default=0)
    owner = models.CharField("Responsável", max_length=50, blank=True, null=True)
    start_date = models.DateField("Data de Início", blank=True, null=True, db_index=True)
    end_date = models.DateField("Previsão de Entrega", blank=True, null=True, db_index=True)
    
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Usuário Responsável"
    )
    
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.client or 'Sem Cliente'})"

# 3. Modelos Adicionais (Documentos e Produtos)
class Document(models.Model):
    title = models.CharField("Título do Documento", max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField("Arquivo", upload_to="documents/")
    uploaded_at = models.DateTimeField("Enviado em", auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField("Nome do Produto", max_length=100)
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    description = models.TextField("Descrição", blank=True)

    def __str__(self):
        return self.name