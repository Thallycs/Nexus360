from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ==============================================================================
# 1. MODELO DE USUÁRIO CUSTOMIZADO (NEXUS 360)
# ==============================================================================
class UsuarioNexus(AbstractUser):
    # Torna o e-mail único e obrigatório para o login
    email = models.EmailField(unique=True, max_length=255)
    
    # Adiciona o campo de telefone solicitado para o cadastro
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # Começa como False para bloquear o login até a confirmação por link de e-mail
    is_active = models.BooleanField(default=False)
    
    # Configura o e-mail como identificador principal de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


# ==============================================================================
# 2. CONFIGURAÇÕES GLOBAIS
# ==============================================================================
class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Nexus 360")
    logo = models.ImageField(upload_to='system/', blank=True, null=True)
    favicon = models.ImageField(upload_to='system/', blank=True, null=True)
    dark_mode_default = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name


# ==============================================================================
# 3. PROJETOS
# ==============================================================================
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
    
    # CORREÇÃO: Aponta dinamicamente para o nosso novo modelo UsuarioNexus
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ==============================================================================
# 4. DOCUMENTOS (UPLOAD/DOWNLOAD)
# ==============================================================================
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.title


# ==============================================================================
# 5. CATÁLOGO DE PRODUTOS/SERVIÇOS
# ==============================================================================
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name