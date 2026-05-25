from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Autenticação e Conta ---
    path('', auth_views.LoginView.as_view(
        template_name='core/login.html', 
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    
    # --- Fluxo de Recuperação de Senha ---
    path('esqueci-senha/', views.PasswordResetVisualView.as_view(), name='password_reset'),
    path('esqueci-senha/sucesso/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/esqueci_senha_enviado.html'
    ), name='password_reset_done'),
    
    path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/redefinir_senha_formulario.html'
    ), name='password_reset_confirm'),
    
    path('redefinir/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/redefinir_senha_concluido.html'
    ), name='password_reset_complete'),

    # --- Operações do Sistema Nexus 360 ---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios_view, name='usuarios_page'),
    path('equipes/', views.equipes, name='equipes_page'),
    path('financas/', views.financas, name='financas_page'),
    path('relatorios/', views.relatorios, name='relatorios_page'),
    path('configuracoes/', views.configuracoes, name='settings_page'),
]