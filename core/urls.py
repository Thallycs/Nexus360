from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),          # Rota de Projetos
    path('equipes/', views.equipes, name='equipes_page'),            # Rota de Equipes
    path('financas/', views.financas, name='financas_page'),          # Rota de Finanças
    path('relatorios/', views.relatorios, name='relatorios_page'),    # Rota de Relatórios
    path('configuracoes/', views.configuracoes, name='settings_page'),# Rota de Configurações
]