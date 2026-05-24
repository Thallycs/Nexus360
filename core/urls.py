from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Tela Inicial Obrigatória (Raiz do site: http://.../)
    path('', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
    
    # 2. Tela de Cadastro de Novo Usuário
    path('cadastro/', views.cadastro_view, name='cadastro'),
    
    # 3. Fluxo de Recuperação de Senha ("Esqueci minha senha")
    path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='core/esqueci_senha.html',
        email_template_name='core/password_reset_email.html',
        subject_template_name='core/password_reset_subject.txt'
    ), name='password_reset'),
    
    # 4. Confirmação de envio do e-mail
    path('esqueci-senha/sucesso/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/esqueci_senha_enviado.html'
    ), name='password_reset_done'),
    
    # 5. Link seguro que o usuário recebe no e-mail para digitar a nova senha
    path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/redefinir_senha_formulario.html'
    ), name='password_reset_confirm'),
    
    # 6. Confirmação de que a senha foi alterada com sucesso
    path('redefinir/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/redefinir_senha_concluido.html'
    ), name='password_reset_complete'),

    # --- Suas rotas originais mantidas abaixo ---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('equipes/', views.equipes, name='equipes_page'),
    path('financas/', views.financas, name='financas_page'),
    path('relatorios/', views.relatorios, name='relatorios_page'),
    path('configuracoes/', views.configuracoes, name='settings_page'),
]