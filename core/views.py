from django.shortcuts import render, redirect
from django.db import models  
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from .models import Project, SiteConfiguration, UsuarioNexus

# ==============================================================================
# 1. VIEW DE CADASTRO DE USUÁRIO (CORRIGIDA: NASCE ATIVO E SEM TRAVAR NO EMAIL)
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
            # CORREÇÃO: Mudamos is_active para True para você conseguir logar imediatamente!
            user = UsuarioNexus.objects.create_user(
                username=email,  # O Django usa username como chave, passamos o e-mail
                email=email,
                password=senha,
                first_name=nome_completo,
                telefone=telefone,
                is_active=True  # Ativo por padrão para testes de deploy estáveis
            )

            # Preparando simulação de e-mail informativa nos bastidores
            assunto = "Nexus 360 - Conta Criada com Sucesso"
            link_painel = "https://nexus360-qyx7.onrender.com/"
            mensagem = f"Olá {nome_completo},\n\nSua conta no Nexus 360 foi criada e já está ativa!\nAcesse o painel para fazer login:\n\n{link_painel}"
            
            # CORREÇÃO: fail_silently=True garante que se o Gmail bloquear, o site NÃO dá erro 500
            send_mail(
                assunto,
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )

            # Injeta a mensagem de sucesso que será lida pela tela de Login
            messages.success(request, "Cadastro realizado com sucesso! Faça seu login abaixo.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Erro interno ao processar cadastro: {str(e)}")
            return render(request, 'core/cadastro.html')

    return render(request, 'core/cadastro.html')


# ==============================================================================
# 2. VIEW CUSTOMIZADA DO FLUXO DE RECUPERAÇÃO DE SENHA (LINK DIRETO NA TELA)
# ==============================================================================
class PasswordResetVisualView(PasswordResetView):
    template_name = 'core/esqueci_senha.html'
    
    def form_valid(self, form):
        # Tenta rodar o fluxo padrão em background sem travar o processamento
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        
        # Coleta os dados e gera o link seguro em tempo de execução para exibir na tela
        email = form.cleaned_data["email"]
        users = UsuarioNexus.objects.filter(email__iexact=email)
        context = {'email_digitado': email}
        
        for user in users:
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = self.token_generator.make_token(user)
            
            domain = self.request.get_host()
            protocol = 'https' if self.request.is_secure() else 'http'
            link_direto = f"{protocol}://{domain}/redefinir/{uid}/{token}/"
            
            context['link_seguro'] = link_direto
            break 
            
        return render(self.request, 'core/esqueci_senha_enviado.html', context)


# ==============================================================================
# 3. VIEW DO DASHBOARD (PROTEGIDA POR LOGIN)
# ==============================================================================
@login_required
def dashboard(request):
    data = Project.objects.values('status').annotate(count=models.Count('id'))
    return render(request, 'core/dashboard.html', {'data': data})


# ==============================================================================
# 4. VIEWS DAS DEMAIS PÁGINAS INTERNAS (MANTIDAS E PROTEGIDAS)
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
# 5. VIEW DE CONFIGURAÇÕES (APENAS ADMINISTRADORES LOGADOS)
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