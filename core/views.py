@login_required
def dashboard(request):
    # 1. Fluxo de Exclusão Física via parâmetro na URL (?excluir=id)
    id_excluir = request.GET.get('excluir')
    if id_excluir:
        Project.objects.filter(id=id_excluir).delete()
        messages.success(request, "Projeto removido permanentemente.")
        return redirect('dashboard')

    # 2. Fluxo de Salvamento/Edição via POST do Modal
    if request.method == 'POST':
        projeto_id = request.POST.get('projeto_id')
        
        # Mapeamento de dados do formulário para os campos do Model
        dados_projeto = {
            'title': request.POST.get('title'),
            'client': request.POST.get('client'),
            'desc': request.POST.get('desc'),
            'status': request.POST.get('status'),
            'priority': request.POST.get('priority'),
            'progress': int(request.POST.get('progress') or 0),
            'owner': request.POST.get('owner'),
            'start_date': request.POST.get('start_date') or None,
            'end_date': request.POST.get('end_date') or None,
        }

        if projeto_id:  # Modo Edição
            Project.objects.filter(id=projeto_id).update(**dados_projeto)
            messages.success(request, "Projeto atualizado com sucesso!")
        else:  # Modo Criação
            Project.objects.create(**dados_projeto)
            messages.success(request, "Projeto criado com sucesso!")
        
        return redirect('dashboard')

    # Coleta de listagem para exibição
    projetos_lista = Project.objects.all().order_by('-id')
    return render(request, 'core/dashboard.html', {'projetos_lista': projetos_lista})