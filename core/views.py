from django.shortcuts import render
from django.db import models  # IMPORTANTE: Adicione esta linha para o models.Count funcionar
from .models import Project   # IMPORTANTE: Importa o seu modelo de Projetos

def dashboard_view(request):
    # Conta quantos projetos existem em cada status
    data = Project.objects.values('status').annotate(count=models.Count('id'))
    
    # Renderiza a tela dashboard.html passando os dados do gráfico
    return render(request, 'core/dashboard.html', {'data': data})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import SiteConfiguration

# Garante que apenas usuários administradores/staff possam acessar essa aba
@user_passes_test(lambda u: u.is_staff)
def settings_view(request):
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