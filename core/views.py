from django.shortcuts import render, redirect
from django.db import models  
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, SiteConfiguration

# ==============================================================================
# 1. VIEW DO DASHBOARD (PROTEGIDA POR LOGIN)
# ==============================================================================
@login_required
def dashboard(request):
    # Conta quantos projetos existem em cada status
    data = Project.objects.values('status').annotate(count=models.Count('id'))
    
    # Renderiza a tela dashboard.html passando os dados do gráfico
    return render(request, 'core/dashboard.html', {'data': data})


# ==============================================================================
# 2. VIEW DE CONFIGURAÇÕES (APENAS ADMINISTRADORES LOGADOS)
# ==============================================================================
@login_required
@user_passes_test(lambda u: u.is_staff)
def configuracoes(request):
    # Pega a configuração existente ou cria uma nova se o banco estiver vazio
    config, created = SiteConfiguration.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        # Atualiza os dados com o que foi digitado/enviado no formulário
        config.site_name = request.POST.get('site_name', 'Nexus 360')
        
        if request.FILES.get('logo'):
            config.logo = request.FILES['logo']
        if request.FILES.get('favicon'):
            config.favicon = request.FILES['favicon']
            
        config.save()
        return redirect('settings_page') # Recarrega a página para aplicar as mudanças
        
    return render(request, 'core/settings.html', {'config': config})