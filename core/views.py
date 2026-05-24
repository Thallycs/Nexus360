from django.shortcuts import render, redirect
from django.db import models  
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, SiteConfiguration, UsuarioNexus

# ==============================================================================
# 1. VIEW DE CADASTRO DE USUÁRIO (PROCESSANDO DADOS E SIMULANDO E-MAIL)
# ==============================================================================
def cadastro_view(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        # Validação básica para evitar duplicidade
        if UsuarioNexus.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado no sistema.")
            return render(request, 'core/cadastro.html')

        try:
            # Cria o usuário desativado (is_active=False) até que seja aprovado/ativado
            user = UsuarioNexus.objects.create_user(
                username=email,  # O Django usa username como chave, passamos o e-mail
                email=email,
                password=senha,
                first_name=nome_completo,
                telefone=telefone,
                is_active=False  # Fica pendente de aprovação
            )

            # Simulando o envio de e-mail com o link de ativação
            # Nota: O link será impresso diretamente no terminal de LOGS do Render!
            assunto = "Nexus 360 - Solicitação de Acesso Recebida"
            link_ativacao = f"https://nexus360-qyx7.onrender.com/admin/core/usuarionexus/{user.id}/change/"
            mensagem = f"Olá {nome_completo},\n\nSua solicitação de acesso ao Nexus 360 foi recebida.\nPara ativar esta conta, acesse o link de aprovação administrativo abaixo:\n\n{link_ativacao}"
            
            send_mail(
                assunto,
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Injeta a mensagem de sucesso que será lida pela tela de Login
            messages.success(request, "Solicitação enviada com sucesso! Verifique as instruções de ativação nos logs do servidor.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Erro interno ao processar cadastro: {str(e)}")
            return render(request, 'core/cadastro.html')

    return render(request, 'core/cadastro.html')


# ==============================================================================
# 2. VIEW DO DASHBOARD (PROTEGIDA POR LOGIN)
# ==============================================================================
@login_required
def dashboard(request):
    data = Project.objects.values('status').annotate(count=models.Count('id'))
    return render(request, 'core/dashboard.html', {'data': data})


# ==============================================================================
# 3. VIEWS DAS DEMAIS PÁGINAS INTERNAS (MANTIDAS E PROTEGIDAS)
# ==============================================================================
@login_required
def equipes(request):
    return render(request, 'core/equipes.html')

@login_required
def financas(request):
    return render(request, 'core/financas.html')

@login_required
def relatorios(request):
    return render(request, 'core/relatorios.html')


# ==============================================================================
# 4. VIEW DE CONFIGURAÇÕES (APENAS ADMINISTRADORES LOGADOS)
# ==============================================================================
@login_required
@user_passes_test(lambda u: u.is_staff)
def configuracoes(request):
    config, created = SiteConfiguration.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        config.site_name = request.POST.get('site_name', 'Nexus 360')
        if request.FILES.get('logo'):
            config.logo = request.FILES['logo']
        if request.FILES.get('favicon'):
            config.favicon = request.FILES['favicon']
            
        config.save()
        return redirect('settings_page')
        
    return render(request, 'core/settings.html', {'config': config})