from django.shortcuts import render, redirect
from django.db import models  
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView
from .models import Project, SiteConfiguration, UsuarioNexus

# ==============================================================================
# 1. VIEW DE CADASTRO (ACESSO IMEDIATO PARA OUTROS UTILIZADORES)
# ==============================================================================
def cadastro_view(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        if UsuarioNexus.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado no sistema.")
            return render(request, 'core/cadastro.html')

        try:
            # Sincroniza o username com o e-mail para evitar falhas de login
            user = UsuarioNexus.objects.create_user(
                username=email,  
                email=email,
                password=senha,
                first_name=nome_completo,
                telefone=telefone,
                is_active=True  
            )
            messages.success(request, "Cadastro realizado com sucesso! Faça o seu login abaixo.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Erro interno ao processar cadastro: {str(e)}")
            return render(request, 'core/cadastro.html')

    return render(request, 'core/cadastro.html')


# ==============================================================================
# 2. VIEW DO DASHBOARD (CRUD COM PERSISTÊNCIA NO POSTGRESQL E FILTRO OPERACIONAL)
# ==============================================================================
@login_required
def dashboard(request):
    # 1. Fluxo de Exclusão Física via parâmetro na URL (?excluir=id)
    id_excluir = request.GET.get('excluir')
    if id_excluir:
        Project.objects.filter(id=id_excluir).delete()
        messages.success(request, "Projeto removido permanentemente do PostgreSQL.")
        return redirect('dashboard')

    # 2. Fluxo de Salvamento / Edição vindo do Modal Global
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        title = request.POST.get('title')
        client = request.POST.get('client')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        owner = request.POST.get('owner')
        
        # Trata o progresso enviado em branco para não quebrar a conversão de tipo
        progress_raw = request.POST.get('progress')
        progress = int(progress_raw) if progress_raw and progress_raw.strip() else 0
        
        # Captura as inputs de data do formulário
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Correção estrita de sintaxe Python: substituído 'null' por 'None'
        if not start_date or not start_date.strip(): start_date = None
        if not end_date or not end_date.strip(): end_date = None

        if projeto_id:  # Modo de Edição de Registro Existente
            Project.objects.filter(id=projeto_id).update(
                title=title, client=client, desc=desc, status=status,
                priority=priority, progress=progress, owner=owner,
                start_date=start_date, end_date=end_date
            )
            messages.success(request, f"Projeto '{title}' atualizado com sucesso!")
        else:  # Modo de Criação de Novo Registro
            Project.objects.create(
                title=title, client=client, desc=desc, status=status,
                priority=priority, progress=progress, owner=owner,
                start_date=start_date, end_date=end_date
            )
            messages.success(request, f"Projeto '{title}' cadastrado com sucesso!")
        
        return redirect('dashboard')

    # Coleta de listagem em tempo real de todos os registros para alimentação do front
    projetos_lista = Project.objects.all().order_by('-id')
    return render(request, 'core/dashboard.html', {'projetos_lista': projetos_lista})


# ==============================================================================
# 3. VIEW DE LISTAGEM DE UTILIZADORES E PERMISSÕES
# ==============================================================================
@login_required
def usuarios_view(request):
    usuarios = UsuarioNexus.objects.all().order_by('first_name')
    return render(request, 'core/usuarios.html', {'usuarios': usuarios})


# ==============================================================================
# 4. DEMAIS ABAS INTERNAS (EQUIPES, FINANÇAS, RELATÓRIOS)
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
# 5. VIEW DE CONFIGURAÇÕES COM SUPORTE A LOGOUT
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


# ==============================================================================
# 6. RECUPERAÇÃO DE SENHA VISUAL
# ==============================================================================
class PasswordResetVisualView(PasswordResetView):
    template_name = 'core/esqueci_senha.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()
        users = UsuarioNexus.objects.filter(email__iexact=email)
        
        if not users.exists():
            messages.error(request, f"O e-mail '{email}' não foi encontrado no banco de dados.")
            return render(request, self.template_name, {'form': self.get_form()})
            
        context = {'email_digitado': email}
        for user in users:
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = self.token_generator.make_token(user)
            
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
            context['link_seguro'] = f"{protocol}://{domain}/redefinir/{uid}/{token}/"
            break
            
        return render(request, 'core/esqueci_senha_enviado.html', context)