from django.db import models
from django.contrib.auth.models import User

# 1. Configurações Globais (Para alterar ícones, imagens e modo)
class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Nexus 360")
    logo = models.ImageField(upload_to='system/', blank=True, null=True)
    favicon = models.ImageField(upload_to='system/', blank=True, null=True)
    dark_mode_default = models.BooleanField(default=True)

# 2. Projetos
class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANEJAMENTO', 'Em Planejamento'),
        ('DESENVOLVIMENTO', 'Em Desenvolvimento'),
        ('TESTES', 'Em Testes'),
        ('ENTREGUE', 'Entregue'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJAMENTO')
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Campo espacial para geolocalizar onde o projeto de TI será aplicado (ex: campus, cliente)
    #location = gis_models.PointField(blank=True, null=True) 

# 3. Documentos (Upload/Download)
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')

# 4. Catálogo de Produtos/Serviços
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
