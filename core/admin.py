from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioNexus

class UsuarioNexusAdmin(UserAdmin):
    # Campos que serão exibidos nas colunas da lista principal no painel admin
    list_display = ('email', 'first_name', 'telefone', 'is_staff', 'is_active')
    
    # Campos pelos quais você poderá pesquisar os usuários na barra de busca
    search_fields = ('email', 'first_name')
    
    # Ordenação padrão da listagem (por e-mail)
    ordering = ('email',)
    
    # Organização e divisão dos campos dentro do formulário de edição do usuário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'telefone', 'email')}),
        ('Permissões e Níveis de Acesso', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Registra o seu modelo customizado com as regras visuais estruturadas acima
admin.site.register(UsuarioNexus, UsuarioNexusAdmin)