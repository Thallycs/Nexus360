from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioNexus, Project

@admin.register(UsuarioNexus)
class UsuarioNexusAdmin(UserAdmin):
    # Ajuste: Adicionado 'username' pois o AbstractUser padrão do Django o exige
    list_display = ('email', 'first_name', 'telefone', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'telefone')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}), 
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('last_login', 'date_joined')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'priority', 'responsible', 'end_date')
    list_filter = ('status', 'priority', 'responsible')
    search_fields = ('title', 'client', 'desc')
    date_hierarchy = 'end_date'
    list_editable = ('status', 'priority')