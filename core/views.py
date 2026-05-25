from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Project
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

@login_required
def dashboard(request):
    # 1. Fluxo de Exclusão (GET)
    if 'excluir' in request.GET:
        project = get_object_or_404(Project, id=request.GET.get('excluir'))
        project.delete()
        messages.success(request, "Projeto removido com sucesso.")
        return redirect('dashboard')

    # 2. Fluxo de Criação/Edição (POST)
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        
        # Filtra dados vazios para evitar erros de banco de dados
        dados = {
            'title': request.POST.get('title'),
            'client': request.POST.get('client'),
            'desc': request.POST.get('desc'),
            'status': request.POST.get('status'),
            'priority': request.POST.get('priority'),
            'progress': int(request.POST.get('progress') or 0),
            'owner': request.POST.get('owner'),
            'start_date': request.POST.get('start_date') or None,
            'end_date': request.POST.get('end_date') or None,
            'responsible': request.user if request.user.is_authenticated else None
        }

        try:
            if projeto_id:
                # Edição
                Project.objects.filter(id=projeto_id).update(**dados)
                messages.success(request, "Projeto atualizado!")
            else:
                # Criação
                Project.objects.create(**dados)
                messages.success(request, "Projeto criado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao salvar: {str(e)}")
        
        return redirect('dashboard')

    # 3. Listagem (GET padrão)
    context = {
        'projetos_lista': Project.objects.all().order_by('-created_at')
    }
    return render(request, 'core/dashboard.html', context)

def cadastro_view(request):
    # Por enquanto, apenas retorna a página de cadastro
    return render(request, 'core/cadastro.html')

class PasswordResetVisualView(PasswordResetView):
    template_name = 'core/esqueci_senha.html' # Certifique-se de ter este arquivo na pasta templates
    success_url = reverse_lazy('password_reset_done')

def usuarios_view(request):
    return render(request, 'core/usuarios.html')

def equipes(request):
    return render(request, 'core/equipes.html')

def financas(request):
    return render(request, 'core/financas.html')

def relatorios(request):
    return render(request, 'core/relatorios.html')

def configuracoes(request):
    return render(request, 'core/configuracoes.html')