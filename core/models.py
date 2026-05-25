from django.db import models
from django.conf import settings

class Project(models.Model):
    # Organização das escolhas (Choices) como constantes
    PLANEJAMENTO = 'PLANEJAMENTO'
    DESENVOLVIMENTO = 'DESENVOLVIMENTO'
    TESTES = 'TESTES'
    ENTREGUE = 'ENTREGUE'
    PAUSADO = 'PAUSADO'
    
    STATUS_CHOICES = [
        (PLANEJAMENTO, 'Em Planejamento'),
        (DESENVOLVIMENTO, 'Em Desenvolvimento'),
        (TESTES, 'Em Testes'),
        (ENTREGUE, 'Entregue'),
        (PAUSADO, 'Pausado'),
    ]

    PRIORITY_CHOICES = [
        ('Alta', 'Alta'),
        ('Média', 'Média'),
        ('Baixa', 'Baixa'),
    ]

    # Campos principais com indexação para performance nas buscas e filtros
    title = models.CharField("Título", max_length=200)
    client = models.CharField("Cliente", max_length=200, blank=True, null=True)
    desc = models.TextField("Descrição", blank=True, null=True)
    
    # db_index=True torna o filtro (o sistema de abas) muito mais rápido
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default=PLANEJAMENTO, db_index=True)
    priority = models.CharField("Prioridade", max_length=10, choices=PRIORITY_CHOICES, default='Alta', db_index=True)
    
    progress = models.IntegerField("Progresso (%)", default=0)
    owner = models.CharField("Responsável", max_length=50, blank=True, null=True)
    
    # Datas com indexação para o filtro de calendário (hoje/semana/mês)
    start_date = models.DateField("Data de Início", blank=True, null=True, db_index=True)
    end_date = models.DateField("Previsão de Entrega", blank=True, null=True, db_index=True)
    
    # Relacionamento de Usuário
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
        return f"{self.title} ({self.client if self.client else 'Nenhum Cliente'})"