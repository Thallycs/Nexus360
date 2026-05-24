from django.shortcuts import render, redirect
from django.db import models  
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, SiteConfiguration

# ==============================================================================
# 1. VIEW DE CADASTRO DE USUÁRIO (ABERTA AO PÚBLICO)
# ==============================================================================
def cadastro_view(request):
    # Se o método for POST, processará o formulário de criação de conta futuramente
    if request.method == 'POST':
        pass 
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